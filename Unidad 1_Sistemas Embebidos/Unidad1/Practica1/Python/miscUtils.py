import serial.tools.list_ports
import random as rd
VID = 0x1a86
PID = 0x7523




def buscarPuertoArduino(vid=VID,pid=PID):
    puertos = serial.tools.list_ports.comports()
    for puerto in puertos:
        if puerto.vid == vid and puerto.pid == pid:
            return puerto.device
    return None



def generarLista(min,max,n):
    return [rd.randint(min,max) for _ in range(n)]

def generarMatriz(max,min,n,m):
   return [generarLista(max=max,min=min,n=n) for _ in range(m)]


def print_tournament_results(parent_matrix):
    print("Resultados Torneo Binario:")
    print("-" * 50)
    for i in range(len(parent_matrix)):
        min_value = parent_matrix[i, 0, 0]  # Get the minimum value
        # Format the number to avoid scientific notation and show 2 decimal places
        formatted_min = f"{min_value:.2f}"
        print(f"Padre {i + 1}:")
        print(f"Valor Minimo: {formatted_min}")
        print(f"Vector: {parent_matrix[i, 1, :]}")
        print("-" * 50)


def print_diccionarios(diccionario):
    for key,value in diccionario.items():
        print(f"Key: {key}, Type: {type(key)}")
        print(f"Valor: {value}, Type: {type(value)}\n")