"""Chat en terminal para probar el agente localmente, sin Streamlit.

Uso:
    python cli_local.py [--model gpt-4o-mini] [--temperature 0.5]

Comandos dentro del chat:
    salir     termina la conversación
    limpiar   borra el historial y empieza de nuevo
"""

import argparse

from langchain_core.messages import AIMessage, HumanMessage

from assistant import generar_respuesta


def main() -> None:
    parser = argparse.ArgumentParser(description="Chat local de YoKaAi")
    parser.add_argument("--model", default=None, help="Modelo de OpenAI a usar")
    parser.add_argument("--temperature", type=float, default=None, help="Temperatura del modelo")
    args = parser.parse_args()

    historial: list[HumanMessage | AIMessage] = []

    print("YoKaAi · chat local (escribe 'salir' para terminar, 'limpiar' para reiniciar)\n")

    while True:
        try:
            texto = input("Tú: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not texto:
            continue
        if texto.lower() == "salir":
            break
        if texto.lower() == "limpiar":
            historial = []
            print("(historial reiniciado)\n")
            continue

        respuesta = generar_respuesta(
            texto,
            historial,
            model=args.model,
            temperature=args.temperature,
        )
        print(f"YoKaAi: {respuesta}\n")

        historial.append(HumanMessage(content=texto))
        historial.append(AIMessage(content=respuesta))


if __name__ == "__main__":
    main()
