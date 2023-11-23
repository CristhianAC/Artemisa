from zipfile import ZipFile
import os

import sys
sys.path.insert(0, f'{os.path.dirname(os.path.dirname(__file__))}')
from ClasesGlobales.VariablesFuncionamiento import VariablesFuncionamiento

'''
|====================================================================|
*                    |Descompresor de Archivos|         
* Descripción:                                                        
*   Clase encargada de la descompresión de los archivos descargados
*   desde la API para Python de GBIF
*   
*   - Recibe archivos en formato .zip
*   - Los archivos son guardados en la carpeta:
*       -> CapaObtencionDatos/ExtraccionDatos/Dataset Descomprimidos
|====================================================================|
'''

class Descompresor (VariablesFuncionamiento):

    def __init__ (self):
        super().__init__()
        self.proceso = 'DESCOMPRESION_ARCHIVO'

    #------------------------|Descomprimir Archivo|------------------------#
    def descomprimirArchivo (self, nombre_archivo) -> dict:

        try:
            direccion_archivo = f"{self.direccion_descarga}/{nombre_archivo}"
            with ZipFile(direccion_archivo, 'r') as zip:
                zip.printdir()
                zip.extractall(self.direccion_descompresion)
            direccion_dataset = f"{self.direccion_descompresion}/{nombre_archivo}"
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error, 
                    'seccion': 'Descompresión de archivo .zip',
                    'error': f'{excepcion}'}
        
        try:
            os.remove(direccion_archivo)
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error, 
                    'seccion': 'Eliminación de archivo .zip',
                    'error': f'{excepcion}'}
        
        return {'proceso': self.proceso,
                'estado': self.exito,
                'direccion_archivo': direccion_dataset}