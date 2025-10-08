import os
from dotenv import load_dotenv
from langchain_community.graphs import Neo4jGraph


def load_neo4j_graph(env_path: str = ".env") -> Neo4jGraph:
    """loading the Graphdatabase"""
    load_dotenv(env_path, override=True)

    NEO4J_URI = os.getenv("NEO4J_URI")
    NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
    NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")

    # Initialize Neo4j graph object
    graph = Neo4jGraph(
        url=NEO4J_URI,
        username=NEO4J_USERNAME,
        password=NEO4J_PASSWORD,
        database=NEO4J_DATABASE,
    )

    return graph


# Gemini Access
SERVICE_ACCOUNT_KEY_PATH = (
    r"############# PATH ###############################"
)

G_PROJECT_NAME = "Project_Name"
G_PROJECT_LOCATION = "Location"
G_MODEL = "gemini-2.0-flash-001"
