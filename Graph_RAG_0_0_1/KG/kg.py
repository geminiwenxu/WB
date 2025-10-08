import tqdm
from langchain_google_vertexai import VertexAIEmbeddings
import vertexai


def create_nodes(graph, data: dict, node_label: str, node_name: str):
    """Adds main nodes without creating relationships."""

    main_node_query = f"""
    MERGE (main:{node_label} {{name: $name}})

    """
    graph.query(main_node_query, params={"name": node_name})

    # Create section nodes only (without relationships)
    for section, content in data.items():
        query = f"""
        MERGE (s:Section {{type: $type, parent_name: $name}})

        """
        params = {"type": section, "name": node_name}
        graph.query(query, params=params)


# Add Chunks
def ingest_Chunks(graph, chunks, node_name, node_label):
    """
    Ingests file chunk data into the knowledge graph by merging chunk nodes.

    Args:
        graph: A knowledge graph client or connection object that has a 'query' method.
        chunks: A list of dictionaries, each representing a file chunk with keys:
                        'chunkId', 'text', 'source', 'formItem' and 'chunkSeqId'.
        node_name: A string used to tag the chunk nodes.
        node_label: The dynamic label for the chunk nodes.
    """
    merge_chunk_node_query = f"""
    MERGE (mergedChunk:{node_label} {{chunkId: $chunkParam.chunkId}})
        ON CREATE SET
            mergedChunk.text = $chunkParam.text,
            mergedChunk.source = $chunkParam.Source,
            mergedChunk.formItem = $chunkParam.formItem,
            mergedChunk.SeqId = $chunkParam.chunkSeqId,
            mergedChunk.node_name = $node_name
    RETURN mergedChunk 
    """

    node_count = 0
    for chunk in chunks:
        print(f"Creating ':{node_label}' node for chunk ID {chunk['chunkId']}")
        graph.query(
            merge_chunk_node_query, params={"chunkParam": chunk, "node_name": node_name}
        )
        node_count += 1
    print(f"Created {node_count} nodes")


def create_relationship(graph, query: str):
    """
    Executes the provided Cypher query on the given graph.

    Parameters:
        graph: An instance of a Neo4j connection.
        query: A string containing a valid Cypher query.
    """
    graph.query(query)

###### The following section is only relevant if you want to perform vector searches ######

# vertex ai embedding index
def create_vector_index(graph, index_name):
    """Creates the vector index if it does not exists, using the dynamic node label"""
    vector_index_query = f"""
    CREATE VECTOR INDEX `{index_name}` IF NOT EXISTS
    FOR (n:{index_name}) ON (n.VertexAIEmbedding) 
    OPTIONS {{ indexConfig: {{
        `vector.dimensions`: 1536,
        `vector.similarity_function`: 'cosine'
    }}}}
    """
    graph.query(vector_index_query)


def embed_text(graph, GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION, node_name):
    """
    Creates embeddings for nodes with a dynamic label using Vertex AI Embeddings,
    and displays a single-line progress bar using tqdm.

    Args:
        graph: A knowledge graph client/connection object that has a `query` method.
        GOOGLE_CLOUD_PROJECT: The cloud project name.
        GOOGLE_CLOUD_LOCATION: The location of the server.
        node_name: The label of nodes to process.
    """
    # VertexAI Embedding Model
    vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_LOCATION)

    # Initialize the a specific Embedding Model version
    embeddings = VertexAIEmbeddings(model_name="gemini-embedding-001")

    print("Starting embedding update...")

    # Fetch nodes without embeddings using elementId to avoid deprecated id() warnings
    fetch_nodes_query = f"""
    MATCH (n:{node_name})
    WHERE n.VertexAIEmbedding IS NULL
    RETURN elementId(n) AS node_id, n.text AS text
    """
    nodes = list(graph.query(fetch_nodes_query))
    total_nodes = len(nodes)
    print(f"Found {total_nodes} nodes without embeddings.")

    # Use a single-line progress bar for node updates
    with tqdm.tqdm(
        total=total_nodes, desc="Embedding nodes", ncols=100, leave=True
    ) as pbar:
        for record in nodes:
            node_id = record["node_id"]
            content = record.get("text") or ""

            # skipping nodes with no content
            if not content:
                pbar.update(1)
                continue

            # Creating vector using VertexAI
            embedding_output = embeddings.embed(
                [content], embeddings_task_type="RETRIEVAL_DOCUMENT", dimensions=1536
            )[0]

            update_query = f"""
            MATCH (n:{node_name})
            WHERE elementId(n) = $node_id
            CALL db.create.setNodeVectorProperty(n, "VertexAIEmbedding", $embedding_output)
            SET  n.embedding_dim = size($embedding_output),
            n.embedding_ts  = datetime()
            """

            graph.query(
                update_query,
                params={"node_id": node_id, "embedding_output": embedding_output},
            )

            pbar.update(1)

    print("Finished embedding update.")
