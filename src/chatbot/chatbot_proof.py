import openai
from dotenv import load_dotenv
import os
from arduino_conect import preguntar

load_dotenv()
key = os.getenv('CHATGPT_KEY')


client = openai.OpenAI(api_key=key)
prompt = ""
messages = [{"role": "system", "content": "eres Eva, robot de wall-e, no eres un personaje ficticio, existes realmente. Seras presentada como un robot con el que se puede hablar, en una muestra de programacion de una secundaria en Argentina. Tienes un armazon cuadrado, dos ojos que se mueven y hablaras con los chicos que pasen por ahi en ese momento" }]

while prompt != "exit":
    prompt = preguntar()
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages= messages,
        temperature=1,
        max_tokens=200
    )
    messages.append({"role": "assistant", "content": response.choices[0].message.content})
    print(response.choices[0].message.content)
    