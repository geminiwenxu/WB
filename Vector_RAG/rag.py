import signal, sys
import google.generativeai as genai
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from model import VertexAIReader
from sentence_transformers import SentenceTransformer
import torch

def get_relevant_context_from_db(query):
    context = ""
    #embedding_function = HuggingFaceEmbeddings(model_name= 'sentence-transformers/all-MiniLM-L6-v2',model_kwargs={"device": "cpu"}, encode_kwargs={"normalize_embeddings": False})
    


    from langchain_community.embeddings import HuggingFaceEmbeddings

    embedding_function = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": False}
)

# Force reload underlying model to CPU only
    embedding_function.client = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2", device="cpu"
)


    vector_db = Chroma(persist_directory='chroma_db_pdf', embedding_function=embedding_function)
    search_results = vector_db.similarity_search(query, k=2) # Chroma distance is the L2 norm squared; k is the amount of documents to return
    print("----------------------------")
    #print(search_results)
    for result in search_results:
        print(type(result))
        print("result",len(result.metadata))
        context += result.metadata['source']+str(result.metadata['page'])+result.metadata["UPLOAD_DATE"]+result.page_content + "\n"
        print("context",context)
    return context


def generate_rag_prompt(query, context):
    """"
    To generate promot based on the query from user and relevant context based on similarity 
    """
    context = context.replace("'", "").replace("\n", "")
    prompt = ("""you are a bot to retrieve information from our RAG system and answer the questions.
              question: '{query}'
              context: '{context}'
              answer: 
                """).format(query=query, context=context)
    return prompt

def RAG(option, country):
    query = "hello world" + option + country 
    context = get_relevant_context_from_db(query)
    prompt = generate_rag_prompt(query=query, context=context)
    generator = VertexAIReader()
    result = generator.generate_content(prompt)
    return context, result

RAG("HELLO", "WORLD")