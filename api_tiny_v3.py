import requests
import json
import time

def obter_pedidos_v3(ACCESS_TOKEN, PARAMS):
    offset = 0
    total = 100
    lista_pedidos = []

    url_params = ''
    for key, value in PARAMS.items():
        url_params += f'{key}={value}&'

    while offset < total:
        try:
            url = f'https://api.tiny.com.br/public-api/v3/pedidos?{url_params}offset={offset}'
            print(url)

            payload = ''
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {ACCESS_TOKEN}'
            }

            response = requests.request("GET", url, headers=headers, data=payload)
            response = response.json()

            offset = offset + 100
            total = response['paginacao']['total']

            lista_pedidos = [*lista_pedidos, *response['itens']]
        except Exception as e:
            print(e)
            time.sleep(5)
    
    return lista_pedidos
