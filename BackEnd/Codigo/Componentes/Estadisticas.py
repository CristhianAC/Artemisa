'''
|------------------------------------------------------------------------------|
|                                                                              |
|                               Estadísticas                                   |
|                                                                              |
|------------------------------------------------------------------------------|
'''
from .Componente import Componente
from .Constantes import Constantes
from typing import Optional
from numpy import log as ln
from numpy import sqrt
from .Dataset import Dataset

class Estadisticas (Componente):
    
    def obtenerConteoRangoTaxonomico (self, dataset, criterio: Optional[list] = [], rango: Optional[str] = "species", condicionales: Optional[dict] = {}):
        if (type(dataset) == Dataset):
            datos = self.procesos.filtrado.filtrarDataSet({rango: criterio}, dataset, condicionales)
        else:
            datos = [[conteo] for conteo in dataset[rango] if (len(criterio) == 0) or (conteo in criterio)]


        conteo = dict()

        for dato in datos:
            try:
                conteo[dato[0]] += 1
            except:
                try:
                    conteo[dato[0]] = 1
                except:
                    return {}


        return conteo

    def obtenerVariacionesDistribucion (self, categoria):
        pass

    def obtenerProporcionesEspecies (self, dataset):
        conteos_especies = self.obtenerInfoAnual(dataset)
        propocion = dict()

        for year in conteos_especies.keys():
            N = conteos_especies[year]['N']
            propocion[year] = {especie: conteos_especies[year]['Especies'][especie]/N for especie in conteos_especies[year]['Especies'].keys()}
        return propocion

    def obtenerConteoEspeciesEndemicas (self, dataset, criterio: Optional[str] = 'species'):
        datos = self.procesos.estadisticos.obtenerInfoAnual(dataset)
        endemicas_anual = {year: {'species':  self.obtenerConteoRangoTaxonomico(self.procesos.filtrado.especiesEndemicas(dataset, self.procesos.endemicas, condicionales={'year': [year]}), rango=criterio)} for year in datos.keys()}
        for year in endemicas_anual.keys():
            endemicas_anual[year]['S'] = len(endemicas_anual[year]['species'].keys())

        return endemicas_anual

    def obtenerInfoAnual (self, dataset):
        conteos_anuales = self.procesos.estadisticos.obtenerConteoRangoTaxonomico(dataset, rango='year')
        conteos_especies = {year: {} for year in conteos_anuales.keys()}

        for year in conteos_especies.keys():
            conteos_especies[year]['N'] = conteos_anuales[year] #Cantidad de individuos
            conteos_especies[year]['Especies'] = self.procesos.estadisticos.obtenerConteoRangoTaxonomico(dataset, condicionales={'year': [year]})
            conteos_especies[year]['S'] = len(conteos_especies[year]['Especies'].keys())
        
        return conteos_especies

    def obtenerCalculosDiversidad (self, dataset):
        pass

    def obtenerDiversidadAlpha (self, dataset):
        conteos_especies = self.obtenerInfoAnual(dataset)
        diversidad_anual = {year: {} for year in conteos_especies.keys()}
        proporcion = self.obtenerProporcionesEspecies(dataset)

        for year in diversidad_anual.keys():
            S = conteos_especies[year]['S']
            N = conteos_especies[year]['N']
            p_i = proporcion[year]

            diversidad_anual[year]['S'] = S
            diversidad_anual[year]['N'] = N
            diversidad_anual[year][self.IND_SIMPSON] = 1 - sum([(p_i[especie]**2) for especie in conteos_especies[year]['Especies'].keys()])
            diversidad_anual[year][self.IND_MENHINICK] = S/sqrt(N)
            diversidad_anual[year][self.IND_SHANNON] =  -sum([(p_i[especie] * ln(p_i[especie])) for especie in conteos_especies[year]['Especies'].keys()])
            diversidad_anual[year][self.IND_PIELOU] = diversidad_anual[year][self.IND_SHANNON]/ln(S)

        return diversidad_anual 
    
    def obtenerDiversidadBeta (self, dataset):
        conteos_especies = self.obtenerInfoAnual(dataset)
        registros = [year for year in list(conteos_especies.keys())]
        registros.sort()

        diversidad_anual = {year: {} for year in registros[:-1]}
        proporcion = self.obtenerProporcionesEspecies(dataset)

        ult_conteo = conteos_especies[registros[-1]]['Especies']

        for year in registros[:-1]:
            S = conteos_especies[year]['S'] #Cantidad de Especies
            N = conteos_especies[year]['N'] #Cantidad de muestras
            conteos = conteos_especies[year]['Especies'] #Conteo individual de especies

            #Obtener lista de todas la especies registradas en los dos años de referencia
            species = {specie for specie in ult_conteo.keys()}
            species.update({specie for specie in conteos.keys()})

            #Obtener cantidad de conteos en ambas muestras
            muestra_1, muestra_2 = [], []
            for specie in species:
                try:
                    muestra_1.append(ult_conteo[specie])
                except:
                    muestra_1.append(0)

                try:
                    muestra_2.append(conteos[specie])
                except:
                    muestra_2.append(0)

            diversidad_anual[year][self.IND_BRAY_CURTIS] = sum([abs(muestra_1[i] - muestra_2[i]) for i in range(len(species))])/sum([muestra_1[i] + muestra_2[i] for i in range(len(species))])

        return diversidad_anual
    
    def calcularCurvaAcumulacion (self, dataset):
        datos = self.obtenerInfoAnual(dataset)
        registros = list(datos.keys())
        registros.sort()
        muestras_mensuales = { year:
                                { month: self.procesos.estadisticos.obtenerConteoRangoTaxonomico(dataset, condicionales= {'year': [year], 'month': [month+1]}) for month in range(12)}
                            for year in registros
                            }
        self.acum = set()
        conteos_mensuales = { year:
                                { month: {'S': len([specie for specie in muestras_mensuales[year][month].keys()]),
                                          'S_acum': len(self.unionConjuntos({specie for specie in muestras_mensuales[year][month].keys()})),
                                          'N': sum([muestras_mensuales[year][month][specie] for specie in muestras_mensuales[year][month].keys()])} for month in range(12)}
                            for year in registros
                            }
        datos_anuales = { year:
                         {'S': [conteos_mensuales[year][month]['S'] for month in conteos_mensuales[year].keys()],
                          'S_acum': [conteos_mensuales[year][month]['S_acum'] for month in conteos_mensuales[year].keys()],
                          'N': [conteos_mensuales[year][month]['N'] for month in conteos_mensuales[year].keys()]}
                         for year in registros
                        }
        return datos_anuales

    def unionConjuntos(self, set2):
        self.acum = self.acum.union(set2)
        return self.acum 