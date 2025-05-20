import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from results_manager import ResultManager, ResultsManager


class ArimaModel:
    """
    Clase para implementar y gestionar modelos ARIMA (AutoRegressive Integrated Moving Average)
    para el análisis y predicción de series temporales.
    """

    def __init__(self, data=None, order=(1, 0, 0)):
        """
        Inicializa un modelo ARIMA con los parámetros especificados.

        Args:
            data (array-like, optional): Serie temporal para entrenar el modelo.
            order (tuple, optional): Orden del modelo ARIMA (p,d,q).
                p: Términos autorregresivos
                d: Diferenciación necesaria para hacer la serie estacionaria
                q: Términos de media móvil
        """
        self.data = data
        self.order = order
        self.model = None
        self.fitted_model = None
        self.predictions = None
        self.residuals = None
        self.results_manager = None

    def fit(self, data=None):
        """
        Entrena el modelo ARIMA con los datos proporcionados.

        Args:
            data (array-like, optional): Serie temporal para entrenar el modelo.
                Si no se proporciona, se utilizan los datos del constructor.

        Returns:
            self: La instancia del modelo entrenado.
        """
        if data is not None:
            self.data = data

        if self.data is None:
            raise ValueError("No se han proporcionado datos para entrenar el modelo")

        self.model = ARIMA(self.data, order=self.order)
        self.fitted_model = self.model.fit()
        self.residuals = self.fitted_model.resid

        return self

    def predict(self, steps=1):
        """
        Realiza predicciones con el modelo ARIMA entrenado.

        Args:
            steps (int, optional): Número de pasos a predecir. Por defecto es 1.

        Returns:
            array: Predicciones del modelo.
        """
        if self.fitted_model is None:
            raise ValueError("El modelo debe ser entrenado antes de realizar predicciones")

        # Realizar predicción
        self.predictions = self.fitted_model.forecast(steps=steps)
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

    def plot_diagnostics(self, figsize=(12, 8)):
        """
        Genera gráficos de diagnóstico para el modelo ARIMA.

        Args:
            figsize (tuple, optional): Tamaño de la figura.
        """
        if self.fitted_model is None:
            raise ValueError("El modelo debe ser entrenado antes de generar diagnósticos")

        fig, axes = plt.subplots(2, 2, figsize=figsize)

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
        plot_acf(self.residuals, ax=axes[1, 0], lags=20)
        axes[1, 0].set_title('ACF de residuos')

        # PACF de residuos
        plot_pacf(self.residuals, ax=axes[1, 1], lags=20)
        axes[1, 1].set_title('PACF de residuos')

        plt.tight_layout()
        plt.show()

    def plot_forecast(self, steps=10, alpha=0.05, figsize=(10, 6)):
        """
        Visualiza las predicciones futuras con intervalos de confianza.

        Args:
            steps (int, optional): Número de pasos a predecir. Por defecto es 10.
            alpha (float, optional): Nivel de significancia para los intervalos de confianza.
            figsize (tuple, optional): Tamaño de la figura.
        """
        if self.fitted_model is None:
            raise ValueError("El modelo debe ser entrenado antes de visualizar predicciones")

        # Realizar predicción
        forecast_result = self.fitted_model.get_forecast(steps=steps)
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

        plt.title('Pronóstico ARIMA')
        plt.legend()
        plt.grid(True)
        plt.show()

    def grid_search(self, data=None, p_range=(0, 2), d_range=(0, 2), q_range=(0, 2)):
        """
        Realiza una búsqueda en malla para encontrar los mejores hiperparámetros (p,d,q).

        Args:
            data (array-like, optional): Serie temporal. Si no se proporciona, se usan los datos del constructor.
            p_range (tuple, optional): Rango de valores para p.
            d_range (tuple, optional): Rango de valores para d.
            q_range (tuple, optional): Rango de valores para q.

        Returns:
            tuple: La mejor configuración (p,d,q) encontrada.
        """
        if data is not None:
            self.data = data

        if self.data is None:
            raise ValueError("No se han proporcionado datos para la búsqueda en malla")

        # Inicializar ResultsManager para guardar resultados
        results = []
        self.results_manager = ResultsManager(results)

        best_aic = float('inf')
        best_order = None

        # Iterar sobre todas las combinaciones
        for p in range(p_range[0], p_range[1] + 1):
            for d in range(d_range[0], d_range[1] + 1):
                for q in range(q_range[0], q_range[1] + 1):
                    try:
                        # Crear y ajustar modelo
                        model = ARIMA(self.data, order=(p, d, q))
                        model_fit = model.fit()

                        # Guardar resultados
                        result = ResultManager(
                            va=model_fit.aic,
                            vo=best_aic,
                            iteracion=p * 100 + d * 10 + q,
                            modelo=f"ARIMA({p},{d},{q})"
                        )
                        self.results_manager.guardar_dato(result)

                        # Actualizar el mejor modelo encontrado
                        if model_fit.aic < best_aic:
                            best_aic = model_fit.aic
                            best_order = (p, d, q)

                        print(f"ARIMA({p},{d},{q}) - AIC: {model_fit.aic}")

                    except Exception as e:
                        print(f"Error en ARIMA({p},{d},{q}): {str(e)}")

        # Actualizar los parámetros del modelo con la mejor configuración
        self.order = best_order

        # Entrenar el modelo con los mejores parámetros
        self.fit()

        return best_order

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
        Devuelve un resumen del modelo ARIMA.

        Returns:
            str: Resumen del modelo.
        """
        if self.fitted_model is None:
            raise ValueError("El modelo debe ser entrenado antes de generar el resumen")

        return self.fitted_model.summary()