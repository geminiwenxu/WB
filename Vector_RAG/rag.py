import signal, sys
import google.generativeai as genai
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from model import VertexAIReader
from sentence_transformers import SentenceTransformer
import torch
import os
import config
import vertexai
from langchain_google_vertexai import VertexAIEmbeddings

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
    search_results = vector_db.similarity_search(query, k=2) # Chroma distance is the L2 norm squared; k is the amount of documents to return
    for result in search_results:
        contexts.append({
        "source": result.metadata['source'],
        "page": result.metadata['page'],
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
    print("CONTEXT: ",context)
    prompt = generate_rag_prompt(query=query, context=context)
    result = VertexAIReader().generate_content(prompt)
    print("--------------------------------------------")
    print("RESULT: ",result)
    return result

RAG(query = "please explain the nature and purpose of the business relationship", country="Germany")