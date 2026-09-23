"""Webhook de WhatsApp Cloud API. Se sirve como Vercel Python Function y,
en local, con `uvicorn api.webhook:app --reload`."""

import hashlib
import hmac
import json
import logging
import os
from collections import OrderedDict

import httpx
from fastapi import FastAPI, Query, Request
from fastapi.responses import PlainTextResponse

from assistant import generar_respuesta

logger = logging.getLogger(__name__)

app = FastAPI()

# Meta reintenta la entrega del webhook si no recibe un 200 a tiempo, y
# generar_respuesta() puede tardar varios segundos (llamada a OpenAI dentro
# de la misma petición). Este set acotado evita responder dos veces al mismo
# mensaje cuando el proceso se reutiliza entre invocaciones; no es una
# garantía porque Vercel puede reciclar el proceso en cualquier momento.
MAX_IDS_RECORDADOS = 256
_mensajes_procesados: "OrderedDict[str, None]" = OrderedDict()


def _ya_fue_procesado(message_id: str) -> bool:
    if message_id in _mensajes_procesados:
        return True
    _mensajes_procesados[message_id] = None
    if len(_mensajes_procesados) > MAX_IDS_RECORDADOS:
        _mensajes_procesados.popitem(last=False)
    return False


def verificar_firma(body: bytes, firma: str | None, secreto: str) -> bool:
    if not firma or not firma.startswith("sha256="):
        return False
    esperada = hmac.new(secreto.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(firma.removeprefix("sha256="), esperada)


def extraer_mensajes(payload: dict) -> list[dict[str, str]]:
    """Extrae solamente mensajes de texto entrantes del payload de Meta."""
    resultado = []
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            for message in value.get("messages", []):
                texto = message.get("text", {}).get("body")
                remitente = message.get("from")
                message_id = message.get("id")
                if texto and remitente and message_id:
                    resultado.append({"from": remitente, "text": texto, "id": message_id})
    return resultado


def enviar_texto(destino: str, texto: str) -> None:
    token = os.environ["WHATSAPP_ACCESS_TOKEN"]
    phone_number_id = os.environ["WHATSAPP_PHONE_NUMBER_ID"]
    api_version = os.getenv("WHATSAPP_API_VERSION", "v23.0")
    respuesta = httpx.post(
        f"https://graph.facebook.com/{api_version}/{phone_number_id}/messages",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": destino,
            "type": "text",
            "text": {"preview_url": False, "body": texto[:4096]},
        },
        timeout=20,
    )
    respuesta.raise_for_status()


@app.get("/api/webhook")
def verificar_webhook(
    # Meta envía los parámetros con puntos (hub.mode), inválidos como
    # nombres de Python, así que se mapean con alias.
    mode: str = Query("", alias="hub.mode"),
    token: str = Query("", alias="hub.verify_token"),
    challenge: str = Query("", alias="hub.challenge"),
):
    verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN")
    if verify_token and mode == "subscribe" and hmac.compare_digest(token, verify_token):
        return PlainTextResponse(challenge, status_code=200)
    return PlainTextResponse("Verificación rechazada", status_code=403)


@app.post("/api/webhook")
async def recibir_webhook(request: Request):
    body = await request.body()
    app_secret = os.getenv("WHATSAPP_APP_SECRET")
    if not app_secret:
        logger.error("Falta WHATSAPP_APP_SECRET")
        return PlainTextResponse("Webhook no configurado", status_code=500)

    firma = request.headers.get("X-Hub-Signature-256")
    if not verificar_firma(body, firma, app_secret):
        return PlainTextResponse("Firma inválida", status_code=401)

    try:
        payload = json.loads(body)
        for mensaje in extraer_mensajes(payload):
            if _ya_fue_procesado(mensaje["id"]):
                logger.info("Mensaje %s ya fue procesado, se omite", mensaje["id"])
                continue
            enviar_texto(mensaje["from"], generar_respuesta(mensaje["text"]))
    except (json.JSONDecodeError, KeyError, ValueError):
        logger.exception("Payload o configuración inválidos")
        return PlainTextResponse("Solicitud inválida", status_code=400)
    except Exception:
        logger.exception("No fue posible procesar el mensaje")
        return PlainTextResponse("Error procesando el mensaje", status_code=500)

    return PlainTextResponse("EVENT_RECEIVED", status_code=200)
