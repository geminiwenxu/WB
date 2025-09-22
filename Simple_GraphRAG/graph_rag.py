import os
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_google_genai import GoogleGenerativeAI
import time
import networkx as nx
from langchain.chains import graph_qa
from langchain_community.chains.graph_qa.base import GraphQAChain
from langchain_core.documents import Document
from langchain_community.graphs.networkx_graph import NetworkxEntityGraph
import google.generativeai as genai
from model import VertexAIReader
import config as config
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.SERVICE_ACCOUNT_KEY_PATH

GOOGLE_API_KEY = "7d00a1fa19974c7c1677698d59b280b5ae013196"
genai.configure(api_key=GOOGLE_API_KEY)


from google import genai
from google.genai import types

llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
text ="Optional list of callback handlers (or callback manager). Defaults to None. Callback handlers are called throughout the lifecycle of a call to a chain, starting with on_chain_start, ending with on_chain_end or on_chain_error. Each custom chain can optionally call additional callback methods, see Callback docs for full details."

documents = [Document(page_content=text)]
llm_transformer = LLMGraphTransformer(llm=llm)
graph_documents = llm_transformer.convert_to_graph_documents(documents)

llm_transformer_filtered = LLMGraphTransformer(
    llm =llm,
    allowed_nodes=["Person", "Country", "Organization"],
    allowed_relationships=["Nationality", "located_in", "worked_at", "spouse","mother"]
)

graph_documents_filtered = llm_transformer.convert_to_graph_documents(documents)

graph = NetworkxEntityGraph()

for node in graph_documents_filtered[0].nodes:
    graph.add_node(node.id)

for edge in graph_documents_filtered[0].relationships:
    graph._graph.add_edge(edge.source.id, edge.target.id,relation=edge.type)

chain = GraphQAChain.from_llm(llm=llm, graph =graph, verbose= True)

question = "hello world"
chain.run(question)