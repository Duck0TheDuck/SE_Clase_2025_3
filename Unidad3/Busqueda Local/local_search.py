from optimization_manager import OptimizationManager
from params import Param
from results_manager import ResultManager, ResultsManager

class LocalSearch:
    def __init__(self, max_iter: int, optimizer: OptimizationManager, rango_vecindad: float) -> None:
        self.max_iter = max_iter
        self.optimizer = optimizer
        self.rango_vecindad = rango_vecindad

    def run(self):
        resultados = ResultsManager([])
        solucion_actual = self.optimizer
        mejor_solucion = solucion_actual
        mejor_valor = solucion_actual.funcion_objetivo()
        
        for i in range(self.max_iter):
            # Generate neighboring solution
            solucion_vecina = solucion_actual.generar_optimizer_vecino(self.rango_vecindad)
            v_actual = solucion_actual.funcion_objetivo()
            v_vecino = solucion_vecina.funcion_objetivo()
            
            # Record results
            r = ResultManager(va=v_actual, vo=mejor_valor, iteracion=i, modelo="Busqueda Local")
            resultados.guardar_dato(r)
            
            # If neighbor is better, move to that solution
            if v_vecino > v_actual:
                solucion_actual = solucion_vecina
                
                # Update best solution if needed
                if v_vecino > mejor_valor:
                    mejor_solucion = solucion_vecina
                    mejor_valor = v_vecino
                    print(f"Solucion mejorada en iteracion {i}, valor: {mejor_valor}")

        return mejor_solucion, mejor_valor, resultados
