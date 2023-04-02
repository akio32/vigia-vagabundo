# Importação das bibliotecas a serem utilizadas
import requests
import csv
import pandas as pd

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

# Função que retorna uma lista de proposicoes, dados macro
def consulta_propostas():

    # Faz requisição para a API e obtém as informações das proposições em tramitação
    response = requests.get(url='https://dadosabertos.camara.leg.br/api/v2/proposicoes?ano=2022&siglaTipo=PL&itens=100')

    # Inicializa lista dos resultados
    keep_loop = True
    count = 0

    while keep_loop:

        ids_proposicoes = {}
        count = count + 1

        print(f"Iteração {count}")
    
        # Verifica se a requisição foi bem sucedida
        if response.status_code == 200:
            keep_loop = True
        else:
            print('Erro ao acessar a API')
            return []

        # Arquivo JSON retornado pela API
        proposicoes = response.json()['dados']

        # Loop na lista para extrair os IDs e URIs das proposições e retorna um dicionário
        for proposicao in proposicoes:
            ids_proposicoes[proposicao['id']] = proposicao['uri']

        #Verifica quantidade de paginas para consulta
        check_next = response.json()['links']

        for next in check_next:
            if next['rel'] == 'next':
                keep_loop = True
                next_request = next['href']
                break
            else:
                keep_loop = False

        list_detalhes = consulta_detalhes_propostas(ids_proposicoes)

        df = pd.DataFrame.from_dict(list_detalhes, orient='columns')

        df.to_csv(f'propostas_2020_arq{count}.csv', sep='|', index=False)

        # Faz requisição para a API e obtém as informações das proposições em tramitação
        response = requests.get(url=next_request)

    return ids_proposicoes


# Função que retorna uma lista detalhaada das proposições passadas via parametro "ids_proposicoes"
def consulta_detalhes_propostas(ids_proposicoes):
    
    detalhes_proposicoes = []

    for id_proposicao in ids_proposicoes:

        response = requests.get(ids_proposicoes[id_proposicao])

        if response.status_code == 200:
            detalhes_proposicoes.append(response.json()['dados']) 
        else:
            print('Erro ao acessar a API')

    return detalhes_proposicoes