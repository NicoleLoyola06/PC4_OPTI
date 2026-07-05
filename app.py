import streamlit as st
import pandas as pd
import plotly.express as px

from hospital import ejecutar_simulacion

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Sistema Hospitalario",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Sistema Hospitalario de Urgencias")
st.caption("Simulación con SimPy - PriorityResource, Resource, Eventos y Estadísticas")

st.divider()

# ==========================================
# PANEL LATERAL
# ==========================================

st.sidebar.header("⚙ Configuración de la simulación")

tiempo_simulacion = st.sidebar.number_input(
    "Tiempo de simulación (min)",
    min_value=60,
    max_value=1440,
    value=480,
    step=60
)

tiempo_llegada = st.sidebar.number_input(
    "Promedio llegada pacientes",
    min_value=1,
    max_value=20,
    value=4
)

num_medicos = st.sidebar.number_input(
    "Cantidad de médicos",
    min_value=1,
    max_value=20,
    value=3
)

num_enfermeras = st.sidebar.number_input(
    "Cantidad de enfermeras",
    min_value=1,
    max_value=20,
    value=4
)

num_camas = st.sidebar.number_input(
    "Cantidad de camas",
    min_value=1,
    max_value=30,
    value=5
)

st.sidebar.divider()

simular = st.sidebar.button(
    "▶ Simular Sistema",
    use_container_width=True
)

# ==========================================
# SIMULACIÓN
# ==========================================

if simular:

    datos = ejecutar_simulacion(
        tiempo_simulacion,
        tiempo_llegada,
        num_medicos,
        num_enfermeras,
        num_camas
    )

    # ==========================
    # MÉTRICAS
    # ==========================

    st.subheader("📋 Resumen general")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Pacientes atendidos",
        datos["atendidos"]
    )

    c2.metric(
        "Pacientes abandonaron",
        datos["abandonan"]
    )

    c3.metric(
        "Uso médicos",
        f'{datos["util_medicos"]:.2f}%'
    )

    c4.metric(
        "Uso camas",
        f'{datos["util_camas"]:.2f}%'
    )

    st.divider()

    # ==========================
    # GRÁFICOS
    # ==========================

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(

            x=[
                "Emergencia",
                "Urgencia",
                "Consulta"
            ],

            y=[
                datos["espera_emergencia"],
                datos["espera_urgencia"],
                datos["espera_consulta"]
            ],

            text_auto=".2f",

            labels={
                "x": "Prioridad",
                "y": "Minutos"
            },

            title="Tiempo promedio de espera"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        fig2 = px.pie(

            names=[
                "Atendidos",
                "Abandonaron"
            ],

            values=[
                datos["atendidos"],
                datos["abandonan"]
            ],

            hole=0.45,

            title="Distribución de pacientes"
        )

        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # ==========================
    # RESUMEN
    # ==========================

    st.subheader("📊 Estadísticas")

    resumen = pd.DataFrame({

        "Indicador": [

            "Tiempo promedio Emergencia",

            "Tiempo promedio Urgencia",

            "Tiempo promedio Consulta",

            "Utilización médicos",

            "Utilización camas",

            "Pacientes atendidos",

            "Pacientes abandonaron"

        ],

        "Valor": [

            f'{datos["espera_emergencia"]:.2f} min',

            f'{datos["espera_urgencia"]:.2f} min',

            f'{datos["espera_consulta"]:.2f} min',

            f'{datos["util_medicos"]:.2f}%',

            f'{datos["util_camas"]:.2f}%',

            datos["atendidos"],

            datos["abandonan"]

        ]

    })

    st.table(resumen)

    st.divider()

    # ==========================
    # EVENTOS
    # ==========================

    st.subheader("📜 Registro de eventos")

    df = pd.DataFrame(

        datos["eventos"],

        columns=[
            "Tiempo",
            "Paciente",
            "Prioridad",
            "Evento"
        ]

    )

    st.dataframe(
        df,
        use_container_width=True,
        height=450
    )