from .Codigo.Componentes.Cartografia import Cartografia
from .Codigo.Componentes.Estadisticas import Estadisticas
from .Codigo.Componentes.Filtrado import Filtrado
from .Codigo.Componentes.Graficos import Graficos
from .Codigo.Componentes.Miscelania import Miscelania
from .ConversorSQL import ConversorSQL
from .Codigo.Componentes.Constantes import Constantes

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
        self.conversor = ConversorSQL('/home/Maldonado/Artemisa_Web/Artemisa/BackEnd')

        #Descargar Bases de Datos

        #Cargar Bases de Datos
        self.datasets = self.conversor.cargarDatasets()
        self.endemicas = self.conversor.cargarEspeciesEndemicas()

procesos = Procesos()

db = procesos.datasets[0]

df = {}
#df = procesos.filtrado.filtrarDataSet({'*': [], 'data_index': [1, 2, 3, 4, 5]}, db)
#df = procesos.estadisticos.obtenerConteoRangoTaxonomico(db, rango='year')
#df = procesos.cartoficos.generarListadoCoordenadas(db, criterio=['Plantae'], rango='kingdom')
#df = procesos.estadisticos.obtenerDiversidadAlpha(db)
#df = procesos.filtrado.especiesEndemicas(db, procesos.endemicas)
#procesos.graficos.temporalBiodiversidadAlpha(db)
#procesos.graficos.temporalBiodiversidadBeta(db)
#procesos.graficos.variacionEspeciesEndemicas(db)
#procesos.graficos.variacionConteoEspeciesEndemicas(db)
#procesos.graficos.proporcionEspeciesEndemicas(db)
#procesos.cartoficos.generarMapaDistribucionEndemicas(db)
#procesos.cartoficos.generarMapaLocalizacionMuestras(db, 'Arremon schlegeli')
#df = procesos.miscelania.generarResumenTextualRegion(db)
#df = procesos.estadisticos.obtenerDiversidadBeta(db)
#df = procesos.estadisticos.calcularCurvaAcumulacion(db)
#procesos.graficos.curvaAcumulacionEspecies(db)

print(df)