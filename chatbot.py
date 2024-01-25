import openai
import pyttsx3
import streamlit as st

# Gerar página

st.sidebar.empty()
st.sidebar.title("Chatbot utilizando a API da OpenAI - GPT")
st.sidebar.subheader("API Key")
st.title("ChatBot")

# Inserir a chave de API para o programa funcionar
chave_api = st.sidebar.text_input("Insira aqui a sua chave de API: ", type="password")
openai.api_key = chave_api

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
if chave_api:
    indice_pergunta = 0
    while True:
        key_pergunta = f"pergunta_{indice_pergunta}"
        pergunta = st.text_input(f"Pergunta {indice_pergunta + 1}: ", key=key_pergunta)
        if pergunta.lower() == "sair" or pergunta == "":
            break
        else:
            resposta = envio_mensagem(pergunta, msg_list)
            msg_list.append({"role": "user", "content": pergunta})
            msg_list.append({"role": "assistant", "content": resposta})
            st.text_area("CopcesckiGPT: ", resposta, key=f"resposta_{indice_pergunta}")
            indice_pergunta += 1
else:
    st.warning("Insira uma chave de API")