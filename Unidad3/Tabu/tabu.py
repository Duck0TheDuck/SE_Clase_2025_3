from optimization_manager import OptimizationManager
from params import Param
from results_manager import ResultsManager,ResultManager

class Tabu:
    def __init__(
        self, tam_tabu: float, optimizer: OptimizationManager, iterations: int
    ):
        self.lista_tabu = []
        self.tam_tabu = tam_tabu
        self.iterations = iterations
        self.optimizer = optimizer
        self.mejor_fitness_global = float("-inf")
        self.mejor_solucion_global = None

    def isTabu(self, valor: float):
        return valor in self.lista_tabu

    def run(self):
        opt_actual = self.optimizer
        mejor_opt = opt_actual
        f_objetivo_actual = opt_actual.funcion_objetivo(True)
        fitness_actual = f_objetivo_actual.get("fitness_total")
        resultados = ResultsManager([])

        for i in range(self.iterations):
            opt_vecino = opt_actual.generar_optimizer_vecino(0.1)
            f_objetivo_vecino = opt_vecino.funcion_objetivo(True)
            fitness_vecino = f_objetivo_vecino.get("fitness_total")
            r = ResultManager(va=fitness_actual,vo=self.mejor_fitness_global,modelo="Tabu",iteracion=i)

            # Update global best solution if needed
            if fitness_vecino > self.mejor_fitness_global:
                self.mejor_fitness_global = fitness_vecino
                self.mejor_solucion_global = opt_vecino

            
            if fitness_vecino > fitness_actual:
                if fitness_vecino not in self.lista_tabu:
                    mejor_opt = opt_vecino
                    opt_actual = mejor_opt
                    fitness_actual = fitness_vecino

                    #print(f"\nMejor solución encontrada: {fitness_vecino}")
                    #print(f"Previa: {fitness_actual}")

                    self.lista_tabu.append(fitness_vecino)
                    if len(self.lista_tabu) > self.tam_tabu:
                        self.lista_tabu.pop(0)

            
            elif fitness_vecino not in self.lista_tabu:
                mejor_opt = opt_vecino
                opt_actual = mejor_opt
                fitness_actual = fitness_vecino

                self.lista_tabu.append(fitness_vecino)
                if len(self.lista_tabu) > self.tam_tabu:
                    self.lista_tabu.pop(0)
            resultados.guardar_dato(r)


        return self.mejor_solucion_global,resultados
