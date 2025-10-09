from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter, TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_google_vertexai import VertexAIEmbeddings
import config as config
import vertexai
import os

# All three are required to use vertex AI.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.SERVICE_ACCOUNT_KEY_PATH
os.environ["GOOGLE_CLOUD_PROJECT"] = config.G_PROJECT_NAME
os.environ["GOOGLE_CLOUD_LOCATION"] = config.G_PROJECT_LOCATION

#Embeddings
#UserWarning: This feature is deprecated as of June 24, 2025 and will be removed on June 24, 2026
vertexai.init(
    project=os.environ["GOOGLE_CLOUD_PROJECT"], 
    location=os.environ["GOOGLE_CLOUD_LOCATION"],
)

loader =PyPDFLoader('/Users/geminiwenxu/Desktop/WB/data/ticket_to_ride.pdf')
docs = []
docs_lazy = loader.lazy_load()

for doc in docs_lazy:
    doc.metadata["UPLOAD_DATE"] = "2025-10-10" #adding more metadata
    #print(type(doc), "------",doc.page_content,"--------")
    print(len(doc.metadata))
    docs.append(doc)

print(type(docs),"----------",docs, "-----------------")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200) # break content

docs =text_splitter.split_documents(docs)

# Initialize the a specific Embeddings Model version
embeddings = VertexAIEmbeddings(
    model_name="gemini-embedding-001"
)
#embeddings_function =HuggingFaceEmbeddings(model_name= 'sentence-transformers/all-MiniLM-L6-v2', model_kwargs={"device":"cpu"})

vectorstore = Chroma.from_documents(docs, embeddings, persist_directory='chroma_db_pdf' )

print(vectorstore._collection.count())
