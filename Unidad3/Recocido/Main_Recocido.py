from params import Param
from optimization_manager import OptimizationManager
from recocido import Annealing  # Cambiado a importar Annealing en lugar de IteratedLocalSearch
import polars as pl
import matplotlib.pyplot as plt


def main():
    # Creación de parámetros (igual que antes)
    param1 = Param(name="Temperatura", min=0, max=40, v_actual=30, weight=0.4, costo_cambio=12, optim_mode="min")
    param2 = Param(name="Humedad", min=0, max=100, v_actual=30, weight=0.4, costo_cambio=12, optim_mode="min")
    param3 = Param(name="Presion", min=900, max=1100, v_actual=1000, weight=0.2, costo_cambio=5, optim_mode="max")

    lista_params = [param1, param2, param3]
    opt = OptimizationManager(lista_params)

    # Configuración del Recocido Simulado (cambiado desde ILS)
    sa = Annealing(
        temp_inicial=100.0,  # Temperatura inicial alta
        temp_minima=0.1,  # Temperatura mínima para detener
        optimizer=opt,
        max_iter=1000,  # Máximo de iteraciones
        tasa_enfriamiento=0.95  # Tasa de enfriamiento (95% en cada iteración)
    )

    # Ejecución del algoritmo
    best_solution, best_value, resultados = sa.run()

    print("\n------ Mejor solución encontrada ------")
    best_solution.show_params()
    print(f"Valor objetivo: {best_value}")

    # Conversión de resultados a DataFrame (igual que antes)
    data = []
    for r in resultados.resultados:
        data.append({
            "valor_actual": r.va,
            "valor_optimo": r.vo,
            "iteracion": r.iteracion,
            "modelo": r.modelo
        })

    df = pl.DataFrame(data)

    # Exportación a CSV (cambiado el nombre del archivo)
    df.write_csv("sa_results.csv")

    # Visualización de resultados (igual estructura, cambiado el título)
    plt.figure(figsize=(10, 6))
    plt.plot(df["iteracion"], df["valor_actual"], 'b-', label='Valor Actual')
    plt.plot(df["iteracion"], df["valor_optimo"], 'r-', label='Mejor Valor')
    plt.xlabel("Iteración")
    plt.ylabel("Valor Objetivo")
    plt.title("Progreso del Recocido Simulado")
    plt.legend()
    plt.grid(True)
    plt.savefig("sa_progress.png")
    plt.show()


if __name__ == "__main__":
    main()