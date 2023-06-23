'''
|------------------------------------------------------------------------------|
|                                                                              |
|                                 Miscelania                                   |
|                                                                              |
|------------------------------------------------------------------------------|
'''
from .Componente import Componente
import requests
from PIL import Image
import io
from io import BytesIO
import plotly.graph_objects as go
from flask import Flask, render_template
import base64
import os
app = Flask(__name__)

class Miscelania (Componente):
    
    def __init__(self, procesos, direccion):
        super().__init__(procesos)
        self.direccion = direccion

    def generarResumenRegion (self, dataset):
        registro_anual = self.procesos.estadisticos.obtenerDiversidadAlpha(dataset)
        endemicas = self.procesos.estadisticos.obtenerConteoEspeciesEndemicas(dataset)
        registros = [year for year in registro_anual.keys() if type(year) == int]
        registros.sort()

        #Obtener información del último año de seguimiento
        ult_registro = registros[-1]
        ult_registro_S = registro_anual[ult_registro]['S']
        ult_registro_N = registro_anual[ult_registro]['N']
        ult_registro_Alfa = registro_anual[ult_registro]['Shannon']
        ult_registro_end = endemicas[ult_registro]['S']

        #Obtener información del penúltimo año "útil" de seguimiento
        try:
            if (var_registro_S * 3 >= ult_registro_S and var_registro_end * 3 >= ult_registro_end):
                comp_registro = registros[-2]
                var_registro_S = registro_anual[comp_registro]['S']
                var_registro_N = registro_anual[comp_registro]['N']
                var_registro_Alfa = registro_anual[comp_registro]['Shannon']
                var_registro_end = endemicas[comp_registro]['S']
                
                return {'seguimiento': [ult_registro, ult_registro_S, ult_registro_N, ult_registro_Alfa, ult_registro_end], 
                        'variacion': [comp_registro, var_registro_S, var_registro_N, var_registro_Alfa, var_registro_end]}
        except:
            pass

        print(f"Para el resumen de {dataset.ubicacion} no se pudieron cargar datos históricos")
        return {'seguimiento': [ult_registro, ult_registro_S, ult_registro_N, ult_registro_Alfa, ult_registro_end]}
    
    def generarResumentTextualBreveRegion (self, dataset):
        datos = self.generarResumenRegion(dataset)

        resumen = f'''{dataset.ubicacion} :\n
            Último registro : {datos['seguimiento'][0]}\n\t
            Cantidad de Muestras : {datos['seguimiento'][2]}\n\t
            Cantidad de Especies : {datos['seguimiento'][1]}\n\t
            Índice de Shannon : {datos["seguimiento"][3]}\n\t
            Cantidad de Especies Endémicas : {datos["seguimiento"][4]}'''

        return resumen

    def generarResumenTextualRegion (self, dataset):
        datos = self.generarResumenRegion(dataset)

        try:
            respuesta = f'''
                    Para una región ubicada en el {dataset.ubicacion}, la empresa Promigas está haciendo labores
                    de restitución del ecosistema, el cual para la última medición realizada en {datos['seguimiento'][0]},
                    fueron recolectadas un total de {datos['seguimiento'][2]} muestras de especies con {datos['seguimiento'][1]}
                    especies registradas, de las cuales, {datos['seguimiento'][4]} son especies endémicas, casi endémicas o amenazadas. 
                    El índice de Shannon de biodiversidad de esta medición apunta a {datos["seguimiento"][3]}
                    '''
        
            comparativa =   f'''
                            , del periodo anterior de estudio, realizado en el {datos['variacion'][0]}, se pudo obtener
                            un total de {datos['variacion'][2]} muestras de {datos['variacion'][1]} especies, de las cuales, 
                            {datos['variacion'][4]} eran de especies endémicas, casi endémicas o amenazadas, lo que supone 
                            una varición de {datos['variacion'][4] - datos['seguimiento'][4]} especies de este tipo reportadas,
                            sacame conclusiones al respecto.
                            \n \n Este texto es un resumen general de las caracteristicas y/o atributos de un filtrado de un dataset donde se analizan condiciones biologicas de biodiversidad. Con respecto a esto realiza unas conclusiones en las que predigas especies que se deban cuidar mas , caracteristicas importantes generales, recomendaciones para el cuidado de las especies y caracteristicas importantes estadisticas.
                            
                            '''
            respuesta += comparativa
        except:
            respuesta += " \n \n Este texto es un resumen general de las caracteristicas y/o atributos de un filtrado de un dataset donde se analizan condiciones biologicas de biodiversidad. Con respecto a esto realiza unas conclusiones en las que predigas especies que se deban cuidar mas , caracteristicas importantes generales y recomendaciones para el cuidado de las especies."
            return respuesta

        return respuesta

    @app.route('/')
    def mostrar_imagen_especie_colombia(self, specie, db):
        datos = self.procesos.filtrado.filtrarDataSet({'species': [], 'speciesKey': []}, db)
        llaves = {dato[0]: dato[1] for dato in datos}

        try:
            species_key = llaves[specie]
        except Exception as e:
            print(str(e))
            print("Especie no encontrada")
            return
        url = f"https://api.gbif.org/v1/species/{species_key}/media"
        params = {
            "limit": 1
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            if data['results']:
                image_url = data['results'][0]['identifier']
                response = requests.get(image_url)
                if response.status_code == 200:
                    im = Image.open(BytesIO(response.content))
                    data = io.BytesIO()

                    dir = self.direccion.replace("\\BackEnd", "")
                    try:
                        os.remove(f"{dir}/static/img/solicitud_imagen.png")
                    except:
                        print("Todavia no existe imagen")

                    try:
                        im.save(f"{dir}/static/img/solicitud_imagen.png", "PNG")
                    except Exception as e:
                        print(str(e))
                        print("Error al guardar imagen")

                    return
                    #encoded_img_data = base64.b64encode(data.getvalue())


                    #return render_template("index.html", img_data=encoded_img_data.decode('utf-8'))
                

        print("No se encontró una imagen para esta especie en Colombia.")
