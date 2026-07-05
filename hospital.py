import simpy
import random

TIEMPOS_ATENCION = {
    "Emergencia": (20, 35),
    "Urgencia": (15, 25),
    "Consulta": (8, 15)
}

PRIORIDADES = {
    "Emergencia": 0,
    "Urgencia": 1,
    "Consulta": 2
}

TIPOS = ["Emergencia", "Urgencia", "Consulta"]
PESOS = [0.2, 0.3, 0.5]

MAX_ESPERA = 30


def ejecutar_simulacion(
    tiempo_simulacion=480,
    tiempo_llegada=4,
    num_medicos=3,
    num_enfermeras=4,
    num_camas=5
):

    espera = {
        "Emergencia": [],
        "Urgencia": [],
        "Consulta": []
    }

    eventos = []

    pacientes_atendidos = 0
    pacientes_abandonan = 0

    tiempo_ocupado_medicos = 0
    tiempo_ocupado_camas = 0

    class Hospital:

        def __init__(self, env):

            self.env = env

            self.medicos = simpy.PriorityResource(
                env,
                capacity=num_medicos
            )

            self.enfermeras = simpy.Resource(
                env,
                capacity=num_enfermeras
            )

            self.camas = simpy.Resource(
                env,
                capacity=num_camas
            )

    env = simpy.Environment()

    hospital = Hospital(env)

    def llegada():

        paciente = 0

        while True:

            nonlocal pacientes_atendidos
            nonlocal pacientes_abandonan
            nonlocal tiempo_ocupado_camas
            nonlocal tiempo_ocupado_medicos

            paciente += 1

            yield env.timeout(
                random.expovariate(1 / tiempo_llegada)
            )

            tipo = random.choices(
                TIPOS,
                PESOS
            )[0]

            env.process(
                atender(paciente, tipo)
            )

    def atender(id, tipo):

        nonlocal pacientes_atendidos
        nonlocal pacientes_abandonan
        nonlocal tiempo_ocupado_camas
        nonlocal tiempo_ocupado_medicos

        llegada = env.now

        eventos.append([
            round(env.now, 2),
            id,
            tipo,
            "Llega"
        ])

        solicitud = hospital.medicos.request(
            priority=PRIORIDADES[tipo]
        )

        resultado = yield solicitud | env.timeout(MAX_ESPERA)

        if solicitud not in resultado:

            pacientes_abandonan += 1

            eventos.append([
                round(env.now, 2),
                id,
                tipo,
                "Abandona"
            ])

            return

        tiempo_espera = env.now - llegada

        espera[tipo].append(tiempo_espera)

        eventos.append([
            round(env.now, 2),
            id,
            tipo,
            "Obtiene médico"
        ])

        with hospital.camas.request() as cama:

            yield cama

            eventos.append([
                round(env.now, 2),
                id,
                tipo,
                "Obtiene cama"
            ])

            with hospital.enfermeras.request() as enfermera:

                yield enfermera

                eventos.append([
                    round(env.now, 2),
                    id,
                    tipo,
                    "Obtiene enfermera"
                ])

                tiempo = random.randint(
                    *TIEMPOS_ATENCION[tipo]
                )

                tiempo_ocupado_medicos += tiempo
                tiempo_ocupado_camas += tiempo

                yield env.timeout(tiempo)

        pacientes_atendidos += 1

        eventos.append([
            round(env.now, 2),
            id,
            tipo,
            "Finaliza"
        ])

        hospital.medicos.release(solicitud)

    env.process(llegada())

    env.run(until=tiempo_simulacion)

    util_medicos = (
        tiempo_ocupado_medicos /
        (num_medicos * tiempo_simulacion)
    ) * 100

    util_camas = (
        tiempo_ocupado_camas /
        (num_camas * tiempo_simulacion)
    ) * 100

    return {

        "atendidos": pacientes_atendidos,

        "abandonan": pacientes_abandonan,

        "util_medicos": round(util_medicos, 2),

        "util_camas": round(util_camas, 2),

        "espera_emergencia":
            round(sum(espera["Emergencia"]) / len(espera["Emergencia"]), 2)
            if espera["Emergencia"] else 0,

        "espera_urgencia":
            round(sum(espera["Urgencia"]) / len(espera["Urgencia"]), 2)
            if espera["Urgencia"] else 0,

        "espera_consulta":
            round(sum(espera["Consulta"]) / len(espera["Consulta"]), 2)
            if espera["Consulta"] else 0,

        "eventos": eventos

    }