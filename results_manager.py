import polars as pl
class ResultManager:
    def __init__(self,va:float,vo:float,iteracion:int,modelo:str) -> None:
        self.va = va
        self.vo = vo
        self.iteracion = iteracion
        self.modelo = modelo

    def __str__(self):
        return f"Valor Actual: {self.va}, Valor Objetivo: {self.vo}, Iteracion: {self.iteracion}, Modelo: {self.modelo}"



class ResultsManager:
    def __init__(self,resultados:list[ResultManager]):
        self.resultados = resultados

    def guardar_dato(self,resultado:ResultManager):
        self.resultados.append(resultado)

    def show(self):
        for r in self.resultados:
            print(f"{r}")

    def to_polars(self):
        import polars as pl 
        data = []

        for r in self.resultados:
            data.append({
                "Valor Actual":r.va,
                "Valor Objetivo":r.vo,
                "Iteracion":r.iteracion,
                "Modelo":r.modelo
            })

        return pl.DataFrame(data)

    def to_csv(self,filepath:str):
        import polars as pl 
        data = []

        for r in self.resultados:
            data.append({
                "Valor Actual":r.va,
                "Valor Objetivo":r.vo,
                "Iteracion":r.iteracion,
                "Modelo":r.modelo
            })

        df = pl.DataFrame(data)
        try:
            df.write_csv(file=filepath)
            print("Archivo escrito")
        except ValueError:
            print("No se pudo escribir")





    

