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