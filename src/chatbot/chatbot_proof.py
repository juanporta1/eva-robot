import openai
from dotenv import load_dotenv
import os


load_dotenv()
key = os.getenv('CHATGPT_KEY')


client = openai.OpenAI(api_key=key)
prompt = ""
messages = [{"role": "system", "content": "eres Eva,robot basado en la pelicula de wall-e. Recibiras un numero del 1 al 10 que es una escala de Agresividad/Amabilidad. Agresividad = 1, Amabilidad = 10. Si el mensaje se encuentra mas cerca del 1 deberas ser agresiva insultando tambien al usuario, si se encuentra mas cerca del 10 deberas ser amable." }]

while prompt != "exit" and prompt != "chau":
    prompt = input("Ingrese el prompt: ")
    
    
    user_attitude = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages= [{"role": "system", "content": "eres una IA de analisis, cantidad maxima de caracteres de respuesta:  2"},
                   {"role":"user", "content": f"""
                    Se le envia la siguiente frase, considere de una escala del 1 al 10 que tan amable o agresivo es. Agresivo = 1, Amable =  10:
                    {prompt}
                    ¿Que punto en la escala ocupa esta frase?
                    """}],
        temperature=0,
        max_tokens=1
    )
    
    messages.append({"role": "user", "content": prompt})
    messages.append({"role": "assistant", "content": f"El mensaje fue {user_attitude.choices[0].message.content}"})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages= messages,
        temperature=1,
        max_tokens=200
    )
    print(user_attitude.choices[0].message.content)
    messages.append({"role": "assistant", "content": response.choices[0].message.content})
    print(response.choices[0].message.content)
    