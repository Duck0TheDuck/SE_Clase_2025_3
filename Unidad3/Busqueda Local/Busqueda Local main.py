from params import Param
from optimization_manager import OptimizationManager
from local_search import LocalSearch
import polars as pl
import matplotlib.pyplot as plt


def main():
    # Parámetros simulando sensores del sistema de iluminación
    param1 = Param(name="LuzAmbiente", min=0, max=100, v_actual=30, weight=0.5, costo_cambio=10, optim_mode="min")
    param2 = Param(name="HoraDia", min=0, max=24, v_actual=20, weight=0.3, costo_cambio=8, optim_mode="min")
    param3 = Param(name="Presencia", min=0, max=1, v_actual=1, weight=0.2, costo_cambio=5, optim_mode="max")

    lista_params = [param1, param2, param3]
    optimizador = OptimizationManager(lista_params)

    # Ejecutar búsqueda local
    ls = LocalSearch(
        max_iter=50,  # Número de iteraciones
        optimizer=optimizador,
        rango_vecindad=0.1  # Cambios pequeños en cada iteración
    )

    mejor_solucion, mejor_valor, resultados = ls.run()

    print("\n------ Mejor configuración encontrada ------")
    mejor_solucion.show_params()
    print(f"Valor objetivo: {mejor_valor:.4f}")

    # Preparar resultados en DataFrame
    data = []
    for r in resultados.resultados:
        data.append({
            "valor_actual": r.va,
            "valor_optimo": r.vo,
            "iteracion": r.iteracion,
            "modelo": r.modelo
        })

    df = pl.DataFrame(data)
    df.write_csv("iluminacion_results.csv")

    # Graficar el progreso
    plt.figure(figsize=(10, 6))
    plt.plot(df["iteracion"], df["valor_actual"], label="Valor Actual", color="blue")
    plt.plot(df["iteracion"], df["valor_optimo"], label="Mejor Valor", color="red")
    plt.xlabel("Iteración")
    plt.ylabel("Valor Objetivo")
    plt.title("Busqueda Local")
    plt.legend()
    plt.grid(True)
    plt.savefig("iluminacion_progress.png")
    plt.show()


if __name__ == "__main__":
    main()