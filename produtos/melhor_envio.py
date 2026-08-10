import requests
from django.conf import settings
from produtos.models import MelhorEnvioToken 

def renovar_token():
    token_banco = MelhorEnvioToken.objects.first()
    
    if not token_banco or not token_banco.refresh_token:
        print("Erro: Nenhum refresh_token encontrado no banco de dados.")
        return None

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
    # ALTERAÇÃO SEGURA: Primeiro tenta pegar o token novo do seu settings.py (.env)
    token_env = getattr(settings, 'MELHOR_ENVIO_ACCESS_TOKEN', None)
    if token_env:
        return token_env
        
    # Se não achar no .env, mantém o comportamento antigo de buscar no banco
    token_banco = MelhorEnvioToken.objects.first()
    if token_banco:
        return token_banco.access_token
    return None


def calcular_frete_api(cep_destino, produtos_carrinho):
    token = obter_access_token()
    
    if not token:
        print("Nenhum token encontrado no banco de dados ou no settings.py.")
        return None

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    url = "https://sandbox.melhorenvio.com.br/api/v2/me/shipment/calculate"

    # Agora o payload envia a lista dinâmica gerada a partir do carrinho da sessão
    payload = {
        "from": {
            "postal_code": settings.CEP_ORIGEM
        },
        "to": {
            "postal_code": str(cep_destino)
        },
        "products": produtos_carrinho
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        resultado = response.json()

        is_unauthorized = (
            response.status_code in [401, 403] or 
            (isinstance(resultado, dict) and (
                resultado.get("message") == "Unauthenticated." or 
                "unauthorized" in str(resultado.get("message", "")).lower()
            ))
        )

        if is_unauthorized:
            print("Token inválido ou não autorizado detectado! Forçando renovação automática...")
            novo_token = renovar_token()
            if novo_token:
                headers["Authorization"] = f"Bearer {novo_token}"
                response = requests.post(url, json=payload, headers=headers)
                return response.json()

        return resultado
    except Exception as e:
        print(f"Erro na requisição do frete: {e}")
        return None