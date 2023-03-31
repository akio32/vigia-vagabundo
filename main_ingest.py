import api_utils as api
import csv

def main():
    # url = 'https://dadosabertos.camara.leg.br/api/v2/proposicoes?ano=2022&siglaTipo=PL&itens=10'
    # response = call_api(url)
    # print(response)

    api.consulta_propostas()

if __name__ == '__main__':
    main()
