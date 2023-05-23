import os
import json
from src import libs

def lambda_handler(events, context):

    consulta_propostas()

# Function to return a list of propositions
def consulta_propostas(): 

    url = 'https://dadosabertos.camara.leg.br/api/v2/proposicoes?ano=2022&siglaTipo=PL&itens=100'
    
    headers = {
        'Accept' : 'application/json'
    }

    file_count = 0
    keep = True

    while keep:
        
        # Increses the count
        file_count = file_count + 1

        # Make the request API 
        response = libs.make_get_request(url=url, headers=headers)

        href_last = []

        # Look for the next call, if exists
        for links in response.json()['links']:
            if links.get('rel') in ['self', 'last']:
                href = links.get('href')
                href_last.append(href)
            if 'next' in links.values():
                url = links['href']
        
        keep = (len(set(href_last)) == len(href_last))

        # Save JSON file
        libs.save_file(response, 'propostas_camara_' + str(file_count).zfill(6), 'json')

    valores_id = []
    valores_ementa = []

    for arquivo in os.listdir('/home/misteryoh/Coding/'):
        if arquivo.endswith('.json'):
            caminho_arquivo = os.path.join('/home/misteryoh/Coding/', arquivo)
            with open(caminho_arquivo, 'r') as arquivo_json:
                dados = json.load(arquivo_json)
                for dicionario in dados['dados']:
                    valor_id = dicionario.get('id')
                    valor_ementa = dicionario.get('ementa')
                    if valor_id is not None:
                        valores_id.append(valor_id)
                    if valor_ementa is not None:
                        valores_ementa.append(valor_ementa)    

    print(valores_id)

    # dados        : list<dict>
    # dados.id     : int
    # dados.uri    : string
    # dados.ementa : string
    # links        : list<dict>
    # links.rel    : string (self, next, first, last)
    # links.href   : string

   

   #     list_detalhes = consulta_detalhes_propostas(ids_proposicoes)

   #     df = pd.DataFrame.from_dict(list_detalhes, orient='columns')

   #     upload_response = upload_file(df=df, bucket_name='vigiavagabundo',
   #                                   folder_name='propostas', object_name=f'propostas_2022_arq{count}.csv')

   #     # Faz requisição para a API e obtém as informações das proposições em tramitação
   #     response = requests.get(url=next_request)

   # return ids_proposicoes


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

lambda_handler(None, None)
