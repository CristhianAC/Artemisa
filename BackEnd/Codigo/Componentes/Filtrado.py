from typing import Optional
import pandas as pd

class Filtrado:
    
    def especiesEndemicas (self, dataset, dt_endemicos, condicionales: Optional[dict] = {}):
        df_filtrado = pd.DataFrame()

        for dataset_end in dt_endemicos:
            df1 = pd.read_sql(self.generarCriterioBusqueda(dataset.nombre_tabla, {'*': []}, condicionales), con=dataset.base_datos)
            df2 = pd.read_sql(self.generarCriterioBusqueda(dataset_end.nombre_tabla, {'species':[], 'Cat':[]}, {}), con=dataset_end.base_datos)

            df_convergencia = pd.merge(df1, df2, how='inner', on=['species', 'species'])
            df_filtrado = pd.concat([df_filtrado, df_convergencia])

        return df_filtrado

    def filtrarDataSet (self, criterios, dataset, condicionales: Optional[dict] = {}):
        cursor = dataset.base_datos.cursor()
        solicitud = self.generarCriterioBusqueda(dataset.nombre_tabla, criterios, condicionales)

        try:
            print(f"Generando con criterio de búsqueda : {solicitud}")
            return cursor.execute(solicitud).fetchall()
        except:
            print(f"Para el criterio de búsqueda : {solicitud}")
            print(f"\t-> No se encontraron los datos buscados\n retornando lista vacia")
            return [()]
    
    def generarCriterioBusqueda (self, nombre_tabla, criterios, condicionales):
        select = ""
        where = ""
        
        if (len(criterios.keys()) == 0 and len(condicionales.keys()) == 0):
            return f"SELECT * FROM {nombre_tabla}"

        for categoria in criterios.keys():
            select += f"{categoria}, "
            where += self.generarCondiciones(criterios, categoria)

        for condicion in condicionales.keys():
            where += self.generarCondiciones(condicionales, condicion)
        select = select[:-2]

        select = f"SELECT {select}"

        if not (where == ""):
            where = f"WHERE {where[:-4]}"

        print(f"{select} FROM {nombre_tabla} {where}")
        return f"{select} FROM {nombre_tabla} {where}"
    
    def generarCondiciones (self, criterios, categoria):
        if (len(criterios[categoria]) == 0):
            return ""
        
        where = "("
        for condicion in criterios[categoria]:
            where += f" {categoria} = \'{condicion}\' OR"
        where = where[:-2]
        if (len(criterios[categoria]) > 0):
            where += ") AND "

        return where

    def especiesPeligroExtincion (self, dataset, dt_endemicos, condicionales: Optional[dict] = {}):
        df_filtrado = pd.DataFrame()

        for dataset_end in dt_endemicos:
            df1 = pd.read_sql(self.generarCriterioBusqueda(dataset.nombre_tabla, {'*': []}, condicionales), con=dataset.base_datos)
            df2 = pd.read_sql(self.generarCriterioBusqueda(dataset_end.nombre_tabla, {'species':[], 'Cat':[]}, {}), con=dataset_end.base_datos)

            df_convergencia = pd.merge(df1, df2, how='inner', on=['species', 'species'])
            df_filtrado = pd.concat([df_filtrado, df_convergencia])

        return df_filtrado