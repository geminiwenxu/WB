
contents ="hello world"
def initialize():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.SERVICE_ACCOUNT_KEY_PATH
    aiplatform.init(project=config.G_PROJECT_NAME, location=config.G_PROJECT_LOCATION)
    client = Client(vertexai=True, project=config.G_PROJECT_NAME, location=config.G_PROJECT_LOCATION,)
    return client
client = initialize()
generate_content_config = types.GenerateContentConfig(temperature=1, top_p=0.95, max_output_tokens=8192, response_modalities=["TEXT"], 
                                                      safety_settings=[types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"), 
                                                                       types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"), 
                                                                       types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"), 
                                                                       types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF")])
output = client.models.generate_content_stream(model=config.G_MODEL, contents=contents, config=generate_content_config)
result = ""
for chunk in output:
    result += chunk.text
print(result)