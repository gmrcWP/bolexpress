import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY no configurada en el archivo .env")

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
    - tendencias
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
            "model": "deepseek/deepseek-v4-flash:free",
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


def analizar_rutas(data):

    prompt = f"""
    Analiza la frecuencia de envíos por ruta y día de la semana para una empresa de envíos en Bolivia.

    Datos (heatmap de rutas por día):
    {json.dumps(data, indent=2)}

    IMPORTANTE:
    Responde SOLO con HTML limpio.
    NO uses markdown.
    NO uses ```html.
    NO uses asteriscos.

    Usa:
    <h4>, <p>, <ul>, <li>, <strong>

    Genera:
    - rutas más demandadas y en qué días
    - rutas con menor tráfico
    - patrones de comportamiento semanal
    - recomendaciones de logística
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
        timeout=30
    )

    resultado = response.json()

    if "choices" not in resultado:
        return "Error al generar análisis"

    return resultado["choices"][0]["message"]["content"]