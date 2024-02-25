# Bot do chat GPT sem interface gráfica

import openai
import pyttsx3


# Puxa a chave de API do arquivo senhagpt.py

openai.api_key = input("Insira aqui a sua chave de API: ")

# Função para o chat gerar resposta e armazenar as respostas no histórico

def envio_mensagem(mensagem, msg_list=[]):
    msg_list.append({"role": "user", "content": mensagem})
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=msg_list,
    )
    return resposta["choices"][0]["message"]["content"]


# Array que armazena as respostas que o ChatGPT gera

msg_list = []

# Laço de repetição para repetir perguntas ao Chat

while True:
    pergunta = input("Digite sua mensagem: ")
    if pergunta.lower() == "sair" or pergunta == "":
        break
    else:
        resposta = envio_mensagem(pergunta, msg_list)
        msg_list.append({"role": "assistant", "content": resposta})
        print("CopeneskiGPT: ", resposta)
        fala = pyttsx3.init()
        fala.say(resposta)
        fala.runAndWait()
