import os
import sys
import ast

from .LectorArchivos import LectorArchivos

sys.path.insert(0, f'{os.path.dirname(os.path.dirname(__file__))}')
from ClasesGlobales.VariablesFuncionamiento import VariablesFuncionamiento
from ExtraccionDatos.EnlaceGbif import EnlaceGbif

'''
|====================================================================|
*                       |Análisis Preliminar|         
* Descripción:                                                        
*   Clase encargada de realizar un análisis simple de los dataset
*
*   Su funcionalidad es principalmente para la obtención de 
*   información de los dataset originales para su consulta
*
*   - Los archivos son guardados en la carpeta:
*       -> CapaObtencionDatos/ExtraccionDatos/Entradas de Capa/ListaConsultas.txt
|====================================================================|
'''

class AnalisisPreliminarDatos (VariablesFuncionamiento):

    def __init__ (self):
        super().__init__()
        self.proceso = 'ANALISIS_PRELIMINAR_DE_DATOS'


    #---------------------------|Obtener Especies de un Dataset|---------------------------#
    def obtenerEspeciesDatasets (self, datasets: list) -> dict:
        try:
            lista_especies = []
            for archivo in datasets:
                especies = archivo['species']
                lista_especies += especies

            conjunto_especies = set(lista_especies)
            lista_especies = list(conjunto_especies)
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error, 
                    'seccion': 'Contabilizar Especies en Conjunto',
                    'error': f'{excepcion}'}

        
        return {'proceso': self.proceso,
                'estado': self.exito,
                'resultado busqueda': lista_especies}
    
    #---------------------------|Registrar Especies para Consulta|---------------------------#
    def registrarEspeciesConsultas (self, datasets: list) -> dict:
        res = self.obtenerEspeciesDatasets(datasets)

        if (res['estado'] == self.error):
            return res
        
        lista_especies = res['resultado busqueda']
        direccion_registro = f'{self.entradas_extraccion_datos}/ListaConsultas.txt'
        direccion_registro2 = f'{self.direccion_componentes_analisis}/ListaConsultas.txt'
        
        try:
            archivo = open(direccion_registro, 'w')
            archivo2 = open(direccion_registro2, 'w')

            for especie in lista_especies:
                archivo.write(f'{especie}\n')
                archivo2.write(f'{especie}\n')
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error, 
                    'seccion': 'Escritura de Especies en Archivo de Consultas',
                    'error': f'{excepcion}'}
        
        return {'proceso': self.proceso,
                'estado': self.exito,
                'direccion registro': direccion_registro}
    
    #---------------------------|Obtener Información Climática (1980-2023)|---------------------------#
    # Entrega la información a manera una lista de diccionarios [{'coords' : ((rang_lat), (rang_long)), 'temp': [], 'precipitacion': [], 'mes': [(mes, año)]}]
    def obtenerInfoClimaticaEspecifica (self,archivo_temp_max, archivo_temp_min, archivo_prec) -> dict:
        try:
            registros = {'temperatura_max': 0, 'temperatura_min': 0, 'precipitacion': 0}
            for archivo, medicion in [(archivo_temp_max, 'temperatura_max'), (archivo_temp_min, 'temperatura_min'), (archivo_prec, 'precipitacion')]:
                n, m = 39, 24
                meses = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                registro_mensual = {f'{ano}': {mes: {'datos':[[0 for j in range(m)] for k in range(n)], 'contador': 0} for mes in meses} for ano in range(1980, 2024)}
                mes = ''

                print(f'Tam del archivo de {medicion} : {len(archivo)}')

                for i, linea in enumerate(archivo):
                    #Leer Fechas de cada Registro
                    if i%(n+1) == 0:

                        #Obtener Fecha del Registro
                        fecha = [dato for dato in linea.split('\t')[0].split(" ") if dato != '']

                        if (mes != fecha[1] and mes != ''):
                            print(f'Sacando {medicion} Promedio del Mes {mes}/{ano}')
                            for j in range(m):
                                for k in range(n):
                                    registro_mensual[ano][mes]['datos'][k][j] = registro_mensual[ano][mes]['datos'][k][j]/registro_mensual[ano][mes]['contador']
                        
                        mes = fecha[1]
                        ano = fecha[2]
                        registro_mensual[ano][mes]['contador'] += 1
                    else:
                        for j, dato in enumerate(linea.split('\t')[1:]):
                            k = i%n
                            registro_mensual[ano][mes]['datos'][k][j] += float(dato)
                    
                    registros[medicion] = registro_mensual
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error, 
                    'seccion': 'Obtener Informacion Climática Mensual entre (1980-2023)',
                    'error': f'{excepcion}'}
        

        try:
            lista_regiones = []

            for j in range(m):
                for k in range(n):
                    longitud = -80 + (j * 0.625)
                    latitud = -5 + (k * 0.5)
                    coordenadas = ((longitud + 0.3125, longitud - 0.3125), (latitud + 0.25, latitud - 0.25))
                    region = {'coords' : coordenadas, 'temp_max': [], 'temp_min': [], 'precipitacion': [], 'mes': []}

                    for ano in registros['temperatura_max'].keys():
                        for mes in registros['temperatura_max'][ano].keys():
                            region['temp_max'].append(registros['temperatura_max'][ano][mes]['datos'][k][j])
                            region['temp_min'].append(registros['temperatura_min'][ano][mes]['datos'][k][j])
                            region['precipitacion'].append(registros['precipitacion'][ano][mes]['datos'][k][j] * 10000)
                            region['mes'].append((meses.index(mes) + 1, int(ano)))

                    lista_regiones.append(region)
                            
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error, 
                    'seccion': 'Estandarización de la Informacion Climática Mensual entre (1980-2023)',
                    'error': f'{excepcion}'}

        
        return {'proceso': self.proceso,
                'estado': self.exito,
                'resultado busqueda': lista_regiones}
    
    #---------------------------|Obtener Información Climática Promedio (2000-2009)|---------------------------#
    # Entrega la información a manera una lista de diccionarios [{'coords' : ((rang_lat), (rang_long)), 'temp': [], 'hum': [], 'mes': []}]
    def obtenerInfoClimaticaPromedio (self, archivo) -> dict:
        try:
            forma_estandar = ast.literal_eval(archivo)
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error, 
                    'seccion': 'Conversión de los Datos a una forma estandarizada',
                    'error': f'{excepcion}'}


        try:
            InfoClimatica = []
            for datos in forma_estandar:
                longitud = datos['location']['coords'][0]
                latitud = datos['location']['coords'][1]
                coordenadas = ((longitud + 0.25, longitud - 0.25), (latitud + 0.25, latitud - 0.25))

                dato = {'coords': coordenadas, 'temp': datos['temp'][0], 'hum': datos['rh'][0], 'mes': [i for i in range(1, len(datos['temp'][0]) + 1)]}
                InfoClimatica.append(dato)
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error, 
                    'seccion': 'Obtener Informacion Climática Promedio entre (2000-2009)',
                    'error': f'{excepcion}'}

        
        return {'proceso': self.proceso,
                'estado': self.exito,
                'resultado busqueda': InfoClimatica}

    #---------------------------|Obtener Información de Ecosistemas|---------------------------#
    def obtenerInfoEcosistemas (self) -> dict:
        try:
            lista_ecosistemas = []
            for tipo_ecosistema in self.lista_ecosistemas.keys():
                for ecosistema in self.lista_ecosistemas[tipo_ecosistema].values():
                    lista_ecosistemas.append({'ecosistema_nombre' : ecosistema, 'ecosistema_tipo' : tipo_ecosistema})
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error, 
                    'seccion': 'Contabilizar Ecosistemas en Colombia',
                    'error': f'{excepcion}'}

        
        return {'proceso': self.proceso,
                'estado': self.exito,
                'resultado busqueda': lista_ecosistemas}
        
    #---------------------------|Obtener Nombres de Especies Endemicas|---------------------------#
    def obtenerEspeciesEndemicas (self, lector_archivos: LectorArchivos) -> dict:
        conjunto_especies = set()

        lista_archivos = [(f'\Endemicas\points_data', ',', 2),
                          (f'\Endemicas\Aves_Endemicas', '\t', 2),
                          (f'\Endemicas\Plantas_Endemicas', '\t', 3)]
        
        for archivo, separador, pos in lista_archivos:
            res_lectura = lector_archivos.leerArchivoComoCadena(archivo, 'csv', True)
            
            if (res_lectura['estado'] == self.error):
                return res_lectura
            
            lista_especies_endemicas = res_lectura['datos archivo']
            for especie_endemica in lista_especies_endemicas:
                datos_especie = especie_endemica.split(separador)
                
                if (len(datos_especie) > pos):
                    nombre_cientifico = datos_especie[pos]
                    conjunto_especies.add(nombre_cientifico)
        
        lista_especies = list(conjunto_especies)
        
        return {'proceso': self.proceso,
                'estado': self.exito,
                'resultado': lista_especies}
    
    #---------------------------|Obtener Nombres y Categorias de Especies en Peligro|---------------------------#
    def obtenerEspeciesCategoriasPeligro (self, lector_archivos: LectorArchivos) -> dict:
        conjunto_especies = set()

        lista_archivos = [f'/Nivel Peligro/MAMMALS/MAMMALS',
                          f'/Nivel Peligro/PLANTS/PLANTS_PART1',
                          f'/Nivel Peligro/PLANTS/PLANTS_PART2',
                          f'/Nivel Peligro/AMPHIBIANS/AMPHIBIANS',
                          f'/Nivel Peligro/REPTILES/REPTILES_PART1',
                          f'/Nivel Peligro/REPTILES/REPTILES_PART2']
        
        for archivo in lista_archivos:
            res_lectura = lector_archivos.leerDocumentoSHP(archivo, True)
            
            if (res_lectura['estado'] == self.error):
                return res_lectura
            
            lista_especies_peligro = res_lectura['datos archivo']
            for especie_peligro in lista_especies_peligro:
                conjunto_especies.add(especie_peligro)

            print(f'\t-> Finalizada la carga del dataset {archivo}')
        lista_especies = list(conjunto_especies)
        
        return {'proceso': self.proceso,
                'estado': self.exito,
                'resultado': lista_especies}
    
    #---------------------------|Obtener Llaves de Especies|---------------------------#
    def obtenerLlavesEspecies (self, lista_especies: str, enlaceGBIF: EnlaceGbif) -> dict:
        try:
            conjunto_claves_especies = set()
            
            cant_claves = len(lista_especies)
            cant_errores = 0
            for i, especie in enumerate(lista_especies):
                res_consulta = enlaceGBIF.consultarCodigoEspecie(especie)
                
                if (res_consulta['estado'] == self.error):
                    cant_errores += 1
                    continue
                
                clave_especie = res_consulta['resultados']
                conjunto_claves_especies.add(clave_especie)
                print(f'\t-> Progreso : {i}/{cant_claves} | Insertados {i - cant_errores}/{cant_claves}')
                
                lista_claves_especies = list(conjunto_claves_especies)
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error, 
                    'seccion': 'Contabilizar Ecosistemas en Colombia',
                    'error': f'{excepcion}'}

        
        return {'proceso': self.proceso,
                'estado': self.exito,
                'resultado': lista_claves_especies}
    
    #---------------------------|Obtener Llaves de Especies y Categoria|---------------------------#
    def obtenerLlavesEspeciesPeligro (self, lista_especies: list, enlaceGBIF: EnlaceGbif) -> dict:
        try:
            conjunto_claves_especies = set()
            
            cant_claves = len(lista_especies)
            cant_errores = 0
            for i, categoria, especie in enumerate(lista_especies):
                res_consulta = enlaceGBIF.consultarCodigoEspecie(especie)
                
                if (res_consulta['estado'] == self.error):
                    cant_errores += 1
                    continue
                
                clave_especie = (res_consulta['resultados'], categoria)
                conjunto_claves_especies.add(clave_especie)
                print(f'\t-> Progreso : {i}/{cant_claves} | Insertados {i - cant_errores}/{cant_claves}')
                
                lista_claves_especies = list(conjunto_claves_especies)
        except Exception as excepcion:
            return {'proceso': self.proceso,
                    'estado': self.error, 
                    'seccion': 'Contabilizar Ecosistemas en Colombia',
                    'error': f'{excepcion}'}

        
        return {'proceso': self.proceso,
                'estado': self.exito,
                'resultado': lista_claves_especies}