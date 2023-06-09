'''
|------------------------------------------------------------------------------|
|                                                                              |
|                                  Gráficos                                    |
|                                                                              |
|------------------------------------------------------------------------------|
'''
from .Componente import Componente
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class Graficos (Componente):

    def temporalVariacionCantEspecies (self, dataset):
        datos = self.procesos.estadisticos.obtenerInfoAnual(dataset)
        df = pd.DataFrame(dict(
            year = [year for year in datos.keys()],
            S = [datos[year]['S'] for year in datos.keys()]
        ))
        df = df.sort_values(by="year")

        print(df)
        fig = px.line(df, x="year", y="S", title="Cantidad Especies Registradas por Año", markers=True) 
        return fig

    def temporalVariacionConteoMuestras (self, dataset):
        datos = self.procesos.estadisticos.obtenerInfoAnual(dataset)
        df = pd.DataFrame(dict(
            year = [year for year in datos.keys()],
            N = [datos[year]['N'] for year in datos.keys()]
        ))
        df = df.sort_values(by="year")

        print(df)
        fig = px.line(df, x="year", y="N", title="Cantidad Especies Registradas por Año", markers=True) 
        return fig

    def temporalVariacionDistribucionEspecies (self, intervalo):
        pass

    def temporalBiodiversidadAlpha (self, dataset):
        datos = self.procesos.estadisticos.obtenerDiversidadAlpha(dataset)
        df = pd.DataFrame(dict(
            year = [year for year in datos.keys()],
            Simpson = [datos[year][self.IND_SIMPSON] for year in datos.keys()],
            Menhinick = [datos[year][self.IND_MENHINICK] for year in datos.keys()],
            Shannon = [datos[year][self.IND_SHANNON] for year in datos.keys()]
        ))
        df = df.sort_values(by="year")
        print(df)

        fig = px.line(df, x="year", y=["Simpson","Menhinick", "Shannon"], title="Índices de medición de Biodiversidad Alfa", markers=True) 
        return fig

    def temporalBiodiversidadBeta (self, dataset):
        datos = self.procesos.estadisticos.obtenerDiversidadBeta(dataset)
        df = pd.DataFrame(dict(
            year = [year for year in datos.keys()],
            BrayCurtis = [datos[year][self.IND_BRAY_CURTIS] for year in datos.keys()]
        ))
        df = df.sort_values(by="year")
        print(df)

        fig = px.bar(df, x="year", y=["BrayCurtis"], title="Índice de Bray-Curtis en relación a la última medición") 
        return fig

    def variacionEspeciesEndemicas (self, dataset):
        endemicas_anual = self.procesos.estadisticos.obtenerConteoEspeciesEndemicas(dataset)
        for year in endemicas_anual.keys():
            endemicas_anual[year]['S'] = len(endemicas_anual[year]['species'].keys())

        df = pd.DataFrame(dict(
            year = [year for year in endemicas_anual.keys()],
            S = [endemicas_anual[year]['S'] for year in endemicas_anual.keys()]
        ))
        df = df.sort_values(by="year")

        print(df)
        fig = px.line(df, x="year", y="S", title="Cantidad Especies Endémicas Registradas por Año", markers=True) 
        return fig  

    def variacionConteoEspeciesEndemicas(self, dataset):
        endemicas_anual = self.procesos.estadisticos.obtenerConteoEspeciesEndemicas(dataset)

        fig = go.Figure()
        species = set()
        for year in endemicas_anual.keys():
            conteo = []
            for specie in endemicas_anual[year]['species'].keys():
                species.add(specie)

                try:
                    dato = endemicas_anual[year]['species'][specie]
                    conteo.append(dato)
                except:
                    conteo.append(0)

            fig.add_trace(go.Bar(
                x=list(species),
                y=conteo,
                name=f'{year}',
            ))

        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(barmode='group', xaxis_tickangle=-45)
        return fig

    def proporcionEspeciesEndemicas (self, dataset):
        endemicas_anual = self.procesos.estadisticos.obtenerConteoEspeciesEndemicas(dataset, 'Cat')

        df = pd.DataFrame(dict(
            cant = [endemicas_anual[year]['species'][categoria] for year in endemicas_anual.keys() for categoria in endemicas_anual[year]['species'].keys()],
            cat = [categoria for year in endemicas_anual.keys() for categoria in endemicas_anual[year]['species'].keys()],
            year = [year for year in endemicas_anual.keys() for categoria in endemicas_anual[year]['species'].keys()],
        ))

        fig = px.sunburst(df, path=['year', 'cat'], values='cant')
        return fig

    def proporcionCategoriasTaxonomicas (self, dataset):
        pass

    def curvaAcumulacionEspecies (self, dataset):
        datos = self.procesos.estadisticos.calcularCurvaAcumulacion(dataset)

        df = pd.DataFrame(dict(
            month = [f"{1+month}/{year}" for year in datos.keys() for month in range(12)],
            S = [datos[year]['S'][month] for year in datos.keys() for month in range(12)],
            S_acum = [datos[year]['S_acum'][month] for year in datos.keys() for month in range(12)],
            N = [datos[year]['N'][month] for year in datos.keys() for month in range(12)]
        ))

        fig = px.line(df, x="month", y=["S","S_acum"], title="Curva de Acumulación de Especies", markers=True) 
        return fig