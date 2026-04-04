import os
import logging
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.agents import create_tool_calling_agent, AgentExecutor

from Mente import prompt, chat
from DataBase import MySQLChatHistory, buscar_perfil
from STT import transcrever
from tools.buscar_devocional_do_dia import buscar_devocional_do_dia
from tools.agendar_lembrete import agendar_lembrete
from tools.atualizar_medicamentos import atualizar_medicamentos
from tools.buscar_fato_historico import buscar_fato_historico

# Configuração básica de log para produção
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Servidor Rafael", description="API de Companhia Digital para Idosos")

# Configuração de CORS lendo de variáveis de ambiente (com fallback para local)
ORIGENS_PERMITIDAS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGENS_PERMITIDAS, 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# 1. Pydantic Blindado (Validação Extrema)
class MensagemEntrada(BaseModel):
    mensagem: str = Field(..., min_length=1, max_length=1000, description="Texto enviado pelo usuário")
    idoso_id: int = Field(..., gt=0, description="ID numérico do idoso no banco")
    sessao_id: int = Field(..., gt=0, description="ID da sessão de chat atual")

# 2. Configurando as Ferramentas e o Agente de forma centralizada
todas_as_tools = [
    buscar_devocional_do_dia,
    agendar_lembrete,
    atualizar_medicamentos,
    buscar_fato_historico
]

chat_com_tools = chat.bind_tools(todas_as_tools)
agente = create_tool_calling_agent(chat_com_tools, todas_as_tools, prompt)

# Reduzimos o verbose em produção para não poluir os logs desnecessariamente
agent_executor = AgentExecutor(agent=agente, tools=todas_as_tools, verbose=True)

# 3. Anexando a Memória Automática (Com Mapeamento Correto da Entrada "input")
chain_com_memoria = RunnableWithMessageHistory(
    agent_executor,
    get_session_history=lambda session_id: MySQLChatHistory(sessao_id=int(session_id)),
    input_messages_key="input", # Alterado para bater com o AgentExecutor
    history_messages_key="memoria",
)

# 4. Dependência: Validação de Perfil Isolada
def obter_perfil_validado(dados: MensagemEntrada) -> dict:
    perfil = buscar_perfil(dados.idoso_id)
    if not perfil:
        logger.warning(f"Tentativa de acesso para idoso inexistente: ID {dados.idoso_id}")
        raise HTTPException(status_code=404, detail="Perfil do idoso não encontrado.")
    return perfil

# 5. O Endpoint Original via Texto
@app.post("/conversar")
def conversar_com_rafael(
    dados: MensagemEntrada, 
    perfil: dict = Depends(obter_perfil_validado) 
):
    try:
        logger.info(f"Processando mensagem. Idoso: {perfil['nome']}, Sessão: {dados.sessao_id}")
        
        resposta_ia = chain_com_memoria.invoke(
            {
                "input": dados.mensagem, # Mandando para o AgentExecutor
                "mensagem": dados.mensagem, # Para template se precisar em fallback
                "nome_idoso": perfil["nome"],
                "medicamentos": perfil.get("medicamentos", "Nenhum"),
                "preferencias": perfil.get("preferencias", "Nenhuma"),
                "contexto_saude": perfil.get("contexto_saude", "Nenhuma observação"),
            },
            config={"configurable": {"session_id": str(dados.sessao_id)}}
        )
        
        return {"resposta": resposta_ia["output"]}

    except Exception as e:
        logger.error(f"Erro ao processar mensagem do Rafael: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail="Ocorreu um erro interno de conexão com o Rafael. Tente novamente em instantes."
        )

# 6. Endpoint de Áudio via Whisper STT
@app.post("/falar")
async def falar_com_rafael_audio(
    audio: UploadFile = File(...),
    idoso_id: int = Form(...),
    sessao_id: int = Form(...)
):
    try:
        logger.info(f"Recebido áudio. Idoso ID: {idoso_id}, Sessão: {sessao_id}")
        audio_bytes = await audio.read()
        
        # 1. Transcreve o áudio para texto
        texto_usuario = transcrever(audio_bytes)
        logger.info(f"O idoso disse: {texto_usuario}")
        
        if not texto_usuario:
            return {"resposta": "", "texto_usuario": ""}

        # 2. Busca perfil
        perfil = buscar_perfil(idoso_id)
        if not perfil:
            raise HTTPException(status_code=404, detail="Perfil não encontrado.")
            
        # 3. LangChain RAG
        resposta_ia = chain_com_memoria.invoke(
            {
                "input": texto_usuario,
                "mensagem": texto_usuario,
                "nome_idoso": perfil["nome"],
                "medicamentos": perfil.get("medicamentos", "Nenhum"),
                "preferencias": perfil.get("preferencias", "Nenhuma"),
                "contexto_saude": perfil.get("contexto_saude", "Nenhuma observação"),
            },
            config={"configurable": {"session_id": str(sessao_id)}}
        )
        
        return {
            "texto_usuario": texto_usuario,
            "resposta": resposta_ia["output"]
        }

    except Exception as e:
        logger.error(f"Erro no processamento de voz: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
