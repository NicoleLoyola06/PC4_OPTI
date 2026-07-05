# Sistema Hospitalario - SimPy + Streamlit

Proyecto desarrollado para el curso **Optimización y Simulación de Sistemas**.

Este proyecto simula el funcionamiento del área de emergencias de un hospital utilizando SimPy para la simulación de eventos discretos y **Streamlit** para la visualización interactiva de los resultados.

---

# Características

* Llegadas aleatorias de pacientes.
* Tres niveles de prioridad:

  * Emergencia
  * Urgencia
  * Consulta
* Gestión de recursos mediante SimPy:

  * Médicos (`PriorityResource`)
  * Enfermeras (`Resource`)
  * Camas (`Resource`)
* Cola de espera con prioridad.
* Abandono de pacientes por exceso de espera (Reneging).
* Cálculo de estadísticas del sistema.
* Visualización de resultados mediante una interfaz web con Streamlit.

---

# Recursos del Hospital

* Médicos
* Enfermeras
* Camas

---

# Estadísticas Generadas

Al finalizar la simulación se muestran:

* Pacientes atendidos.
* Pacientes que abandonan la cola.
* Tiempo promedio de espera por prioridad.
* Utilización de médicos.
* Utilización de camas.
* Registro de eventos de la simulación.
* Gráficos estadísticos interactivos.

---

# Requisitos

Instalar las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

O instalar manualmente:

```bash
pip install simpy
pip install streamlit
pip install pandas
pip install plotly
```

---

# Ejecutar la Aplicación

Desde la carpeta del proyecto ejecutar:

```bash
streamlit run app.py
```

---

# Estructura del Proyecto

SistemaHospitalario/
│
├── app.py                 
├── hospital.py           
├── requirements.txt       
├── README.md
└── assets/                


# Tecnologías Utilizadas

* Python
* SimPy
* Streamlit
* Pandas
* Plotly

