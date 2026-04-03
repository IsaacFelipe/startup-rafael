from langchain_core.tools import tool
from pydantic import BaseModel, Field
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from DataBase import get_conexao
class LembreteSchema(BaseModel):
    mensagem: str = Field(description="O conteúdo do lembrete (ex: 'tomar o remédio', 'ligar para a filha')")
    data_hora: str = Field(description="A data e hora formatada em YYYY-MM-DD HH:MM:SS")
    idoso_id: int = Field(description="O ID único do idoso responsável pelo lembrete.")

@tool("agendar_lembretes", args_schema=LembreteSchema)
def agendar_lembrete(mensagem: str, data_hora: str, idoso_id: int):
    """Agenda um lembrete no banco de dados para ser disparado no futuro."""
    try:
        conn = get_conexao()
        cursor = conn.cursor()

        sql="INSERT INTO lembretes (idoso_id, mensagem, data_hora) VALUES (%s,%s,%s)"
        cursor.execute(sql,(idoso_id, mensagem, data_hora))
        conn.commit()
        cursor.close()
        conn.close()
        return "Lembrete agendado com sucesso!"
    except Exception as e:
        return f"Erro ao agendar lembrete: {str(e)}"