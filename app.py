import streamlit as st
import pandas as pd
import plotly.express as px

from hospital import ejecutar_simulacion

st.set_page_config(
    page_title="Sistema Hospitalario",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Simulación del Área de Emergencias")

st.write("---")

if st.button("▶ Ejecutar Simulación"):

    datos=ejecutar_simulacion()

    c1,c2,c3,c4=st.columns(4)

    c1.metric("Pacientes atendidos",datos["atendidos"])

    c2.metric("Pacientes abandonaron",datos["abandonan"])

    c3.metric("Utilización Médicos",f'{datos["util_medicos"]}%')

    c4.metric("Utilización Camas",f'{datos["util_camas"]}%')

    st.write("---")

    col1,col2=st.columns(2)

    with col1:

        fig=px.bar(

            x=["Emergencia","Urgencia","Consulta"],

            y=[

                datos["espera_emergencia"],

                datos["espera_urgencia"],

                datos["espera_consulta"]

            ],

            color=["Emergencia","Urgencia","Consulta"],

            title="Tiempo promedio de espera"

        )

        st.plotly_chart(fig,use_container_width=True)

    with col2:

        fig2=px.pie(

            values=[datos["atendidos"],datos["abandonan"]],

            names=["Atendidos","Abandonaron"],

            title="Distribución de pacientes"

        )

        st.plotly_chart(fig2,use_container_width=True)

    st.write("---")

    st.subheader("Registro de eventos")

    df=pd.DataFrame(

        datos["eventos"],

        columns=["Tiempo","Paciente","Prioridad","Evento"]

    )

    st.dataframe(df,use_container_width=True)