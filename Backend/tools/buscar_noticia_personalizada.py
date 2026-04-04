from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing import Optional
from langchain_community.tools import DuckDuckGoSearchResults

class BuscarNoticia(BaseModel):
    categoria: str = Field(description="Categoria da noticia a ser buscada")
    região: Optional[str] = Field(description="Região da noticia a ser buscada")
    tempo: Optional[str] = Field(description="Tempo da noticia a ser buscada")

@tool(args_schema=BuscarNoticia)
def buscar_noticia_personalizada(categoria: str, regiao: Optional[str], tempo: Optional[str]):
    """
    Busca notícias reais na internet com base nas preferências do idoso.
    Use esta ferramenta quando o idoso quiser saber as novidades do seu time de futebol, 
    política local ou quando ele comentar sobre um tema que exija que você saiba das notícias atuais para dialogar.
    """

    try:
        pergunta = f"noticias {categoria}"
        if regiao:
            pergunta += f" {regiao}"
        if tempo:
            pergunta += f" {tempo}"
        
        pesquisa = DuckDuckGoSearchResults(num_results = 3)
        resultados = pesquisa.run(pergunta)

        if resultados:
            return f"Sucesso! Encontrei estas notícias na internet sobre '{pergunta}':\n\n{resultados}\n\nLeia os resumos e conte a novidade para o idoso de forma natural e amigável."
        else:
            return f"Aviso ao sistema: Nenhuma notícia recente encontrada para '{pergunta}'. Diga ao idoso que não houve grandes novidades sobre isso hoje."
            
    except Exception as e:
        return f"Aviso ao sistema: Ocorreu um erro ao pesquisar as notícias na internet. Mude de assunto de forma sutil. Erro: {str(e)}"    
        


