import openai
from dotenv import load_dotenv
import os


load_dotenv()
key = os.getenv('CHATGPT_KEY')


client = openai.OpenAI(api_key=key)


def get_response(input,context,name):
    prompt = input
    
    
    # user_attitude = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages= [{"role": "system", "content": """eres una IA de analisis, debes dar un numero que va del 1 al 10, escala que definira que tan agresivo es un mensaje, el 1 es muy agresivo, el 10 es nada agresivo.
    #     Por ejemplo:
    #     Mensaje: Sos un tonto.
    #     Devuelve: 1
    #     Mensaje: Muchas Gracias, sos muy lindo.
    #     Devuelve: 10
    #         """},   
    #             {"role":"user", "content": f"{prompt}"}],
    #     temperature=0,
    #     max_tokens=1
    # )
    
    # has_name = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[{"role": "system", "content": "Primero debes detectar si el prompt tiene "}]
    # )
    
    
    context.append({"role": "user", "content": f"""{prompt}
                    Nombre: {name}
                    """})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages= context,
        temperature=1,
        max_tokens=750
    )
    
    context.append({"role": "assistant", "content": response.choices[0].message.content})
    print(response.choices[0].message.content)
    
    return response.choices[0].message.content, context
    