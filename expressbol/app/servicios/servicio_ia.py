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


def analizar_proyeccion(datos_historicos):

    import math
    from datetime import datetime

    hoy = datetime.now()

    valores = [h["valor"] for h in datos_historicos if h["valor"] > 0]
    n = len(valores)
    if n < 2:
        return {"proyeccion": [], "analisis": "<p>Datos insuficientes para proyección</p>"}

    x = list(range(n))
    log_y = [math.log(v) for v in valores]

    sum_x = sum(x)
    sum_y = sum(log_y)
    sum_xy = sum(x[i] * log_y[i] for i in range(n))
    sum_xx = sum(x[i] * x[i] for i in range(n))

    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x * sum_x)
    intercept = (sum_y - slope * sum_x) / n

    meses_nombres = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

    ultimo = datos_historicos[-1]["fecha"] if "fecha" in datos_historicos[-1] else ""
    if ultimo:
        ano = int(ultimo[:4])
        mes = int(ultimo[5:7])
    else:
        ano = hoy.year
        mes = hoy.month

    proyeccion = []
    for i in range(1, 7):
        sig_mes = mes + i
        sig_ano = ano
        while sig_mes > 12:
            sig_mes -= 12
            sig_ano += 1
        label = f"{meses_nombres[sig_mes-1]} {sig_ano}"
        pred_log = intercept + slope * (n - 1 + i)
        pred_val = round(math.exp(pred_log), 2)
        proyeccion.append({"mes": label, "valor": pred_val})

    prompt = f"""
    Eres un analista financiero de una empresa de envios en Bolivia.
    Hoy es {hoy.strftime("%B %Y")}.

    Datos historicos de ingresos mensuales:
    {json.dumps(datos_historicos, indent=2)}

    Proyeccion generada por regresion exponencial para los proximos 6 meses:
    {json.dumps(proyeccion, indent=2)}

    IMPORTANTE:
    Responde SOLO con HTML limpio.
    NO uses markdown.
    NO uses ```html.
    NO uses asteriscos.

    Usa: <h4>, <p>, <ul>, <li>, <strong>

    Genera:
    - analisis de la tendencia historica
    - interpretacion de la proyeccion
    - factores de riesgo
    - recomendaciones estrategicas
    """

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek/deepseek-chat",
            "messages": [{"role": "user", "content": prompt}]
        },
        timeout=30
    )

    resultado_ia = response.json()
    analisis = "Error al generar análisis"
    if "choices" in resultado_ia:
        analisis = resultado_ia["choices"][0]["message"]["content"]

    return {"proyeccion": proyeccion, "analisis": analisis}


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