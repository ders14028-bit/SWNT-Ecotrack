# 🌱 EcoTrack — Huella de carbono en lenguaje natural

App web hecha en Streamlit que estima el impacto ambiental de tus actividades
diarias. Escribes en lenguaje natural (ej. "Hoy comí carne y viajé 20km en bus")
y EcoTrack calcula cuántos kg de CO₂ generaste ese día.

---

## Entregables

| Archivo | Descripción |
|---|---|
| [.cursorrules](.cursorrules) | Reglas del agente de IA para este proyecto |
| [VIBE_REPORT.md](VIBE_REPORT.md) | Reflexión sobre el proceso de Vibe Coding |

---

## El problema que resuelve

Registrar la huella de carbono diaria normalmente implica formularios largos con
categorías técnicas (kg de CO2/km, factores de emisión, etc.) que la mayoría de
personas no entiende ni quiere llenar. EcoTrack elimina esa fricción: basta con
describir el día como se lo contarías a alguien, y la app se encarga de interpretar
la actividad y calcular el impacto.

---

## Configuración del ecosistema de IA

### Qué hace el `.cursorrules`

Define el comportamiento del agente (Cursor + Claude/Gemini) para todo el proyecto:

- **Stack**: Python 3.11+, Streamlit, sin frameworks de frontend adicionales.
- **Arquitectura esperada**: módulos con responsabilidad única (interfaz,
  extracción, cálculo, factores de emisión).
- **Estilo de código**: funciones cortas (~30 líneas máx.), comentarios sobre el
  "por qué" y no el "qué".
- **Comportamiento ante errores**: proponer la solución más simple primero, nunca
  reescribir todo el proyecto de golpe.

### Flujo de trabajo usado

```
Cursor (editor) + Gemini (motor de extracción)
    → prompt de arquitectura → generación del MVP completo
    → pruebas locales (streamlit run)
    → errores corregidos de forma incremental con el agente
    → commit y push a GitHub
    → import del repo en Replit
    → Run del workflow en Replit
```

---

## Arquitectura

| Módulo | Responsabilidad |
|---|---|
| `app.py` | Interfaz de Streamlit: input de texto, botón de registro, resultado de la última entrada y total acumulado del día. |
| `extractor.py` | Llama a la API de Gemini para convertir el texto libre en un JSON estructurado de actividades (tipo, categoría, cantidad, unidad). |
| `calculadora.py` | Aplica los factores de emisión fijos sobre el JSON del extractor y calcula el total de CO2. |
| `factores.py` | Diccionario de factores de emisión (kg CO2 por unidad) para transporte y alimentación. |

---

## Instalación y ejecución local

```bash
# 1. Clonar el repositorio
git clone https://github.com/ders14028-bit/SWNT-Ecotrack.git
cd SWNT-Ecotrack

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar la API key
cp .env.example .env
# Editar .env y agregar tu GEMINI_API_KEY (gratis en aistudio.google.com/apikey)

# 4. Ejecutar la app
streamlit run app.py
```

La app abre en `http://localhost:8501`.

---

## Despliegue en Replit

1. Ve a [replit.com](https://replit.com) e inicia sesión.
2. Crea un nuevo Repl → **Import from GitHub**.
3. Pega la URL del repositorio: `https://github.com/ders14028-bit/SWNT-Ecotrack`
4. Replit detecta el archivo `.replit` incluido en el repo y configura el workflow
   de Streamlit automáticamente.
5. En **Secrets**, agrega `GEMINI_API_KEY` con tu key real (nunca en el código).
6. Corre el workflow "Streamlit App".

---

## Ejemplo de uso

**Input:** `"Hoy comí carne y viajé 20km en bus"`

**Output:**
```
Última entrada
- carne_roja (alimentacion): 1 comida → 6.00 kg CO2
- bus (transporte): 20 km → 2.00 kg CO2

CO2 de esta entrada: 8.00 kg
Total del día: 8.00 kg
```

Si una actividad mencionada no encaja en ninguna categoría conocida (ej. "viajé
100 km" sin especificar el medio de transporte), se marca como "no se pudo
calcular" en lugar de inventar un valor.

---

## Supuestos y categorías

**Transporte** (kg CO2/km): carro 0.21, bus 0.10, moto 0.11, bicicleta 0, avión 0.15.

**Alimentación** (kg CO2/comida): carne roja 6.0, pollo/pescado 1.5, vegetariano 0.7.

---

## Limitaciones

1. **Factores de emisión aproximados**: son valores ilustrativos para fines
   educativos, no certificados para reportes de sostenibilidad.
2. **Requiere especificar el medio y la cantidad**: frases ambiguas ("viajé
   100 km" sin decir en qué) no se calculan, para evitar inventar datos.
3. **Sin persistencia entre sesiones**: el acumulado del día vive en
   `st.session_state` y se pierde al cerrar o refrescar el navegador.
4. **Dependiente de una API externa**: la extracción de actividades requiere
   la API de Gemini; sin conexión o sin key configurada, la app no puede
   interpretar el texto.

---

## Capturas de pantalla

*Agregar antes de entregar:*

- [ ] Cursor con el código y el chat del agente
- [ ] App corriendo localmente con un ejemplo de input/output
- [ ] Replit con la app desplegada
