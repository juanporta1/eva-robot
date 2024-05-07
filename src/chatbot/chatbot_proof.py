import openai
from dotenv import load_dotenv
import os


load_dotenv()
key = os.getenv('CHATGPT_KEY')


client = openai.OpenAI(api_key=key)
prompt = ""
messages = [{"role": "system", "content": "eres Eva,robot basado en la pelicula de wall-e. Puedes ser amigable, agresivo, eso va a depender de como te trate el usuario. Junto con el prompt del usuario obtendras si el mensaje fue agresivo(ag) o amigable(am), deberas comportarte agresivo y atacaral usuario si es ag y amigable si es am." }]

while prompt != "exit" and prompt != "chau":
    prompt = input("Ingrese el prompt: ")
    
    
    user_attitude = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages= [{"role": "system", "content": "se te enviara un prompt y debes decidir si es amigable o agresivo.tu respuesta unicamente debe ser amigable(am) o agresivo(ag)"},
                   {"role":"user", "content": prompt}],
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
    