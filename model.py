
import os
from google.cloud import aiplatform
from google.genai import types, Client
import config




class VertexAIReader:
    def __init__(self):
        # Set the path to your service account key file
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.SERVICE_ACCOUNT_KEY_PATH

        # Initialize the AI Platform client
        aiplatform.init(project=config.G_PROJECT_NAME, location=config.G_PROJECT_LOCATION)
        self.client = Client(
            vertexai=True,
            project=config.G_PROJECT_NAME,
            location=config.G_PROJECT_LOCATION,
        )
        self.model = config.G_MODEL

    def generate_content(self, question: str):
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=f"""Analyze the following question {question} and answer the questions accordingly.""")
                ]
            )
        ]

        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            max_output_tokens=8192,
            response_modalities=["TEXT"],
            safety_settings=[
                types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF")
            ],
        )

        result = ""
        try:
            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=generate_content_config,
            ):
                result += chunk.text
        except Exception as e:
            result = f"An error occurred: {e}"
        
        return result
if __name__ == "__main__":
    generator = VertexAIReader()
    result = generator.generate_content("hello world")
    print(result)
