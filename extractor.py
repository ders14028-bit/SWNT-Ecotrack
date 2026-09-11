"""Extrae actividades de una frase libre usando el LLM."""

import json
import os
import re

import google.generativeai as genai
from dotenv import load_dotenv

from factores import CATEGORIA_NO_RECONOCIDA, CATEGORIAS_VALIDAS

MODELO = "gemini-3.6-flash"

SISTEMA = """Eres un extractor de actividades de huella de carbono.
Devuelve SOLO un JSON válido, sin markdown ni texto extra, con esta forma:
{"actividades":[{"tipo":"transporte|alimentacion","categoria":"...","cantidad":numero,"unidad":"km|comida"}]}

Categorías de transporte: carro, bus, moto, bicicleta, avion. Unidad: km.
Categorías de alimentación: carne_roja, pollo_pescado, vegetariano. Unidad: comida.
Si no encaja en ninguna categoría, usa "categoria": "no_reconocida" y el tipo más cercano (transporte o alimentacion).
cantidad debe ser un número (usa 1 si no se indica). Extrae todas las actividades mencionadas."""


def extraer_actividades(texto: str) -> dict:
    """Llama al LLM y normaliza categorías para que el cálculo no reciba valores inventados."""
    modelo = _modelo_gemini()
    respuesta = modelo.generate_content(texto)
    crudo = respuesta.text or ""
    datos = _parsear_json(crudo)
    actividades = datos.get("actividades", [])
    if not isinstance(actividades, list):
        actividades = []
    return {"actividades": [_normalizar(act) for act in actividades]}


def _modelo_gemini() -> genai.GenerativeModel:
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Falta GEMINI_API_KEY. Configúrala como variable de entorno."
        )
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name=MODELO,
        system_instruction=SISTEMA,
        generation_config={
            "response_mime_type": "application/json",
            "max_output_tokens": 1024,
        },
    )


def _parsear_json(texto: str) -> dict:
    limpio = texto.strip()
    bloque = re.search(r"```(?:json)?\s*([\s\S]*?)```", limpio)
    if bloque:
        limpio = bloque.group(1).strip()
    datos = json.loads(limpio)
    if not isinstance(datos, dict):
        raise ValueError("El LLM no devolvió un objeto JSON.")
    return datos


def _normalizar(actividad: dict) -> dict:
    tipo = str(actividad.get("tipo", "")).strip().lower()
    categoria = str(actividad.get("categoria", "")).strip().lower()
    try:
        cantidad = float(actividad.get("cantidad", 1) or 1)
    except (TypeError, ValueError):
        cantidad = 1.0
    unidad = str(actividad.get("unidad", "")).strip().lower()
    validas = CATEGORIAS_VALIDAS.get(tipo, set())
    if categoria not in validas:
        categoria = CATEGORIA_NO_RECONOCIDA
    if not unidad:
        unidad = "km" if tipo == "transporte" else "comida"
    return {
        "tipo": tipo,
        "categoria": categoria,
        "cantidad": cantidad,
        "unidad": unidad,
    }
