# Importação das bibliotecas a serem utilizadas
import requests
import csv
import pandas as pd
import logging
import boto3
from botocore.exceptions import ClientError
import os


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

        # df.to_csv(f'propostas_2022_arq{count}.csv', sep='|', index=False)

        upload_response = upload_file(df=df, bucket_name='vigiavagabundo', folder_name='propostas', object_name=f'propostas_2022_arq{count}.csv')

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


def upload_file(df, bucket_name, folder_name, object_name):
    """Upload a file to an S3 bucket

    :param df: Pandas Dataframe to upload
    :param folder: Bucket to upload to
    :param bucket_name: Folder to upload to
    :param object_name: S3 object name
    :return: True if file was uploaded, else False
    """

    # Upload the file
    # Create a session using the specified configuration file
    session = boto3.Session(profile_name='default')
    s3_client = session.client('s3')

    try:
        # response = s3_client.upload_file(file_name, bucket, object_name)

        # Convert the DataFrame to CSV and upload to S3
        csv_buffer = df.to_csv(sep='|', index=False)
        s3_object = s3_client.put_object(Bucket=bucket_name, Key=f"{folder_name}/{object_name}", Body=csv_buffer.encode())
    except ClientError as e:
        logging.error(e)
        return False
    return True