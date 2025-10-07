from langchain_google_vertexai import VertexAIEmbeddings
import KG.config as config
import vertexai
import os

# All three are required to use vertex AI.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.SERVICE_ACCOUNT_KEY_PATH
os.environ["GOOGLE_CLOUD_PROJECT"] = config.G_PROJECT_NAME
os.environ["GOOGLE_CLOUD_LOCATION"] = config.G_PROJECT_LOCATION

#Embeddings
#UserWarning: This feature is deprecated as of June 24, 2025 and will be removed on June 24, 2026
vertexai.init(
    project=os.environ["GOOGLE_CLOUD_PROJECT"], 
    location=os.environ["GOOGLE_CLOUD_LOCATION"],
)

# Initialize the a specific Embeddings Model version
embeddings = VertexAIEmbeddings(
    model_name="gemini-embedding-001"
)

text = "LangChain is the framework for building context-aware reasoning applications."

embedding_output = embeddings.embed(
    [text], 
    embeddings_task_type="RETRIEVAL_DOCUMENT"
    , dimensions=1536
)[0]

#single_vector = embeddings.embed_query(text)
print(str(embedding_output))
print(len(embedding_output))