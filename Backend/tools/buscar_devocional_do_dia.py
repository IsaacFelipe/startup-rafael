from langchain_core.tools import tool
from pydantic import BaseModel, Field
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# 1. Schema da Ferramenta
class BuscarDevocionalDoDia(BaseModel):
    tema: str = Field(description="O tema espiritual para o devocional de hoje. Ex: 'esperança', 'paciência', 'cura'.", default="fé")
    origem: str = Field(description="Escolha 'web' para buscar no site, ou 'pdf' para buscar nos documentos locais.", default="web")
    
# 2. A Ferramenta Corrigida (Sem espaços no nome!)
@tool("buscar_devocional_do_dia", args_schema=BuscarDevocionalDoDia)
def buscar_devocional_do_dia(tema: str, origem: str = "web") -> str:
    """Pesquisa um versículo e reflexão cristã baseada em um tema específico."""
    
    texto_final = f"=== Resultados da busca para o tema: {tema.upper()} ===\n\n"
    
    # ---------------------------------------------------------
    # FLUXO 1: BUSCA RAG NO BANCO VETORIAL (PDFs)
    # ---------------------------------------------------------
    if origem == "pdf":
        try:
            # Carrega o modelo de embeddings (o mesmo que você usou para salvar o banco)
            embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
            
            # Conecta ao banco de dados Chroma já existente na sua máquina
            vectorstore = Chroma(
                persist_directory="./.chroma_db", 
                embedding_function=embedding_model
            )
            
            # Faz a busca inteligente nos PDFs pelo "tema"
            docs_encontrados = vectorstore.similarity_search(tema, k=2)
            
            if not docs_encontrados:
                return texto_final + f"Falha: Nenhum conteúdo sobre '{tema}' foi encontrado nos materiais."
                
            # Junta os trechos encontrados
            textos_extraidos = [doc.page_content for doc in docs_encontrados]
            return texto_final + "\n\n---\n\n".join(textos_extraidos)

        except Exception as e:
            return texto_final + f"[Erro crítico ao acessar o banco vetorial: {str(e)}]"

    # ---------------------------------------------------------
    # FLUXO 2: BUSCA AO VIVO NA WEB
    # ---------------------------------------------------------
    else:
        url = "https://www.bibliaon.com/devocional_diario/"
        
        try:
            loader = WebBaseLoader(url)
            documents = loader.load()
            
            if not documents or not documents[0].page_content.strip():
                return texto_final + "[Aviso: Não foi possível carregar o devocional da web.]"
                
            return texto_final + documents[0].page_content
            
        except Exception as e:
            return texto_final + f"[Erro crítico de conexão com a Web: {str(e)}]"