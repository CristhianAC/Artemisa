from .EnlaceGbif import EnlaceGbif
from .Descompresor import Descompresor
import os
import datetime
import time

import sys
sys.path.insert(0, f'{os.path.dirname(os.path.dirname(__file__))}')
from ClasesGlobales.VariablesFuncionamiento import VariablesFuncionamiento

'''
|====================================================================|
*                        |Extracción de Datos|         
* Descripción:                                                        
*   Clase de gestión general encargada de manejar las solicitudes a la
*   capa de Extracción de Datos
*
*   En esta capa se accede a la descarga de los datasets de GBIF en
*   formato .csv
*
*   Se puede solicitar el seguimiento de archivos por parte de la
*   aplicación para su actualización periódica
|====================================================================|
'''

class ExtraccionDatos (VariablesFuncionamiento):

    def __init__(self):
        super().__init__()
        self.enlazadorGBIF = EnlaceGbif()
        self.descompresor = Descompresor()

        self.proceso = 'EXTRACCION_DATOS'
    
    #---------------------------|Verificar Dataset en Memoria|---------------------------#
    def verificarDescargaDataset (self, nombre_archivo) -> dict:
        direccion_archivo = f"{self.direccion_descompresion}/{nombre_archivo}"
        if (os.path.isfile(direccion_archivo)):
            return {'proceso': self.proceso,
                    'estado': self.error, 
                    'seccion': 'Verificación de Archivo en Memoria',
                    'error': f'Archivo ya se encuentra descargado en {direccion_archivo}'}
        
        return {'proceso': self.proceso,
                'estado': self.exito}

    #------------------------------|Descargar Dataset|------------------------------#
    def ejecutarDescargaDataset (self, criterios_busqueda: dict = {}) -> dict:
        res_consulta = self.enlazadorGBIF.buscarInfoDataset(criterios_busqueda)
        
        #En caso de que el canal de descargas esté saturado -> Insistir
        while (res_consulta['estado'] == self.error and res_consulta['error'] == self.error_limitation_exceeded):
            res_consulta = self.enlazadorGBIF.buscarInfoDataset(criterios_busqueda)
            print("...Esperando a que se despeje el canal de descarga")
            time.sleep(20)

        if (res_consulta['estado'] == self.error):
            return res_consulta

        print(f"{res_consulta['proceso']} : {res_consulta['estado']}")

        llave_dataset = res_consulta['resultado búsqueda'][0]
        res_verificacion = self.verificarDescargaDataset(f'{llave_dataset}.csv')

        if (res_verificacion['estado'] == self.error):
            return res_verificacion
        
        print(f"{res_verificacion['proceso']} : {res_verificacion['estado']}")

        res_descarga = self.enlazadorGBIF.descargarDataset(llave_dataset)

        if (res_descarga['estado'] == self.error):
            return res_descarga
        
        print(f"{res_descarga['proceso']} : {res_descarga['estado']}")

        res_descompresion = self.descompresor.descomprimirArchivo(res_descarga['nombre_archivo'])

        if (res_descompresion['estado'] == self.error):
            return res_descompresion

        return {'proceso': self.proceso,
                'estado': self.exito}
    
    #-------------------------|Descargar Lista de Datasets|-------------------------#
    def descargarListaDatasets (self):
        archivo = open(f'{self.entradas_extraccion_datos}/ListaDatasets.txt')
        registro = open(f'{self.registro_extraccion_datos}/Registro_descargas.txt', "w")
        
        for dataset in archivo:
            dataset = dataset.replace('\n', '')
            consulta = {'datasetKey ': dataset}
            res = self.ejecutarDescargaDataset(consulta)
            registro.write(f"\t({datetime.datetime.now()}) -> {res}\n")

        return {'proceso': self.proceso,
                'estado': self.exito,
                'direccion_informe': f'{self.registro_extraccion_datos}/Registro_descargas.txt'}
    
    #------------------------|Buscar Incidencias de Especie|------------------------#
    def registrarDatasetsIncidencias (self) -> dict:
        consultas = open(f'{self.entradas_extraccion_datos}/ListaConsultas.txt')
        archivo = open(f'{self.entradas_extraccion_datos}/ListaDatasets.txt', 'w')
        registro = open(f'{self.registro_extraccion_datos}/Registro_consultas.txt', "w")

        lista_datasets = []
        for consulta in consultas:
            res_consulta = self.enlazadorGBIF.buscarIncidencias(consulta)

            if (res_consulta['estado'] == self.exito):
                lista_datasets += res_consulta['resultados']

            registro.write(f"\t({datetime.datetime.now()}) -> {res_consulta}\n")

        conjunto_datasets = set(lista_datasets)
        lista_datasets = list(conjunto_datasets)
        for dataset in lista_datasets:
            archivo.write(f'{dataset}\n')

        return {'proceso': self.proceso,
                'estado': self.exito,
                'direccion_informe': f'{self.registro_extraccion_datos}/Registro_consultas.txt'}
