# 🌱 EcoTrack — Huella de carbono en lenguaje natural

App web hecha en Streamlit que estima el impacto ambiental de tus actividades
diarias. Escribes en lenguaje natural (ej. "Hoy comí carne y viajé 20km en bus")
y EcoTrack calcula cuántos kg de CO₂ generaste ese día.

---

## Entregables

| Archivo | Descripción |
|---|---|
| [.cursorrules](.cursorrules) | Reglas del agente de IA para este proyecto |
| [README.md](README.md) | Este documento, incluye el Vibe Report al final |

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
cursor:
<img width="1905" height="1023" alt="image" src="https://github.com/user-attachments/assets/eacaa176-3200-49a3-a850-4765d6de7050" />
replit desplegado:
<img width="1626" height="990" alt="image" src="https://github.com/user-attachments/assets/8c65bc51-21bf-4bef-b0c2-712f8c4d65cf" />

---

## Vibe Report
 
### Cómo configuré las reglas de mi agente
 
Definí un archivo `.cursorrules` con el stack (Python + Streamlit), la arquitectura
esperada (módulos separados para interfaz, extracción, cálculo y factores de emisión)
y el estilo de código (funciones cortas, modulares, comentarios sobre el "por qué").
También incluí reglas de comportamiento: que el agente explique brevemente cada
cambio y proponga la solución más simple ante un error, en lugar de reescribir todo
el proyecto. Esto evitó que la IA sobre-diseñara el MVP y mantuvo el código alineado
con la arquitectura que definí desde el inicio.
 
### Dificultades al delegar el código a la IA
 
La generación inicial del código fue sorprendentemente fluida: en un solo prompt
de arquitectura obtuve la app funcionando localmente, calculando correctamente el
CO2 de frases como "Hoy comí carne y viajé 20km en bus".
 
Las dificultades reales aparecieron en el despliegue, no en el código:
 
- **Autenticación de API**: pasé por dos proveedores de LLM (Anthropic, luego
  Gemini) por temas de créditos, y cada cambio de proveedor requirió ajustar el
  extractor — la arquitectura modular hizo que este cambio fuera rápido.
- **Configuración de infraestructura ambigua**: Replit generó inicialmente una
  plantilla mezclada con Node.js/pnpm en lugar de un proyecto Python puro, lo que
  causó conflictos de puerto difíciles de diagnosticar. El agente reportaba éxito
  ("está corriendo") mientras la vista pública seguía fallando, lo cual me enseñó
  a no confiar ciegamente en el resumen del agente sin verificar con evidencia
  directa (logs, curl, la URL real).
- **Secretos expuestos**: en un punto, una API key terminó commiteada en el
  historial de git por una edición del agente. Tuve que revocarla, reiniciar el
  historial de git desde cero, y aprender a verificar explícitamente que los
  secretos nunca queden en archivos versionados.
- **Límites de plan**: agoté créditos de agente tanto en Cursor como en Replit
  iterando sobre estos problemas, y descubrí que publicar un deployment permanente
  en Replit requiere plan pago — así que terminé versionando el proyecto en GitHub
  e importándolo a Replit con un archivo `.replit` ya definido por mí, en vez de
  dejar que el agente adivinara la configuración desde cero.
### De escribir código a orquestar una visión
 
Delegar la lógica del producto se sintió natural casi de inmediato: describir el
comportamiento deseado en lenguaje natural y ver la app tomar forma es genuinamente
más rápido que escribir cada función a mano. Pero orquestar no significa dejar de
pensar como ingeniero — significa mover el pensamiento técnico a otro nivel: en vez
de preguntarme "¿cómo escribo esta función?", me preguntaba "¿qué le estoy pidiendo
exactamente al agente, y cómo verifico que hizo lo correcto?".
 
La mayor dificultad de este taller no fue generar código, fue **verificar** lo que
la IA decía que había hecho. Un agente que reporta éxito con confianza no siempre
refleja la realidad del sistema, especialmente en infraestructura (puertos, entornos,
despliegues). Orquestar bien terminó pareciéndose menos a "dar órdenes" y más a
mantener una postura de revisión constante: pedir logs, probar con `curl`, y no
avanzar al siguiente paso hasta confirmar con evidencia real, no solo con el resumen
del agente.

