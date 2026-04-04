from langchain_core.tools import tool # Importação correta
from pydantic import BaseModel, Field
from typing import Optional
from DataBase import buscar_perfil, registrar_dose_remedio # Importa as duas funções

class ConfirmarMedicamentoTomado(BaseModel):
    medicamento: str = Field(description="Nome do medicamento que o idoso tomou ou quer saber")
    idoso_id: int = Field(description="ID numérico do idoso") # Mudado para int para bater com o DB

@tool(args_schema=ConfirmarMedicamentoTomado)
def confirmar_medicamento_tomado(medicamento: str, idoso_id: int) -> str:
    """
    Use esta ferramenta quando o idoso disser que 'já tomou' um remédio ou quando perguntar se deve tomar algum agora.
    Ela registra o horário da dose no sistema para a família ver e confirma as informações do banco.
    """
    try:
        # 1. Tenta registrar no banco de dados que ele tomou
        sucesso = registrar_dose_remedio(idoso_id, medicamento)
        
        # 2. Busca o perfil para dar uma resposta personalizada
        perfil = buscar_perfil(idoso_id)
        
        if not perfil:
            return "Erro: Perfil do idoso não encontrado no sistema."

        nome = perfil.get('nome', 'você')
        
        if sucesso:
            return f"Perfeito, {nome}! Já anotei aqui no meu caderninho que você tomou o {medicamento} agora. Sua família já pode ficar tranquila!"
        else:
            return f"Oi {nome}, eu entendi que você tomou o {medicamento}, mas tive um probleminha para salvar. De qualquer forma, o importante é que você se cuidou!"

    except Exception as e:
        return f"Aviso ao sistema: Erro ao processar registro de medicamento. Erro: {str(e)}"