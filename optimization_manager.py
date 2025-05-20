import random
import math
import copy
from params import Param
from results_manager import ResultsManager

class OptimizationManager:
    """
    Clase encargada de manejar una lista de parámetros y calcular su estado óptimo
    usando distintos métodos de optimización (búsqueda local, SA, Tabu, etc.).
    """

    def __init__(self, params_list: list[Param]):
        """
        Inicializa el administrador con una lista de parámetros a optimizar.

        Args:
            params_list (list[params]): Lista de objetos de tipo `params`.
        """
        self.params_list = params_list
        self.best_solution = None
        self.best_fitnes = float("-inf")

    def show_params(self):
        """
        Muestra en consola todos los parámetros actuales.
        """
        for param in self.params_list:
            param.show()

    def funcion_objetivo(self, detailed=False):
        """
        Calcula la función objetivo (fitness total) de la solución actual.

        Args:
            detailed (bool, optional): Si True, devuelve un resumen detallado por parámetro.

        Returns:
            float o dict: Fitness total o un diccionario con detalles de cada parámetro.
        """
        fitness_componentes = []
        fitness_total = 0

        for param in self.params_list:
            satisfaction = param.calc_satisfaction()
            satisfaccion_ponderada = satisfaction * param.weight

            penalty = 0
            if not param.is_in_range(param.v_actual):
                penalty = param.calc_satisfaction_con_penalty()

            param_fitness = satisfaccion_ponderada - penalty

            fitness_componentes.append(
                {
                    "name": param.name,
                    "satisfaction": satisfaction,
                    "peso": param.weight,
                    "satisfaccion ponderada": satisfaccion_ponderada,
                    "penalty": penalty,
                    "fitness": param_fitness,
                }
            )

            fitness_total += param_fitness

        if detailed:
            return {"fitness_total": fitness_total, "componentes": fitness_componentes}
        return fitness_total

    def generar_vecinos(self, step_percentage: float = 0.1) -> list[Param]:
        """
        Genera una nueva lista de parámetros vecinos con pequeños cambios aplicados.

        Args:
            step_percentage (float): Porcentaje del rango a utilizar como paso de modificación.

        Returns:
            list[params]: Lista de parámetros modificados (vecinos).
        """
        neighbor = copy.deepcopy(self)
        for param in neighbor.params_list:
            valor_vecino = param.generate_neighbor_v_actual(step_percentage)
            param.v_actual = valor_vecino
        return neighbor.params_list

    def generar_optimizer_vecino(self, step_percentage: float):
        """
        Genera una nueva instancia de OptimizationManager con valores vecinos.

        Args:
            step_percentage (float): Porcentaje del rango a utilizar como paso de modificación.

        Returns:
            OptimizationManager: Nuevo optimizador con parámetros vecinos.
        """
        neighbor = copy.deepcopy(self)
        for param in neighbor.params_list:
            valor_vecino = param.generate_neighbor_v_actual(step_percentage)
            param.v_actual = valor_vecino
        return neighbor

    def cruzar(self,otro_optimizer:'OptimizationManager')->'OptimizationManager':

        hijo = copy.deepcopy(self)
        for i,param in enumerate(hijo.params_list):
            if random.random() < 0.5:
                param.v_actual = self.params_list[i].v_actual
            else:
                param.v_actual = otro_optimizer.params_list[i].v_actual
        return hijo
        
