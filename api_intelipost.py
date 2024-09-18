import requests

def consulta_entrega(TOKEN_INTELIPOST, pedido_entrega):
    url = f'https://api.intelipost.com.br/api/v1/shipment_order/{pedido_entrega}'

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'api-key': TOKEN_INTELIPOST
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()