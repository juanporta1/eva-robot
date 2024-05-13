import openai
from dotenv import load_dotenv
import os


load_dotenv()
key = os.getenv("CHATGPT_KEY")
client = openai.OpenAI(api_key=key)
def convert(text):
    

    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    os.remove("src/chatbot/chatbot_audio.mp3")
    response.stream_to_file("src/chatbot/chatbot_audio.mp3")