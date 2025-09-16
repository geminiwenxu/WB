import signal, sys
from langchain_core.tools import tool 
import google.generativeai as genai
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from Vector_RAG.model import VertexAIReader
from langchain.agents import AgentExecutor, create_tool_calling_agent




def signal_handler(sig, frame):
    print('\nThanks for using gemini')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def generate_rag_prompt(query, context):
    """"
    To generate promot based on the query from user and relevant context based on similarity 
    """
    escaped = context.replace("'", "").replace("\n", "")
    prompt = ("""you are a bot to retrieve information from our RAG system and answer the questions.
              question: '{query}'
              context: '{context}'
              answer: 
                """).format(query=query, context=context)
    return prompt


def get_relevant_context_from_db(query):
    context = ""
    embedding_function = HuggingFaceEmbeddings(model_name= 'sentence-transformers/all-MiniLM-L6-v2', model_kwargs={"device":"cpu"})
    vector_db = Chroma(persist_directory='chroma_db_pdf', embedding_function=embedding_function)
    search_results = vector_db.similarity_search(query, k=6) # Chroma distance is the L2 norm squared; k is the amount of documents to return
    for result in search_results:
        context += result.page_content + "\n"
    return context

# create the tools
@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Retrieve information related to a query."""
    embedding_function = HuggingFaceEmbeddings(model_name= 'sentence-transformers/all-MiniLM-L6-v2', model_kwargs={"device":"cpu"})
    vector_db = Chroma(persist_directory='chroma_db_pdf', embedding_function=embedding_function)
    retrieved_docs = vector_db.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs

generator = VertexAIReader()
llm = generator.generate_content("hello world")

def agentic_rag(prompt):
    tools =[retrieve]
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    response = agent_executor.invoke({"input": "why is agentic rag better than naive rag?"})
    return response["output"]





while True:
    print('----------------')
    print('what is your question?')
    query = input('question: ')
    response = agentic_rag(query)