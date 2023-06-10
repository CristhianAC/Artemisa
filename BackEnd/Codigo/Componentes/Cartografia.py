'''
|------------------------------------------------------------------------------|
|                                                                              |
|                                Cartografía                                   |
|                                                                              |
|------------------------------------------------------------------------------|
'''
from .Componente import Componente
from typing import Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class Cartografia (Componente):

    def generarMapaRegiones (self, datasets):
        ubicaciones = {'ubicacion': [], 'latitude': [], 'longitude':[]}
        for dataset in datasets:
            coord = self.generarListadoCoordenadas(dataset)
            ubicaciones['ubicacion'].append(dataset.ubicacion)
            ubicaciones['latitude'].append(coord[0][2])
            ubicaciones['longitude'].append(coord[0][1])
        df = pd.DataFrame(ubicaciones)

        token = 'pk.eyJ1Ijoic2ViYXN0aWFubWFsZG9uYWRvMTk0NSIsImEiOiJjbGluYnRobHkwbDQyM2xwOGc4aGN5ZnpvIn0.Jal1X7da0VhVK8gkKrWBng'
        fig = go.Figure(go.Scattermapbox(
            mode = "markers+text",
            width = 500,
            lon = ubicaciones['latitude'], lat = ubicaciones['longitude'],
            marker = {'size': 20, 'symbol': ["park" for i in ubicaciones['ubicacion']]},
            text = ubicaciones['ubicacion'],textposition = "bottom right"))

        fig.update_layout(
            mapbox = {
                'accesstoken': token,
                'style': "outdoors", 'zoom': 8,
                'center': dict(lat = ubicaciones['longitude'][1], lon = ubicaciones['latitude'][1])},
            showlegend = False)
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

    def generarListadoCoordenadas (self, dataset, criterio: Optional[list] = [], rango: Optional[str] = "species"):
        return self.procesos.filtrado.filtrarDataSet({'species':[], 'decimalLatitude': [], 'decimalLongitude': []}, dataset, condicionales={rango: criterio})
    
    def calcularAreaDistribucion (self, dataset, criterio: Optional[list] = [], rango: Optional[str] = "species"):
        coordenadas = self.generarListadoCoordenadas(dataset, criterio, rango)

    #Generar particiones de las áreas de distribución según la distancia entre puntos
    def generarSeparacionesCoordenadasDistribucion (self, coordenadas):
        pass

    def generarMapaDistribucionEndemicas (self, dataset):
        df = self.procesos.filtrado.especiesEndemicas(dataset, self.procesos.endemicas)

        token = 'pk.eyJ1Ijoic2ViYXN0aWFubWFsZG9uYWRvMTk0NSIsImEiOiJjbGluYnRobHkwbDQyM2xwOGc4aGN5ZnpvIn0.Jal1X7da0VhVK8gkKrWBng'
        fig = px.scatter_mapbox(df, lat="decimalLatitude", lon="decimalLongitude", hover_name="species", hover_data=["species"],
                                color_discrete_sequence=["fuchsia"], zoom=11, height=300)

        fig.update_layout(
            mapbox = {
                'accesstoken': token,
                'style': "satellite", 'zoom': 11},
            showlegend = False)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig

    def generarMapaLocalizacionMuestras (self, dataset, especie):
        coord = self.generarListadoCoordenadas(dataset, criterio=[especie])
        df = pd.DataFrame({'species': [i[0] for i in coord],'latitude': [i[1] for i in coord], 'longitude':[j[2] for j in coord], 'conteo':[1 for z in coord]})

        try:
            pos = (list(df['latitude'])[0], list(df['longitude'])[0])
        except:
            pos (0, 0)
        
        fig = px.density_mapbox(df, lat = 'latitude', lon = 'longitude', z = 'conteo',
                                radius = 10,
                                center = dict(lat = pos[0], lon = pos[1]),
                                zoom = 11,
                                mapbox_style = 'carto-positron',
                                opacity = 0.5)
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
