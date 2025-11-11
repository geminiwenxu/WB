from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter, TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_google_vertexai import VertexAIEmbeddings
import config, os, vertexai
from langchain.embeddings.base import Embeddings
from constants import CHUNK_SIZE, CHUNK_OVERLAY, EMBEDDING_MODEL, DB_DIRECTORY, COUNTRIES

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
        loader = PyPDFLoader(f"C:\\Users\\leonu\\Desktop\\Dokumente\\Research\\WB\\data\\{country}\\Guidelines on the use of Remote Customer Onboarding Solutions.pdf")
        docs_lazy = loader.lazy_load()

        for doc in docs_lazy:
            #adding more metadata
            doc.metadata["UPLOAD_DATE"] = "2025-10-10" 
            docs.append(doc)
        return docs
    
    def inject_table(self, docs):
        # TODO: replace "hello world string with table info string"
        table_doc = Document(
            page_content="Hello, world!", metadata={'producer': 'Adobe PDF Library 22.3.98', 'creator': 'Acrobat PDFMaker 22 for Word', 'creationdate': '2023-03-30T08:57:36+02:00', 'author': '', 'classificationcontentmarkingheaderfontprops': '#000000,12,Calibri', 'classificationcontentmarkingheadershapeids': '1,2,3,d,15,16,17,1c,1d', 'classificationcontentmarkingheadertext': 'EBA Regular Use', 'comments': '', 'company': '', 'contenttypeid': '0x01010039B2671E3DAA274C89DACECC5CECCBB8', 'grammarlydocumentid': '36b4ac6da13f3902d397481eda509c4c71438fa2e33f5b4e3c262d4563136e4b', 'keywords': '', 'moddate': '2023-03-30T08:57:49+02:00', 'sourcemodified': 'D:20230329082115', 'subject': '', 'title': '', 'source': '/Users/geminiwenxu/Desktop/WB/data/Guidelines on the use of Remote Customer Onboarding Solutions.pdf', 'total_pages': 45, 'page': 0, 'page_label': '1', 'UPLOAD_DATE': '2025-10-10'}
        )

        docs.append(table_doc)
        print(type(docs),"----------",docs, "-----------------")
    
    def chunk(self, docs):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAY)
        docs =text_splitter.split_documents(docs)
        return docs 

    # def generate_embeddings(self, docs, country):
    #     embeddings = VertexAIEmbeddings(model_name=EMBEDDING_MODEL)
    #     vectorstore = Chroma.from_documents(docs, embeddings, persist_directory=f"chroma_db_pdf_{country}")
    #     print(vectorstore._collection.count())

    def generate_embeddings(self, docs, country):
        embeddings = VertexAIEmbeddings(model_name=EMBEDDING_MODEL)
        vectorstore = Chroma(persist_directory=f"chroma_db_pdf_{country}", embedding_function=embeddings)

        BATCH = 100  # sicher unter 250 bleiben
        for i in range(0, len(docs), BATCH):
             vectorstore.add_documents(docs[i:i+BATCH])

        vectorstore.persist()
        print(f"Vectorstore Chunks: {vectorstore._collection.count()}")
    
    def pipeline(self):
        for country in COUNTRIES:
            docs = self.load_pdf(country)
            docs= self.chunk(docs)
            self.generate_embeddings(docs, country)

Embedding().pipeline()