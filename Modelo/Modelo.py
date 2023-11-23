import os
import pandas as pd
import numpy as np

import geopandas as gpd
import matplotlib.pyplot as plt
import shapely
import glob
import rasterio

import matplotlib.pyplot as plt
import matplotlib as mpl

import random

from .ClasesGlobales.VariablesFuncionamiento import VariablesFuncionamiento
from .ClasesGlobales.ConectorBaseDatos import ConectorBaseDatos
from .ConversionDatos.ConversionDatos import ConversionDatos

conector = ConectorBaseDatos()
conversor = ConversionDatos()

import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from shapely.geometry import mapping
import rioxarray as rxr
import xarray as xr
import geopandas as gpd

import earthpy as et
import earthpy.plot as ep
from shapely.geometry.point import Point
from shapely.geometry import Polygon
import rasterio

def guardarRasterComoTif (raster: xr.DataArray, direccion_salida: str) -> None:
    raster = raster.load()

    if len(raster.shape) == 2:
        count = 1
        height = raster.shape[0]
        width = raster.shape[1]
        band_indicies = 1
    else:
        count = raster.shape[0]
        height = raster.shape[1]
        width = raster.shape[2]
        band_indicies = np.arange(count) + 1

    processed_attrs = {}

    try:
        val = raster.rio.transform().to_gdal()
        processed_attrs['transform'] = rasterio.Affine.from_gdal(*val)
    except KeyError:
        pass

    try:
        processed_attrs['crs'] = rasterio.crs.CRS.from_string("EPSG:4326")
    except KeyError:
        pass

    with rasterio.open(direccion_salida, 'w',
                       driver='GTiff',
                       height=height, width=width,
                       dtype=str(raster.dtype), count=count,
                       **processed_attrs) as dst:
        raster.values[np.isnan(raster.values)] = -32768
        dst.write(raster.values, band_indicies)
        
def guardarRasterComoASC (raster: xr.DataArray, direccion_salida: str) -> None:
    raster = raster.load()

    if len(raster.shape) == 2:
        count = 1
        height = raster.shape[0]
        width = raster.shape[1]
        band_indicies = 1
    else:
        count = raster.shape[0]
        height = raster.shape[1]
        width = raster.shape[2]
        band_indicies = np.arange(count) + 1

    processed_attrs = {}

    try:
        val = raster.rio.transform().to_gdal()
        processed_attrs['transform'] = rasterio.Affine.from_gdal(*val)
    except KeyError:
        pass

    try:
        processed_attrs['crs'] = rasterio.crs.CRS.from_string("EPSG:4326")
    except KeyError:
        pass
    
    with rasterio.open(
        direccion_salida,
        'w',
        driver='AAIGrid',
        height=height,
        width=width,
        count=1,
        dtype=raster.values.dtype,
        crs=processed_attrs['crs'],
        transform=processed_attrs['transform'],
        force_cellsize=True
    ) as dst:
        raster.values[np.isnan(raster.values)] = -32768
        dst.write(raster.values, band_indicies)
        
def delimitarRegionRasters (coordenadas):
    direccion_descarga_rasters = f'{conversor.direccion_entradas_analisis_datos}/variables_climaticas/Rasters_delimitados'
    direccion_rasters_globales = f'{conversor.direccion_entradas_analisis_datos}/variables_climaticas/Rasters_globales'
    lista_rasters_globales = os.listdir(direccion_rasters_globales)
    cant_rasters = len(lista_rasters_globales)
    
    for i, dir_raster_global in enumerate(lista_rasters_globales):
        # Lectura del archivo .tif
        raster_global = rxr.open_rasterio(f"{direccion_rasters_globales}/{dir_raster_global}", masked=True).squeeze()
        print(f'\t-> Delimitando región en archivo {dir_raster_global}')
        
        # Generación de Polígono para la delimitación del raster
        puntos = [Point(longitud, latitud) for longitud, latitud in coordenadas]
        poligono = Polygon(puntos)
        area_delimitada = gpd.GeoDataFrame({'id':[1], 'geometry':[poligono]})
        
        # Recorte del Área delimitada
        raster_delimitado = raster_global.rio.clip(area_delimitada.geometry.apply(mapping),
                                                area_delimitada.crs)
        
        # Guardar Raster como archivo .tif
        nombre_raster = dir_raster_global
        dir_raster_delimitado = f'{direccion_descarga_rasters}/{nombre_raster}'
        
        guardarRasterComoTif(raster_delimitado, dir_raster_delimitado)
        print(f'\t\t-> Raster guardado exitosamente  - Progreso : {i+1}/{cant_rasters}')
        print(f'\t\t-> Polígono de Delimitación : {coordenadas}')
        
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
        '''
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
        '''
        # Evaluar distancia con todos los puntos
        evaluacion_distancias = []
        for coord in coordenadas:
            distancia = distanciaCoordenadas(coord[0], coord[1], latitud, longitud)
            evaluacion_distancias.append(distancia < rango_distancias[0] or distancia > rango_distancias[1])
        
        if any(evaluacion_distancias):
            continue
        
        encontrado = True

    return (latitud, longitud)

def obtenerDataset (nombre_especie):
    # Establecer Conexión con la Base de Datos
    res_conexion = conector.establecerConexionBaseDatos()
    print(res_conexion)

    res_consulta = conector.consultarBaseDatos({'especie_nombre':[f'= \'{nombre_especie}\''], 'especie_ID':[]}, 'Especie')
    print(res_consulta)
    especie = res_consulta['resultado'][0][1]

    # Obtener Lista de Registros para la Especie
    res_consulta = conector.consultarBaseDatos({'registro_especie':[f'= {especie}'], 'registro_latitud':[], 'registro_longitud':[]}, 'Registro')
    print(res_consulta['estado'])

    # Almacenar los datos en GeoDataFrame
    datos = {'CLASS':[], 'lon':[], 'lat':[], 'geometry':[]}
    for registro in res_consulta['resultado']:
        datos['CLASS'].append(1)
        datos['lat'].append(float(registro[1]))
        datos['lon'].append(float(registro[2]))
        datos['geometry'].append(shapely.geometry.point.Point(registro[2], registro[1]))

    # Generación de un Perímetro de Selección
    perimetro_seleccion = ((min(datos['lat']), max(datos['lat'])), (min(datos['lon']), max(datos['lon'])))
    print(f'{perimetro_seleccion}')

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
        datos['geometry'].append(shapely.geometry.point.Point(coordenadas[1], coordenadas[0]))
        print(f"Coordenadas cargadas {i}/{cantidad_ausencias}")
        
    return datos, perimetro_seleccion

def generarRegionRasters (perimetro_seleccion):
    min_lat, max_lat = perimetro_seleccion[0]
    min_lon, max_lon = perimetro_seleccion[1]

    poligono = [(max_lon, min_lat),
        (min_lon, min_lat),
        (min_lon, max_lat),
        (max_lon, max_lat),]

    delimitarRegionRasters(poligono)
    
def obtenerDatosAleatorios (datos):
    # Ordenar Aleatoriamento los datos
    datos_aleatorios = list(zip(datos['CLASS'], datos['lat'], datos['lon'], datos['geometry']))
    random.shuffle(datos_aleatorios)

    # Reincorporar datos al diccionario
    datos = {'CLASS':[], 'lon':[], 'lat':[], 'geometry':[]}
    for muestra in datos_aleatorios:
        datos['CLASS'].append(muestra[0])
        datos['lat'].append(muestra[1])
        datos['lon'].append(muestra[2])
        datos['geometry'].append(muestra[3])
        
    dataset = gpd.GeoDataFrame(datos, crs='epsg:4326')

    print(dataset)

    print("number of duplicates: ", dataset.duplicated(subset='geometry', keep='first').sum())
    print("number of NA's: ", dataset['geometry'].isna().sum())
    print("Coordinate reference system is: {}".format(dataset.crs))
    print("{} observations with {} columns".format(*dataset.shape))
    
    return dataset
        
def cargarDatosEntrenamiento (dataset):
    direccion_rasters = f'{conversor.direccion_entradas_analisis_datos}/variables_climaticas/Rasters_delimitados/wc2.1_2.5m_bio_*.tif'
    raster_features = sorted(glob.glob(direccion_rasters))
    # check number of features 
    print('\nThere are', len(raster_features), 'raster features.')

    from pyimpute import load_training_vector
    from pyimpute import load_targets
    train_xs, train_y = load_training_vector(dataset, raster_features, response_field='CLASS')
    target_xs, raster_info = load_targets(raster_features)
    print(f'{(train_xs.shape, train_y.shape)}') # check shape, does it match the size above of the observations?
    
    return train_xs, train_y, target_xs, raster_info

# Definir Conjuntos de Entrenamiento y Prueba
def construirConjuntosDatos (train_xs, train_y, proporcion):    
    
    conjunto_datos = {
                        1:
                            {
                                'X':[],
                                'Y':[],
                                'cant': 0
                            },
                        0:
                            {
                                'X': [],
                                'Y': [],
                                'cant': 0
                            },
                    } 
    
    for x, y in zip(train_xs, train_y):
        
        # Limpieza de los datos en caso de existir 0 o None
        if (all(x == 0) or any(x == None)):
            continue
        
        conjunto_datos[y]['X'].append(x)
        conjunto_datos[y]['Y'].append(y)
        conjunto_datos[y]['cant'] += 1
    
    cant_prop_0 = int(conjunto_datos[0]['cant']*proporcion)
    cant_prop_1 = int(conjunto_datos[1]['cant']*proporcion)
    
    train_xs_entrenamiento = conjunto_datos[0]['X'][:cant_prop_0] + conjunto_datos[1]['X'][:cant_prop_1]
    train_y_entrenamiento = conjunto_datos[0]['Y'][:cant_prop_0] + conjunto_datos[1]['Y'][:cant_prop_1]
    train_xs_prueba = conjunto_datos[0]['X'][cant_prop_0:] + conjunto_datos[1]['X'][cant_prop_1:]
    train_y_prueba = conjunto_datos[0]['Y'][cant_prop_0:] + conjunto_datos[1]['Y'][cant_prop_1:]
    
    return train_xs_entrenamiento, train_y_entrenamiento, train_xs_prueba, train_y_prueba

def generarImagenesModelo (train_xs_entrenamiento, train_y_entrenamiento, target_xs, train_xs_prueba, train_y_prueba, raster_info):
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
    from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_curve
    # model fitting and spatial range prediction

    curva_roc = []
    for name, (model) in CLASS_MAP.items():
        # cross validation for accuracy scores (displayed as a percentage)
        k = 5 # k-fold
        kf = model_selection.KFold(n_splits=k, shuffle=True, random_state=0)
        accuracy_scores = model_selection.cross_val_score(model, train_xs_entrenamiento, train_y_entrenamiento, cv=kf, scoring='recall')
        print(name + " %d-fold Cross Validation Accuracy: %0.2f (+/- %0.2f)"
            % (k, accuracy_scores.mean() * 100, accuracy_scores.std() * 200))
        print(accuracy_scores)
        
        # spatial prediction
        model.fit(train_xs_entrenamiento, train_y_entrenamiento)
        impute(target_xs, model, raster_info, outdir=f'{conversor.direccion_salidas_analisis_datos}/Modelo/' + name + '-images',
            class_prob=True, certainty=True)
        
        pred = model.predict(train_xs_prueba)
        cm = confusion_matrix(train_y_prueba,pred)
        print(cm)
        accuracy = accuracy_score(train_y_prueba, pred)
        print ("SCORE:", accuracy)


def obtenerImagenResultado (dataset, perimetro_seleccion):
    # define spatial plotter
    def plotit(datos, title, cmap="Blues"):
        ax = plt.gca()
        
        mapa = rasterio.open(f"{conversor.direccion_entradas_analisis_datos}/variables_climaticas/Rasters_delimitados/wc2.1_2.5m_bio_1.tif").read(1)
        imgplot = ax.imshow(mapa, cmap='Greys', interpolation='nearest', alpha=0.6)   
        
        imgplot = ax.imshow(datos, cmap=cmap, interpolation='nearest', alpha=0.6)    
        
        min_lat, max_lat = perimetro_seleccion[0]
        min_lon, max_lon = perimetro_seleccion[1]
        
        x_prop = datos.shape[1]/(max_lon - min_lon)
        y_prop = datos.shape[0]/(max_lat - min_lat)
        
        x = (dataset[dataset.CLASS == 1]['lon'] - min_lon) * x_prop
        y = datos.shape[0] - (dataset[dataset.CLASS == 1]['lat'] - min_lat) * y_prop
        plt.scatter(x=x, y=y, c='red', s=5)
        
            
        plt.colorbar()
        plt.title(title, fontweight = 'bold')
        
        direccion_imagen = f'{os.path.dirname(os.path.dirname(__file__))}\static\img\modelo.png'
        plt.savefig(direccion_imagen)
        
    distr_rf = rasterio.open(f"{conversor.direccion_salidas_analisis_datos}/Modelo/rf-images/probability_1.tif").read(1)
    distr_et = rasterio.open(f"{conversor.direccion_salidas_analisis_datos}/Modelo/et-images/probability_1.tif").read(1)
    distr_xgb =  rasterio.open(f"{conversor.direccion_salidas_analisis_datos}/Modelo/xgb-images/probability_1.tif").read(1)
    distr_lgbm =  rasterio.open(f"{conversor.direccion_salidas_analisis_datos}/Modelo/lgbm-images/probability_1.tif").read(1)
    distr_averaged = (distr_rf + distr_et + distr_xgb + distr_lgbm)/4

    plotit(distr_averaged, "Distribución de la Especie", cmap="Greens")

def generarModelo (nombre_especie):
    datos, perimetro_seleccion = obtenerDataset(nombre_especie)
    generarRegionRasters(perimetro_seleccion)
    dataset = obtenerDatosAleatorios(datos)
    train_xs, train_y, target_xs, raster_info = cargarDatosEntrenamiento(dataset)
    train_xs_entrenamiento, train_y_entrenamiento, train_xs_prueba, train_y_prueba = construirConjuntosDatos(train_xs, train_y, 0.8)
    generarImagenesModelo(train_xs_entrenamiento, train_y_entrenamiento, target_xs, train_xs_prueba, train_y_prueba, raster_info)
    obtenerImagenResultado(dataset, perimetro_seleccion)