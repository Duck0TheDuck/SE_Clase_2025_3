from params import Param
from optimization_manager import OptimizationManager
from Unidad3.Genetico.genetico import Genetico  # Cambiado a importar Genetico
import polars as pl
import matplotlib.pyplot as plt


def main():
    # Creación de parámetros (igual que antes)
    param1 = Param(name="Temperatura", min=0, max=40, v_actual=30, weight=0.4, costo_cambio=12, optim_mode="min")
    param2 = Param(name="Humedad", min=0, max=100, v_actual=30, weight=0.4, costo_cambio=12, optim_mode="min")
    param3 = Param(name="Presion", min=900, max=1100, v_actual=1000, weight=0.2, costo_cambio=5, optim_mode="max")

    lista_params = [param1, param2, param3]
    opt = OptimizationManager(lista_params)

    # Configuración del Algoritmo Genético
    ga = Genetico(
        tam_poblacion=50,  # Tamaño de la población
        optimizer_inicial=opt  # Solución inicial
    )

    # Ejecución del algoritmo genético
    best_solution, resultados = ga.run(
        num_generaciones=100,  # Número de generaciones
        prob_cruza=0.8,  # Probabilidad de cruce
        prob_muta=0.2,  # Probabilidad de mutación
        potencia_muta=0.1,  # Intensidad de la mutación
        num_padres=15  # Número de padres para selección
    )

    print("\n------ Mejor solución encontrada ------")
    best_solution.show_params()
    print(f"Valor objetivo: {best_solution.funcion_objetivo()}")

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
    df.write_csv("ga_results.csv")

    # Visualización de resultados
    plt.figure(figsize=(10, 6))
    plt.plot(df["iteracion"], df["valor_actual"], 'b-', label='Mejor actual')
    plt.plot(df["iteracion"], df["valor_optimo"], 'r-', label='Mejor global')
    plt.xlabel("Generación")
    plt.ylabel("Valor de Fitness")
    plt.title("Progreso del Algoritmo Genético")
    plt.legend()
    plt.grid(True)
    plt.savefig("ga_progress.png")
    plt.show()


if __name__ == "__main__":
    main()