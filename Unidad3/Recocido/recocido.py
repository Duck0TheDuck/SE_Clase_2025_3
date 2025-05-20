from optimization_manager import OptimizationManager
import copy
from params import Param
import math
import random
from pickletools import optimize
from results_manager import ResultManager,ResultsManager

class Annealing:
    def __init__(
        self,
        temp_inicial: float,
        temp_minima: float,
        optimizer: OptimizationManager,
        max_iter: int,
        tasa_enfriamiento: float,
    ):
        self.temp_inicial = temp_inicial
        self.temp_minima = temp_minima
        self.optimizer = optimizer
        self.max_iter = max_iter
        self.tasa_enfriamiento = tasa_enfriamiento

    def run(self):
        optimizer_actual = copy.deepcopy(self.optimizer)
        mejor_opt = copy.deepcopy(optimizer_actual)
        mejor_resultado = optimizer_actual.funcion_objetivo()
        temp_actual = self.temp_inicial
        iteracion_actual = 0
        r = []
        resultados = ResultsManager(r)

        while temp_actual >= self.temp_minima and iteracion_actual < self.max_iter:
            # Generar vecino
            opt_vecino = optimizer_actual.generar_optimizer_vecino(0.2)
            resultado_actual:float = optimizer_actual.funcion_objetivo()
            resultado_vecino:float = opt_vecino.funcion_objetivo()


            # Si es para maximizar delta es vecino -actual (en este caso es maximizar el fitness)
            delta = resultado_vecino - resultado_actual
            if delta >= 0:  # Igual mayor que para maximizar
                optimizer_actual = opt_vecino
            else:  # Si no es mejor acepta con probabilidad
                p = math.exp(-delta / temp_actual)  # probabilidad hamilton creo
                if random.random() < p:
                    optimizer_actual = opt_vecino

            current_fitness = optimizer_actual.funcion_objetivo()
            if current_fitness > mejor_resultado:
                mejor_opt = copy.deepcopy(optimizer_actual)
                mejor_resultado = current_fitness

            temp_actual *= self.tasa_enfriamiento
            r_actual = ResultManager(va=resultado_actual,vo=mejor_resultado,iteracion=iteracion_actual,modelo="Recocido")
            iteracion_actual += 1
            resultados.guardar_dato(r_actual)

        self.optimizer = mejor_opt
        return mejor_opt, mejor_resultado,resultados


