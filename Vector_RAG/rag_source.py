from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load PDF
loader = PyPDFLoader("data/monopoly.pdf")
pages = loader.load_and_split()

# Each `pages[i]` is a Document with `metadata={"page": i+1}`
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(pages)


from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

db = FAISS.from_documents(docs, embeddings)
query = "How old can I play this game?"
results = db.similarity_search(query, k=3)

for r in results:
    print(f"Page {r.metadata['page']}: {r.page_content}")
    print("----------------------------------------------------------")