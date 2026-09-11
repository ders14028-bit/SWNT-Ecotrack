"""Interfaz Streamlit de EcoTrack."""

from dotenv import load_dotenv
import streamlit as st

from calculadora import calcular_emisiones
from extractor import extraer_actividades

# Carga GEMINI_API_KEY desde .env sin ponerla en el código.
load_dotenv()

st.set_page_config(page_title="EcoTrack", page_icon="🌱", layout="centered")


def main() -> None:
    _inicializar_estado()
    st.title("EcoTrack")
    st.caption("Registra tu huella de carbono diaria en lenguaje natural.")
    _formulario()
    _ultima_entrada()
    _total_del_dia()


def _inicializar_estado() -> None:
    if "entradas" not in st.session_state:
        st.session_state.entradas = []
    if "ultima" not in st.session_state:
        st.session_state.ultima = None
    if "error" not in st.session_state:
        st.session_state.error = None


def _formulario() -> None:
    with st.form("registro"):
        texto = st.text_area(
            "¿Qué hiciste hoy?",
            placeholder='Ej: "Hoy comí carne y viajé 20km en bus"',
            height=100,
        )
        enviado = st.form_submit_button("Registrar", type="primary")

    if not enviado:
        return
    if not texto.strip():
        st.session_state.error = "Escribe al menos una actividad."
        return
    _registrar(texto.strip())


def _registrar(texto: str) -> None:
    try:
        with st.spinner("Extrayendo actividades..."):
            extraccion = extraer_actividades(texto)
        resultado = calcular_emisiones(extraccion)
        entrada = {"texto": texto, **resultado}
        st.session_state.entradas.append(entrada)
        st.session_state.ultima = entrada
        st.session_state.error = None
    except Exception as exc:
        st.session_state.error = str(exc)


def _ultima_entrada() -> None:
    if st.session_state.error:
        st.error(st.session_state.error)
    ultima = st.session_state.ultima
    if not ultima:
        return

    st.subheader("Última entrada")
    st.write(f"_{ultima['texto']}_")
    _mostrar_actividades(ultima)
    st.metric("CO₂ de esta entrada", f"{ultima['total_kg_co2']:.2f} kg")


def _mostrar_actividades(entrada: dict) -> None:
    for act in entrada["calculadas"]:
        st.write(
            f"- {act['categoria']} ({act['tipo']}): "
            f"{act['cantidad']:g} {act['unidad']} → **{act['kg_co2']:.2f} kg CO₂**"
        )
    for act in entrada["no_reconocidas"]:
        detalle = act.get("categoria", "no_reconocida")
        st.warning(
            f"No se pudo calcular: {act.get('tipo', 'actividad')} "
            f"({detalle}, {act.get('cantidad', '?')} {act.get('unidad', '')})."
        )


def _total_del_dia() -> None:
    st.subheader("Total del día")
    total = sum(e["total_kg_co2"] for e in st.session_state.entradas)
    st.metric("CO₂ acumulado", f"{total:.2f} kg")
    st.caption(f"{len(st.session_state.entradas)} entrada(s) registradas.")

    if st.button("Reiniciar el día"):
        st.session_state.entradas = []
        st.session_state.ultima = None
        st.session_state.error = None
        st.rerun()


if __name__ == "__main__":
    main()
