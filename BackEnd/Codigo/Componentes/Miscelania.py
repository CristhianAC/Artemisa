'''
|------------------------------------------------------------------------------|
|                                                                              |
|                                 Miscelania                                   |
|                                                                              |
|------------------------------------------------------------------------------|
'''
from .Componente import Componente

class Miscelania (Componente):
    
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
            comp_registro = registros[-2]
            var_registro_S = registro_anual[comp_registro]['S']
            var_registro_N = registro_anual[comp_registro]['N']
            var_registro_Alfa = registro_anual[comp_registro]['Shannon']
            var_registro_end = endemicas[comp_registro]['S']
                
            return {'seguimiento': [ult_registro, ult_registro_S, ult_registro_N, ult_registro_Alfa, ult_registro_end], 
                    'variacion': [comp_registro, var_registro_S, var_registro_N, var_registro_Alfa, var_registro_end]}
        except:
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

        respuesta = f'''
                    Para una región ubicada en el {dataset.ubicacion}, la empresa Promigas está haciendo labores
                    de restitución del ecosistema, el cual para la última medición realizada en {datos['seguimiento'][0]},
                    fueron recolectadas un total de {datos['seguimiento'][2]} muestras de especies con {datos['seguimiento'][1]}
                    especies registradas, de las cuales, {datos['seguimiento'][4]} son especies endémicas, casi endémicas o amenazadas. 
                    El índice de Shannon de biodiversidad de esta medición apunta a {datos["seguimiento"][3]}
                    '''
        
        try:
            comparativa =   f'''
                            , del periodo anterior de estudio, realizado en el {datos['variacion'][0]}, se pudo obtener
                            un total de {datos['variacion'][2]} muestras de {datos['variacion'][1]} especies, de las cuales, 
                            {datos['variacion'][4]} eran de especies endémicas, casi endémicas o amenazadas, lo que supone 
                            una varición de {datos['variacion'][4] - datos['seguimiento'][4]} especies de este tipo reportadas,
                            '''
            respuesta += comparativa
        except:
            return respuesta

        return respuesta