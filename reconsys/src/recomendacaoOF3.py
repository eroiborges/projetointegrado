# recomendacaoOF3.py
# Quantum Finance — Função de Recomendação
#
# Função principal:
#   getRecomendacoes(usuario) → list  (produtos recomendados com weighted score)
#
# Algoritmo: User-Based Collaborative Filtering
#   1. Obtém vizinhos ordenados por similaridade
#   2. Para cada vizinho, acumula: score += sim * rating   (por produto não possuído)
#   3. Normaliza: weighted_score = score_acumulado / soma_similaridades
#   4. Retorna produtos ordenados por weighted_score (decrescente)

from recomendacaoOF import clientes
from recomendacaoOF2 import getSimilares


def getRecomendacoes(usuario):
    """
    Gera recomendações de produtos financeiros para o usuario informado.

    Lógica:
      - Considera apenas produtos que o usuario ainda NÃO possui
      - Calcula um score ponderado por similaridade dos vizinhos que possuem o produto
      - Normaliza o score pela soma das similaridades dos vizinhos que contribuíram

    Retorna:
      Lista de tuplas [(weighted_score, produto), ...] ordenada por score (maior primeiro)
      Lista vazia se o usuario já possui todos os produtos disponíveis no dataset
    """
    if usuario not in clientes:
        return []

    similares = getSimilares(usuario)

    scores = {}      # { produto: soma(sim * rating) }
    total_sim = {}   # { produto: soma(sim) }

    for sim, vizinho in similares:
        for produto, rating in clientes[vizinho].items():
            if produto not in clientes[usuario]:
                scores.setdefault(produto, 0)
                total_sim.setdefault(produto, 0)
                scores[produto] += sim * rating
                total_sim[produto] += sim

    recomendacoes = [
        (round(scores[p] / total_sim[p], 4), p)
        for p in scores
    ]
    recomendacoes.sort(reverse=True)
    return recomendacoes
