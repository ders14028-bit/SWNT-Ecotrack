"""Aplica factores de emisión fijos sobre el JSON de actividades."""

from factores import CATEGORIA_NO_RECONOCIDA, FACTORES


def calcular_emisiones(extraccion: dict) -> dict:
    """Separa reconocidas y no reconocidas para no sumar lo que no tiene factor."""
    calculadas = []
    no_reconocidas = []
    total = 0.0

    for actividad in extraccion.get("actividades", []):
        if actividad.get("categoria") == CATEGORIA_NO_RECONOCIDA:
            no_reconocidas.append(actividad)
            continue
        kg_co2 = _kg_co2(actividad)
        if kg_co2 is None:
            no_reconocidas.append(actividad)
            continue
        item = {**actividad, "kg_co2": round(kg_co2, 4)}
        calculadas.append(item)
        total += kg_co2

    return {
        "calculadas": calculadas,
        "no_reconocidas": no_reconocidas,
        "total_kg_co2": round(total, 4),
    }


def _kg_co2(actividad: dict) -> float | None:
    tipo = actividad.get("tipo")
    categoria = actividad.get("categoria")
    factores_tipo = FACTORES.get(tipo)
    if not factores_tipo or categoria not in factores_tipo:
        return None
    cantidad = float(actividad.get("cantidad", 0) or 0)
    return cantidad * factores_tipo[categoria]
