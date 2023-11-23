import os
import pandas as pd
import numpy as np

import sys
sys.path.insert(0, f'{os.path.dirname(os.path.dirname(__file__))}')
from ClasesGlobales.VariablesFuncionamiento import VariablesFuncionamiento
from ClasesGlobales.ConectorBaseDatos import ConectorBaseDatos

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

class AnalisisDatos (VariablesFuncionamiento):

    def __init__ (self):
        super().__init__()

        self.conector_bd = ConectorBaseDatos()

        self.proceso = 'ANALISIS_CONTEO_DATOS'

    #---------------------------|Contabilizar Incidencias entre Especies|---------------------------#
    def contabilizarIncidenciasEspecies (self, rango_distancia_incidencia: float, distancia_regiones: float):
        
        # Establecer Conexión con la Base de Datos
        res_conexion = self.conector_bd.establecerConexionBaseDatos()

        if (res_conexion['estado'] == self.error):
            return res_conexion
        
        print("Conexión con Base de Datos Establecida")

        # Obtener Lista de Llaves de Especies
        res_consulta = self.obtenerEspeciesConsulta()

        if (res_consulta['estado'] == self.error):
            return res_consulta

        lista_especies = res_consulta['resultado']
        lista_especies_total = [especie for especie in lista_especies]
        cant_total_especies = len(lista_especies_total)
        
        print("Lista de Especies de Interés Obtenida")

        # Generar DataFrame para almacenar incidencias
        dataframe_vacio = {especie: [0.0 for i in range(len(lista_especies))] for especie in lista_especies}
        incidencias = pd.DataFrame(data=dataframe_vacio,
                                   index=pd.Index(lista_especies),
                                   columns=pd.Index(lista_especies))

        # Recorrer las especies
        especie_objetivo = lista_especies.pop(0)
        while (len(lista_especies) > 0):

            # Obtener lista de registros para la especie objetivo
            res_consulta = self.obtenerRegistrosDeEspecie(especie_objetivo)

            if (res_consulta['estado'] == self.error):
                return res_consulta

            lista_registros_objetivo = res_consulta['resultado']
            cant_registros = len(lista_registros_objetivo)

            print(f"-> Inicio de Conteo para la especie {especie_objetivo}")
            print(f"\t-> Analizando {cant_registros} registros:")
            
            # Generar DataFrame para almacenar incidencias de cada especie
            columnas = ['latitud', 'longitud'] + lista_especies_total
            incidencias_especie = {especie: [0 for i in range(cant_registros)] for especie in columnas}

            # Recorrer todos los registros de la especie objetivo
            for k, registro_objetivo in enumerate(lista_registros_objetivo):

                # Determinar rango de distancias para incidencias con la especie
                latitud = registro_objetivo['registro_latitud']
                longitud = registro_objetivo['registro_longitud']
                coordenadas = (latitud, longitud)
                rango_latitud = (latitud - distancia_regiones, latitud + distancia_regiones)
                rango_longitud = (longitud - distancia_regiones, longitud + distancia_regiones)
                
                incidencias_especie['latitud'][k] = latitud
                incidencias_especie['longitud'][k] = longitud
                
                # Obtener regiones dada un rango de distancias para la especie
                res_consulta = self.obtenerRegiones (rango_latitud, rango_longitud)

                if (res_consulta['estado'] == self.error):
                    return res_consulta
                
                lista_regiones_delimitadas = res_consulta['resultado']
                cant_regiones_delimitadas = len(lista_regiones_delimitadas)
                print(f"\t\t-> Escaneando un total de {cant_regiones_delimitadas} regiones en coordenadas {coordenadas}")
                
                lista_especies_en_region = set()

                # Recorrer la región de conteo para el registro
                for region_delimitada in lista_regiones_delimitadas:

                    # Obtener lista de especies en la región
                    res_consulta = self.obtenerEspeciesEnRadioRegionEspecifica(region_delimitada, coordenadas, rango_distancia_incidencia)

                    if (res_consulta['estado'] == self.error):
                        return res_consulta
                    
                    for especie_en_region in res_consulta['resultado']:
                        lista_especies_en_region.add(especie_en_region)
                
                # Recorrer lista de especie en la region
                lista_especies_en_region = list(lista_especies_en_region)
                cant_especies_en_region = len(lista_especies_en_region)
                print(f"\t\t-> Escaneando un total de {cant_especies_en_region} especies")
                for especie in lista_especies_en_region:
                    incidencias[especie_objetivo][especie] += (1/cant_registros)
                    incidencias_especie[especie][k] = 1
                    
            
            # Guardar progreso
            df_incidencias_especie = pd.DataFrame(data=incidencias_especie,
                                    columns=pd.Index(columnas))
            df_incidencias_especie.to_csv(f'{self.direccion_salidas_analisis_datos}/Lista Incidencias/{especie_objetivo}.csv')
            incidencias.to_csv(f'{self.direccion_salidas_analisis_datos}/Incidencias_Especies.csv')
            cant_especies_contadas = cant_total_especies - len(lista_especies_total)
            print(f'Progreso guardado correctamente - {cant_especies_contadas}/{cant_total_especies}')
            print(df_incidencias_especie)

            # Escoger la siguiente especie objetivo
            especie_objetivo = lista_especies.pop(0)

        print(incidencias)
    
    #---------------------------|Obtener Especies ya Registradas|---------------------------#
    def obtenerEspeciesContadas (self) -> dict:
        try:
            direccion_archivo = f'{self.direccion_salidas_analisis_datos}/especies_contadas.txt'
            archivo = open(direccion_archivo, 'r', encoding='cp932', errors='ignore')

            lista_especies = []
            for linea in archivo.readlines():
                especie = int(linea)
                lista_especies.append(especie)

            archivo.close()
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error, 
                    'seccion': f'Lectura de Archivo de Especies ya Contadas',
                    'error': f'{excepcion}'}

        return {'proceso': self.proceso,
                'estado': self.exito,
                'datos archivo': lista_especies}
    
    #---------------------------|Obtener Identificación Todas las Especies|---------------------------#
    def obtenerEspeciesConsulta (self):
        try:
            res_consulta = self.conector_bd.consultarBaseDatos({'especie_ID': []},
                                                                "Especie")

            if (res_consulta['estado'] == self.error):
                return res_consulta
            
            ID_especies = [especie[0] for especie in res_consulta['resultado']]
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error, 
                    'seccion': f'Obtención de Especies para Consulta de Incidencias',
                    'error': f'{excepcion}'}

        return {'proceso': self.proceso,
                'estado': self.exito,
                'resultado': ID_especies}

    #---------------------------|Obtener Registros de una Especie|---------------------------#
    def obtenerRegistrosDeEspecie (self, especie: int) -> dict:
        try:
            res_consulta = self.conector_bd.consultarBaseDatos({'registro_especie': [f"= {especie}"],
                                                                'registro_latitud': [],
                                                                'registro_longitud': [],
                                                                'registro_ano': []},
                                                                "Registro")

            if (res_consulta['estado'] == self.error):
                return res_consulta
            
            registros = [{'registro_latitud': float(registro[1]),
                          'registro_longitud': float(registro[2]),
                          'registro_ano': registro[3]} 
                          for registro in res_consulta['resultado']]
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error, 
                    'seccion': f'Obtención de Registros para la Especie de ID : {especie}',
                    'error': f'{excepcion}'}

        return {'proceso': self.proceso,
                'estado': self.exito,
                'resultado': registros}

    #---------------------------|Obtener Especies en una RegionEspecífica dado un Radio|---------------------------#
    def obtenerEspeciesEnRadioRegionEspecifica (self, region: int, coords: float, dist: float) -> dict:
        try:
            res_consulta = self.conector_bd.consultarBaseDatos({'registro_especie': [],
                                                                'registro_latitud': [],
                                                                'registro_longitud': [],
                                                                'registro_region_esp': [f' = {region}']},
                                                                "Registro")

            if (res_consulta['estado'] == self.error):
                return res_consulta
            
            registros = list(set([registro[0] for registro in res_consulta['resultado'] 
                                  if self.distanciaCoordenadas(coords[0], coords[1], float(registro[1]), float(registro[2])) <= dist]))
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error, 
                    'seccion': f'Obtención de Especies en la RegionEspecifica de ID : {region}',
                    'error': f'{excepcion}'}

        return {'proceso': self.proceso,
                'estado': self.exito,
                'resultado': registros}

    #---------------------------|Obtener Regiones en un Rango de Coordenadas|---------------------------#
    def obtenerRegiones (self, rango_latitud: tuple, rango_longitud: tuple) -> dict:
        try:
            res_consulta = self.conector_bd.consultarBaseDatos({'region_esp_ID': [],
                                                                'region_esp_latitud_N': [f"> {rango_latitud[0]}"], 
                                                                'region_esp_latitud_S': [f"< {rango_latitud[1]}"], 
                                                                'region_esp_longitud_E': [f"> {rango_longitud[0]}"],
                                                                'region_esp_longitud_O':[f"< {rango_longitud[1]}"]},
                                                                "RegionEspecifica")

            if (res_consulta['estado'] == self.error):
                return res_consulta
            
            ID_regiones = [region[0] for region in res_consulta['resultado']]
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error, 
                    'seccion': f'Obtención de IDs para RegionEspecifica en las coordenadas ({rango_latitud}, {rango_longitud})',
                    'error': f'{excepcion}'}

        return {'proceso': self.proceso,
                'estado': self.exito,
                'resultado': ID_regiones}
        
    #---------------------------|Convertir de coordenadas a metros|---------------------------#
    def distanciaCoordenadas (self, lat1: float, lon1: float, lat2: float, lon2: float): 
        R = 6378.137
        dLat = lat2 * np.pi / 180 - lat1 * np.pi / 180
        dLon = lon2 * np.pi / 180 - lon1 * np.pi / 180
        a = np.sin(dLat/2) * np.sin(dLat/2) + np.cos(lat1 * np.pi / 180) * np.cos(lat2 * np.pi / 180) * np.sin(dLon/2) * np.sin(dLon/2)
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
        d = R * c
        return d * 1000