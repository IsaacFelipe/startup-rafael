from langchain_core.tools import tool
from pydantic import BaseModel, Field
from langchain_community.tools import DuckDuckGoSearchRun
import datetime
import locale

try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
except:
    pass 

class BuscaFatoHistorico(BaseModel):
    termo_busca: str = Field(
        description="Pode ser um tema (ex: 'Guerra Fria') ou uma data (ex: 'hoje', '12 de abril').",
        default="hoje"
    )

@tool("buscar_fato_historico", args_schema=BuscaFatoHistorico)
def buscar_fato_historico(termo_busca: str) -> str:
    """
    Pesquisa na internet fatos históricos. 
    
    DIRETIVA OBRIGATÓRIA: Você receberá um resumo bruto da internet. 
    Transforme essa informação em uma história fascinante, acolhedora e fluida para o usuário. 
    Não responda como um verbete. Crie contexto e emoção.
    """
    
    if termo_busca.lower() == "hoje":
        hoje = datetime.datetime.now()
        termo_busca = hoje.strftime("%d de %B") 
        
    query = f"fatos históricos importantes que aconteceram em {termo_busca}"
    
    try:
        buscador = DuckDuckGoSearchRun()
        
        resultados = buscador.invoke(query)
        
        if resultados:
            return f"RESULTADOS DA INTERNET ({termo_busca}):\n{resultados}"
        else:
            return f"Não achei nada relevante na internet para '{termo_busca}'."
            
    except Exception as e:
        return f"Erro técnico ao buscar na internet: {str(e)}"