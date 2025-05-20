import copy
import random
from optimization_manager import OptimizationManager
from results_manager import ResultManager, ResultsManager
from params import Param

class IteratedLocalSearch:
    def __init__(self, 
                 max_ils_iter: int,
                 max_ls_iter: int, 
                 optimizer: OptimizationManager, 
                 ls_vecindad: float,
                 perturbation_strength: float) -> None:
        """
        Inicializa el algoritmo de búsqueda local iterada.
        
        Args:
            max_ils_iter: Número máximo de iteraciones ILS
            max_ls_iter: Número máximo de iteraciones de búsqueda local en cada reinicio
            optimizer: Gestor de optimización con la solución inicial
            ls_vecindad: Tamaño de vecindad para búsqueda local
            perturbation_strength: Fuerza de la perturbación (mayor que ls_vecindad)
        """
        self.max_ils_iter = max_ils_iter
        self.max_ls_iter = max_ls_iter
        self.optimizer = optimizer
        self.ls_vecindad = ls_vecindad
        self.perturbation_strength = perturbation_strength
        
    def local_search(self, initial_solution: OptimizationManager):
        """Búsqueda local hasta alcanzar un óptimo local"""
        solucion_actual = copy.deepcopy(initial_solution)
        mejor_solucion = copy.deepcopy(solucion_actual)
        mejor_valor = solucion_actual.funcion_objetivo()
        
        for i in range(self.max_ls_iter):
            # Generate neighboring solution
            solucion_vecina = solucion_actual.generar_optimizer_vecino(self.ls_vecindad)
            v_actual = solucion_actual.funcion_objetivo()
            v_vecino = solucion_vecina.funcion_objetivo()
            
            # If neighbor is better, move to that solution
            if v_vecino > v_actual:
                solucion_actual = solucion_vecina
                
                # Update best solution if needed
                if v_vecino > mejor_valor:
                    mejor_solucion = copy.deepcopy(solucion_vecina)
                    mejor_valor = v_vecino
            else:
                # If no improvement, we've reached a local optimum
                break
                
        return mejor_solucion, mejor_valor
        
    def perturb_solution(self, solution: OptimizationManager):
        """
        Perturba fuertemente la solución para escapar del óptimo local.
        Usa una perturbación más fuerte que la vecindad de búsqueda local.
        """
        perturbed = copy.deepcopy(solution)
        
        # Apply stronger perturbation to multiple parameters
        for param in perturbed.params_list:
            # Randomly decide if we perturb this parameter (50% chance)
            if random.random() < 0.5:
                continue
                
            # Perturb with higher strength to escape local optima
            valor_perturbado = param.generate_neighbor_v_actual(self.perturbation_strength)
            param.v_actual = valor_perturbado
            
        return perturbed
        
    def run(self):
        """Ejecuta el algoritmo de búsqueda local iterada"""
        resultados = ResultsManager([])
        
        # Initial solution and first local search
        current_solution = copy.deepcopy(self.optimizer)
        best_solution, best_value = self.local_search(current_solution)
        
        # Record initial results
        r = ResultManager(va=current_solution.funcion_objetivo(), vo=best_value, 
                          iteracion=0, modelo="ILS")
        resultados.guardar_dato(r)
        
        for i in range(1, self.max_ils_iter + 1):
            # Perturb the current solution
            perturbed_solution = self.perturb_solution(best_solution)
            
            # Apply local search from the perturbed solution
            candidate_solution, candidate_value = self.local_search(perturbed_solution)
            
            # Record results for this iteration
            r = ResultManager(va=candidate_value, vo=best_value, 
                             iteracion=i, modelo="ILS")
            resultados.guardar_dato(r)
            
            # Accept if better (or implement other acceptance criteria)
            if candidate_value > best_value:
                best_solution = copy.deepcopy(candidate_solution)
                best_value = candidate_value
                print(f"ILS: Nueva mejor solución en iteración {i}, valor: {best_value}")
        
        return best_solution, best_value, resultados
