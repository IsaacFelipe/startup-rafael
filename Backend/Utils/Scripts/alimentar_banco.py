import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def criar_banco_vetorial():
    # 1. Camiho da pasta de PDFs usando caminhos relativos
    base_dir = os.path.dirname(os.path.abspath(__file__))
    caminhos = [
        os.path.join(base_dir, "PDFs", "77-Dias-Novos-Cristaos.pdf"), 
        os.path.join(base_dir, "PDFs", "livreto-devocional.pdf")
    ]

    # 2. Carregamento dos Arquivos
    print("Carregando PDFs da pasta Backend/PDFs...")
    documentos = []
    
    for caminho in caminhos:
        if os.path.exists(caminho):
            try:
                loader = PyPDFLoader(caminho)
                documentos.extend(loader.load())
                print(f"✅ Sucesso ao ler: {os.path.basename(caminho)}")
            except Exception as e:
                print(f"❌ Erro ao ler {caminho}: {e}")
        else:
            print(f"⚠️ Atenção: Arquivo não encontrado no caminho -> {caminho}")

    if not documentos:
        print("🚨 Nenhum documento foi carregado. O processo foi abortado.")
        return

    # 3. Quebra de Texto (Chunking)
    print("\nDividindo as páginas em pedaços (chunks)...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,   
        chunk_overlap=200, 
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = text_splitter.split_documents(documentos)
    print(f"Total de chunks gerados: {len(chunks)}")

    # 4. Geração de Embeddings e Criação do Banco
    print("\nBaixando modelo de embeddings e salvando no ChromaDB...")
    
    embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")

    chroma_dir = os.path.join(base_dir, ".chroma_db")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=chroma_dir
    )

    print(f"\n🚀 FIM DO PROCESSO! Banco ChromaDB alimentado e salvo com sucesso em '{chroma_dir}'.")

if __name__ == "__main__":
    criar_banco_vetorial()
