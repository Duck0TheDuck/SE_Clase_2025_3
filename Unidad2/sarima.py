import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from results_manager import ResultManager, ResultsManager


class SarimaModel:
    """
    Clase para implementar y gestionar modelos SARIMA (Seasonal AutoRegressive Integrated Moving Average)
    para el análisis y predicción de series temporales con patrones estacionales.
    """

    def __init__(self, data=None, order=(1, 0, 0), seasonal_order=(0, 0, 0, 0)):
        """
        Inicializa un modelo SARIMA con los parámetros especificados.

        Args:
            data (array-like, optional): Serie temporal para entrenar el modelo.
            order (tuple, optional): Orden del modelo ARIMA (p,d,q).
                p: Términos autorregresivos
                d: Diferenciación necesaria para hacer la serie estacionaria
                q: Términos de media móvil
            seasonal_order (tuple, optional): Orden estacional (P,D,Q,s).
                P: Términos autorregresivos estacionales
                D: Diferenciación estacional
                Q: Términos de media móvil estacionales
                s: Período estacional
        """
        self.data = data
        self.order = order
        self.seasonal_order = seasonal_order
        self.model = None
        self.fitted_model = None
        self.predictions = None
        self.residuals = None
        self.results_manager = None

    def fit(self, data=None, exog=None):
        """
        Entrena el modelo SARIMA con los datos proporcionados.

        Args:
            data (array-like, optional): Serie temporal para entrenar el modelo.
                Si no se proporciona, se utilizan los datos del constructor.
            exog (array-like, optional): Variables exógenas para la regresión.

        Returns:
            self: La instancia del modelo entrenado.
        """
        if data is not None:
            self.data = data

        if self.data is None:
            raise ValueError("No se han proporcionado datos para entrenar el modelo")

        self.model = SARIMAX(
            self.data,
            exog=exog,
            order=self.order,
            seasonal_order=self.seasonal_order,
            enforce_stationarity=False,
            enforce_invertibility=False
        )

        self.fitted_model = self.model.fit(disp=False)
        self.residuals = self.fitted_model.resid

        return self

    def predict(self, steps=1, exog=None):
        """
        Realiza predicciones con el modelo SARIMA entrenado.

        Args:
            steps (int, optional): Número de pasos a predecir. Por defecto es 1.
            exog (array-like, optional): Variables exógenas para la predicción.

        Returns:
            array: Predicciones del modelo.
        """
        if self.fitted_model is None:
            raise ValueError("El modelo debe ser entrenado antes de realizar predicciones")

        # Realizar predicción
        self.predictions = self.fitted_model.forecast(steps=steps, exog=exog)
        return self.predictions

    def evaluate(self):
        """
        Evalúa el rendimiento del modelo calculando métricas comunes.

        Returns:
            dict: Diccionario con las métricas de evaluación.
        """
        if self.fitted_model is None:
            raise ValueError("El modelo debe ser entrenado antes de evaluarlo")

        # Calcular predicciones en muestra
        in_sample_predictions = self.fitted_model.fittedvalues

        # Calcular errores
        residuals = self.data - in_sample_predictions
        mse = np.mean(residuals ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(residuals))

        # Crear diccionario de resultados
        metrics = {
            'AIC': self.fitted_model.aic,
            'BIC': self.fitted_model.bic,
            'MSE': mse,
            'RMSE': rmse,
            'MAE': mae
        }

        return metrics

    def plot_diagnostics(self, figsize=(16, 12)):
        """
        Genera gráficos de diagnóstico para el modelo SARIMA.

        Args:
            figsize (tuple, optional): Tamaño de la figura.
        """
        if self.fitted_model is None:
            raise ValueError("El modelo debe ser entrenado antes de generar diagnósticos")

        fig, axes = plt.subplots(3, 2, figsize=figsize)

        # Gráfico de la serie original y las predicciones
        axes[0, 0].plot(self.data, label='Observado')
        axes[0, 0].plot(self.fitted_model.fittedvalues, color='red', label='Predicciones')
        axes[0, 0].set_title('Valores observados vs predicciones')
        axes[0, 0].legend()

        # Gráfico de residuos
        axes[0, 1].plot(self.residuals)
        axes[0, 1].set_title('Residuos')
        axes[0, 1].axhline(y=0, color='red', linestyle='--')

        # ACF de residuos
        plot_acf(self.residuals, ax=axes[1, 0], lags=40)
        axes[1, 0].set_title('ACF de residuos')

        # PACF de residuos
        plot_pacf(self.residuals, ax=axes[1, 1], lags=40)
        axes[1, 1].set_title('PACF de residuos')

        # Histograma de residuos
        axes[2, 0].hist(self.residuals, bins=25)
        axes[2, 0].set_title('Histograma de residuos')

        # QQ plot de residuos
        from scipy import stats
        stats.probplot(self.residuals, dist="norm", plot=axes[2, 1])
        axes[2, 1].set_title('QQ plot de residuos')

        plt.tight_layout()
        plt.show()

    def plot_forecast(self, steps=10, alpha=0.05, figsize=(12, 6), exog=None):
        """
        Visualiza las predicciones futuras con intervalos de confianza.

        Args:
            steps (int, optional): Número de pasos a predecir. Por defecto es 10.
            alpha (float, optional): Nivel de significancia para los intervalos de confianza.
            figsize (tuple, optional): Tamaño de la figura.
            exog (array-like, optional): Variables exógenas para la predicción.
        """
        if self.fitted_model is None:
            raise ValueError("El modelo debe ser entrenado antes de visualizar predicciones")

        # Realizar predicción
        forecast_result = self.fitted_model.get_forecast(steps=steps, exog=exog)
        forecast_index = np.arange(len(self.data), len(self.data) + steps)

        # Obtener predicciones e intervalos de confianza
        forecast_mean = forecast_result.predicted_mean
        conf_int = forecast_result.conf_int(alpha=alpha)

        # Crear figura
        plt.figure(figsize=figsize)

        # Graficar datos históricos
        plt.plot(np.arange(len(self.data)), self.data, label='Observado')

        # Graficar predicciones
        plt.plot(forecast_index, forecast_mean, color='red', label='Predicción')

        # Graficar intervalos de confianza
        plt.fill_between(forecast_index,
                         conf_int.iloc[:, 0],
                         conf_int.iloc[:, 1],
                         color='pink', alpha=0.3, label=f'Intervalo de confianza {(1 - alpha) * 100}%')

        plt.title('Pronóstico SARIMA')
        plt.legend()
        plt.grid(True)
        plt.show()

    def grid_search(self, data=None, p_range=(0, 2), d_range=(0, 1), q_range=(0, 2),
                    P_range=(0, 1), D_range=(0, 1), Q_range=(0, 1), s_values=[12]):
        """
        Realiza una búsqueda en malla para encontrar los mejores hiperparámetros.

        Args:
            data (array-like, optional): Serie temporal. Si no se proporciona, se usan los datos del constructor.
            p_range (tuple): Rango de valores para p (componente AR).
            d_range (tuple): Rango de valores para d (componente I).
            q_range (tuple): Rango de valores para q (componente MA).
            P_range (tuple): Rango de valores para P (componente AR estacional).
            D_range (tuple): Rango de valores para D (componente I estacional).
            Q_range (tuple): Rango de valores para Q (componente MA estacional).
            s_values (list): Lista de valores estacionales a probar.

        Returns:
            tuple: La mejor configuración (p,d,q)(P,D,Q,s) encontrada.
        """
        if data is not None:
            self.data = data

        if self.data is None:
            raise ValueError("No se han proporcionado datos para la búsqueda en malla")

        # Inicializar ResultsManager para guardar resultados
        results = []
        self.results_manager = ResultsManager(results)

        best_aic = float('inf')
        best_params = None

        # Contador para iteración
        iteration_counter = 0

        # Iterar sobre todas las combinaciones
        for p in range(p_range[0], p_range[1] + 1):
            for d in range(d_range[0], d_range[1] + 1):
                for q in range(q_range[0], q_range[1] + 1):
                    for P in range(P_range[0], P_range[1] + 1):
                        for D in range(D_range[0], D_range[1] + 1):
                            for Q in range(Q_range[0], Q_range[1] + 1):
                                for s in s_values:
                                    iteration_counter += 1

                                    # Validar combinación
                                    if p == 0 and q == 0 and P == 0 and Q == 0:
                                        continue

                                    # Mostrar progreso
                                    print(f"Evaluando SARIMA({p},{d},{q})({P},{D},{Q},{s})")

                                    try:
                                        # Crear y ajustar modelo
                                        model = SARIMAX(
                                            self.data,
                                            order=(p, d, q),
                                            seasonal_order=(P, D, Q, s),
                                            enforce_stationarity=False,
                                            enforce_invertibility=False
                                        )
                                        model_fit = model.fit(disp=False)

                                        # Guardar resultados
                                        result = ResultManager(
                                            va=model_fit.aic,
                                            vo=best_aic,
                                            iteracion=iteration_counter,
                                            modelo=f"SARIMA({p},{d},{q})({P},{D},{Q},{s})"
                                        )
                                        self.results_manager.guardar_dato(result)

                                        # Actualizar el mejor modelo encontrado
                                        if model_fit.aic < best_aic:
                                            best_aic = model_fit.aic
                                            best_params = (p, d, q, P, D, Q, s)

                                        print(f"SARIMA({p},{d},{q})({P},{D},{Q},{s}) - AIC: {model_fit.aic}")

                                    except Exception as e:
                                        print(f"Error en SARIMA({p},{d},{q})({P},{D},{Q},{s}): {str(e)}")

        # Actualizar los parámetros del modelo con la mejor configuración
        if best_params:
            p, d, q, P, D, Q, s = best_params
            self.order = (p, d, q)
            self.seasonal_order = (P, D, Q, s)

            # Entrenar el modelo con los mejores parámetros
            self.fit()

        return best_params

    def to_csv(self, filepath):
        """
        Guarda los resultados de la búsqueda en malla en un archivo CSV.

        Args:
            filepath (str): Ruta donde guardar el archivo CSV.
        """
        if self.results_manager:
            self.results_manager.to_csv(filepath)
        else:
            print("No hay resultados para guardar")

    def summary(self):
        """
        Devuelve un resumen del modelo SARIMA.

        Returns:
            str: Resumen del modelo.
        """
        if self.fitted_model is None:
            raise ValueError("El modelo debe ser entrenado antes de generar el resumen")

        return self.fitted_model.summary()

    def decompose(self, type='additive'):
        """
        Descompone la serie temporal en sus componentes de tendencia,
        estacionalidad y residuos.

        Args:
            type (str): Tipo de descomposición ('additive' o 'multiplicative').

        Returns:
            object: Resultado de la descomposición.
        """
        from statsmodels.tsa.seasonal import seasonal_decompose

        if self.data is None:
            raise ValueError("No hay datos para descomponer")

        # Crear un índice para la descomposición
        index = pd.date_range(start='2000-01-01', periods=len(self.data), freq='D')
        series = pd.Series(self.data, index=index)

        # Descomponer la serie
        decomposition = seasonal_decompose(series, model=type, period=self.seasonal_order[3])

        # Graficar los resultados
        fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)

        axes[0].plot(decomposition.observed)
        axes[0].set_title('Serie Original')

        axes[1].plot(decomposition.trend)
        axes[1].set_title('Tendencia')

        axes[2].plot(decomposition.seasonal)
        axes[2].set_title('Estacionalidad')

        axes[3].plot(decomposition.resid)
        axes[3].set_title('Residuos')

        plt.tight_layout()
        plt.show()

        return decomposition