from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter, TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_google_vertexai import VertexAIEmbeddings
import config as config
import vertexai
import os
from langchain.embeddings.base import Embeddings
from constants import CHUNK_SIZE, CHUNK_OVERLAY, EMBEDDING_MODEL, DB_DIRECTORY, COUNTRIES
import extract

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.SERVICE_ACCOUNT_KEY_PATH
os.environ["GOOGLE_CLOUD_PROJECT"] = config.G_PROJECT_NAME
os.environ["GOOGLE_CLOUD_LOCATION"] = config.G_PROJECT_LOCATION
vertexai.init(
    project=os.environ["GOOGLE_CLOUD_PROJECT"], 
    location=os.environ["GOOGLE_CLOUD_LOCATION"])

class Embedding():
    def __init__(self):
        pass

    def load_pdf(self, country="Germany"):
        """ Go to a country folder to load files in this folder
        When packing doc into docs, it is possible to add meta-data
        Returns: List of lists of langchain Document object
        """
        docs = []
        pdf_path = f"/Users/geminiwenxu/Desktop/WB/data/{country}/Guidelines on the use of Remote Customer Onboarding Solutions.pdf"
        loader = PyPDFLoader(pdf_path)
        docs_lazy = loader.lazy_load()

        for doc in docs_lazy:
            #adding more metadata
            doc.metadata["UPLOAD_DATE"] = "2025-10-10" 
            docs.append(doc)
        return docs, pdf_path

    def table_extract(self, pdf_path):
        table_list = extract.extract_tables_for_rag(pdf_path)
        return table_list
    
    def inject_table(self, docs, pdf_path):
        """
        Adds all extracted Tables at the end of the doc
        """
        table_strings = self.table_extract(pdf_path)

        for idx, table_text in enumerate(table_strings):
            if not table_text.strip():
                continue

            table_doc = Document(
                page_content=table_text,
                metadata={
                    "source": pdf_path,
                    "type": "table",
                    "table_index": idx,
                    "UPLOAD_DATE": "2025-10-10",
                    "country": docs[0].metadata.get("country", "unknown") if docs else "unknown"
                }
            )
            docs.append(table_doc)

        print(f"Table(s) added. New Document count: {len(docs)}")
        return docs
    
    def chunk(self, docs):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAY)
        docs =text_splitter.split_documents(docs)
        return docs 

    def generate_embeddings(self, docs, country):
        embeddings = VertexAIEmbeddings(model_name=EMBEDDING_MODEL)
        vectorstore = Chroma.from_documents(docs, embeddings, persist_directory=f"chroma_db_pdf_{country}")
        print(vectorstore._collection.count())
    
    def pipeline(self):
        for country in COUNTRIES:
            docs, pdf_path = self.load_pdf(country)
            docs = self.inject_table(docs, pdf_path)
            docs = self.chunk(docs)
            self.generate_embeddings(docs, country)

Embedding().pipeline()
