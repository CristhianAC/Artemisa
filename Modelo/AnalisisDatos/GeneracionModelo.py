import os
import pandas as pd
import numpy as np

import geopandas as gpd
import matplotlib.pyplot as plt
import shapely
import shutil
import glob

import random

import sys
sys.path.insert(0, f'{os.path.dirname(os.path.dirname(__file__))}')
from ClasesGlobales.VariablesFuncionamiento import VariablesFuncionamiento
from ClasesGlobales.ConectorBaseDatos import ConectorBaseDatos
from ConversionDatos.ConversionDatos import ConversionDatos

conector = ConectorBaseDatos()
conversor = ConversionDatos()

#---------------------------|Convertir de coordenadas a metros|---------------------------#
def distanciaCoordenadas (lat1: float, lon1: float, lat2: float, lon2: float): 
    R = 6378.137
    dLat = lat2 * np.pi / 180 - lat1 * np.pi / 180
    dLon = lon2 * np.pi / 180 - lon1 * np.pi / 180
    a = np.sin(dLat/2) * np.sin(dLat/2) + np.cos(lat1 * np.pi / 180) * np.cos(lat2 * np.pi / 180) * np.sin(dLon/2) * np.sin(dLon/2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    d = R * c
    return d * 1000

def generarCoordenadas (coordenadas: list, perimetro_seleccion: tuple, rango_distancias: tuple, imagen) -> tuple:
    rang_lat, rang_lon = perimetro_seleccion
    encontrado = False
    
    while (not(encontrado)):    
        # Generar Coordenadas aleatorias dentro del perímetro
        latitud = random.uniform(rang_lat[0], rang_lat[1])
        longitud = random.uniform(rang_lon[0], rang_lon[1])
        
        # Obtener Ecosistema de la coordenada
        x, y = conversor.convertirCoordenadasAPixeles(longitud, latitud) #Calcular pixeles
        color, tipo_ecosistema = conversor.obtenerColorTipoEcosistema(imagen, x, y) #Obtener Color y Tipo de Ecosistema
        
        # Evaluar validez de la ubicación a partir del tipo de ecosistema        
        tipo_ecosistemas_admitidos = ['Ecosistemas Terrestres',
                                        'Ecosistemas Acuaticos Continentales',
                                        'Ecosistemas Costeros',
                                        'Ecosistemas Insulares']
        if not(any([tipo_ecosistema == tipo_ecosistema_admitido for tipo_ecosistema_admitido in tipo_ecosistemas_admitidos])):
            continue
        
        # Evaluar validez de la ubicación a partir del ecosistema
        ecosistemas_no_admitidos = ['Sin informacion',
                                    'Territorio artificializado',
                                    'Sin informacion']
        ecosistema = conversor.lista_ecosistemas[tipo_ecosistema][color]
        if any([ecosistema == ecosistema_no_admitido for ecosistema_no_admitido in ecosistemas_no_admitidos]):
            continue
        
        # Evaluar distancia con todos los puntos
        evaluacion_distancias = []
        for coord in coordenadas:
            distancia = distanciaCoordenadas(coord[0], coord[1], latitud, longitud)
            evaluacion_distancias.append(distancia < rango_distancias[0] or distancia > rango_distancias[1])
        
        if any(evaluacion_distancias):
            continue
        
        encontrado = True

    return (latitud, longitud)


# Establecer Conexión con la Base de Datos
res_conexion = conector.establecerConexionBaseDatos()
print(res_conexion['estado'])

# Obtener Lista de Registros para la Especie
res_consulta = conector.consultarBaseDatos({'registro_especie':['= 1091988'], 'registro_latitud':[], 'registro_longitud':[]}, 'Registro')
print(res_consulta['estado'])

# Almacenar los datos en GeoDataFrame
datos = {'CLASS':[], 'lon':[], 'lat':[], 'geometry':[]}
for registro in res_consulta['resultado']:
    datos['CLASS'].append(1)
    datos['lat'].append(float(registro[1]))
    datos['lon'].append(float(registro[2]))
    datos['geometry'].append(shapely.geometry.point.Point(registro[1], registro[2]))

# Generación de un Perímetro de Selección
perimetro_seleccion = ((min(datos['lat']), max(datos['lat'])), (min(datos['lon']), max(datos['lon'])))

# Lectura de la imagen de Ecosistemas
res_lectura = conversor.lector_archivos.leerImagen ('E_ECCMC_Ver21_100K' , 'png')
imagen = res_lectura['datos archivo']

# Generación de Datos de Ausencia
cantidad_ausencias = len(res_consulta['resultado'])   # Proporción 1:1 con datos de presencia

rango_distancias = (100, 1000) # Distancias mínimas y máximas de generación (en Metros)
for i in range(cantidad_ausencias):
    coordenadas = generarCoordenadas(zip(datos['lat'], datos['lon']), perimetro_seleccion, rango_distancias, imagen)
    
    datos['CLASS'].append(0)
    datos['lat'].append(coordenadas[0])
    datos['lon'].append(coordenadas[1])
    datos['geometry'].append(shapely.geometry.point.Point(coordenadas[0], coordenadas[1]))
    print(f"Coordenadas cargadas {i}/{cantidad_ausencias}")
    

dataset = gpd.GeoDataFrame({'CLASS': datos['CLASS'], 'geometry': datos['geometry']}, crs='epsg:4326')

print(dataset)

print("number of duplicates: ", dataset.duplicated(subset='geometry', keep='first').sum())
print("number of NA's: ", dataset['geometry'].isna().sum())
print("Coordinate reference system is: {}".format(dataset.crs))
print("{} observations with {} columns".format(*dataset.shape))

direccion_rasters = f'{conversor.direccion_entradas_analisis_datos}/variables_climaticas/wc2.1_2.5m_bio_*.tif'
raster_features = sorted(glob.glob(direccion_rasters))
# check number of features 
print('\nThere are', len(raster_features), 'raster features.')

from pyimpute import load_training_vector
from pyimpute import load_targets
train_xs, train_y = load_training_vector(dataset, raster_features, response_field='CLASS')
target_xs, raster_info = load_targets(raster_features)
print(f'{(train_xs.shape, train_y.shape)}') # check shape, does it match the size above of the observations?


print(train_y)

# import machine learning classifiers
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

CLASS_MAP = {
    'rf': (RandomForestClassifier()),
    'et': (ExtraTreesClassifier()),
    'xgb': (XGBClassifier()),
    'lgbm': (LGBMClassifier())
    }

from pyimpute import impute
from sklearn import model_selection
# model fitting and spatial range prediction
for name, (model) in CLASS_MAP.items():
    # cross validation for accuracy scores (displayed as a percentage)
    k = 5 # k-fold
    kf = model_selection.KFold(n_splits=k)
    accuracy_scores = model_selection.cross_val_score(model, train_xs, train_y, cv=kf, scoring='accuracy')
    print(name + " %d-fold Cross Validation Accuracy: %0.2f (+/- %0.2f)"
          % (k, accuracy_scores.mean() * 100, accuracy_scores.std() * 200))
    
    # spatial prediction
    model.fit(train_xs, train_y)
    os.mkdir('outputs/' + name + '-images')
    impute(target_xs, model, raster_info, outdir='outputs/' + name + '-images',
           class_prob=True, certainty=True)
    

from pylab import plt

# define spatial plotter
def plotit(x, title, cmap="Blues"):
    plt.imshow(x, cmap=cmap, interpolation='nearest')
    plt.colorbar()
    plt.title(title, fontweight = 'bold')

import rasterio
distr_rf = rasterio.open("outputs/rf-images/probability_1.0.tif").read(1)
distr_et = rasterio.open("outputs/et-images/probability_1.0.tif").read(1)
distr_xgb =  rasterio.open("outputs/xgb-images/probability_1.0.tif").read(1)
distr_lgbm =  rasterio.open("outputs/lgbm-images/probability_1.0.tif").read(1)
distr_averaged = (distr_rf + distr_et + distr_xgb + distr_lgbm)/4  

plotit(distr_averaged, "Joshua Tree Range, averaged", cmap="Greens")