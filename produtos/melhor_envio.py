import requests
from django.conf import settings
from produtos.models import MelhorEnvioToken 

def renovar_token():
    token_banco = MelhorEnvioToken.objects.first()
    
    if not token_banco or not token_banco.refresh_token:
        print("Erro: Nenhum refresh_token encontrado no banco de dados.")
        return None

    # Colocamos o 'sandbox.' aqui
    url = "https://sandbox.melhorenvio.com.br/oauth/token"
    payload = {
        "grant_type": "refresh_token",
        "client_id": settings.MELHOR_ENVIO_CLIENT_ID,
        "client_secret": settings.MELHOR_ENVIO_CLIENT_SECRET,
        "refresh_token": token_banco.refresh_token
    }

    response = requests.post(url, json=payload)
    dados = response.json()

    if response.status_code == 200 and "access_token" in dados:
        token_banco.access_token = dados.get("access_token")
        token_banco.refresh_token = dados.get("refresh_token")
        token_banco.save()
        print("Tokens renovados e salvos com sucesso no banco de dados!")
        return token_banco.access_token
    else:
        print(f"Erro ao renovar token: {dados}")
        return None


def obter_access_token():
    token_banco = MelhorEnvioToken.objects.first()
    if token_banco:
        return token_banco.access_token
    return None


def consultar_frete():
    token = obter_access_token()
    
    if not token:
        return {"error": "Nenhum token encontrado no banco de dados."}

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Colocamos o 'sandbox.' aqui
    url = "https://sandbox.melhorenvio.com.br/api/v2/me/shipment/calculate"

    payload = {
        "from": {
            "postal_code": settings.CEP_ORIGEM
        },
        "to": {
            "postal_code": "30140071"
        },
        "products": [
            {
                "id": "1",
                "width": 20,
                "height": 20,
                "length": 20,
                "weight": 1,
                "insurance_value": 100,
                "quantity": 1
            }
        ]
    }

    response = requests.post(url, json=payload, headers=headers)
    resultado = response.json()

    if response.status_code == 401 or resultado.get("message") == "Unauthenticated.":
        print("Token expirado detectado! Tentando renovar automaticamente...")
        novo_token = renovar_token()
        if novo_token:
            headers["Authorization"] = f"Bearer {novo_token}"
            response = requests.post(url, json=payload, headers=headers)
            return response.json()

    return resultado


def trocar_code_por_token(code):
    # Colocamos o 'sandbox.' aqui também
    url = "https://sandbox.melhorenvio.com.br/oauth/token"

    payload = {
        "grant_type": "authorization_code",
        "client_id": settings.MELHOR_ENVIO_CLIENT_ID,
        "client_secret": settings.MELHOR_ENVIO_CLIENT_SECRET,
        "redirect_uri": settings.MELHOR_ENVIO_REDIRECT_URI,
        "code": code
    }

    response = requests.post(url, json=payload)
    return response.json()