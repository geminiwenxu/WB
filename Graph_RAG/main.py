from Graph_RAG.KG.config import load_neo4j_graph
from Graph_RAG.VectorRAG import query_vector_rag
from Graph_RAG.GraphRAG import generate_cypher_query
graph, openAI_api, openAI_endpoint = load_neo4j_graph()



question = "who killed napoleon?"
vector_index_name = 'Chunk'
vector_node_label = 'Chunk'
vector_source_property= 'text'
vector_embedding_property = 'textEmbeddingOpenAI'

Vector_RAG = query_vector_rag(
    question=question, 
    vector_index_name=vector_index_name, 
    vector_node_label=vector_node_label, 
    vector_source_property=vector_source_property, 
    vector_embedding_property=vector_embedding_property
    )
print(Vector_RAG)


generate_cypher_query(graph=graph, question=question)