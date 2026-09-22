"""Envía un payload de WhatsApp Cloud API firmado contra el webhook local,
sin necesitar ngrok ni una app real en Meta.

Ejemplos:
    python scripts/simular_webhook.py --texto "precios del filete"
    python scripts/simular_webhook.py --texto "hola" --firma-invalida
    python scripts/simular_webhook.py --texto "hola" --repetir
"""

import argparse
import hashlib
import hmac
import json
import os
import uuid

import httpx
from dotenv import load_dotenv

load_dotenv()


def construir_payload(telefono: str, texto: str, message_id: str) -> dict:
    # Forma mínima real de un evento de Meta con un mensaje de texto entrante.
    return {
        "entry": [
            {
                "changes": [
                    {
                        "value": {
                            "messages": [
                                {
                                    "from": telefono,
                                    "id": message_id,
                                    "text": {"body": texto},
                                    "type": "text",
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    }


def firmar(body: bytes, secreto: str) -> str:
    return "sha256=" + hmac.new(secreto.encode(), body, hashlib.sha256).hexdigest()


def enviar(url: str, body: bytes, firma: str) -> httpx.Response:
    return httpx.post(
        url,
        content=body,
        headers={"Content-Type": "application/json", "X-Hub-Signature-256": firma},
        timeout=30,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Simula un webhook entrante de WhatsApp Cloud API")
    parser.add_argument("--texto", required=True, help="Texto del mensaje entrante a simular")
    parser.add_argument("--url", default="http://localhost:8000/api/webhook", help="URL del webhook local")
    parser.add_argument("--telefono", default="573000000000", help="Número remitente simulado")
    parser.add_argument("--firma-invalida", action="store_true", help="Envía una firma incorrecta (debe dar 401)")
    parser.add_argument("--repetir", action="store_true", help="Envía el mismo message.id dos veces (prueba dedup)")
    args = parser.parse_args()

    secreto = os.getenv("WHATSAPP_APP_SECRET")
    if not secreto and not args.firma_invalida:
        raise SystemExit("Falta WHATSAPP_APP_SECRET en el entorno (.env)")

    message_id = f"wamid.simulado-{uuid.uuid4()}"
    payload = construir_payload(args.telefono, args.texto, message_id)
    # Se serializa una sola vez: la firma se calcula sobre estos bytes
    # exactos, y son los mismos que se envían en el POST.
    body = json.dumps(payload).encode("utf-8")

    firma = "sha256=" + "0" * 64 if args.firma_invalida else firmar(body, secreto)

    envios = 2 if args.repetir else 1
    for intento in range(envios):
        respuesta = enviar(args.url, body, firma)
        print(f"[{intento + 1}/{envios}] POST {args.url} -> {respuesta.status_code}")
        print(respuesta.text)


if __name__ == "__main__":
    main()
