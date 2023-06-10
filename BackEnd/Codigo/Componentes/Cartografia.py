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
import numpy as np
import plotly.express as px

class Cartografia (Componente):

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
        return fig
