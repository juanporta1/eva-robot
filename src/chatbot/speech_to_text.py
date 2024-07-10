import openai
from dotenv import load_dotenv
import os
load_dotenv()
key = os.getenv("CHATGPT_KEY")
client = openai.OpenAI(api_key=key)
def convert(path):
    audio_file = open(path,"rb")

    response = client.audio.transcriptions.create(
        model= "whisper-1",
        file=audio_file
        )
    print(response.text)
    return response.text