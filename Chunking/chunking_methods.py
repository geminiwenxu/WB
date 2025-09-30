#Fixed-size chunking
from langchain.text_splitter import CharacterTextSplitter
#Conten-aware chunking
from langchain.text_splitter import NLTKTextSplitter
from langchain.document_loaders import TextLoader
#Recursive chunking
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import WebBaseLoader
#Specialized chunking
from langchain.text_splitter import MarkdownTextSplitter
from langchain.document_loaders import UnstructuredMarkdownLoader
#Semantic chunking
from langchain.text_splitter import SemanticChunker
from langchain.embeddings import OpenAIEmbeddings

def Fixed_size_chunking(text:str): 
    """Full size text as string required"""

    text_splitter = CharacterTextSplitter(
    seperator = "\n\n",
    chunk_size = 256,
    chunk_overlap = 20
    )

    chunks = text_splitter.create_documents([text])
    return chunks

def Content_aware_chunking(document:str):
    """document_name.txt is required"""

    loader = TextLoader(document)
    documents = loader.load()

    text_splitter = NLTKTextSplitter()
    sentence_docs = text_splitter.split_documents(documents)

    return sentence_docs

def Recursive_chunking(document: str):
    """document_name.txt is required"""

    loader = TextLoader(document)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 256,
        chunk_overlap = 20,
        seperators = {"\n\n", "\n", " ", ""} #customizable
    )

    chunks = text_splitter.split_documents(documents)
    return chunks

def Specialized_chunking(documentation_md: str):
    """documentation_name.md required"""
    loader = UnstructuredMarkdownLoader(documentation_md)
    documents = loader.load()

    markdown_splitter = MarkdownTextSplitter(chunk_size=100, chunk_overlap=0)
    markdown_chunks = markdown_splitter.split_documents(documents)
    return markdown_chunks

def Semantic_chunking(text: str):
    """whole text as str required"""
    embeddings = OpenAIEmbeddings()
    semantic_chunker = SemanticChunker(embeddings)

    semantic_chunks = semantic_chunker.create_documents([text])
    return semantic_chunks