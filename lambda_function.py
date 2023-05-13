from src import libs

def lambda_handler(events, context):
    url = 'https://dadosabertos.camara.leg.br/api/v2/proposicoes?ano=2022&siglaTipo=PL&itens=10'
    data_results = []
    # response = call_api(url)
    # print(response)

    # api.consulta_propostas()
    api.recursive_api_call(url, data_results)


if __name__ == '__main__':
    main()
