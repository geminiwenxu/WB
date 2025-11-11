
#import google.generativeai as genai
from langchain_community.vectorstores import Chroma
from model import VertexAIReader
#from sentence_transformers import SentenceTransformer
import os, config, vertexai
from langchain_google_vertexai import VertexAIEmbeddings
from constants import q1,q2,q3,q4,q5,q6,q7,q8,q9,q10

def get_relevant_context_from_db(query, country):
    contexts = []

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.SERVICE_ACCOUNT_KEY_PATH
    os.environ["GOOGLE_CLOUD_PROJECT"] = config.G_PROJECT_NAME
    os.environ["GOOGLE_CLOUD_LOCATION"] = config.G_PROJECT_LOCATION

    vertexai.init(
    project=os.environ["GOOGLE_CLOUD_PROJECT"], 
    location=os.environ["GOOGLE_CLOUD_LOCATION"])

    embeddings = VertexAIEmbeddings(model_name="text-embedding-004")

    vector_db = Chroma(persist_directory=f'chroma_db_pdf_{country}', embedding_function=embeddings)
    search_results = vector_db.similarity_search(query, k=3) # Chroma distance is the L2 norm squared; k is the amount of documents to return
    for result in search_results:
        correct_page = result.metadata['page']+1,
        contexts.append({
        "source": result.metadata['source'],
        "page": correct_page,
        "upload_date": result.metadata["UPLOAD_DATE"],
        "content": result.page_content
    })
    return contexts


def generate_rag_prompt(query, context):
    """"
    To generate promot based on the query from user and relevant context based on similarity 
    """
    #context = context.replace("'", "").replace("\n", "")
    prompt = ("""you are a bot to retrieve information from our RAG system and answer the questions.
              question: '{query}'
              context: '{context}'
              answer: 
                """).format(query=query, context=context)
    return prompt


def RAG(query,country):
    context = get_relevant_context_from_db(query,country)
    print('-' * 150)
    print(f"1. Question: {query}")
    print('-' * 150)
    print("2. CONTEXT: ",context)
    prompt = generate_rag_prompt(query=query, context=context)
    result = VertexAIReader().generate_content(prompt)
    print('-' * 150)
    print(result)
    return result

RAG(query = "¿Cuándo entraron oficialmente en vigor las directrices de la EBA?", country="Germany")