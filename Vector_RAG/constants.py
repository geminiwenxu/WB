SYS_PROMOT= """ you are a smart document reader, your task is to generate answer based on the retrieved context """
RESPONSE_SCHEMA = """{
    
    List the numbers from 1 to 10 and their names in English, French, German, Chinese, Russian and Arabic.
    Provide the output in this exact JSON format:
    {
      "numbers": [
        {
          "number": 1,
          "English": "one",
          "French": "un",
          "German": "ein"
          "Chinese": "一"
          "Russian": "один"
          "Arabic": "واحد"
        },
        ...and so on for numbers 1-10
      ]
    }
}"""
