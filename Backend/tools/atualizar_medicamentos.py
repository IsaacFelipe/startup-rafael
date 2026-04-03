from langchain_core.tools import tool
from pydantic import BaseModel, Field
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from DataBase import get_conexao
class AtualizarMedicamentos(BaseModel):
    medicamentos: str = Field(description="A nova lista completa de medicamentos e horários prescritos.")
    idoso_id: int = Field(description="O ID único do idoso no banco de dados.")

@tool("atualizar_medicamentos", args_schema=AtualizarMedicamentos)
def atualizar_medicamentos(medicamentos: str, idoso_id: int) -> str:
    """Atualiza a prescrição de medicamentos do idoso diretamente no banco de dados."""
    try:
        conn = get_conexao()
        cursor = conn.cursor()

        sql = "UPDATE idosos SET medicamentos = %s WHERE id = %s"
        cursor.execute(sql, (medicamentos, idoso_id))
        conn.commit()
        linhas_afetadas = cursor.rowcount
        cursor.close()
        conn.close()
        if linhas_afetadas > 0:
            return f"Sucesso: Medicamentos do idoso {idoso_id} atualizados para: '{medicamentos}'."
        else:
            return f"Erro: Nenhum idoso encontrado com o ID {idoso_id}."
    except Exception as e:
        return f"Erro ao atualizar medicamentos: {str(e)}"