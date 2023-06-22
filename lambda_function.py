import json
from src import libs

def lambda_handler(events, context):
    
    #Etapa 1 - Consulta Propostas
    consulta_propostas(events=events)

    
# Função que retorna uma lista de proposicoes, dados macro
def consulta_propostas(events):

    url = events['url']
    params = events['params']

    # Faz requisição para a API e obtém as informações das proposições em tramitação
    response = libs.make_request(url=url, method="GET", dados=params)
    
    # Inicializa lista dos resultados
    keep_loop = True
    count = 0

    while keep_loop:

        count = count + 1
        ids_proposicoes = {}

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

        # Verifica quantidade de paginas para consulta
        check_next = response.json()['links']

        for next in check_next:
            if next['rel'] == 'next':
                keep_loop = True
                next_request = next['href']
                break
            else:
                keep_loop = False

        list_detalhes = consulta_detalhes_propostas(ids_proposicoes)
        upload_file = json.dumps(list_detalhes)

        upload_response = libs.upload_s3_object(content=upload_file, profile='default', bucket='neosentinel',
                                      folder='propostas', filename=f'propostas_2023_arq{count}.json')

        # Faz requisição para a API e obtém as informações das proposições em tramitação
        response = libs.make_request(url=next_request, method="GET")

    return True


# Função que retorna uma lista detalhaada das proposições passadas via parametro "ids_proposicoes"
def consulta_detalhes_propostas(ids_proposicoes):

    detalhes_proposicoes = []

    for id_proposicao in ids_proposicoes:

        response = libs.make_request(url=ids_proposicoes[id_proposicao], method="GET")

        if response.status_code == 200:
            detalhes_proposicoes.append(response.json()['dados'])
        else:
            print('Erro ao acessar a API')

    return detalhes_proposicoes