import streamlit as st
from PyPDF2 import PdfReader
from langchain.chains import create_retrieval_chain
from utils import (
    create_document_chain,
    load_llm_model,
    split_doc_to_chunks,
    vectorize_chunks,
)


def upload_pdf_doc():
    uploaded_pdf = st.sidebar.file_uploader("## Upload", type=["pdf"])
    return uploaded_pdf


def read_pdf_file(pdf_file):
    page_content = ""
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        page_content += page.extract_text()
    num_pages = len(pdf_reader.pages)
    st.sidebar.write(f"The uploaded PDF file has {num_pages} pages.")
    return page_content


def ask_question(vector_db, document_chain):
    db_retriever = vector_db.as_retriever()
    retrieval_chain = create_retrieval_chain(db_retriever, document_chain)
    st.markdown("<h5>Enter your question</h5>", unsafe_allow_html=True)
    user_input = st.text_input("user query", label_visibility="hidden")
    submit_button = st.button("Submit")
    if submit_button and user_input:
        if user_input:
            st.write("Question: ", user_input)
            res = retrieval_chain.invoke({"input": user_input})
            st.write("Answer: ", res["answer"])

    return user_input


def main():
    st.set_page_config(layout="wide", page_title="Understand Document")

    st.title("Understand Document")
    st.subheader("Let's understand one research paper at a time.")

    st.sidebar.write("## Please upload a PDF file :newspaper:", unsafe_allow_html=True)
    uploaded_pdf = upload_pdf_doc()
    if uploaded_pdf is None:
        st.write("Please upload a PDF file to analyze.")
    else:
        pdf_doc = read_pdf_file(uploaded_pdf)
        document_chunks = split_doc_to_chunks(pdf_doc)
        # st.write(document_chunks[2:20])
        vector_db = vectorize_chunks(document_chunks)
        llm = load_llm_model()
        doc_chain = create_document_chain(llm)
        ask_question(vector_db, doc_chain)


if __name__ == "__main__":
    main()
