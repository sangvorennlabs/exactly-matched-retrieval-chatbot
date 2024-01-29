from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

def load_pdf_file(file, chunk_overlap):
    loader = PyPDFLoader(file)
    docs = loader.load()

    documents = RecursiveCharacterTextSplitter(
        chunk_size=chunk_overlap*2, chunk_overlap=chunk_overlap
    ).split_documents(docs)

    # vectordb = FAISS.from_documents(documents, OpenAIEmbeddings(openai_api_key = "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"))
    # retriever = vector.as_retriever() # pass the search algo you want to use here
    return documents