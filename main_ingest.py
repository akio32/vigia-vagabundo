from api_utils import call_api

def main():
    url = 'https://dadosabertos.camara.leg.br/api/v2/proposicoes/2313792'
    response = call_api(url)
    print(response)

if __name__ == '__main__':
    main()
