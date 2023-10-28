import openai
from senhagpt import API_KEY

# Puxa a chave de API do arquivo senhagpt.py

openai.api_key = API_KEY

# Função para o chat gerar resposta e armazenar as respostas no histórico


def envio_mensagem(mensagem, msg_list=[]):

    msg_list.append({"role": "user", "content": mensagem})

    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=msg_list,
    )

    return resposta["choices"][0]["message"]

# Comandos e laço de repetição para o usuário realizar a pergunta e o programa exibir a resposta


msg_list = []
while True:
    pergunta = input("Digite sua mensagem: ")
    if pergunta.lower() == "sair" or pergunta == "":
        break
    else:
        resposta = envio_mensagem(pergunta, msg_list)
        msg_list.append(resposta)
        print("Chatbot: ", resposta["content"])
