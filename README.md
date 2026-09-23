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




# 🤖 YoKaAi — chatbot de WhatsApp con LangChain + FastAPI

Asesor comercial virtual para el catálogo de productos de YoKaAi (Filete de Pechuga, Cordon Blue),
construido con LangChain + OpenAI. Se expone como un webhook de la **WhatsApp Cloud API** desplegado
en **Vercel**, y se puede probar en local sin necesidad de WhatsApp ni de Vercel.

## ✨ Características

- **Webhook de WhatsApp Cloud API** (`api/webhook.py`, FastAPI) — verifica el challenge de Meta y
  valida la firma `X-Hub-Signature-256` de cada mensaje entrante.
- **Lógica del agente reutilizable** (`assistant.py`) — mismo código para el webhook y el CLI local.
- **Catálogo e instrucciones en `prompts/`** como archivos markdown, editables sin tocar código.
- **Deduplicación best-effort** de mensajes repetidos (reintentos de Meta) por `message.id`.
- **Sin interfaz gráfica**: se prueba con un chat de terminal o simulando payloads de Meta.

## 📋 Requisitos

- Python 3.10 o superior (recomendado 3.12, igual que en Vercel)
- Cuenta de OpenAI con API Key válida
- Para producción: una app de WhatsApp Cloud API en [Meta for Developers](https://developers.facebook.com/)

## 🚀 Instalación

1. **Clona el repositorio**:

   ```bash
   git clone "url-del-repositorio"
   cd yocaai
   ```

2. **Crea un entorno virtual**:

   ```bash
   python -m venv venv
   ```

   ```bash
   # Windows
   venv\Scripts\activate

   # macOS/GNU-Linux
   source venv/bin/activate
   ```

3. **Instala las dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configura las variables de entorno**: copia `.env.example` a `.env` y completa los valores.
   Nunca subas `.env` al repositorio (ya está en `.gitignore`).

   ```bash
   cp .env.example .env
   ```

## 🧪 Probar en local (sin Streamlit)

No hay interfaz web. Hay dos formas de probar el agente:

### 1. Chat de terminal

Para iterar rápido sobre los prompts, con historial de conversación real:

```bash
python cli_local.py
python cli_local.py --model gpt-4o --temperature 0.2
```

Comandos dentro del chat: `salir` termina, `limpiar` reinicia el historial.

### 2. Simular el webhook completo

Levanta el servidor local:

```bash
uvicorn api.webhook:app --reload --port 8000
```

Y en otra terminal, envía un mensaje simulado con la firma HMAC correcta (usa `WHATSAPP_APP_SECRET`
de tu `.env`):

```bash
python scripts/simular_webhook.py --texto "cuanto vale el filete de pechuga de 150 grs"
```

Flags útiles:

- `--firma-invalida` — envía una firma incorrecta; el webhook debe responder `401`.
- `--repetir` — envía el mismo `message.id` dos veces; la segunda debe omitirse por deduplicación.

> El simulador ejercita el webhook real, así que al final intentará llamar a la Graph API de
> WhatsApp con `enviar_texto()`. Sin credenciales válidas de WhatsApp esa llamada fallará, pero la
> respuesta generada por el agente queda igual en los logs del servidor — suficiente para verificar
> que el catálogo y las instrucciones responden bien.

## ☁️ Despliegue en Vercel

1. Importa el repositorio en Vercel. El **Root Directory** es la raíz del proyecto (no hace falta
   `vercel.json`: Vercel detecta `api/webhook.py` como una Python Function ASGI).
2. En **Project Settings → Environment Variables**, crea todas las variables de `.env.example`.
3. Despliega. El callback del webhook será:

   ```text
   https://TU-PROYECTO.vercel.app/api/webhook
   ```

## 📲 Configuración en Meta

1. Agrega el producto **WhatsApp** a tu app en Meta for Developers y obtén el `Phone number ID` y un
   access token (en producción, un token permanente de usuario del sistema).
2. En **WhatsApp → Configuration → Webhook**, registra la URL de Vercel del paso anterior.
3. Usa exactamente el valor de `WHATSAPP_VERIFY_TOKEN` como *verify token* del challenge.
4. Suscribe el campo `messages`.
5. Copia el *App Secret* de la app a `WHATSAPP_APP_SECRET`; el webhook valida la firma
   `X-Hub-Signature-256` de todos los eventos entrantes.

## Variables de entorno

| Variable | Uso |
| --- | --- |
| `OPENAI_API_KEY` | Credencial de OpenAI |
| `OPENAI_MODEL` | Modelo, por defecto `gpt-4o-mini` |
| `OPENAI_TEMPERATURE` | Temperatura, por defecto `0.5` |
| `WHATSAPP_ACCESS_TOKEN` | Token de la WhatsApp Cloud API |
| `WHATSAPP_PHONE_NUMBER_ID` | ID del número emisor |
| `WHATSAPP_API_VERSION` | Versión de la Graph API, por defecto `v23.0` |
| `WHATSAPP_VERIFY_TOKEN` | Secreto elegido para el challenge inicial de Meta |
| `WHATSAPP_APP_SECRET` | App Secret usado para validar la firma de cada evento |

## ⚠️ Limitaciones conocidas

- **Sin historial entre mensajes de WhatsApp**: Vercel no conserva estado entre invocaciones, así
  que cada mensaje entrante se responde de forma independiente (`assistant.generar_respuesta()` ya
  acepta un `historial`, pero el webhook no lo usa todavía). El chat de terminal sí mantiene contexto,
  porque vive en un solo proceso.
- **Deduplicación best-effort**: los `message.id` procesados se guardan en memoria del proceso, no en
  una base de datos. Si Vercel recicla el proceso entre invocaciones, un reintento de Meta puede
  volver a procesarse.
- **Respuesta síncrona**: el webhook llama a OpenAI dentro de la misma petición HTTP antes de
  responder `200` a Meta, así que una respuesta lenta puede disparar un reintento.

El siguiente paso natural para resolver los tres puntos es conectar Redis (p. ej. Upstash) para
guardar historial por número de teléfono y `message.id` vistos con TTL, y devolver el `200` a Meta
antes de llamar a OpenAI (procesando el mensaje de forma asíncrona).

## Estructura del proyecto

```
yocaai/
├── api/
│   ├── __init__.py
│   └── webhook.py          # FastAPI: GET (challenge) + POST (mensajes)
├── prompts/
│   ├── catalogo.md
│   ├── empresa.md
│   └── instrucciones.md
├── scripts/
│   └── simular_webhook.py  # payload de Meta firmado -> servidor local
├── assistant.py             # lógica del agente, compartida por CLI y webhook
├── cli_local.py             # chat en terminal
├── requirements.txt
├── .env.example
└── standard.md               # estándar de trabajo del equipo
```