import os
from langchain_google_genai import ChatGoogleGenerativeAI
import config_llm as config

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.SERVICE_ACCOUNT_KEY_PATH

llm = ChatGoogleGenerativeAI(model=config.G_MODEL)

response = llm.invoke("Gebe mir 3 verschiedene Zahlen aus")
print(response.content)