import streamlit as st
import openai
from openai import AuthenticationError
from PIL import Image
import requests
from io import BytesIO

# Títulos no Streamlit
st.sidebar.empty()
st.sidebar.title("Bot utilizando a API da OpenAI - GPT")
st.sidebar.subheader("API Key")

api_key = st.sidebar.text_input("Insira aqui a sua chave de API: ", type="password")
openai.api_key = api_key

# Definir bot
bot_list = ["",'ChatBot', 'ImageBot']
opcao = st.sidebar.selectbox("Selecione um Bot", bot_list)

# Gerar chatbot
if opcao == "ChatBot" and api_key != "":
    st.title("ChatBot")
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Faça sua pergunta"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            # Chame a API OpenAI para obter a resposta
            response = openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )

            # Obtenha a resposta do assistente
            assistant_response = response.get("choices", [])
            content = assistant_response[0].get("message", {}).get("content", "")

            # Adicione a resposta à lista de mensagens
            st.session_state.messages.append({"role": "assistant", "content": content})

            # Exiba a resposta na interface do usuário
            with st.chat_message("assistant"):
                st.markdown(content)
        except AuthenticationError:
            st.warning("Erro de autenticação: Verifique se a sua chave de API está correta.")

# Gerar imagebot            
elif opcao == 'ImageBot' and api_key != "":
    st.title("ImageBot")
    
    # Solicitar imagem:
    texto = st.text_input("Sugira uma imagem...")
    
    if texto:
        response = openai.Image.create(
            model="dall-e-3",
            prompt=texto,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        if 'data' in response and response['data']:
            image_url = response["data"][0]["url"]
            # Carregue a imagem a partir da URL
            image = Image.open(requests.get(image_url, stream=True).raw)
            # Exiba a imagem no Streamlit
            st.image(image, caption=f"{texto}")
        else:
            st.warning("Chave 'url' não encontrada na resposta da OpenAI.")
                
elif api_key == "":
     st.warning("Insira a chave de API")
else:
    st.warning("Selecione um bot")
