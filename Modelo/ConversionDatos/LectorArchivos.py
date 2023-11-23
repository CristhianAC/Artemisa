import os
from PIL import Image
Image.MAX_IMAGE_PIXELS = 1199491200

import geopandas as gpd

import sys
sys.path.insert(0, f'{os.path.dirname(os.path.dirname(__file__))}')
from ClasesGlobales.VariablesFuncionamiento import VariablesFuncionamiento

'''
|====================================================================|
*                       |Lector de Archivos|         
* Descripción:                                                        
*   Clase encargada de la lectura de los archivos resultantes del
*   proceso de extracción de datos
*   
*   - Recibe archivos en formato .csv delimitados por "\t"
*   - Los archivos son guardados en la carpeta:
*       -> CapaObtencionDatos/ConversionDatos/Base de Datos - Sin Procesar
|====================================================================|
'''

class LectorArchivos (VariablesFuncionamiento):

    def __init__ (self):
        super().__init__()
        self.proceso = 'LECTURA_ARCHIVO_CSV'

    '''
    //---------------------------------------------------------------------------\\
    //                         |Lectura de Archivos csv|                         \\
    //---------------------------------------------------------------------------\\
    '''

    #---------------------------|Obtener Lista de Datasets Descargados|---------------------------#
    def obtenerListaDatasetsDescargados (self) -> dict:
        try:
            lista_archivos = os.listdir(self.direccion_descompresion)
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error, 
                    'seccion': f'Revisión de Inventario de Datasets',
                    'error': f'{excepcion}'}

        return {'proceso': self.proceso,
                'estado': self.exito,
                'datos archivo': lista_archivos}

    #---------------------------|Leer Grupo de Datasets|---------------------------#
    def leerDatasetsGBIF (self) -> dict:
        res_revision = self.obtenerListaDatasetsDescargados()

        if (res_revision['estado'] == self.error):
            return res_revision
        
        lista_archivos = res_revision['datos archivo']

        datos_archivos = {archivo: self.leerDatasetGBIF(self.direccion_descompresion, archivo) for archivo in lista_archivos}

        return {'proceso': self.proceso,
                'estado': self.exito,
                'datos archivos': datos_archivos}
    
    #---------------------------|Leer Grupo de Datasets para su Estudio|---------------------------#
    def leerDatasetsEstudioGBIF (self) -> dict:
        lista_archivos = os.listdir(self.direccion_dataset_estudio)

        datos_archivos = {archivo: self.leerDatasetGBIF(self.direccion_dataset_estudio, archivo) for archivo in lista_archivos}

        return {'proceso': self.proceso,
                'estado': self.exito,
                'datos archivos': datos_archivos}

    #--------------------------|Leer Dataset Individual|--------------------------#
    def leerDatasetGBIF (self, direccion: str, nombre_archivo:str) -> list:
        try:
            archivo = open(f'{direccion}/{nombre_archivo}', 'r', encoding='cp932', errors='ignore')
            
            columnas = archivo.readline().split("\t")
            columnas[-1] = columnas[-1].replace("\n", "")
            datos_archivo = {columna: [] for columna in columnas}

            for linea in archivo.readlines():
                datos = linea.split("\t")
                datos[-1] = datos[-1].replace("\n", "")

                for dato, columna in zip(datos, columnas):
                    datos_archivo[columna].append(dato)
            
            archivo.close()
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error, 
                    'seccion': f'Lectura de Archivo [{nombre_archivo}]',
                    'error': f'{excepcion}'}

        return {'proceso': self.proceso,
                'estado': self.exito,
                'datos archivo': datos_archivo}
    
    #--------------------------|Leer Archivo Individual|--------------------------#
    def leerArchivoComoCadena (self, nombre_archivo: str, formato: str, separacion: bool) -> dict:
        try:
            texto = ''
            direccion_archivo = f'{self.direccion_componentes_analisis}/{nombre_archivo}.{formato}'
            archivo = open(direccion_archivo, 'r', encoding='cp932', errors='ignore')

            if not(separacion):
                for linea in archivo.readlines():
                    texto += linea
                lista_texto = [texto]
            else:
                lista_texto = [linea.replace('\n', '') for linea in archivo.readlines()]

            archivo.close()
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error, 
                    'seccion': f'Lectura de Archivo [{nombre_archivo}]',
                    'error': f'{excepcion}'}

        return {'proceso': self.proceso,
                'estado': self.exito,
                'datos archivo': lista_texto}

    #--------------------------|Leer Archivo SHP Individual|--------------------------#
    def leerDocumentoSHP (self, nombre_archivo: str, separacion: bool) -> dict:
        try:
            texto = ''
            direccion_archivo = f'{self.direccion_componentes_analisis}/{nombre_archivo}.shp'
            archivo = gpd.read_file(direccion_archivo)
            
            lista_texto = [(archivo['sci_name'][i], archivo['category'][i]) for i in range(len(archivo['sci_name']))]
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error, 
                    'seccion': f'Lectura de Archivo [{nombre_archivo}]',
                    'error': f'{excepcion}'}

        return {'proceso': self.proceso,
                'estado': self.exito,
                'datos archivo': lista_texto}
    
    #--------------------------|Leer Archivo Individual|--------------------------#
    def leerImagen (self, nombre_archivo: str, formato: str) -> dict:
        try:
            direccion_imagen = f'{self.direccion_componentes_analisis}/{nombre_archivo}.{formato}'
            imagen = Image.open(direccion_imagen)
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error, 
                    'seccion': f'Lectura de Imagen [{nombre_archivo}.{formato}]',
                    'error': f'{excepcion}'}

        return {'proceso': self.proceso,
                'estado': self.exito,
                'datos archivo': imagen}