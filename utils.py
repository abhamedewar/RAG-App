from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate


def load_llm_model(model="llama3.1:8b"):
    llm = Ollama(model=model)
    return llm


def split_doc_to_chunks(pdf_doc):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100)
    document_chunks = text_splitter.split_text(pdf_doc)
    return document_chunks


def vectorize_chunks(document_chunks):
    vector_db = FAISS.from_texts(document_chunks[2:4], OllamaEmbeddings())
    return vector_db


def create_document_chain(llm):
    promt = ChatPromptTemplate.from_template("""
    Answer questions based on the provided context.
    <context>{context}</context>
    Question: {input}""")
    doc_chain = create_stuff_documents_chain(llm, promt)
    return doc_chain
