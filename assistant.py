"""Lógica del agente YoKaAi, compartida por el CLI local y el webhook."""

import logging
import os
from pathlib import Path
from typing import Iterable

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

load_dotenv()

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

logging.basicConfig(
    level=logging.INFO,  # Usar DEBUG solo en entorno local
    format=LOG_FORMAT,
)
logger = logging.getLogger(__name__)

PROMPTS_DIR = Path(__file__).parent / "prompts"


def _leer_prompt(nombre: str) -> str:
    return (PROMPTS_DIR / nombre).read_text(encoding="utf-8")


SYSTEM_PROMPT = """# Contexto de la empresa
{empresa}

# Instrucciones
{instrucciones}

# Catálogo de productos
{catalogo}
""".format(
    empresa=_leer_prompt("empresa.md"),
    instrucciones=_leer_prompt("instrucciones.md"),
    catalogo=_leer_prompt("catalogo.md"),
)


def generar_respuesta(
    mensaje: str,
    historial: Iterable[BaseMessage] | None = None,
    *,
    model: str | None = None,
    temperature: float | None = None,
) -> str:
    """Genera una respuesta del agente. Compartida por el CLI y el webhook."""
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Falta la variable de entorno OPENAI_API_KEY")

    chat = ChatOpenAI(
        model=model or os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=temperature if temperature is not None else float(os.getenv("OPENAI_TEMPERATURE", "0.5")),
    )
    mensajes = [SystemMessage(content=SYSTEM_PROMPT)]
    mensajes.extend(historial or [])
    mensajes.append(HumanMessage(content=mensaje))

    logger.info("Generando respuesta (modelo=%s)", chat.model_name)
    return str(chat.invoke(mensajes).content)
