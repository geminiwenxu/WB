from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain.text_splitter import NLTKTextSplitter
from langchain.text_splitter import MarkdownTextSplitter
from langchain.document_loaders import UnstructuredMarkdownLoader

class Chunker():
    def __init__(self, document):
        self.document = document

    def fixed_sized(self):
        # fixed-sized(character) chunking 
        splitter = CharacterTextSplitter(chunk_size= 50, chun_overlap=2)
        chunks = splitter.split_documents()

    def recursive_char(self):
        # recursive to preserve text 
        splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10)
        chunks = splitter.split_documents()
    
    def setences(self):
        # sentence/paragraph splitting
        text =""
        sentences = text.split("\n")
    
    def Content_aware_chunking(document:str):
        text_splitter = NLTKTextSplitter()
        sentence_docs = text_splitter.split_documents()

        return sentence_docs

    def content(self):
        # content-aware splitting: splitting based in documents structure
        text = "# Header 1\nContent under header.\n\n## Header 2\nMore content here."
        splitter = MarkdownTextSplitter(chunk_size=50)
        chunks = splitter.split_documents(text)
        print(chunks)

    def Specialized_chunking(documentation_md: str):
        """documentation_name.md required"""
        loader = UnstructuredMarkdownLoader(documentation_md)
        documents = loader.load()

    def semantic_chunking(self):
        embedding_model = ""
        splitter = SemanticChunker(embedding_model, breakpoint_threshold_amount=0.95,breakpoint_threshold_type="percentile")
        splitter.split_documents()