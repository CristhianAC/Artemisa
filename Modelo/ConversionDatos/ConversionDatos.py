import os
import numpy as np

from .LectorArchivos import LectorArchivos
from .AnalisisPreliminarDatos import AnalisisPreliminarDatos

import sys
sys.path.insert(0, f'{os.path.dirname(os.path.dirname(__file__))}')
from ClasesGlobales.VariablesFuncionamiento import VariablesFuncionamiento
from ClasesGlobales.ConectorBaseDatos import ConectorBaseDatos
from ExtraccionDatos.EnlaceGbif import EnlaceGbif

'''
|====================================================================|
*                       |Convertidor a SQL|         
* Descripción:                                                        
*   Clase encargada de la lectura de los archivos resultantes del
*   proceso de extracción de datos
*   
*   - Los archivos son guardados en la carpeta:
*       -> CapaObtencionDatos\ExtraccionDatos\Dataset Descargados
|====================================================================|
'''

class ConversionDatos (VariablesFuncionamiento):
    
    def __init__ (self):
        super().__init__()
        self.conector_bd = ConectorBaseDatos()
        self.lector_archivos = LectorArchivos()
        self.analizador = AnalisisPreliminarDatos()

        self.proceso = 'CONVERSION_DATOS_A_SQL'

    #---------------------------|Registrar Especies para Consulta|---------------------------#
    def registrarEspeciesConsultas (self):
        res_lectura = self.lector_archivos.leerDatasetsEstudioGBIF()

        if (res_lectura['estado'] == self.error):
            return res_lectura

        lista_datasets = [res_lectura['datos archivos'][archivo]['datos archivo'] for archivo in res_lectura['datos archivos'].keys()]

        res_analisis = self.analizador.registrarEspeciesConsultas(lista_datasets)

        return res_analisis
    
    #---------------------------|Registrar Especies Endemicas|---------------------------#
    def registrarEspeciesEndemicas (self, enlaceGBIF: EnlaceGbif) -> dict:
        
        # Establecer Conexión con la Base de Datos
        res_conexion = self.conector_bd.establecerConexionBaseDatos()
        
        if (res_conexion['estado'] == self.error):
            return res_conexion
        
        print('-> Conexión con la Base de Datos Establecida')
        
        '''
        # Consultar lista de Especies Endémicas
        res_consulta = self.analizador.obtenerEspeciesEndemicas()
        
        if (res_consulta['estado'] == self.error):
            return res_consulta
        
        print('-> Lista de Especies Endémicas Obtenida')
        lista_especies_endemicas = res_consulta['resultado']
        '''
        
        direccion_archivo = f'/Nombres_Especies_Endemicas'
        res_lectura = self.lector_archivos.leerArchivoComoCadena(direccion_archivo, 'txt', True)
        
        if (res_lectura['estado'] == self.error):
            return res_lectura
        
        print('-> Lista de Especies Endémicas Cargada')
        lista_especies_endemicas = res_lectura['datos archivo']
        
        # Guardar Lista de Nombres de Especies como Archivo
        res_guardado = self.guardarListaEspeciesRegistro('Nombres_Especies_Endemicas', lista_especies_endemicas)
        
        if (res_guardado['estado'] == self.error):
            return res_guardado
        
        print('-> Lista de Especies Endémicas Guardada')
        direccion_guardado = res_guardado['resultado']
        
        # Consultar lista de Claves de Especies Endémicas
        res_consulta = self.analizador.obtenerLlavesEspecies(lista_especies_endemicas, enlaceGBIF)
        
        if (res_consulta['estado'] == self.error):
            return res_consulta
        
        print('-> Lista de Claves de Especies Endémicas Obtenida')
        lista_claves_especies = res_consulta['resultado']
        
        # Guardar Lista de Claves como Archivo
        res_guardado = self.guardarListaEspeciesRegistro('Codigos_Especies_Endemicas', lista_claves_especies)
        
        if (res_guardado['estado'] == self.error):
            return res_guardado
        
        print('-> Lista de Claves de Especies Endémicas Guardada')
        direccion_guardado = res_guardado['resultado']
        
        # Obtener Lista de Claves presentes en la Base de Datos
        res_consulta = self.conector_bd.consultarBaseDatos({'especie_ID': []}, 'Especie')
        
        if (res_consulta['estado'] == self.error):
            return res_consulta
        
        print('-> Lista de Claves de Especies Endémicas en la Base de Datos Obtenida')
        lista_claves_especies_base_datos = [dato[0] for dato in res_consulta['resultado']]
        
        # Cruzar con las Claves de Especies Endémicas disponibles
        lista_claves_especies_presentes = [especie for especie in lista_claves_especies if especie in lista_claves_especies_base_datos]
        print('-> Lista de Claves para insertar Obtenida')
        
        # Insertar todos los datos en la Base de Datos
        cant_claves = len(lista_claves_especies_presentes)
        cant_errores = 0
        for i, especie_endemica in enumerate(lista_claves_especies_presentes):
            res_insertar = self.conector_bd.insertarEspecieEndemica(i, especie_endemica)
            
            if (res_insertar['estado'] == self.error):
                print(res_insertar)
                cant_errores += 1

            print(f'\t-> Progreso : {i}/{cant_claves} | Insertados {i - cant_errores}/{cant_claves}')
        print('-> Datos de Especies Endémicas insertados en Base de Datos')
        return {'proceso': self.proceso,
                'estado': self.exito}
    
    #---------------------------|Registrar Categoría de Peligro Especies|---------------------------#
    def registrarEspeciesCategoriaPeligro (self, enlaceGBIF: EnlaceGbif) -> dict:
        # Establecer Conexión con la Base de Datos
        res_conexion = self.conector_bd.establecerConexionBaseDatos()
        
        if (res_conexion['estado'] == self.error):
            return res_conexion
        
        print('-> Conexión con la Base de Datos Establecida')
        
        # Consultar lista de Especies en Peligro
        res_consulta = self.analizador.obtenerEspeciesCategoriasPeligro(self.lector_archivos)
        
        if (res_consulta['estado'] == self.error):
            return res_consulta
        
        print('-> Lista de Especies en Peligro Obtenida')
        lista_especies_peligro = res_consulta['resultado']

        # Cargar lista de Especies Registrada anteriormente
        '''
        direccion_archivo = f'/Nombres_Especies_Endemicas'
        res_lectura = self.lector_archivos.leerArchivoComoCadena(direccion_archivo, 'txt', True)
        
        if (res_lectura['estado'] == self.error):
            return res_lectura
        
        print('-> Lista de Especies Endémicas Cargada')
        lista_especies_endemicas = res_lectura['datos archivo']
        '''
        
        # Guardar Lista de Nombres de Especies como Archivo
        res_guardado = self.guardarListaEspeciesRegistro('Nombres_Especies_Peligro', lista_especies_peligro)
        
        if (res_guardado['estado'] == self.error):
            return res_guardado
        
        print('-> Lista de Especies Endémicas Guardada')
        direccion_guardado = res_guardado['resultado']
        
        '''# Consultar lista de Claves de Especies Endémicas
        res_consulta = self.analizador.obtenerLlavesEspeciesPeligro(lista_especies_peligro, enlaceGBIF)
        
        if (res_consulta['estado'] == self.error):
            return res_consulta
        
        print('-> Lista de Claves de Especies Endémicas Obtenida')
        lista_claves_especies = res_consulta['resultado']
        
        # Guardar Lista de Claves como Archivo
        res_guardado = self.guardarListaEspeciesRegistro('Codigos_Especies_Endemicas', lista_claves_especies)
        
        if (res_guardado['estado'] == self.error):
            return res_guardado
        
        print('-> Lista de Claves de Especies Endémicas Guardada')
        direccion_guardado = res_guardado['resultado']
        
        # Obtener Lista de Claves presentes en la Base de Datos
        res_consulta = self.conector_bd.consultarBaseDatos({'especie_ID': []}, 'Especie')
        
        if (res_consulta['estado'] == self.error):
            return res_consulta
        
        print('-> Lista de Claves de Especies Endémicas en la Base de Datos Obtenida')
        lista_claves_especies_base_datos = [dato[0] for dato in res_consulta['resultado']]
        
        # Cruzar con las Claves de Especies Endémicas disponibles
        lista_claves_especies_presentes = [especie for especie in lista_claves_especies if especie in lista_claves_especies_base_datos]
        print('-> Lista de Claves para insertar Obtenida')
        
        # Insertar todos los datos en la Base de Datos
        cant_claves = len(lista_claves_especies_presentes)
        cant_errores = 0
        for i, especie_endemica in enumerate(lista_claves_especies_presentes):
            res_insertar = self.conector_bd.insertarEspecieEndemica(i, especie_endemica)
            
            if (res_insertar['estado'] == self.error):
                print(res_insertar)
                cant_errores += 1

            print(f'\t-> Progreso : {i}/{cant_claves} | Insertados {i - cant_errores}/{cant_claves}')
        print('-> Datos de Especies Endémicas insertados en Base de Datos')'''
        return {'proceso': self.proceso,
                'estado': self.exito}
    
    #---------------------------|Registrar Especies Endemicas|---------------------------#
    def guardarListaEspeciesRegistro (self, nombre_archivo: str, lista_especies: list) -> dict:
        try:
            direccion_archivo = f'{self.direccion_componentes_analisis}/{nombre_archivo}.txt'
            archivo = open(direccion_archivo, 'w')
            
            for especie in lista_especies:
                archivo.write(f'{especie}\n')
            
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error, 
                    'seccion': f'Registro de la Lista de Especies en Componentes',
                    'error': f'{excepcion}'}

        return {'proceso': self.proceso,
                'estado': self.exito,
                'resultado': direccion_archivo}
        
    #---------------------------|Registrar Factores Bióticos en Base de Datos|---------------------------#
    # Método de única ejecución : se registran los datos de [Especie, Especie Endemica, Dataset]
    def registrarFactoresBioticos (self):
        
        res_conexion = self.conector_bd.establecerConexionBaseDatos()

        if (res_conexion['estado'] == self.error):
            return res_conexion

        # Registrar Especies para su Análisis en la Base de Datos
        # Para este programa se utilizarán los datos en GBIF del Cerrejón
        res_lectura = self.lector_archivos.leerDatasetsEstudioGBIF()
        
        if (res_lectura['estado'] == self.error):
            return res_lectura
        
        res_consulta = self.lector_archivos.leerArchivoComoCadena('ListaConsultas', 'txt', True)
        
        if (res_consulta['estado'] == self.error):
            return res_consulta
        
        contador = 0
        lista_especies = {especie.replace('\n', ''): False for especie in res_consulta['datos archivo']}

        for dataset in res_lectura['datos archivos'].keys():

            for i, especie in enumerate(res_lectura['datos archivos'][dataset]['datos archivo']['species']):

                if especie != '' and not(lista_especies[especie]):
                    ID = res_lectura['datos archivos'][dataset]['datos archivo']['speciesKey'][i]
                    reino = res_lectura['datos archivos'][dataset]['datos archivo']['kingdom'][i]
                    filo = res_lectura['datos archivos'][dataset]['datos archivo']['phylum'][i]
                    clase = res_lectura['datos archivos'][dataset]['datos archivo']['class'][i]
                    orden = res_lectura['datos archivos'][dataset]['datos archivo']['order'][i]
                    familia = res_lectura['datos archivos'][dataset]['datos archivo']['family'][i]
                    genero = res_lectura['datos archivos'][dataset]['datos archivo']['genus'][i]
                    nombre = especie
                    categoria = ''
                    peligro = ''

                    lista_especies[especie] = True
                    contador += 1

                    res_insercion = self.conector_bd.insertarEspecie(ID=ID,
                                                                    reino=reino,
                                                                    filo=filo,
                                                                    clase=clase,
                                                                    orden=orden,
                                                                    familia=familia,
                                                                    genero=genero,
                                                                    nombre=nombre,
                                                                    categoria=categoria,
                                                                    peligro=peligro)

                    if (res_insercion['estado'] == self.error):
                        return res_insercion
            
            # Registrar Datasets de Estudio
            dataset_ID = res_lectura['datos archivos'][dataset]['datos archivo']['datasetKey'][0]
            dataset_institucion = res_lectura['datos archivos'][dataset]['datos archivo']['institutionCode'][0]
            dataset_cant_registros = i
            res_insercion = self.conector_bd.insertarDataset(ID=dataset_ID,
                                                            institucion=dataset_institucion,
                                                            cant_registros=dataset_cant_registros)
                            
            if (res_insercion['estado'] == self.error):
                        return res_insercion

            print(f'Dataset {dataset_ID} fue insertado exitosamente')
        

        # Guardar información de su estado de conservación


        # Registrar si la Especie es Endémica
        
    #---------------------------|Registrar Factores Abióticos en Base de Datos|---------------------------#
    # Método de única ejecución : se registran los datos de [RegionGeneral, RegionEspecífica, Ecosistema]
    def registrarFactoresAbioticos (self):

        res_conexion = self.conector_bd.establecerConexionBaseDatos()

        if (res_conexion['estado'] == self.error):
            return res_conexion

        # Registrar Mediciones Específicas de Colombia (entre 01/01/1980 - 23/09/2023)
        # Temperatura (K) y Precipitaciones (mm)
        res_archivo_temp_min = self.lector_archivos.leerArchivoComoCadena('Info-Completa(1980-2023)', 'tsv', True)

        if (res_archivo_temp_min['estado'] == self.error):
            return res_archivo_temp_min
        
        res_archivo_temp_max = self.lector_archivos.leerArchivoComoCadena('Info-Completa-Max(1980-2023)', 'tsv', True)
        
        if (res_archivo_temp_max['estado'] == self.error):
            return res_archivo_temp_max
        
        res_archivo_prec = self.lector_archivos.leerArchivoComoCadena('Info-Completa-Prec(1980-2023)', 'tsv', True)

        if (res_archivo_prec['estado'] == self.error):
            return res_archivo_prec

        archivo_temp_max = res_archivo_temp_max['datos archivo']
        archivo_temp_min = res_archivo_temp_min['datos archivo']
        res_archivo_prec = res_archivo_prec['datos archivo']
        res_climatica_esp = self.analizador.obtenerInfoClimaticaEspecifica(archivo_temp_max, archivo_temp_min, res_archivo_prec)

        if (res_climatica_esp['estado'] == self.error):
            return res_climatica_esp
        
        lista_regiones_esp = res_climatica_esp['resultado busqueda']

        contador = 0
        for ID_region, region_esp in enumerate(lista_regiones_esp):
            '''res_insercion = self.conector_bd.insertarRegionEspecifica(ID=ID_region,
                                                   longitud_E=region_esp['coords'][0][0],
                                                   longitud_O=region_esp['coords'][0][1],
                                                   latitud_N=region_esp['coords'][1][0],
                                                   latitud_S=region_esp['coords'][1][1])

            if (res_insercion['estado'] == self.error):
                    return res_insercion'''
            
            for i in range(len(region_esp['temp_max'])):
                res_insercion = self.conector_bd.insertarMedicionEspecifica(ID=contador,
                                                               ano=region_esp['mes'][i][1],
                                                               mes=region_esp['mes'][i][0],
                                                               temperatura_max=region_esp['temp_max'][i],
                                                               temperatura_min=region_esp['temp_min'][i],
                                                               precipitacion=region_esp['precipitacion'][i],
                                                               region=ID_region)
                if (res_insercion['estado'] == self.error):
                    return res_insercion
                
                contador += 1
            print(f'-> Registradas las mediciones de la region {ID_region}')
            self.conector_bd.commitQueryEnBaseDatos()
        
        # Registrar Mediciones Promedio de Colombia (entre 2000 - 2009)
        # Temperatura (C) y Humedad (rh %)
        res_archivo = self.lector_archivos.leerArchivoComoCadena('Info-Promedio(2000-2009)', 'txt', False)

        if (res_archivo['estado'] == self.error):
            return res_archivo

        archivo = res_archivo['datos archivo'][0]
        res_climatica_prom = self.analizador.obtenerInfoClimaticaPromedio(archivo)

        if (res_climatica_prom['estado'] == self.error):
            return res_climatica_prom

        lista_regiones_prom = res_climatica_prom['resultado busqueda']
        print(lista_regiones_prom)

        contador = 0
        for ID_region, region_prom in enumerate(lista_regiones_prom):
            res_insercion = self.conector_bd.insertarRegionGeneral(ID=ID_region,
                                                   longitud_E=region_prom['coords'][0][0],
                                                   longitud_O=region_prom['coords'][0][1],
                                                   latitud_N=region_prom['coords'][1][0],
                                                   latitud_S=region_prom['coords'][1][1])

            if (res_insercion['estado'] == self.error):
                    return res_insercion
            
            for i in range(len(region_prom['temp'])):
                res_insercion = self.conector_bd.insertarMedicionRegionGeneral(ID=contador,
                                                               ano=0,
                                                               mes=region_prom['mes'][i],
                                                               temperatura=region_prom['temp'][i],
                                                               humedad=region_prom['hum'][i],
                                                               region=ID_region)
                if (res_insercion['estado'] == self.error):
                    return res_insercion
                
                contador += 1

        # Registrar Ecosistemas de Colombia
        # Datos extraídos del IDEAM
        contador = 0
        for tipo_ecosistema in self.lista_ecosistemas.keys():
            for ecosistema in self.lista_ecosistemas[tipo_ecosistema].values():
                res_insercion = self.conector_bd.insertarEcosistema(ID=contador,
                                                                    nombre=ecosistema,
                                                                    tipo_ecosistema=tipo_ecosistema)
                
                print(f'Insertado : {ecosistema} | {tipo_ecosistema}')
                contador += 1

                if (res_insercion['estado'] == self.error):
                    return res_insercion

        return {'proceso': self.proceso,
                'estado': self.exito}

    #---------------------------|Obtener ID de Ecosistema|---------------------------#
    def obtenerEcosistema (self, imagen, longitud: float, latitud: float) -> dict:
        try:
            # Obtener ecosistema en la imagen a partir de coordenadas
            x, y = self.convertirCoordenadasAPixeles(longitud, latitud) #Calcular pixeles

            color, tipo_ecosistema = self.obtenerColorTipoEcosistema(imagen, x, y) #Obtener Color y Tipo de Ecosistema

            # Obtener ID del Ecosistema a partir del color encontrado
            nombre_ecosistema = self.lista_ecosistemas[tipo_ecosistema][color]
            res_consulta = self.conector_bd.consultarBaseDatos({'ecosistema_ID': [], 'ecosistema_nombre':[f"= \'{nombre_ecosistema}\'"]}, "Ecosistema")

            if (res_consulta['estado'] == self.error):
                return res_consulta
            
            ecosistema = res_consulta['resultado'][0][0]
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error, 
                    'seccion': f'Obtención de ID para Ecosistema en las coordenadas ({longitud}, {latitud})',
                    'error': f'{excepcion}'}

        return {'proceso': self.proceso,
                'estado': self.exito,
                'resultado': ecosistema}

    #---------------------------|Obtener ID de Region General|---------------------------#
    def obtenerRegionGeneral (self, longitud: float, latitud: float) -> dict:
        try:
            res_consulta = self.conector_bd.consultarBaseDatos({'region_ID': [],
                                                                'region_latitud_N': [f"> {latitud}"], 
                                                                'region_latitud_S': [f"< {latitud}"], 
                                                                'region_longitud_E': [f"> {longitud}"],
                                                                'region_longitud_O':[f"< {longitud}"]},
                                                                "RegionGeneral")

            if (res_consulta['estado'] == self.error):
                return res_consulta
            
            ID_region_general = res_consulta['resultado'][0][0]
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error, 
                    'seccion': f'Obtención de ID para RegionGeneral en las coordenadas ({longitud}, {latitud})',
                    'error': f'{excepcion}'}

        return {'proceso': self.proceso,
                'estado': self.exito,
                'resultado': ID_region_general}

    #---------------------------|Obtener ID de Region Específica|---------------------------#
    def obtenerRegionEspecifica (self, longitud: float, latitud: float) -> dict:
        try:
            res_consulta = self.conector_bd.consultarBaseDatos({'region_esp_ID': [],
                                                                'region_esp_latitud_N': [f"> {latitud}"], 
                                                                'region_esp_latitud_S': [f"< {latitud}"], 
                                                                'region_esp_longitud_E': [f"> {longitud}"],
                                                                'region_esp_longitud_O':[f"< {longitud}"]},
                                                                "RegionEspecifica")

            if (res_consulta['estado'] == self.error):
                return res_consulta
            
            ID_region_especifica = res_consulta['resultado'][0][0]
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error, 
                    'seccion': f'Obtención de ID para RegionEspecifica en las coordenadas ({longitud}, {latitud})',
                    'error': f'{excepcion}'}

        return {'proceso': self.proceso,
                'estado': self.exito,
                'resultado': ID_region_especifica}

    #---------------------------|Ingresar Registros de Especies de Interés en Base de Datos|---------------------------#
    def ingresarRegistrosEspecies (self) -> dict:
        
        print('Ingresando Registros de Especies : ')

        # Establecimiento de Conexión con la Base de Datos
        res_conexion = self.conector_bd.establecerConexionBaseDatos()

        if (res_conexion['estado'] == self.error):
            return res_conexion
        
        print('\t-> Base de Datos Conectada')
        
        # Lectura de la imagen de Ecosistemas
        res_lectura = self.lector_archivos.leerImagen ('E_ECCMC_Ver21_100K' , 'png')

        if (res_lectura['estado'] == self.error):
            return res_lectura
        
        print('\t-> Imagen de Ecosistemas Cargada')

        imagen = res_lectura['datos archivo']

        # Obtener IDs de las Especies de Interés alojados en la Base de Datos
        res_consulta = self.conector_bd.consultarBaseDatos({'especie_ID': []}, "Especie")
        
        if (res_consulta['estado'] == self.error):
            return res_consulta
        
        lista_especies_interes = [especie[0] for especie in res_consulta['resultado']]
        
        print('\t-> Especies de Interés Cargadas')

        # Reconocimiento de Inventario de Datasets 
        res_revision = self.lector_archivos.obtenerListaDatasetsDescargados()

        if (res_revision['estado'] == self.error):
             return res_revision
        
        print('\t-> Lista de Datasets Inventariada')

        lista_archivos = res_revision['datos archivo']
        lista_datasets = set()

        res_consulta = self.obtenerEcosistema(imagen, -73.349567, 7.033435)

        if (res_consulta['estado'] == self.error):
            print(res_consulta)
            
        
        ecosistema = res_consulta['resultado']

        # Lectura de Datasets -> Proceso no se detiene en caso de error
        for archivo in lista_archivos:
            res_lectura = self.lector_archivos.leerDatasetGBIF(self.direccion_descompresion, archivo)

            # No considerar el Archivo por defecto de 'Artemisa.txt'
            if (archivo == 'Artemisa.txt'):
                continue

            if (res_lectura['estado'] == self.error):
                print(res_lectura)
                continue
            
            # Registrar Llave de Dataset en Lista -> Si ya existe se ignora
            llave_dataset = res_lectura['datos archivo']['datasetKey'][0]
            if (llave_dataset in lista_datasets):
                continue

            lista_datasets.add(llave_dataset)

            # Filtrar a únicamente los registros que cuenten información sobre la especie
            lista_especies = [int(especie) for especie in res_lectura['datos archivo']['speciesKey'] if especie != '']

            # Registrar Dataset en la Base de Datos
            
            dataset_ID = res_lectura['datos archivo']['datasetKey'][0]
            dataset_institucion = res_lectura['datos archivo']['institutionCode'][0]
            dataset_cant_registros = len(lista_especies)
            res_insercion = self.conector_bd.insertarDataset(ID=dataset_ID,
                                                            institucion=dataset_institucion,
                                                            cant_registros=dataset_cant_registros)

            if (res_insercion['estado'] == self.error):
                print(f'\t-> Error Registrando Dataset {llave_dataset}')
                continue
            
            print(f'\t-> Inicio de Registros {llave_dataset} :')

            # Revisión de cada registro -> Si es una especie de interés se registra en la Base de Datos
            for i, especie in enumerate(lista_especies):

                # Verificar si la especie es de interés -> Si no lo es se ignora
                if not (especie in lista_especies_interes):
                    continue
                
                # En caso de cualquier error de formato -> Descartar Registro
                try:
                    ID = res_lectura['datos archivo']['occurrenceID'][i]
                    latitud = float(res_lectura['datos archivo']['decimalLatitude'][i])
                    longitud = float(res_lectura['datos archivo']['decimalLongitude'][i])
                    ano = int(res_lectura['datos archivo']['year'][i])
                    mes = int(res_lectura['datos archivo']['month'][i])
                except:
                    continue

                # Obtener Ecosistema del Registro
                res_consulta = self.obtenerEcosistema(imagen, -73.349567, 7.033435)

                if (res_consulta['estado'] == self.error):
                    print(res_consulta)
                    continue
        
                ecosistema = res_consulta['resultado']

                # Obtener RegionEspecífica del Registro
                res_consulta = self.obtenerRegionEspecifica(longitud, latitud)

                if (res_consulta['estado'] == self.error):
                    #print(res_consulta)
                    continue
        
                region_especifica = res_consulta['resultado']

                # Obtener RegionGeneral del Registro
                res_consulta = self.obtenerRegionGeneral(longitud, latitud)

                if (res_consulta['estado'] == self.error):
                    print(res_consulta)
                    region_general = -1
                else: 
                    region_general = res_consulta['resultado']

                #print(f'\t\t-> {ID} | {latitud} | {longitud} | {ano} | {mes} | {ecosistema} | {region_general} | {region_especifica}')

                
                res_insercion = self.conector_bd.insertarRegistro (ID = ID, 
                                                                    latitud = latitud, 
                                                                    longitud = longitud, 
                                                                    ano = ano, 
                                                                    mes = mes, 
                                                                    especie = especie, 
                                                                    ecosistema = ecosistema, 
                                                                    region_general = region_general, 
                                                                    region_especifica = region_especifica, 
                                                                    dataset = llave_dataset)
                                    
                if (res_insercion['estado'] == self.error):
                    print(res_insercion)
                    return res_insercion
                
            self.conector_bd.commitQueryEnBaseDatos()
            print(f'\t-> Dataset {llave_dataset} cargado')

        print(len(lista_datasets))
            


        #print(lista_datasets)


        #res_leer = self.lector_archivos.leerImagen('E_ECCMC_Ver21_100K', 'png')

    #---------------------------|Obtener Color de la Imagen de Ecosistemas|---------------------------#
    def obtenerColorTipoEcosistema (self, imagen, x: int, y: int) -> list:
        precision = 100
        color = imagen.getpixel((x, y))

        #Obtener lista de Colores por Ecosistema
        lista_colores = [[color_ecosistema, tipo_ecosistema] 
                             for tipo_ecosistema in self.lista_ecosistemas.keys() 
                             for color_ecosistema in self.lista_ecosistemas[tipo_ecosistema]]
        
        # Se determinan las distancias con la lista de colores para cada coordenadas
        distancias = [self.distanciaColores(color, color_eco[0]) for color_eco in lista_colores]  #O(4c)
        # Verificar si alguna de las coordenadas cumple el criterio de precisión cada alguno de los colores
        encontrado = any([d < precision for d in distancias])

        if (encontrado):
            # Obtener el color más cercano al de la coordenada
            ind_color = distancias.index(min(distancias))

            # Obtener color y ecosistema
            color, tipo_ecosistema = lista_colores[ind_color]

            return [color, tipo_ecosistema]


        # Si el color es negro se busca el vecino más cercano
        iteraciones = 0
        precision_coordenadas = 10
        coordenadas = [(x, y), (x, y), (x, y), (x, y)]
        while not(encontrado) and iteraciones < precision_coordenadas:
            # Se genera una lista de (4) coordenadas en forma de x
            coordenadas = [(c[0] + (-1)**(int(i/2)+1), c[1] + (-1)**i) for i, c in enumerate(coordenadas)]

            # Se obtienen los colores para cada una
            colores_coord = [imagen.getpixel(c) for c in coordenadas]

            # Se determinan las distancias con la lista de colores para cada coordenadas
            distancias = [[self.distanciaColores(color, color_eco[0]) for color_eco in lista_colores] for color in colores_coord]  #O(4c)

            # Verificar si alguna de las coordenadas cumple el criterio de precisión cada alguno de los colores
            comprobacion = [any([d < precision for d in distancia_color]) for distancia_color in distancias]

            # Si alguna de las coordenadas cumple el criterio se detiene el programa
            encontrado = any(comprobacion)

            # Considerar una precisión conforme a la distancia con el punto original
            iteraciones += 1

        # Obtener el índice de la lista que más se aproxima a la respuesta
        distancia_min_conjuntos = {min(distancia): i for i, distancia in enumerate(distancias)}
        mejor_conjunto = min(list(distancia_min_conjuntos.keys()))

        ind_coordenada = distancia_min_conjuntos[mejor_conjunto]
        distancias_coordenada = distancias[ind_coordenada]

        # Obtener el color más cercano a la coordenada encontrada
        ind_color = distancias_coordenada.index(min(distancias_coordenada))

        # Obtener color y ecosistema
        color, tipo_ecosistema = lista_colores[ind_color]

        return [color, tipo_ecosistema]

    #---------------------------|Obtener Distancia entre 2 Colores|---------------------------#
    def distanciaColores (self, color1, color2) -> list:
        r = (color1[0] + color2[0])/2
        dif_r = color1[0] - color2[0]
        dif_g = color1[1] - color2[1]
        dif_b = color1[2] - color2[2]
        
        dif_c = np.sqrt((2 + r/256) * (dif_r**2) + 4*(dif_g**2) + (2 + (255 - r)/256) * (dif_b**2))
        return dif_c

    #---------------------------|Convertir Coordenadas Geográficas a Pixeles en Imagen|---------------------------#
    def convertirCoordenadasAPixeles (self, longitud: float, latitud: float) -> list:
        x = int(2320 + (abs(-79 - longitud) * 1824))
        y = int(3057 + (abs(13 - latitud) * 1824))
        return (x, y)