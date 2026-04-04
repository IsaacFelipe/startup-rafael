from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing import Optional
from DataBase import buscar_perfil

class BuscarPerfilIdoso(BaseModel):
    nome: Optional[str] = Field(description="Nome do idoso")
    idoso_id: int = Field(description="ID numérico do idoso no banco de dados")

@tool(args_schema=BuscarPerfilIdoso)
def buscar_perfil_idoso(idoso_id: int, nome: Optional[str] = None) -> str:
    """
    Carrega a ficha médica e pessoal do idoso (nome, remédios, preferências e histórico de saúde).
    Use esta ferramenta SEMPRE que precisar relembrar quais são os medicamentos do idoso, 
    seus gostos pessoais ou o seu contexto de saúde para dar uma resposta mais precisa.
    """
    try:
        # Chama a função que já existe no seu DataBase.py
        perfil = buscar_perfil(idoso_id)
        
        if perfil:
            # Formata os dados do banco para o Rafael ler facilmente
            return f"""
            Ficha do Idoso Encontrada:
            - Nome: {perfil.get('nome', 'Não informado')}
            - Medicamentos: {perfil.get('medicamentos', 'Nenhum listado')}
            - Preferências/Gostos: {perfil.get('preferencias', 'Nada específico')}
            - Contexto de Saúde: {perfil.get('contexto_saude', 'Sem observações médicas')}
            """
        else:
            return f"Aviso ao sistema: Nenhum perfil encontrado no banco de dados para o ID {idoso_id}."
            
    except Exception as e:
        return f"Aviso ao sistema: Erro ao conectar com o banco de dados. Erro: {str(e)}"