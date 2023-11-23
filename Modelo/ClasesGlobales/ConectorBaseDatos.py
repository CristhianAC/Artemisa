import os
import pyodbc
import struct
from azure import identity

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

import sys
sys.path.insert(0, f'{os.path.dirname(os.path.dirname(__file__))}')
from ClasesGlobales.VariablesFuncionamiento import VariablesFuncionamiento

'''
|====================================================================|
*                       |Convertidor a SQL|         
* Descripción:                                                        
*   Clase encargada del establecimiento de la Conexión con la
*   Base de Datos remota del servicio de Microsoft Azure
*   
*   La información de las credenciales y cuentas necesarias para su 
*   funcionamiento se encuentran en la clase VariablesFuncionamiento
|====================================================================|
'''

class ConectorBaseDatos (VariablesFuncionamiento):

    def __init__ (self):
        super().__init__()
        self.proceso = 'CONEXION_BASE_DATOS'
        self.conexion = None

        os.environ["AZURE_SQL_CONNECTIONSTRING"] = self.CLAVE_SERVIDOR_SQL


    #---------------------------|Establecimiento de Conexión|---------------------------#
    def establecerConexionBaseDatos (self):
        try:
            conn = pyodbc.connect(self.CLAVE_SERVIDOR_SQL)
            conexion = conn.cursor()
            self.conexion = conexion
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error,
                    'seccion': f'Establecimiento de Conexión con el Servidor',
                    'error': f'{excepcion}'}

        return {'proceso': self.proceso,
                'estado': self.exito,
                'conexion': conexion}
    
    #---------------------------|Obtención de Consultas a la Base de Datos|---------------------------#
    # La función recibe las consultas en forma de diccionario con la siguiente estructura
    # consulta = {'%nombre_columna%': ["= \'%condicion_1%\'", ... ,"= \'%condicion_n%\'"]} -> En caso de no haber condición dejar lista vacía []
    def consultarBaseDatos (self, consulta: dict, tabla: str) -> dict:
        try:
            lista_columnas = f"{list(consulta.keys())}"[1:-1].replace("\'", "")
            condicionales = [f"{columna} {condicion}".replace("\'", "¡").replace(',', 'ª') for columna in consulta.keys() for condicion in consulta[columna] if len(consulta[columna]) > 0]
            lista_condicionales = f"{condicionales}"[1:-1].replace('\"', "").replace("\'", "").replace("¡", "\'").replace(',', ' and').replace('ª', ',')

            if lista_condicionales != '':
                lista_condicionales = f'WHERE {lista_condicionales}'

            query = f"SELECT {lista_columnas} FROM {tabla} {lista_condicionales}"
            self.conexion.execute(query)
            resultados = self.conexion.fetchall()
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error,
                    'seccion': f'Ejecución de consulta {query} a Tabla {tabla}',
                    'error': f'{excepcion}'}

        return {'proceso': self.proceso,
                'estado': self.exito,
                'resultado': resultados}

    #---------------------------|Commit los Querys en la Base de Datos|---------------------------#
    def commitQueryEnBaseDatos (self):
        try:
            self.conexion.commit()
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error,
                    'seccion': f'Commit de Query en la Base de Datos',
                    'error': f'{excepcion}'}
        
        return {'proceso': self.proceso,
                'estado': self.exito,
                'seccion': f'Commit de Query en la Base de Datos'}

    #---------------------------|Generación y Ejecución Query INSERT|---------------------------#
    def insertarDatoEnTabla (self, tabla: str, datos: list) -> dict:
        try:
            lista_datos = f'{datos}'[1:-1]
            query = f"INSERT INTO [dbo].[{tabla}] Values ({lista_datos});"
            self.conexion.execute(query)
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error,
                    'seccion': f'Ingreso de Datos a la Tabla {tabla} -> {datos}',
                    'error': f'{excepcion}'}
        
        return {'proceso': self.proceso,
                'estado': self.exito,
                'seccion': f'Ingreso de Datos a la Tabla {tabla} -> {datos}'}
    
    #---------------------------|Insertar en Tabla [Especie]|---------------------------#
    def insertarEspecie (self, ID: int, reino: str, filo: str, clase: str, orden: str, familia: str, genero: str, nombre: str, categoria: str, peligro: str) -> dict:
        datos = [ID, reino, filo, clase, orden, familia, genero, nombre, categoria, peligro]
        res_insercion = self.insertarDatoEnTabla('Especie', datos)
        return res_insercion

    #---------------------------|Insertar en Tabla [EspecieEndemica]|---------------------------#
    def insertarEspecieEndemica (self, ID: int, especie_ID: int) -> dict:
        datos = [ID, especie_ID]
        res_insercion = self.insertarDatoEnTabla('EspecieEndemica', datos)
        return res_insercion
    
    #---------------------------|Insertar en Tabla [EspeciePeligro]|---------------------------#
    def insertarEspeciePeligro (self, ID: int, categoria: str, especie_ID: int) -> dict:
        datos = [ID, categoria, especie_ID]
        res_insercion = self.insertarDatoEnTabla('EspeciePeligro', datos)
        return res_insercion
    
    #---------------------------|Insertar en Tabla [Dataset]|---------------------------#
    def insertarDataset (self, ID: str, institucion: str, cant_registros: int) -> dict:
        datos = [ID, institucion, cant_registros]
        res_insercion = self.insertarDatoEnTabla('Dataset', datos)
        return res_insercion
    
    #---------------------------|Insertar en Tabla [Ecosistema]|---------------------------#
    def insertarEcosistema (self, ID: str, nombre: str, tipo_ecosistema: str) -> dict:
        datos = [ID, nombre, tipo_ecosistema]
        res_insercion = self.insertarDatoEnTabla('Ecosistema', datos)
        return res_insercion

    #---------------------------|Insertar en Tabla [RegionGeneral]|---------------------------#
    def insertarRegionGeneral (self, ID: int, longitud_E: float, longitud_O: float, latitud_N: float, latitud_S: float) -> dict:
        datos = [ID, round(latitud_N, 4), round(latitud_S, 4), round(longitud_E, 4), round(longitud_O, 4)]
        res_insercion = self.insertarDatoEnTabla('RegionGeneral', datos)
        return res_insercion

    #---------------------------|Insertar en Tabla [MedicionRegionGeneral]|---------------------------#
    def insertarMedicionRegionGeneral (self, ID: int, ano: int, mes: int, temperatura: float, humedad: float, region: int) -> dict:
        datos = [ID, ano, mes, round(temperatura, 3), round(humedad, 3), region]
        res_insercion = self.insertarDatoEnTabla('MedicionRegionGeneral', datos)
        return res_insercion

    #---------------------------|Insertar en Tabla [RegionEspecifica]|---------------------------#
    def insertarRegionEspecifica (self, ID: int, longitud_E: float, longitud_O: float, latitud_N: float, latitud_S: float) -> dict:
        datos = [ID, round(latitud_N, 4), round(latitud_S, 4), round(longitud_E, 4), round(longitud_O, 4)]
        res_insercion = self.insertarDatoEnTabla('RegionEspecifica', datos)
        return res_insercion
    
    #---------------------------|Insertar en Tabla [MedicionRegionEspecifica]|---------------------------#
    def insertarMedicionEspecifica (self, ID: int, ano: int, mes: int, temperatura_max: float, temperatura_min: float, precipitacion: float, region: int) -> dict:
        datos = [ID, ano, mes, round(temperatura_max, 3), round(temperatura_min, 3), round(precipitacion, 3), region]
        res_insercion = self.insertarDatoEnTabla('MedicionRegionEspecifica', datos)
        return res_insercion
    
    #---------------------------|Insertar en Tabla [Registro]|---------------------------#
    def insertarRegistro (self, ID: int, latitud: float, longitud: float, ano: int, mes: int, especie: str, ecosistema: int, region_general: list, region_especifica: list, dataset: str) -> dict:  
        datos = [ID, latitud, longitud, ano, mes, especie, ecosistema, region_general, region_especifica, dataset]
        res_insercion = self.insertarDatoEnTabla('Registro', datos)
        return res_insercion