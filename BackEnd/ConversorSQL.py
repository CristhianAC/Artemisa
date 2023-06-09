import sqlite3, os
import pandas as pd
import geopandas as gpd
from Codigo.Componentes.Dataset import Dataset

class ConversorSQL:

    def __init__ (self, dir):
        self.dir_carpeta = dir
        
    def cargarDatasets (self):
        lista_archivos = os.listdir(self.dir_carpeta + "/Datasets")
        bases_datos = []

        lista_indices = ["data_index INTEGER PRIMARY KEY",
                        "gbifID INTEGER",
                        "datasetKey TEXT" ,
                        "occurrenceID TEXT" ,
                        "kingdom TEXT" ,
                        "phylum TEXT" ,
                        "class TEXT" ,
                        "orden TEXT" ,
                        "family TEXT" ,
                        "genus TEXT" ,
                        "species TEXT" ,
                        "infraspecificEpithet TEXT",
                        "taxonRank TEXT" ,
                        "scientificName TEXT" ,
                        "verbatimScientificName TEXT" ,
                        "verbatimScientificNameAuthorship TEXT" ,
                        "countryCode TEXT",
                        "locality TEXT" ,
                        "stateProvince TEXT" ,
                        "occurrenceStatus TEXT" ,
                        "individualCount TEXT",
                        "publishingOrgKey TEXT",
                        "decimalLatitude INTEGER",
                        "decimalLongitude INTEGER", 
                        "coordinateUncertaintyInMeters INTEGER",
                        "coordinatePrecision INTEGER",
                        "elevation INTEGER",
                        "elevationAccuracy INTEGER",
                        "depth INTEGER",
                        "depthAccuracy INTEGER",
                        "eventDate TEXT" ,
                        "day INTEGER",
                        "month INTEGER",
                        "year INTEGER",
                        "taxonKey INTEGER",	
                        "speciesKey INTEGER",
                        "basisOfRecord TEXT" ,
                        "institutionCode TEXT" ,
                        "collectionCode TEXT",
                        "catalogNumber TEXT",
                        "recordNumber TEXT",
                        "identifiedBy TEXT",
                        "dateIdentified TEXT",
                        "license TEXT" ,
                        "rightsHolder TEXT",
                        "recordedBy TEXT",
                        "typeStatus TEXT",
                        "establishmentMeans TEXT",
                        "lastInterpreted TEXT",
                        "mediaType TEXT",
                        "issue TEXT"]
                
        for nombre_archivo in lista_archivos:
            nombre_bd = f"Muestra-{len(bases_datos)+1}.bd"
            nombre_tabla = f"Muestra_{len(bases_datos)+1}"
            conn = self.convertirCSVaSQL(nombre_bd, self.dir_carpeta + "/Datasets/" + nombre_archivo, nombre_tabla, lista_indices)
            nuevo_bd = Dataset(conn, nombre_bd, nombre_tabla)

            bases_datos.append(nuevo_bd)

        return bases_datos

    def generarSQL (self, df, nombre, lista_indices, nombre_tabla):
        # Connect to SQL Server
        conn = sqlite3.connect(self.dir_carpeta + "/BaseDatos/" + nombre, check_same_thread=False)
        cursor = conn.cursor()

        # Crear Tabla
        try:
            indices = ""
            texto_indices = ""
            cant_indices = ""
            for indice in lista_indices:
                texto_indices += f"{indice}, "
                ind = indice.split(" ")[0]
                indices += f"{ind}, "
                cant_indices += "?,"

            cursor.execute(f'''
                    CREATE TABLE {nombre_tabla} (
                        {texto_indices[:-2]})
                        ''')

            # Insert DataFrame to Table
            for row in df.itertuples(index=True, name=None):
                cursor.execute(f'''
                            INSERT INTO {nombre_tabla} ({indices[:-2]})
                            VALUES ({cant_indices[:-1]})
                            ''',
                            row
                            )
            conn.commit()
        except Exception as e:
            print(f"Tabla {nombre_tabla} ya existente")
            print(f"An exception occurred: {str(e)}")

        print(f"\t-> Cargada Tabla \'{nombre_tabla}\'")
        return conn
    
    def convertirCSVaSQL (self, nombre, archivo, nombre_tabla, lista_indices):
        data = pd.read_csv (archivo, header=0, sep='\t')   
        df = pd.DataFrame(data)

        return self.generarSQL (df, nombre, lista_indices, nombre_tabla)

    def cargarEspeciesEndemicas (self):
        lista_archivos = os.listdir(self.dir_carpeta + "/EspeciesEndemicas")
        bases_datos = []

        lista_indices = {lista_archivos[0]: [
                         'datos_ind INT PRIMARY KEY',
                         'species TEXT', 
                         'Nombre_Esp TEXT', 
                         'Nombre_Ing TEXT', 
                         'Cat TEXT', 
                         'Paises TEXT', 
                         'Region TEXT',
                         'Fuente TEXT'
                        ],

                        lista_archivos[1]: [
                         'datos_ind INTEGER PRIMARY KEY',
                         'N INTEGER',
                         'Familia TEXT', 
                         'Genero TEXT', 
                         'species TEXT', 
                         'Autor TEXT', 
                         'Sinonimos TEXT', 
                         'Referencias TEXT',
                         'Taxones_infraespeceficos TEXT', 
                         'Habito TEXT', 
                         'Origen TEXT',
                         'Cat TEXT', 
                         'Especimen_Representativo TEXT', 
                         'Notas TEXT',
                         'Regiones_Biogeograficas TEXT', 
                         'Elevacion_Minima INTEGER', 
                         'Elevacion_Maxima INTEGER',
                         'Departamentos TEXT', 
                         'Distribucion_global TEXT']}
                
        for nombre_archivo in lista_archivos:
            nombre_bd = f"EspEnd-{len(bases_datos)+1}.bd"
            nombre_tabla = f"EspEnd_{len(bases_datos)+1}"
            conn = self.convertirCSVaSQL(nombre_bd, self.dir_carpeta + "/EspeciesEndemicas/" + nombre_archivo, nombre_tabla, lista_indices[nombre_archivo])
            nuevo_bd = Dataset(conn, nombre_bd, nombre_tabla)

            bases_datos.append(nuevo_bd)

        return bases_datos
    
    def cargarPeligroExtincion (self):
        lista_archivos = os.listdir(self.dir_carpeta + "/PeligroExtincion")
        bases_datos = []

        lista_indices = ['datos_ind INTEGER PRIMARY KEY',
                         'id_no INTEGER', 
                         'specie TEXT', 
                         'presence TEXT', 
                         'origin TEXT', 
                         'seasonal TEXT', 
                         'compiler TEXT',
                         'yrcompiled TEXT', 
                         'citation TEXT', 
                         'subspecies TEXT', 
                         'subpop TEXT', 
                         'source TEXT', 
                         'island TEXT',
                         'tax_comm TEXT', 
                         'dist_comm TEXT', 
                         'generalisd TEXT', 
                         'legend TEXT', 
                         'kingdom TEXT', 
                         'phylum TEXT',
                         'class TEXT', 
                         'order_ TEXT', 
                         'family TEXT', 
                         'genus TEXT', 
                         'category TEXT', 
                         'marine TEXT',
                         'terrestial TEXT', 
                         'freshwater TEXT', 
                         'SHAPE_Leng TEXT', 
                         'SHAPE_Area TEXT', 
                        ]
                
        for nombre_archivo in lista_archivos:
            if (nombre_archivo.split(".")[1] == "shp"):
                archivo_shp = gpd.read_file(self.dir_carpeta + "/PeligroExtincion/" + nombre_archivo)
                archivo_shp.drop(columns=["geometry"], inplace=True)
                print(archivo_shp)

                nombre_bd = f"EspExt-{len(bases_datos)+1}.bd"
                nombre_tabla = f"EspExt_{len(bases_datos)+1}"
                conn = self.generarSQL(archivo_shp, nombre_bd, lista_indices, nombre_archivo.split(".")[0])
                nuevo_bd = Dataset(conn, nombre_bd, nombre_tabla)

                bases_datos.append(nuevo_bd)

        return bases_datos