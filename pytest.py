import lambda_function

events = {
    'url' : 'https://dadosabertos.camara.leg.br/api/v2/proposicoes',
    'params' : {
        'siglaTipo' : 'PL',
        'ano' : '2023',
        'itens' : '100',
        'ordem' : 'ASC',
        'ordenarPor' : 'id'
    }
}

lambda_function.lambda_handler(events=events, context=None)


