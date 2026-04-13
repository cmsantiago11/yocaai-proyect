 ______     ______     ______     _____     __    __     ______    
/\  == \   /\  ___\   /\  __ \   /\  __-.  /\ "-./  \   /\  ___\   
\ \  __<   \ \  __\   \ \  __ \  \ \ \/\ \ \ \ \-./\ \  \ \  __\   
 \ \_\ \_\  \ \_____\  \ \_\ \_\  \ \____-  \ \_\ \ \_\  \ \_____\ 
  \/_/ /_/   \/_____/   \/_/\/_/   \/____/   \/_/  \/_/   \/_____/ 
                                                                   





╔─────────────────────────────────────────────────────────────────────────────╗
│                                                                             │
│                                                                             │
│    ___    ___ ________  ___  __    ________  ________  ___                  │
│   |\  \  /  /|\   __  \|\  \|\  \ |\   __  \|\   __  \|\  \                 │
│   \ \  \/  / | \  \|\  \ \  \/  /|\ \  \|\  \ \  \|\  \ \  \                │
│    \ \    / / \ \  \\\  \ \   ___  \ \   __  \ \   __  \ \  \               │
│     \/  /  /   \ \  \\\  \ \  \\ \  \ \  \ \  \ \  \ \  \ \  \              │
│   __/  / /      \ \_______\ \__\\ \__\ \__\ \__\ \__\ \__\ \__\             │
│  |\___/ /        \|_______|\|__| \|__|\|__|\|__|\|__|\|__|\|__|             │
│  \|___|/                                                                    │
│                                                                             │
│                                                                             │
│   ________  ________  ________        ___  _______   ________ _________     │
│  |\   __  \|\   __  \|\   __  \      |\  \|\  ___ \ |\   ____\\___   ___\   │
│  \ \  \|\  \ \  \|\  \ \  \|\  \     \ \  \ \   __/|\ \  \___\|___ \  \_|   │
│   \ \   ____\ \   _  _\ \  \\\  \  __ \ \  \ \  \_|/_\ \  \       \ \  \    │
│    \ \  \___|\ \  \\  \\ \  \\\  \|\  \\_\  \ \  \_|\ \ \  \____   \ \  \   │
│     \ \__\    \ \__\\ _\\ \_______\ \________\ \_______\ \_______\  \ \__\  │
│      \|__|     \|__|\|__|\|_______|\|________|\|_______|\|_______|   \|__|  │
│                                                                             │
│                                                                             │
╚─────────────────────────────────────────────────────────────────────────────╝


        This guy is a heretic and
          should be flamed at once.
                      /
                     /
            )            (
           /(   (\___/)  )\
          ( #)  \ ('')| ( #
           ||___c\  > '__||
           ||**** ),_/ **'|
     .__   |'* ___| |___*'|
      \_\  |' (    ~   ,)'|
       ((  |' /(.  '  .)\ |
        \\_|_/ <_ _____> \______________
         /   '-, \   / ,-'      ______  \
b'ger   /      (//   \\)     __/     /   \
                            './_____/




# 🤖 Chatbot Básico con LangChain + Streamlit

Aplicación de chatbot interactivo construida con Python, utilizando LangChain para la integración con modelos de OpenAI y Streamlit para la interfaz web.

## ✨ Características

- **Interfaz web intuitiva** construida con Streamlit
- **Integración con OpenAI** mediante LangChain
- **Múltiples modelos disponibles**: GPT-4o, GPT-4o-mini, GPT-4-turbo, GPT-3.5-turbo
- **Control de temperatura** ajustable (0.0 - 1.0) para personalizar la creatividad de las respuestas
- **Historial de conversación persistente** durante la sesión
- **Configuración en sidebar** para ajustes rápidos del modelo

## 📋 Requisitos

- Python 3.8 o superior
- Cuenta de OpenAI con API Key válida

## 🚀 Instalación

1. **Clona o descarga el repositorio**:

   ```bash
   git clone "url-del-repositorio"
   cd "nombre-del-proyecto"


## Crea un entorno virutal

python -m venv venv

#### Windows
venv\Scripts\activate

#### macOS/GNU-Linux
source venv/bin/activate

### Instala las dependencias

`pip install -r requirements.txt`

- Considera tus entornoe de variable. Normalmente se ubican en un archivo oculo *.env*.

`OPENAI_API_KEY=tu-api-key-de-openai`

- Y corre el programa con:

`streamlit run streamlit_chatboy.py`