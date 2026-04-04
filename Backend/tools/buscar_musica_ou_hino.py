from langchain_core.tools import tool
from pydantic import BaseModel, Field
from youtubesearchpython import VideosSearch

class BuscarMusica(BaseModel):
    musica: str = Field(description="Nome do hino, louvor ou número da Harpa Cristã (ex: 'Porque Ele Vive')")

@tool(args_schema=BuscarMusica)
def buscar_musica_no_youtube(musica: str) -> str:
    """
    Busca um hino da Harpa Cristã ou música gospel no YouTube.
    Use esta ferramenta sempre que o idoso quiser ouvir um louvor ou pedir uma música.
    """
    try:
        # Faz a busca no YouTube e limita a trazer apenas o 1º resultado (o mais relevante)
        busca = VideosSearch(musica, limit=1)
        resultado = busca.result()
        
        # Verifica se o YouTube encontrou algum vídeo
        if resultado['result']:
            video = resultado['result'][0]
            titulo = video['title']
            link = video['link']
            canal = video['channel']['name']
            
            # Devolve as informações para o Rafael formular a resposta
            return f"Sucesso! Encontrei o vídeo '{titulo}' do canal '{canal}'. O link é: {link}"
        else:
            return f"Aviso ao sistema: Não foi encontrado nenhum vídeo no YouTube para a busca '{musica}'."
            
    except Exception as e:
        return f"Aviso ao sistema: Ocorreu um erro ao buscar a música. Diga ao idoso que você teve um probleminha técnico. Erro: {str(e)}"