from langchain_community.graphs import Neo4jGraph
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import GraphCypherQAChain
from langchain_google_vertexai import ChatVertexAI
from LLM.prompt import retrieval_qa_chat_prompt
import textwrap, vertexai, os, KG.config as config


# Graph search runs exclusively via Cypher on labels/relationships/properties.
def generate_cypher_query(
    question: str, graph, temperature: float = 0, verbose: bool = True
) -> str:
    """
    Generates a Cypher query from a natural language question using a Graph QA chain.

    Args:
        question (str): The natural language question.
        graph: The graph connection object.
        retrieval_qa_chat_prompt (str): The prompt template used by the chain.
        temperature (float, optional): The temperature setting for Gemini. Defaults to 0.
        verbose (bool, optional): Whether to run the chain in verbose mode. Defaults to True.

    Returns:
        str: A formatted Cypher query, wrapped to 60 characters per line.

    Note:
        This chain has the potential to make dangerous requests, so you must set
        'allow_dangerous_requests' to True. Use with caution.
    """

    # Vertex AI via Service Account
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.SERVICE_ACCOUNT_KEY_PATH
    os.environ["GOOGLE_CLOUD_PROJECT"] = config.G_PROJECT_NAME
    os.environ["GOOGLE_CLOUD_LOCATION"] = config.G_PROJECT_LOCATION

    vertexai.init(
        project=os.environ["GOOGLE_CLOUD_PROJECT"],
        location=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"),
    )

    llm = ChatVertexAI(model_name=config.G_MODEL, temperature=temperature)

    #### Protection against dangerous requests still needs to be implemented. ####

    # Create a prompt template for the chain.
    cypher_prompt = PromptTemplate(
        input_variables=["schema", "question"], template=retrieval_qa_chat_prompt
    )

    # Create the QA chain using the provided graph and prompt.
    cypher_chain = GraphCypherQAChain.from_llm(
        llm=llm,
        graph=graph,
        verbose=verbose,
        cypher_prompt=cypher_prompt,
        allow_dangerous_requests=True,  # Acknowledge the risks here.
    )

    # Run the chain with the input question.
    response = cypher_chain.run(question)

    # Format and return the Cypher query.
    return textwrap.fill(response, 60)
