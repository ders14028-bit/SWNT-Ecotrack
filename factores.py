"""Factores fijos de emisión (kg CO2 por unidad)."""

FACTORES = {
    "transporte": {
        "carro": 0.21,
        "bus": 0.10,
        "moto": 0.11,
        "bicicleta": 0.0,
        "avion": 0.15,
    },
    "alimentacion": {
        "carne_roja": 6.0,
        "pollo_pescado": 1.5,
        "vegetariano": 0.7,
    },
}

CATEGORIAS_VALIDAS = {
    tipo: set(categorias)
    for tipo, categorias in FACTORES.items()
}

CATEGORIA_NO_RECONOCIDA = "no_reconocida"
