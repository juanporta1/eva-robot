import openai
from dotenv import load_dotenv
import os
load_dotenv()
key = os.getenv("CHATGPT_KEY")
client = openai.OpenAI(api_key=key)

audio_file = open("src/chatbot/grabacion.wav","rb")

response = client.audio.transcriptions.create(
    model= "whisper-1",
    file=audio_file
    )

print(response.text)