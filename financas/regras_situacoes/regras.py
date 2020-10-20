'''
Responsável por criar as regras aplicadas em situações
'''


def get_status(valor):
    status = ''
    limite = 500
    if valor >= limite:
        status = 'p'
    elif valor < 0:
        status = 'n'
    else:
        status = 'l'
    return status


def aplica_calculo(tipo, valor):
    pass
