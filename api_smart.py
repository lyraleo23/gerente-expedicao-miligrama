import requests

def login_smart(CNPJ, USERNAME_, PASSWORD):
    url = "https://api2.naiferautomacao.com.br/login"

    payload = {}
    headers = {
        'cnpj': CNPJ,
        'username': USERNAME_,
        'password': PASSWORD
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()[0]['token']

def status_receita(TOKEN_SMART, PARAMS):
    url_params = ''
    for key, value in PARAMS.items():
        url_params += f'{key}={value}&'
    
    url = f'https://api2.naiferautomacao.com.br/recstatus/showdash?{url_params}'

    payload = {}
    headers = {
        'Authorization': f'Bearer {TOKEN_SMART}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response
