import time
import sys, os
sys.path.insert(0, f'{os.path.dirname(os.path.dirname(__file__))}')

from ConversionDatos.ConversionDatos import ConversionDatos
from ExtraccionDatos.ExtraccionDatos import ExtraccionDatos
from AnalisisDatos.AnalisisDatos import AnalisisDatos

'''
|====================================================================|
*                       |Gestión Global|         
* Descripción:                                                        
*   Archivo en el que se tiene acceso a todas las clases del programa
*   con el fin de ejecutar procesos conjuntos entre las diferentes
*   capas del sistema
|====================================================================|
'''

extraccion = ExtraccionDatos()
conversor = ConversionDatos()
analizador = AnalisisDatos()

# Descargar todos los Datasets ingresados en las Entradas de la Capa de Extracción de Datos
#   -> Artemisa-2.0/CapaObtencionDatos/ExtraccionDatos/Entradas de Capa/ListaDatasets.txt
#res_descarga = extraccion.descargarListaDatasets()
#print(res_descarga)

'''
 Para encontrar el resultado de cada operación de descarga consultar:
   -> Artemisa-2.0/CapaObtencionDatos/ExtraccionDatos/Historial/Registro_descargas.txt
'''

# Analizar preliminarmente los datasets descargados para registrar las especies
#   -> Artemisa-2.0/CapaObtencionDatos/ExtraccionDatos/Entradas de Capa/ListaConsultas.txt
#res_registro = conversor.registrarEspeciesConsultas()
#print(res_registro)

# Consultar todos los nombres de las especies encontradas en los datasets, los resultados se guardarán en
#   -> Artemisa-2.0/CapaObtencionDatos/ExtraccionDatos/Entradas de Capa/ListaDatasets.txt
#res_consultas = extraccion.registrarDatasetsIncidencias()
#print(res_consultas)

'''
 Para encontrar el resultado de cada operación de descarga consultar:
   -> Artemisa-2.0/CapaObtencionDatos/ExtraccionDatos/Historial/Registro_consultas.txt
'''

# Registrar en la Base de Datos toda la información climática y geográfica de Colombia
# Será almacenada la información de las tablas [RegionGeneral, RegionEspecífica, Ecosistema]
#res_registro = conversor.registrarFactoresAbioticos()
#print(res_registro)

# Registrar en la Base de Datos toda la información biológica para el estudio
# Será almacenada la información de las tablas [Especie, EspecieEndemica, Dataset]
#res_registro = conversor.registrarFactoresBioticos()
#print(res_registro)

# Ingresar en la Base de Datos todas las incidencias de las especies de interés
# Las especies serán relacionadas a su vez con un ecosistema según sus coordenadas
# El origen de los datos es la imagen generada por el IDEAM (revisar referencias) alojada en
#   -> Artemisa-2.0/CapaObtencionDatos/ConversionDatos/Componentes/E_ECCMC_Ver21_100K.png
# A su vez, la información de las especies se encontrará contenida en los dataset alojados en
#   -> Artemisa-2.0/CapaObtencionDatos/ExtraccionDatos/Dataset Descomprimidos
#res_registro = conversor.ingresarRegistrosEspecies()
#print(res_registro)

# Registrar las especies endemicas en la Base de Datos
# Las especies endémicas se encuentran relacionadas a una fila de la tabla Especie
# Los nombres y claves de las especies obtenidos en este proceso se alejarán en
#   -> CapaObtencionDatos\ConversionDatos\Componentes\Codigos_Especies_Endemicas.txt
#   -> CapaObtencionDatos\ConversionDatos\Componentes\Nombres_Especies_Endemicas.txt
# Estos datos fueron extraídos de los registros de IUCN así como documentos
# suministrados por colaboradores de la Universidad del Norte
#res_registro = conversor.registrarEspeciesEndemicas(extraccion.enlazadorGBIF)
#print(res_registro)

# Registrar la categoría de conservación de las especies dentro de la Base de Datos
# Las especies serán almacenadas conforme a la relación con la tabla de Especie
# Los nombres y claves de las especies obtenidos en este proceso se alejarán en
#   -> CapaObtencionDatos\ConversionDatos\Componentes\Codigos_Especies_Peligro.txt
#   -> CapaObtencionDatos\ConversionDatos\Componentes\Nombres_Especies_Peligro.txt
# Estos datos fueron extraídos de los registros de IUCN
#res_registro = conversor.registrarEspeciesCategoriaPeligro(extraccion.enlazadorGBIF)
#print(res_registro) 

# Registro de incidencias de una especie en relación a todas las demás
# Se realizará un conteo de presencia de la especie y bajo un determinado rango, calcular
# una proporción de registros_con_presencia_especie_n / registros_totales_especie
#analizador.contabilizarIncidenciasEspecies(0.1)