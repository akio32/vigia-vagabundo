from api_utils import call_api

def main():
    url = 'https://dadosabertos.camara.leg.br/api/v2/proposicoes?ano=2022&siglaTipo=PL&itens=10'
    response = call_api(url)
    print(response)

if __name__ == '__main__':
    main()
