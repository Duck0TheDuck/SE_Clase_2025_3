
from os import error
from optimization_manager import OptimizationManager
import copy
from params import Param
from typing import List, Tuple
import random as rd
from results_manager import ResultManager,ResultsManager
class Genetico:
    def __init__(self,tam_poblacion,optimizer_inicial:OptimizationManager):
        self.tam_poblacion = tam_poblacion
        self.opt_inicial = optimizer_inicial

    def generar_poblacion(self):
        poblacion = [self.opt_inicial.generar_optimizer_vecino(rd.random()) for _ in range(self.tam_poblacion)]
        return poblacion

    def calc_fitness_poblacion(self,poblacion:List[OptimizationManager]):
        mejores = []
        for p in poblacion:
            mejores.append((p,p.funcion_objetivo()))
        return mejores

    def seleccion(self,num_padres:int,lista_fitness:List[Tuple[OptimizationManager,float]]):
        if num_padres > self.tam_poblacion:
            raise ValueError("El numero de seleccion de padres no puede ser mayor a la poblacion")
        else:
            mejores = sorted(lista_fitness, key=lambda x: x[1], reverse=True)[:num_padres]
            return mejores

    def cruza(self,padres:List[Tuple[OptimizationManager,float]],prob_cruza:float):
        descendientes = []
        optimizer_padres = [p[0] for p in padres]

        while len(descendientes) < self.tam_poblacion:
            padre1,padre2 = rd.sample(optimizer_padres,2)

            if rd.random() < prob_cruza:
                hijo1 = padre1.cruzar(padre2)
                hijo2 = padre2.cruzar(padre1)
                descendientes.append(hijo1)
                if len(descendientes) < self.tam_poblacion:
                    descendientes.append(hijo2)
            else:
                descendientes.append(copy.deepcopy(padre1))
                if len(descendientes) < self.tam_poblacion:
                    descendientes.append(copy.deepcopy(padre2))

        return descendientes

    def mutar_poblacion(self,poblacion:List[OptimizationManager],prob_muta:float,potencia_muta:float):
        poblacion_mutada = []
        for p in poblacion:
            if rd.random() < prob_muta: 
                poblacion_mutada.append(p.generar_optimizer_vecino(potencia_muta))
            else:
                poblacion_mutada.append(p)
        return poblacion_mutada

    def run(self,num_generaciones,prob_cruza,prob_muta,potencia_muta,num_padres):
        poblacion = self.generar_poblacion()
        mejor_global = None
        fitness_mejor_global = float('-inf')
        resultados = ResultsManager([])
        

        for generacion in range(num_generaciones):
            lista_fitness = self.calc_fitness_poblacion(poblacion)

            mejor_actual = max(lista_fitness,key=lambda x: x[1])
            if mejor_actual[1] > fitness_mejor_global:
                mejor_global = mejor_actual[0]
                fitness_mejor_global = mejor_actual[1]

            padres = self.seleccion(num_padres=num_padres,lista_fitness=lista_fitness)

            #Cruza
            descendientes = self.cruza(padres=padres,prob_cruza=prob_cruza)
            
            poblacion = self.mutar_poblacion(descendientes,prob_muta,potencia_muta)

            #print(f"Generación {generacion}: Mejor fitness = {mejor_actual[1]}")
            r = ResultManager(va=mejor_actual[1],vo=fitness_mejor_global,iteracion=generacion,modelo="Genetico")
            resultados.guardar_dato(r)
        
        return mejor_global,resultados



    

