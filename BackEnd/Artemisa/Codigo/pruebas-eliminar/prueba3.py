import requests

def download_gbif_occurrence_csv(publisher_key, dataset_key):
    # URL base de la API de GBIF
    base_url = 'https://api.gbif.org/v1/'

    # Construye la URL para obtener la descarga de la tabla de ocurrencias del conjunto de datos
    url = f'{base_url}occurrence/download/request'

    # Parámetros de la solicitud
    params = {
        'datasetKey': dataset_key,
        'publishingOrgKey': publisher_key,
        'format': 'SIMPLE_CSV'
    }

    # Realiza la solicitud GET a la API de GBIF para obtener la descarga del archivo CSV
    response = requests.get(url, params=params, stream=True)

    # Verifica el código de estado de la respuesta
    if response.status_code == 200:
        # La solicitud fue exitosa, guarda el archivo CSV en disco
        file_path = f'{dataset_key}.csv'  # Nombre de archivo basado en la clave del conjunto de datos
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        return file_path
    else:
        # La solicitud no fue exitosa, muestra el código de estado y el mensaje de error
        print(f'Error: {response.status_code} - {response.text}')

# Ejemplo de uso
publisher_key = 'dbc2ab56-d499-403c-8db5-c1a49cd0b75f'
dataset_key = '01598aee-87a8-4a95-83ec-263469faaf4d'

csv_file = download_gbif_occurrence_csv(publisher_key, dataset_key)
print(f'Archivo CSV descargado: {csv_file}')