import requests

def get_gbif_occurrence_records(publisher_key, dataset_key):
    # URL base de la API de GBIF
    base_url = 'https://api.gbif.org/v1/'

    # Construye la URL para obtener los registros de ocurrencias del conjunto de datos
    url = f'{base_url}/occurrence/download/statistics/export'

    # Parámetros de la solicitud
    params = {
        'datasetKey': dataset_key,
        'publishingOrgKey': publisher_key,
        'fromDate': '2019-01',
        'toDate': '2023-06',
        'format': 'CSV'
    }

    # Realiza la solicitud POST a la API de GBIF para solicitar la descarga de los registros
    response = requests.post(url, data=params)

    # Verifica el código de estado de la respuesta
    if response.status_code == 200:
        # La solicitud fue exitosa, devuelve la URL de descarga de los registros
        download_url = response.json()['downloadLink']
        return download_url
    else:
        # La solicitud no fue exitosa, muestra el código de estado y el mensaje de error
        print(f'Error: {response.status_code} - {response.text}')

# Ejemplo de uso
publisher_key = 'dbc2ab56-d499-403c-8db5-c1a49cd0b75f'
dataset_key = '01598aee-87a8-4a95-83ec-263469faaf4d'

download_url = get_gbif_occurrence_records(publisher_key, dataset_key)
print(f'URL de descarga de registros: {download_url}')