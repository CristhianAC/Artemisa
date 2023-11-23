from abc import ABC
import os

class VariablesFuncionamiento (ABC):

    def __init__ (self):
 
        #Variables de control de errores
        self.exito = 'EXITO'
        self.error = 'ERROR'

        #Variables de Validación de Usuario de GBIF
        self.GBIF_USER = 'artemisapc01'
        self.GBIF_PWD = 'Artemisa1945'
        self.GBIF_EMAIL = 'artemisapc01@gmail.com'

        #Variables de Validación de Usuario para MySQL
        self.SQL_HOST = ''
        self.SQL_USER = 'artemisa'
        self.SQL_PWD = 'Datachallenge2023'

        self.CLAVE_SERVIDOR_SQL = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:artemisa-serv.database.windows.net,1433;Database=Artemisa-Base-Datos;Uid=artemisa;Pwd={Datachallenge2023};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

        #Variables de manejo de direcciones
        self.direccion_carpeta = f'{os.path.dirname(os.path.dirname(__file__))}'
        
        self.direccion_descarga = f"{self.direccion_carpeta}/ExtraccionDatos/Dataset Descargados"
        self.direccion_descompresion = f"{self.direccion_carpeta}/ExtraccionDatos/Dataset Descomprimidos"
        self.direccion_bd_sin_procesar = f'{self.direccion_carpeta}/ConversionDatos/Base de Datos - Sin Procesar'
        self.entradas_extraccion_datos = f'{self.direccion_carpeta}/ExtraccionDatos/Entradas de Capa'
        self.registro_extraccion_datos = f'{self.direccion_carpeta}/ExtraccionDatos/Historial'
        
        self.direccion_datos_globales = f'{self.direccion_carpeta}/DatosGlobales'
        self.direccion_componentes_analisis = f'{self.direccion_carpeta}/ConversionDatos/Componentes'

        self.direccion_entradas_analisis_datos = f'{self.direccion_carpeta}/AnalisisDatos/Entradas_Capa'
        self.direccion_salidas_analisis_datos = f'{self.direccion_carpeta}/AnalisisDatos/Salidas_Capa'


        #Reconocimiento de Errores
        self.error_limitation_exceeded = '''error: A download limitation is exceeded:\nUser artemisapc01 has too many simultaneous downloads; the limit is 3.\nPlease wait for some to complete, or cancel any unwanted downloads.  See your user page.\n, with error status code 420check your number of active downloads.'''
        self.error_not_succeeded =  'download \"_descarga_\" not of status SUCCEEDED'

        # Lista Datasets Cerrejón
        self.direccion_dataset_estudio = f'{self.direccion_carpeta}/ConversionDatos/Componentes/Dataset Estudio'
        self.datasets_estudio = ['5fdcdc28-2a80-4236-a257-866b42ed250c',
                                'edaa3a20-1d73-42ee-85f2-19105c1c8525',
                                'd0a95d44-3622-4c40-bbaf-79a5968c697d',
                                'eaa86a97-f30f-4240-979c-7160052e9327',
                                'd1af197e-f7f5-4ba7-bffb-c11bf9cb6b79',
                                'f1065731-92e2-43fe-b402-ed7736b95c79',
                                '4af23e2d-30ab-4bea-a7a6-bee77285dfc3',
                                'fa5d6d5c-adf3-4395-9ef4-548cb318cc5a',
                                'cf5bf349-8151-4437-9298-8dc285726fb7']

        # Lista Ecosistemas
        self.lista_ecosistemas = {'Ecosistemas Terrestres': {
                                    (190, 203, 121): 'Arbustal andino humedo',
                                    (182, 193, 118): 'Arbustal basal humedo',
                                    (148, 158, 97): 'Arbustal subandino humedo',

                                    (106, 197, 106): 'Bosque andino humedo',
                                    (105, 191, 102): 'Bosque andino seco',
                                    (102, 186, 101): 'Bosque basal humedo',
                                    (101, 185, 100): 'Bosque basal seco',
                                    (99, 182, 97): 'Bosque de galeria basal humedo',
                                    (97, 178, 96): 'Bosque de galeria basal seco',
                                    (84, 141, 82): 'Bosque subandino humedo',
                                    (83, 139, 82): 'Bosque subandino seco',

                                    (192, 122, 108): 'Complejos rocosos de los andes',
                                    (172, 115, 102): 'Complejos rocosos de serranias',
                                    (253, 203, 83): 'Desierto',

                                    (246, 244, 242): 'Glaciares y nivales',

                                    (218, 204, 114): 'Herbazal andino humedo',
                                    (210, 197, 113): 'Herbazal basal humedo',
                                    (165, 157, 100): 'Herbazal subandino humedo',

                                    (169, 76, 193): 'Paramo',
                                    
                                    (252, 229, 90): 'Sabana estacional',

                                    (237, 77, 222): 'Subxerofitia andina',
                                    (224, 153, 224): 'Subxerofitia basal',
                                    (255, 95, 221): 'Subxerofitia subandina',
                                    (239, 138, 223): 'Xerofitia arida',
                                    (252, 142, 235): 'Xerofitia desertica',

                                    (90, 164, 89): 'Bosque fragmentado con pastos y cultivos',
                                    (91, 165, 90): 'Bosque fragmentado con vegetacion secundaria',
                                    (144, 231, 121): 'Vegetacion secundaria',
                                    
                                    (255, 248, 241): 'Agroecosistema arrocero',
                                    (253, 243, 235): 'Agroecosistema cafetero',
                                    (252, 240, 230): 'Agroecosistema cañero',
                                    (248, 233, 220): 'Agroecosistema de cultivos permanentes',
                                    (248, 230, 216): 'Agroecosistema de cultivos transitorios',
                                    (248, 223, 207): 'Agroecosistema de mosaico de cultivos y espacios naturales',
                                    (246, 218, 202): 'Agroecosistema de mosaico de cultivos y pastos',
                                    (253, 215, 197): 'Agroecosistema de mosaico de cultivos, pastos y espacios naturales',
                                    (244, 211, 191): 'Agroecosistema de mosaico de pastos y espacios naturales',
                                    (242, 208, 188): 'Agroecosistema forestal',
                                    (242, 204, 184): 'Agroecosistema ganadero',
                                    (241, 199, 178): 'Agroecosistema palmero',
                                    (241, 197, 175): 'Agroecosistema papero',
                                    (245, 216, 204): 'Agroecosistema platanero y bananero',

                                    (207, 207, 204): 'Otras areas',
                                    (252, 80, 90): 'Territorio artificializado',
                                    (255, 255, 255): 'Sin informacion'},
                                 

                                'Ecosistemas Acuaticos Continentales': {

                                    (167, 179, 108): 'Arbustal inundable andino',
                                    (161, 172, 105): 'Arbustal inundable basal',
                                    (154, 165, 102): 'Arbustal inundable subandino',

                                    (96, 177, 95): 'Bosque de galeria inundable basal',
                                    (90, 160, 89): 'Bosque inundable andino',
                                    (89, 157, 88): 'Bosque inundable basal',
                                    (88, 151, 86): 'Bosque inundable subandino',
                                    (86, 144, 83): 'Bosque ripario inundable subandino',

                                    (159, 182, 201): 'Cuerpo de agua artificia',

                                    (202, 189, 109): 'Herbazal inundable andino',
                                    (192, 182, 108): 'Herbazal inundable basal',
                                    (175, 165, 102): 'Herbazal inundable subandino',

                                    (76, 204, 215): 'Lago Tectonico',
                                    (76, 203, 226): 'Laguna Aluvial',
                                    (129, 221, 223): 'Laguna Glacial',
                                    (105, 214, 228): 'Laguna tectonica',

                                    (76, 156, 215): 'Rio de Aguas Blancas',
                                    (76, 121, 159): 'Rio de Aguas Claras',
                                    (76, 115, 151): 'Rio de Aguas Negras',
                                    (134, 204, 215): 'Sabana inundable',
                                    (76, 144, 163): 'Transicional transformado',
                                    (141, 230, 189): 'Turbera andina',
                                    (141, 230, 211): 'Turbera de paramo',
                                    (116, 142, 186): 'Zona pantanosa andina',
                                    (119, 138, 177): 'Zona pantanosa basal',
                                    (118, 127, 157): 'Zona pantanosa subandina',

                                    (255, 255, 221): 'Zonas arenosas naturales'},
                                

                                'Ecosistemas Costeros': {
                                    (154, 165, 102): 'Arbustal inundable costero',
                                    (102, 199, 101): 'Bosque basal humedo costero',
                                    (95, 172, 94): 'Bosque de galeria inundable costero',
                                    (89, 154, 87): 'Bosque inundable costero',
                                    (86, 147, 83): 'Bosque mixto de guandal',
                                    (184, 172, 105): 'Herbazal inundable costero',

                                    (76, 161, 191): 'Laguna costera',
                                    (175, 233, 223): 'Llanura marea',

                                    (82, 134, 81): 'Manglar',
                                    (82, 133, 81): 'Manglar de aguas marinas',
                                    (81, 129, 80): 'Manglar de aguas mixohalinas',

                                    (121, 144, 158): 'Transicional transformado costero',
                                    (116, 127, 156): 'Zonas pantanosas costeras',
                                    (147, 178, 208): 'Zonas pantanosas salinas',
                                    (255, 255, 197): 'Playas costeras'},


                                'Ecosistemas Insulares': {
                                    (101, 185, 100): 'Bosque basal seco',
                                    (102, 186, 101): 'Bosque basal humedo',
                                    (82, 134, 81): 'Manglar',
                                    (144, 231, 121): 'Vegetacion secundaria',

                                    (248, 233, 220): 'Agroecosistema de cultivos permanentes',
                                    (242, 204, 184): 'Agroecosistema ganadero',

                                    (76, 144, 163): 'Transicional transformado',
                                    (121, 144, 158): 'Transicional transformado costero',

                                    (252, 80, 90): 'Territorio artificializado'},


                                'Ecosistemas Marinos': {
                                    (244, 145, 165): 'Coralino continental',
                                    (161, 176, 248): 'Coralino oceanico',
                                    (242, 231, 112): 'Fondos blandos',
                                    (210, 255, 239): 'Fondos blandos con vegetacion no vascular',
                                    (146, 223, 167): 'Fondos duros con vegetacion no vascular',
                                    (224, 185, 124): 'Fondos duros no coralinos',
                                    (184, 241, 76): 'Pradera de pastos marinos'}
                                }                                  