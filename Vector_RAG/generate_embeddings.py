from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter, TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

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
#char_spliiter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#token_spliiter = TokenTextSplitter(chunk_size=1000, chunk_overlap=200)

docs =text_splitter.split_documents(docs)

embeddings_function =HuggingFaceEmbeddings(model_name= 'sentence-transformers/all-MiniLM-L6-v2', model_kwargs={"device":"cpu"})

vectorstore = Chroma.from_documents(docs, embeddings_function, persist_directory='chroma_db_pdf' )

print(vectorstore._collection.count())
