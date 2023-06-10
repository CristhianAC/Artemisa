from Codigo.Componentes.Cartografia import Cartografia
from Codigo.Componentes.Estadisticas import Estadisticas
from Codigo.Componentes.Filtrado import Filtrado
from Codigo.Componentes.Graficos import Graficos
from Codigo.Componentes.Miscelania import Miscelania
from Codigo.Componentes.IA import Openaai
from ConversorSQL import ConversorSQL
from Codigo.Componentes.Constantes import Constantes
import os

import pandas as pd
import sqlite3, os

class Procesos:

    def __init__ (self):
        #Crear Procesos
        self.cartoficos = Cartografia(self)
        self.estadisticos = Estadisticas(self)
        self.filtrado = Filtrado()
        self.graficos = Graficos(self)
        self.miscelania = Miscelania(self)
        self.ia = Openaai(self.miscelania)
        print('Directory Name: ', os.path.dirname(__file__))
        self.conversor = ConversorSQL(os.path.dirname(__file__))

        #Cargar Bases de Datos
        self.datasets = self.conversor.cargarDatasets()
        self.endemicas = self.conversor.cargarEspeciesEndemicas()
        self.peligro_extincion = self.conversor.cargarPeligroExtincion()

        self.dataset = self.datasets[2]

        #Generar Resúmenes
        '''res = [self.miscelania.generarResumentTextualBreveRegion(self.datasets[0]),
                self.miscelania.generarResumentTextualBreveRegion(self.datasets[1]),
                self.miscelania.generarResumentTextualBreveRegion(self.datasets[2]),
                self.miscelania.generarResumentTextualBreveRegion(self.datasets[3]),
                self.miscelania.generarResumentTextualBreveRegion(self.datasets[4]),
                self.miscelania.generarResumentTextualBreveRegion(self.datasets[5]),
                self.miscelania.generarResumentTextualBreveRegion(self.datasets[6]),
                self.miscelania.generarResumentTextualBreveRegion(self.datasets[7]),
                self.miscelania.generarResumentTextualBreveRegion(self.datasets[8]),
                self.miscelania.generarResumentTextualBreveRegion(self.datasets[9]),
                self.miscelania.generarResumentTextualBreveRegion(self.datasets[10]),
                self.miscelania.generarResumentTextualBreveRegion(self.datasets[11])]


        #Cargar Gráficas para todos los dataset
        for db in self.datasets:
            db.cargarGraficas(
                context = {
                #Gráficas
                "varCantEsp": self.graficos.temporalVariacionCantEspecies(db).to_html(),
                "varContMuestra": self.graficos.temporalVariacionConteoMuestras(db).to_html(),
                "BiodivAlpha": self.graficos.temporalBiodiversidadAlpha(db).to_html(),
                "BiodivBeta": self.graficos.temporalBiodiversidadBeta(db).to_html(),
                "varConteoEspEnd": self.graficos.variacionConteoEspeciesEndemicas(db).to_html(),
                "varEspEnd": self.graficos.variacionEspeciesEndemicas(db).to_html(),
                "propEspEnd": self.graficos.proporcionEspeciesEndemicas(db).to_html(),
                "acumEsp": self.graficos.curvaAcumulacionEspecies(db).to_html(),
                "varEspecie": self.graficos.variacionConteoEspecie(db, "Spondias mombin").to_html(),
                
                #Mapas
                "mapEspEnd": self.cartoficos.generarMapaDistribucionEndemicas(db).to_html(),
                "mapMuestra": self.cartoficos.generarMapaLocalizacionMuestras(db, "Spondias mombin").to_html(),
                "mapRegiones": self.cartoficos.generarMapaRegiones(self.datasets).to_html(),

                #Conclusiones
                "conclusiones": self.ia.generarConclusion(db),
                
                #Descripciones
                "res_dataset1": res[0],
                "res_dataset2": res[1],
                "res_dataset3": res[2],
                "res_dataset4": res[3],
                "res_dataset5": res[4],
                "res_dataset6": res[5],
                "res_dataset7": res[6],
                "res_dataset8": res[7],
                "res_dataset9": res[8],
                "res_dataset10": res[9],
                "res_dataset11": res[10],
                "res_dataset12": res[11]}
            )'''

        #Cargar Gráficas
        db = self.dataset
        '''self.context = {
                #Gráficas
                "varCantEsp": self.graficos.temporalVariacionCantEspecies(db).to_html(),
                "varContMuestra": self.graficos.temporalVariacionConteoMuestras(db).to_html(),
                "BiodivAlpha": self.graficos.temporalBiodiversidadAlpha(db).to_html(),
                "BiodivBeta": self.graficos.temporalBiodiversidadBeta(db).to_html(),
                "varConteoEspEnd": self.graficos.variacionConteoEspeciesEndemicas(db).to_html(),
                "varEspEnd": self.graficos.variacionEspeciesEndemicas(db).to_html(),
                "propEspEnd": self.graficos.proporcionEspeciesEndemicas(db).to_html(),
                "acumEsp": self.graficos.curvaAcumulacionEspecies(db).to_html(),
                "varEspecie": self.graficos.variacionConteoEspecie(db, "Spondias mombin").to_html(),
                
                #Mapas
                "mapEspEnd": self.cartoficos.generarMapaDistribucionEndemicas(db).to_html(),
                "mapMuestra": self.cartoficos.generarMapaLocalizacionMuestras(db, "Spondias mombin").to_html(),
                "mapRegiones": self.cartoficos.generarMapaRegiones(self.datasets).to_html(),

                #Conclusiones
                
                #Descripciones
                "res_dataset1": self.miscelania.generarResumentTextualBreveRegion(self.datasets[0]),
                "res_dataset2": self.miscelania.generarResumentTextualBreveRegion(self.datasets[1]),
                "res_dataset3": self.miscelania.generarResumentTextualBreveRegion(self.datasets[2]),
                "res_dataset4": self.miscelania.generarResumentTextualBreveRegion(self.datasets[3]),
                "res_dataset5": self.miscelania.generarResumentTextualBreveRegion(self.datasets[4]),
                "res_dataset6": self.miscelania.generarResumentTextualBreveRegion(self.datasets[5]),
                "res_dataset7": self.miscelania.generarResumentTextualBreveRegion(self.datasets[6]),
                "res_dataset8": self.miscelania.generarResumentTextualBreveRegion(self.datasets[7]),
                "res_dataset9": self.miscelania.generarResumentTextualBreveRegion(self.datasets[8]),
                "res_dataset10": self.miscelania.generarResumentTextualBreveRegion(self.datasets[9]),
                "res_dataset11": self.miscelania.generarResumentTextualBreveRegion(self.datasets[10]),
                "res_dataset12": self.miscelania.generarResumentTextualBreveRegion(self.datasets[11])}'''

    def obternerHTML (self, ind: int = 2):
        self.dataset = self.datasets[ind]
        self.context = self.dataset.context
        return self.context

    def solicitarInfoEspecie (self, especie):
        self.context['mapMuestra'] = self.cartoficos.generarMapaLocalizacionMuestras(self.dataset, especie).to_html()
        self.context['varEspecie'] = self.cartoficos.generarMapaLocalizacionMuestras(self.dataset, especie).to_html()

        return self.context

procesos = Procesos()
db = procesos.datasets[2]
procesos.graficos.proporcionEspeciesPeligroExtincion(db).show()
#print(df)