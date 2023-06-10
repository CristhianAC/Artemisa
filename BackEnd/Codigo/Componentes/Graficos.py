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
        fig = px.line(df, x="year", y="S", title="Cantidad Especies Registradas por Año", markers=True, color_discrete_sequence=["darkgreen", "green", "lawngreen", "blue", "steelblue"]) 
        fig.update_layout(paper_bgcolor="rgb(15,163,72,0)", 
                          font=dict(
                                    family="Courier New, monospace",
                                    size=18,
                                    color="White"
                            ))
        return fig

    def temporalVariacionConteoMuestras (self, dataset):
        datos = self.procesos.estadisticos.obtenerInfoAnual(dataset)
        df = pd.DataFrame(dict(
            year = [year for year in datos.keys()],
            N = [datos[year]['N'] for year in datos.keys()]
        ))
        df = df.sort_values(by="year")

        print(df)
        fig = px.line(df, x="year", y="N", title="Cantidad Muestras Registradas por Año", markers=True, color_discrete_sequence=["green", "lawngreen", "blue", "steelblue"]) 
        fig.update_layout(paper_bgcolor="rgb(15,163,72,0)", 
                          font=dict(
                                    family="Courier New, monospace",
                                    size=18,
                                    color="White"
                            ))
        return fig

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

        fig = px.line(df, x="year", y=["Simpson","Menhinick", "Shannon"], title="Índices de medición de Biodiversidad Alfa", markers=True, color_discrete_sequence=["darkgreen", "blue", "steelblue"], width=600)
        fig.update_layout(paper_bgcolor="rgb(15,163,72,0)", 
                          font=dict(
                                    family="Courier New, monospace",
                                    size=12,
                                    color="White"),
                          legend=dict(
                            yanchor="top",
                            y=0.99,
                            xanchor="left",
                            x=0.01))    
        return fig

    def temporalBiodiversidadBeta (self, dataset):
        datos = self.procesos.estadisticos.obtenerDiversidadBeta(dataset)
        df = pd.DataFrame(dict(
            year = [year for year in datos.keys()],
            BrayCurtis = [datos[year][self.IND_BRAY_CURTIS] for year in datos.keys()]
        ))
        df = df.sort_values(by="year")
        print(df)

        fig = px.bar(df, x="year", y=["BrayCurtis"], title="Índice de Bray-Curtis en relación a la última medición", color_discrete_sequence=["blue", "steelblue"], width=600) 
        fig.update_layout(paper_bgcolor="rgb(15,163,72,0)", 
                          font=dict(
                            family="Courier New, monospace",
                            size=12,
                            color="White"),
                          legend=dict(
                            yanchor="top",
                            y=0.99,
                            xanchor="left",
                            x=0.01))
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
        fig = px.line(df, x="year", y="S", title="Cantidad Especies Endémicas Registradas por Año", markers=True, color_discrete_sequence=["darkgreen", "green", "lawngreen", "blue", "steelblue"], width=600) 
        fig.update_layout(paper_bgcolor="rgb(15,163,72,0)", 
                          font=dict(
                                    family="Courier New, monospace",
                                    size=12,
                                    color="White"
                            ),
                          legend=dict(
                            yanchor="top",
                            y=0.99,
                            xanchor="left",
                            x=0.01))
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
        fig.update_layout(paper_bgcolor="rgb(15,163,72,0)", 
                          font=dict(
                                    family="Courier New, monospace",
                                    size=12,
                                    color="White"
                            ))
        return fig

    def proporcionEspeciesEndemicas (self, dataset):
        endemicas_anual = self.procesos.estadisticos.obtenerConteoEspeciesEndemicas(dataset, 'Cat')

        df = pd.DataFrame(dict(
            cant = [endemicas_anual[year]['species'][categoria] for year in endemicas_anual.keys() for categoria in endemicas_anual[year]['species'].keys()],
            cat = [categoria for year in endemicas_anual.keys() for categoria in endemicas_anual[year]['species'].keys()],
            year = [year for year in endemicas_anual.keys() for categoria in endemicas_anual[year]['species'].keys()],
        ))

        fig = px.sunburst(df, path=['year', 'cat'], values='cant', color_discrete_sequence=["blue", "green", "lawngreen", "blue", "steelblue"], title='Proporción Especies Endémicas')
        fig.update_layout(paper_bgcolor="rgb(15,163,72,0)", 
                          font=dict(
                                    family="Courier New, monospace",
                                    size=18,
                                    color="White"
                            ))
        return fig

    def curvaAcumulacionEspecies (self, dataset):
        datos = self.procesos.estadisticos.calcularCurvaAcumulacion(dataset)

        df = pd.DataFrame(dict(
            month = [f"{1+month}/{year}" for year in datos.keys() for month in range(12)],
            S = [datos[year]['S'][month] for year in datos.keys() for month in range(12)],
            S_acum = [datos[year]['S_acum'][month] for year in datos.keys() for month in range(12)],
            N = [datos[year]['N'][month] for year in datos.keys() for month in range(12)]
        ))

        fig = px.line(df, x="month", y=["S","S_acum"], title="Curva de Acumulación de Especies", markers=True, color_discrete_sequence=["lawngreen", "steelblue"])
        fig.update_layout(paper_bgcolor="rgb(15,163,72,0)", 
                          font=dict(
                                    family="Courier New, monospace",
                                    size=18,
                                    color="White"
                            ))
        return fig

    def variacionConteoEspecie (self, dataset, specie):
        datos = self.procesos.estadisticos.obtenerInfoAnual(dataset)
        registros = list(datos.keys())
        registros.sort()
        muestras_mensuales = { year:
                                { month: self.procesos.estadisticos.obtenerConteoRangoTaxonomico(dataset, condicionales= {'year': [year], 'month': [month+1], 'species': [specie]}) for month in range(12)}
                            for year in registros
                            }
        
        self.acum = 0

        try:
            df = pd.DataFrame(dict(
                        month = [f"{1+month}/{year}" for year in datos.keys() for month in range(12)],
                        conteos_muestras = [muestras_mensuales[year][month][specie] if len(muestras_mensuales[year][month]) > 0 else 0 for year in muestras_mensuales for month in muestras_mensuales[year]],
                        acum_muestras = [self.acumular(muestras_mensuales[year][month][specie]) if len(muestras_mensuales[year][month]) > 0 else self.acum for year in muestras_mensuales for month in muestras_mensuales[year]],
                    ))
        except:
            df = pd.DataFrame(dict(
                        month = [f"" for i in range(12)],
                        conteos_muestras = [0 for i in range(12)],
                        acum_muestras = [f"" for i in range(12)]
                    ))

        fig = px.line(df, x="month", y=["conteos_muestras","acum_muestras"], title=f"Conteo de Muestras para {specie}", markers=True, color_discrete_sequence=["lawngreen", "steelblue"])
        fig.update_layout(paper_bgcolor="rgb(15,163,72,0)", 
                          font=dict(
                                    family="Courier New, monospace",
                                    size=18,
                                    color="White"
                            ))
        return fig

    def conteoEspeciesPeligroExtincion (self, dataset):
        #peligro_ext_anual = self.procesos.estadisticos.obtenerConteoEspeciesPeligroExtincion(dataset, 'category')
        esp_peligro_ext_anual = self.procesos.estadisticos.obtenerConteoEspeciesPeligroExtincion(dataset)
        cat_por_especie = self.procesos.filtrado.especiesPeligroExtincion(dataset, self.procesos.peligro_extinsion)
        print(cat_por_especie)

        df = pd.DataFrame(dict(
            cant = [esp_peligro_ext_anual[year][specie] for year in esp_peligro_ext_anual.keys() for specie in esp_peligro_ext_anual[year].keys()],
            esp = [specie for year in esp_peligro_ext_anual.keys() for specie in esp_peligro_ext_anual[year].keys()],
            cat = [year for year in esp_peligro_ext_anual.keys() for specie in esp_peligro_ext_anual[year].keys()],
            year = [year for year in esp_peligro_ext_anual.keys() for specie in esp_peligro_ext_anual[year].keys()],
        ))

        fig = px.sunburst(df, path=['year', 'cat', 'esp'], values='cant', color_discrete_sequence=["lawngreen", "blue", "steelblue"])
        fig.update_layout(paper_bgcolor="rgb(15,163,72,0)", 
                          font=dict(
                                    family="Courier New, monospace",
                                    size=18,
                                    color="White"
                            ))
        return fig
    
    def proporcionEspeciesPeligroExtincion (self, dataset):
        peligro_ext_anual = self.procesos.estadisticos.obtenerConteoEspeciesPeligroExtincion(dataset, 'category')

        df = pd.DataFrame(dict(
            cant = [peligro_ext_anual[year]['species'][categoria] for year in peligro_ext_anual.keys() for categoria in peligro_ext_anual[year]['species'].keys()],
            cat = [categoria for year in peligro_ext_anual.keys() for categoria in peligro_ext_anual[year]['species'].keys()],
            year = [year for year in peligro_ext_anual.keys() for categoria in peligro_ext_anual[year]['species'].keys()],
        ))

        fig = px.sunburst(df, path=['year', 'cat'], values='cant', color_discrete_sequence=["blue", "green", "lawngreen", "blue", "steelblue"], title='Proporción Especies por categoría IUCN')
        fig.update_layout(paper_bgcolor="rgb(15,163,72,0)", 
                          font=dict(
                                    family="Courier New, monospace",
                                    size=18,
                                    color="White"
                            ))
        return fig

    def acumular (self, num):
        self.acum += num
        return self.acum
