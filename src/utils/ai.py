from ollama import chat
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from sentence_transformers import SentenceTransformer
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from asyncio import run

from gurinovich import documents

llm = OllamaLLM(model="mistral:latest")

# Create an embedding model
embeddings = SentenceTransformerEmbeddings(model_name="DiTy/bi-encoder-russian-msmarco")
# Create Chroma vector store
vector_store = Chroma.from_documents(documents, embedding=embeddings)

# Load the QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever()
)
print(f'Модель подготовлена.')


class AI:
    async def ask(self, message: str) -> str:
        response = qa_chain.run(message)
        return response
