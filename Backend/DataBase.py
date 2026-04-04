import mysql.connector
import os
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from typing import List

def get_conexao():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("MYSQL_PASSWORD"),
        database="Rafael"
    )

def buscar_perfil(idoso_id: int) -> dict:
    conn = get_conexao()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM idosos WHERE id = %s", (idoso_id,))
    perfil = cursor.fetchone()
    cursor.close()
    conn.close()
    return perfil

def registrar_alerta_saude(idoso_id: int, descricao: str, gravidade: int = 3) -> list:
    """
    Grava o alerta no histórico de saúde e retorna a lista de contatos familiares.
    """
    try:
        conn = get_conexao()
        cursor = conn.cursor(dictionary=True)
        
        # 1. Registrar na tabela eventos_saude que você já criou
        sql_evento = "INSERT INTO eventos_saude (idoso_id, tipo, descricao, gravidade) VALUES (%s, 'alerta', %s, %s)"
        cursor.execute(sql_evento, (idoso_id, descricao, gravidade))
        
        # 2. Buscar contatos de emergência do idoso
        sql_familia = "SELECT nome, telefone FROM familiares WHERE idoso_id = %s AND notificar_emergencia = 1"
        cursor.execute(sql_familia, (idoso_id,))
        contatos = cursor.fetchall()
        
        conn.commit()
        cursor.close()
        conn.close()
        return contatos
    except Exception as e:
        print(f"Erro no banco: {e}")
        return []

def registrar_dose_remedio(idoso_id: int, medicamento: str) -> bool:
    try:
        conn = get_conexao()
        cursor = conn.cursor()
        sql = "INSERT INTO eventos_saude (idoso_id, tipo, descricao, gravidade) VALUES (%s, 'remédio_tomado', %s, 1)"
        cursor.execute(sql, (idoso_id, medicamento))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Erro no banco: {e}")
        return False

class MySQLChatHistory(BaseChatMessageHistory):
    def __init__(self, sessao_id: int):
        self.sessao_id = sessao_id

    @property
    def messages(self) -> List[BaseMessage]:
        conn = get_conexao()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT role, conteudo FROM mensagens WHERE sessao_id = %s ORDER BY timestamp",
            (self.sessao_id,)
        )
        rows = cursor.fetchall()
        conn.close()

        historico = []
        for row in rows:
            if row["role"] == "human":
                historico.append(HumanMessage(content=row["conteudo"]))
            else:
                historico.append(AIMessage(content=row["conteudo"]))
        return historico

    def add_message(self, message: BaseMessage):
        role = "human" if isinstance(message, HumanMessage) else "ai"
        conn = get_conexao()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO mensagens (sessao_id, role, conteudo) VALUES (%s, %s, %s)",
            (self.sessao_id, role, message.content)
        )
        conn.commit()
        conn.close()

    def clear(self):
        conn = get_conexao()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM mensagens WHERE sessao_id = %s", (self.sessao_id,))
        conn.commit()
        conn.close()

# ── cria uma sessão nova no banco e retorna o id ──
def iniciar_sessao(idoso_id: int) -> int:
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sessoes (idoso_id) VALUES (%s)",
        (idoso_id,)
    )
    conn.commit()
    sessao_id = cursor.lastrowid
    conn.close()
    return sessao_id