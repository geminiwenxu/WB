import os
from PIL import Image
from langchain_google_genai import ChatGoogleGenerativeAI
import config_llm as config
from langchain_core.messages import HumanMessage
import base64

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.SERVICE_ACCOUNT_KEY_PATH

llm = ChatGoogleGenerativeAI(model=config.G_MODEL)

# Load the PNG in the LLM
png_path = os.path.join(os.path.dirname(__file__), "Data", "images")

png_files = []
for root, dirs, files in os.walk(png_path):
    for file in files:
        if file.endswith(".png"):
            png_files.append(os.path.join(root, file))
print(f"{len(png_files)} Files loaded")

if not png_files:
    print("No PNG files found in the directory. Please check the path:", png_path)
    exit()


# Loading the first png
try:
    img_path = png_files[0]
    img = Image.open(img_path)
    print(f"Image loaded successfully: {img_path}")
except Exception as e:
    print(f"Error loading image {img_path}: {e}")
    exit()


# Konvert png in base64
try:
    with open(img_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")
except Exception as e:
    print(f"Error converting the image to Base64: {e}")
    exit()


prompt = (
    "Analyze the image and describe its content in as much detail as possible in text form, "
    "so that a blind person can imagine the image 1:1. Describe colors, shapes, objects, "
    "background, text (if any), and the overall composition of the image."
)

message = HumanMessage(
    content=[
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": f"data:image/png;base64,{image_data}"}
    ]
)

# Sende die Anfrage an das Modell
try:
    response = llm.invoke([message])
    print("Model's response:")
    print(response.content)
except Exception as e:
    print(f"Error when querying the model: {e}")