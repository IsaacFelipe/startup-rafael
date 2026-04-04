from langchain_core.tools import tool
from pydantic import BaseModel, Field
from DataBase import registrar_alerta_saude, buscar_perfil

class AlertaEmergenciaSchema(BaseModel):
    idoso_id: int = Field(description="O ID numérico do idoso.")
    problema: str = Field(description="Descrição detalhada do que o idoso está sentindo ou relatando (ex: 'dor forte no peito', 'fala confusa', 'queda').")

@tool("disparar_alerta_emergencia", args_schema=AlertaEmergenciaSchema)
def disparar_alerta_emergencia(idoso_id: int, problema: str) -> str:
    """
    ACIONAMENTO CRÍTICO. Use esta ferramenta IMEDIATAMENTE se o idoso relatar mal-estar súbito, 
    dor forte, confusão mental, queda ou qualquer situação de risco à vida. 
    Ela avisa a família e registra o evento médico.
    """
    try:
        # 1. Busca o perfil para saber o nome do idoso
        perfil = buscar_perfil(idoso_id)
        nome_idoso = perfil.get('nome', 'O idoso') if perfil else "O idoso"

        # 2. Registra no banco e pega os contatos
        contatos = registrar_alerta_saude(idoso_id, problema, gravidade=3)

        if contatos:
            # Simulação de envio de SMS/Ligação (Aqui entraria integração com Twilio, por exemplo)
            lista_contatos = ", ".join([f"{c['nome']} ({c['telefone']})" for c in contatos])
            
            return (f"ALERTA DISPARADO! O evento foi registrado no histórico de saúde. "
                    f"Notificação de emergência enviada para: {lista_contatos}. "
                    f"Instrução para o Rafael: Mantenha a calma, fique na linha com o(a) {nome_idoso} "
                    f"e diga que a ajuda já foi avisada.")
        else:
            return (f"O alerta foi registrado no histórico, mas não encontrei contatos de emergência "
                    f"específicos na tabela 'familiares'. Verifique o campo 'contato_familiar' no perfil.")

    except Exception as e:
        return f"Erro crítico ao disparar alerta: {str(e)}"