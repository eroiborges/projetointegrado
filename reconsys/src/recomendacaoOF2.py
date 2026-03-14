# recomendacaoOF2.py
# Quantum Finance — Funções de Distância e Similaridade
#
# Funções:
#   euclidiana(usuario1, usuario2) → float  (distância entre dois clientes)
#   similaridade(usuario1, usuario2) → float  (score 0→1)
#   getSimilares(usuario) → list  (lista de vizinhos ordenada por similaridade)

from math import sqrt
from recomendacaoOF import clientes


def euclidiana(usuario1, usuario2):
    """
    Calcula a distância euclidiana entre dois clientes
    com base nos produtos que ambos possuem em comum.

    Retorna:
      -1 se usuario1 não existe no dataset
      -2 se usuario2 não existe no dataset
      -3 se os dois usuários não têm nenhum produto em comum
      float (>= 0) caso contrário
    """
    if usuario1 not in clientes:
        return -1
    if usuario2 not in clientes:
        return -2

    si = {item: 1 for item in clientes[usuario1] if item in clientes[usuario2]}

    if len(si) == 0:
        return -3

    soma = sum([
        pow(clientes[usuario1][item] - clientes[usuario2][item], 2)
        for item in clientes[usuario1] if item in clientes[usuario2]
    ])
    return sqrt(soma)


def similaridade(usuario1, usuario2):
    """
    Converte a distância euclidiana em um score de similaridade entre 0 e 1.
    Score 1.0 = clientes idênticos. Score próximo de 0 = muito diferentes.

    Fórmula: sim = 1 / (1 + distância)
    """
    de = euclidiana(usuario1, usuario2)
    if de < 0:
        return 0
    return 1 / (1 + de)


def getSimilares(usuario):
    """
    Retorna lista de todos os outros clientes ordenados por similaridade
    em relação ao usuario informado (decrescente — mais similar primeiro).

    Formato de retorno: [(score_similaridade, nome_cliente), ...]
    """
    lista = [
        (round(similaridade(usuario, outro), 4), outro)
        for outro in clientes if outro != usuario
    ]
    lista.sort(reverse=True)
    return lista
