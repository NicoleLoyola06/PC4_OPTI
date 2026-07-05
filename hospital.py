import simpy
import random

TIEMPO_SIMULACION = 480
TIEMPO_LLEGADA = 4

NUM_MEDICOS = 3
NUM_ENFERMERAS = 4
NUM_CAMAS = 5

TIEMPOS_ATENCION = {
    "Emergencia": (20,35),
    "Urgencia": (15,25),
    "Consulta": (8,15)
}

PRIORIDADES = {
    "Emergencia":0,
    "Urgencia":1,
    "Consulta":2
}

TIPOS = ["Emergencia","Urgencia","Consulta"]
PESOS = [0.2,0.3,0.5]

MAX_ESPERA = 30


def ejecutar_simulacion():

    espera = {
        "Emergencia":[],
        "Urgencia":[],
        "Consulta":[]
    }

    eventos=[]

    pacientes_atendidos=0
    pacientes_abandonan=0

    tiempo_ocupado_medicos=0
    tiempo_ocupado_camas=0

    class Hospital:

        def __init__(self,env):

            self.env=env

            self.medicos=simpy.PriorityResource(env,capacity=NUM_MEDICOS)
            self.enfermeras=simpy.Resource(env,capacity=NUM_ENFERMERAS)
            self.camas=simpy.Resource(env,capacity=NUM_CAMAS)

    env=simpy.Environment()

    hospital=Hospital(env)

    def llegada():

        paciente=0

        while True:

            nonlocal pacientes_atendidos
            nonlocal pacientes_abandonan
            nonlocal tiempo_ocupado_camas
            nonlocal tiempo_ocupado_medicos

            paciente+=1

            yield env.timeout(random.expovariate(1/TIEMPO_LLEGADA))

            tipo=random.choices(TIPOS,PESOS)[0]

            env.process(atender(paciente,tipo))

    def atender(id,tipo):

        nonlocal pacientes_atendidos
        nonlocal pacientes_abandonan
        nonlocal tiempo_ocupado_camas
        nonlocal tiempo_ocupado_medicos

        llegada=env.now

        eventos.append([env.now,id,tipo,"Llega"])

        solicitud=hospital.medicos.request(priority=PRIORIDADES[tipo])

        resultado=yield solicitud | env.timeout(MAX_ESPERA)

        if solicitud not in resultado:

            pacientes_abandonan+=1

            eventos.append([env.now,id,tipo,"Abandona"])

            return

        tiempo_espera=env.now-llegada

        espera[tipo].append(tiempo_espera)

        eventos.append([env.now,id,tipo,"Obtiene médico"])

        with hospital.camas.request() as cama:

            yield cama

            eventos.append([env.now,id,tipo,"Obtiene cama"])

            with hospital.enfermeras.request() as enfermera:

                yield enfermera

                eventos.append([env.now,id,tipo,"Obtiene enfermera"])

                tiempo=random.randint(*TIEMPOS_ATENCION[tipo])

                tiempo_ocupado_medicos+=tiempo
                tiempo_ocupado_camas+=tiempo

                yield env.timeout(tiempo)

        pacientes_atendidos+=1

        eventos.append([env.now,id,tipo,"Finaliza"])

        hospital.medicos.release(solicitud)

    env.process(llegada())

    env.run(until=TIEMPO_SIMULACION)

    return{

        "atendidos":pacientes_atendidos,

        "abandonan":pacientes_abandonan,

        "util_medicos":round(tiempo_ocupado_medicos/(NUM_MEDICOS*TIEMPO_SIMULACION)*100,2),

        "util_camas":round(tiempo_ocupado_camas/(NUM_CAMAS*TIEMPO_SIMULACION)*100,2),

        "espera_emergencia":round(sum(espera["Emergencia"])/len(espera["Emergencia"]),2) if espera["Emergencia"] else 0,

        "espera_urgencia":round(sum(espera["Urgencia"])/len(espera["Urgencia"]),2) if espera["Urgencia"] else 0,

        "espera_consulta":round(sum(espera["Consulta"])/len(espera["Consulta"]),2) if espera["Consulta"] else 0,

        "eventos":eventos
    }