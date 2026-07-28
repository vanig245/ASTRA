import os
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

kb_docs = os.path.join("kb_docs")
loader = DirectoryLoader(kb_docs)
documents = loader.load()

chunk_text = []
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50,
    length_function = len
)
texts = text_splitter.split_documents(documents)
embedding_model = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")

chromadb = Chroma.from_documents(
    documents = texts,
    embedding = embedding_model,
    persist_directory = "./chroma_db"
)