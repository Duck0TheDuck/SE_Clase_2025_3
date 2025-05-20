# Example usage in main.py
from params import Param
from optimization_manager import OptimizationManager
from Unidad3.Busqueda_Local_iterada.iterated_ls import IteratedLocalSearch
import polars as pl
import matplotlib.pyplot as plt

def main():
    # Create parameters
    param1 = Param(name="Temperatura", min=0, max=40, v_actual=30, weight=0.4, costo_cambio=12, optim_mode="min")
    param2 = Param(name="Humedad", min=0, max=100, v_actual=30, weight=0.4, costo_cambio=12, optim_mode="min")
    param3 = Param(name="Presion", min=900, max=1100, v_actual=1000, weight=0.2, costo_cambio=5, optim_mode="max")
    
    lista_params = [param1, param2, param3]
    opt = OptimizationManager(lista_params)
    
    # Run Iterated Local Search
    ils = IteratedLocalSearch(
        max_ils_iter=20,        # Number of ILS iterations
        max_ls_iter=50,         # Max iterations for each local search
        optimizer=opt,          
        ls_vecindad=0.1,        # Small neighborhood for local search
        perturbation_strength=0.5  # Stronger perturbation to escape local optima
    )
    
    best_solution, best_value, resultados = ils.run()
    
    print("\n------ Mejor solución encontrada ------")
    best_solution.show_params()
    print(f"Valor objetivo: {best_value}")
    
    # Convert results to Polars DataFrame
    data = []
    for r in resultados.resultados:
        data.append({
            "valor_actual": r.va,
            "valor_optimo": r.vo,
            "iteracion": r.iteracion,
            "modelo": r.modelo
        })
    
    df = pl.DataFrame(data)
    
    # Export to CSV
    df.write_csv("ils_results.csv")
    
    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(df["iteracion"], df["valor_actual"], 'b-', label='Valor Actual')
    plt.plot(df["iteracion"], df["valor_optimo"], 'r-', label='Mejor Valor')
    plt.xlabel("Iteración")
    plt.ylabel("Valor Objetivo")
    plt.title("Progreso de Búsqueda Local Iterada")
    plt.legend()
    plt.grid(True)
    plt.savefig("ils_progress.png")
    plt.show()

if __name__ == "__main__":
    main()
