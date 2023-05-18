from src import libs

def lambda_handler(events, context):
    url = 'https://dadosabertos.camara.leg.br/api/v2/proposicoes?ano=2022&siglaTipo=PL&itens=10'

# Função que retorna uma lista de proposicoes, dados macro
def consulta_propostas(): 

    url = 'https://dadosabertos.camara.leg.br/api/v2/proposicoes?ano=2022&siglaTipo=PL&itens=10'
    
    headers = {
        'Accept' : 'application/json'
    }

    # Faz requisição para a API e obtém as informações das proposições em tramitação
    response = libs.make_get_request(path=url, headers=headers)  


def make_get_request(url, params=None, headers=None):

    requests.get(
        url='https://dadosabertos.camara.leg.br/api/v2/proposicoes?ano=2022&siglaTipo=PL&itens=100')

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

        df = pd.DataFrame.from_dict(list_detalhes, orient='columns')

        upload_response = upload_file(df=df, bucket_name='vigiavagabundo',
                                      folder_name='propostas', object_name=f'propostas_2022_arq{count}.csv')

        # Faz requisição para a API e obtém as informações das proposições em tramitação
        response = requests.get(url=next_request)

    return ids_proposicoes


# Função que retorna uma lista detalha da das proposições passadas via parametro "ids_proposicoes"
def consulta_detalhes_propostas(ids_proposicoes):

    detalhes_proposicoes = []

    for id_proposicao in ids_proposicoes:

        response = requests.get(ids_proposicoes[id_proposicao])

        if response.status_code == 200:
            detalhes_proposicoes.append(response.json()['dados'])
        else:
            print('Erro ao acessar a API')

    return detalhes_proposicoes


