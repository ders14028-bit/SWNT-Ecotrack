# Vibe Report — EcoTrack

## Cómo configuré las reglas de mi agente

Definí un archivo `.cursorrules` con el stack (Python + Streamlit), la arquitectura
esperada (módulos separados para interfaz, extracción, cálculo y factores de emisión)
y el estilo de código (funciones cortas, modulares, comentarios sobre el "por qué").
También incluí reglas de comportamiento: que el agente explique brevemente cada
cambio y proponga la solución más simple ante un error, en lugar de reescribir todo
el proyecto. Esto evitó que la IA sobre-diseñara el MVP y mantuvo el código alineado
con la arquitectura que definí desde el inicio.

## Dificultades al delegar el código a la IA

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

## De escribir código a orquestar una visión

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
