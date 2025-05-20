from params import Param
from optimization_manager import OptimizationManager
from tabu import Tabu  # Cambiado a importar Tabu en lugar de IteratedLocalSearch
import polars as pl
import matplotlib.pyplot as plt


def main():
    # Creación de parámetros del sistema
    param1 = Param(name="Temperatura", min=0, max=40, v_actual=30, weight=0.4,
                   costo_cambio=12, optim_mode="min")
    param2 = Param(name="Humedad", min=0, max=100, v_actual=30, weight=0.4,
                   costo_cambio=12, optim_mode="min")
    param3 = Param(name="Presion", min=900, max=1100, v_actual=1000, weight=0.2,
                   costo_cambio=5, optim_mode="max")

    lista_params = [param1, param2, param3]
    opt = OptimizationManager(lista_params)

    # Configuración del algoritmo Tabú
    tabu_search = Tabu(
        tam_tabu=10,  # Tamaño de la lista Tabú
        optimizer=opt,  # Solución inicial
        iterations=100  # Número de iteraciones
    )

    # Ejecución del algoritmo
    best_solution, resultados = tabu_search.run()

    # Obtención del mejor valor objetivo
    best_value = best_solution.funcion_objetivo(True).get("fitness_total")

    print("\n------ Mejor solución encontrada ------")
    best_solution.show_params()
    print(f"Valor objetivo: {best_value}")

    # Conversión de resultados a DataFrame
    data = []
    for r in resultados.resultados:
        data.append({
            "valor_actual": r.va,
            "valor_optimo": r.vo,
            "iteracion": r.iteracion,
            "modelo": r.modelo
        })

    df = pl.DataFrame(data)

    # Exportación a CSV
    df.write_csv("tabu_results.csv")

    # Visualización de resultados
    plt.figure(figsize=(10, 6))
    plt.plot(df["iteracion"], df["valor_actual"], 'b-', label='Valor Actual')
    plt.plot(df["iteracion"], df["valor_optimo"], 'r-', label='Mejor Valor')
    plt.xlabel("Iteración")
    plt.ylabel("Valor de Fitness")
    plt.title("Progreso de la Búsqueda Tabú")
    plt.legend()
    plt.grid(True)
    plt.savefig("tabu_progress.png")
    plt.show()


if __name__ == "__main__":
    main()