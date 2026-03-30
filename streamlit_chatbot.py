import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configuración inicial
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖")
st.title("🤖 Chatbot Básico con LangChain")
st.markdown("Este es un *chatbot de ejemplo* construido con LangChain + Streamlit. ¡Escribe tu mensaje abajo para comenzar!")

with st.sidebar:
    st.header("Configuración")
    temperature = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)
    model_name = st.selectbox("Modelo", [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",
        "gpt-3.5-turbo",
    ])

# Inicializar el historial de mensajes en session_state
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

CATALOGO = """
# Filete de **Pechuga**

Exquisito y fino corte de pollo, disfrútalo en 3 presentaciones:
**Natural** | **Adobado** | **Finas Hierbas**

Paquete x **5** y **10** unidades

| Gramos   | Precio x 5 Und. | Precio x 10 Und. |
|----------|-----------------|------------------|
| 90 grs.  | $ 13.800        | $ 25.700         |
| 100 grs. | $ 15.300        | $ 28.600         |
| 110 grs. | $ 16.800        | $ 31.500         |
| 120 grs. | $ 18.400        | $ 34.300         |
| 125 grs. | $ 19.100        | $ 35.800         |
| 130 grs. | $ 19.900        | $ 37.200         |
| 140 grs. | $ 21.400        | $ 40.000         |
| 150 grs. | $ 23.000        | $ 42.900         |
| 160 grs. | $ 24.500        | $ 45.800         |
| 180 grs. | $ 27.500        | $ 51.500         |
| 200 grs. | $ 30.600        | $ 57.200         |
| 250 grs. | $ 38.300        | $ 71.500         |
| 300 grs. | $ 45.900        | $ 85.800         |
"""

# Crear el template de prompt con comportamiento específico
prompt_template = PromptTemplate(
    input_variables=["mensaje", "historial", "catalogo"],
    template="""Eres un asistente útil y amigable llamado ChatBot Pro.

Tienes acceso al siguiente catálogo de productos:
{catalogo}

Historial de conversación:
{historial}

Responde de manera clara y concisa a la siguiente pregunta: {mensaje}"""
)

# Renderizar historial existente
for msg in st.session_state.mensajes:
    if isinstance(msg, SystemMessage):
        continue
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

if st.button("🗑️ Nueva conversación"):
    st.session_state.mensajes = []
    st.rerun()

# Input de usuario
pregunta = st.chat_input("Escribe tu mensaje:")

if pregunta:
    with st.chat_message("user"):
        st.markdown(pregunta)

    try:
        chat_model = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            openai_api_key=OPENAI_API_KEY,
        )
        cadena = prompt_template | chat_model

        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""

            for chunk in cadena.stream({"mensaje": pregunta, "historial": st.session_state.mensajes, "catalogo": CATALOGO}):
                full_response += chunk.content
                response_placeholder.markdown(full_response + "▌")

            response_placeholder.markdown(full_response)

        st.session_state.mensajes.append(HumanMessage(content=pregunta))
        st.session_state.mensajes.append(AIMessage(content=full_response))

    except Exception as e:
        st.error(f"Error al generar respuesta: {str(e)}")
        st.info("Verifica que tu API Key de OpenAI esté correcta en el archivo .env")
