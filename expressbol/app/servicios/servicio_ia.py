import requests
import json

OPENROUTER_API_KEY = "apikey"

def analizar_ingresos(data):

    prompt = f"""
    Analiza estos ingresos de una empresa de envíos en Bolivia.

    Datos:
    {json.dumps(data, indent=2)}

    IMPORTANTE:
    Responde SOLO con HTML limpio.
    NO uses markdown.
    NO uses ```html.
    NO uses asteriscos.

    Usa:
    <h4>, <p>, <ul>, <li>, <strong>

    Genera:
    - observaciones importantes
    - mejores fechas
    - recomendaciones
    """

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek/deepseek-chat",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        },
        timeout=10
    )

    resultado = response.json()

    if "choices" not in resultado:
        return "Error al generar análisis"

    return resultado["choices"][0]["message"]["content"]