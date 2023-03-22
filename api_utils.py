# Importação das bibliotecas a serem utilizadas
import requests

# Função que realiza chamada de API e retorna o resultado em JSON
def call_api(url, headers=None, params=None):
    try:
        # Faz requisição para a API e obtém as informações das proposições em tramitação
        response = requests.get(url, headers=headers, params=params)
        return response.json()
    except requests.exceptions.RequestException as e:
        # Log do erro
        print(f"An error occurred: {e}")

        # Retorna o objeto de erro
        error = {
            "message": str(e),
            "status_code": response.status_code if response else None,
            "url": url,
            "headers": headers
        }
        return error