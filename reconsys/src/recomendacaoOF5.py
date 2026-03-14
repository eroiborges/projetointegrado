# recomendacaoOF5.py
# Quantum Finance — Inteligência de Mercado (Open Finance APIs)
#
# Responsabilidade:
#   - Consultar APIs Open Data do Open Finance (sem autenticação) de 4 IFs
#   - Extrair taxas mínimas por produto (empréstimos, cartões)
#   - Gerar proposta Quantum Finance com desconto de 5% sobre a melhor taxa
#   - Modo Batch: gerar DataFrame com todos os clientes + proposta
#   - Modo Ad-hoc: receber perfil avulso → recomendação + proposta
#
# Bancos consultados: Itaú, Caixa Econômica Federal, XP, PicPay
#
# Taxas reais coletadas (Open Finance OpenData, Mar/2026):
#   Consignado PRE_FIXADO: Itaú min=1.00%, XP min=1.00%, PicPay min=1.24%, Caixa max=3.10%
#   Sem Consignação PRE_FIXADO: Itaú min=1.00%, Caixa min=1.18%, PicPay min=1.49%
#
# Nota de segurança: verify=False é aceitável em PoC de Open Data público.
# Em produção com dados de clientes (FAPI 2.0/mTLS), NUNCA desabilitar TLS.

import requests
import warnings
import pandas as pd
warnings.filterwarnings('ignore')  # suprime InsecureRequestWarning para PoC

from recomendacaoOF import clientes
from recomendacaoOF3 import getRecomendacoes

# ─────────────────────────────────────────────────────────────────────────────
# Configuração: IFs, endpoints e fallback
# ─────────────────────────────────────────────────────────────────────────────

BANCOS = {
    'Itaú':   'https://api.itau',
    'Caixa':  'https://api.openbanking.caixa.gov.br',
    'XP':     'https://banking-openfinance.xpi.com.br',
    'PicPay': 'https://resources.openbanking.picpay.com'
}

ENDPOINTS = {
    'Crédito Pessoal':   '/open-banking/opendata-loans/v1/personal-loans',
    'Cartão de Crédito': '/open-banking/opendata-creditcards/v1/personal-credit-cards'
}

TIPO_PRODUTO = {
    'Crédito Pessoal': 'EMPRESTIMO_CREDITO_PESSOAL_CONSIGNADO'
}

# Fallback com taxas reais coletadas em Mar/2026 (caso APIs offline)
TAXAS_FALLBACK = {
    'Crédito Pessoal': {
        'Itaú': 0.0100, 'XP': 0.0100, 'PicPay': 0.0124, 'Caixa': 0.0310
    }
}

DESCONTO_QF = 0.05  # Proposta Quantum Finance: 5% abaixo da melhor taxa

# ─────────────────────────────────────────────────────────────────────────────
# Coleta de taxas de mercado
# ─────────────────────────────────────────────────────────────────────────────

def buscar_taxas_mercado(produto):
    """
    Consulta APIs Open Finance de todas as IFs e retorna {banco: taxa_min_mensal}.
    Pula IFs com timeout ou erro HTTP e usa fallback se nenhuma responder.

    Parâmetros:
      produto: str — chave em ENDPOINTS ('Crédito Pessoal', 'Cartão de Crédito')

    Retorna:
      dict {banco: float} com taxas em decimal (ex.: 0.01 = 1% a.m.)
    """
    endpoint = ENDPOINTS.get(produto)
    filtro_tipo = TIPO_PRODUTO.get(produto)
    taxas = {}

    if not endpoint:
        return TAXAS_FALLBACK.get(produto, {})

    for banco, base_url in BANCOS.items():
        try:
            resp = requests.get(
                base_url + endpoint,
                verify=False,     # equivalente ao curl -k (PoC Open Data)
                timeout=8
            )
            if resp.status_code != 200:
                continue
            dados = resp.json().get('data', [])
            for item in dados:
                if filtro_tipo and item.get('type') != filtro_tipo:
                    continue
                for r in item.get('interestRates', []):
                    mn = float(r.get('minimumRate', '0'))
                    if mn > 0:
                        taxas[banco] = min(taxas.get(banco, 99), mn)
                        break
        except Exception:
            continue  # IF inativa ou timeout → pular silenciosamente

    return taxas if taxas else TAXAS_FALLBACK.get(produto, {})


def gerar_proposta_qf(produto):
    """
    Coleta taxas de mercado e calcula proposta Quantum Finance.

    Retorna:
      dict com produto, taxas_mercado, melhor_taxa, banco_referencia, taxa_qf, economia_pct
      ou {} se produto não tiver taxas disponíveis.
    """
    taxas = buscar_taxas_mercado(produto)
    if not taxas:
        return {}

    banco_ref = min(taxas, key=taxas.get)
    melhor = taxas[banco_ref]
    taxa_qf = round(melhor * (1 - DESCONTO_QF), 6)

    return {
        'produto': produto,
        'taxas_mercado': taxas,
        'melhor_taxa': melhor,
        'banco_referencia': banco_ref,
        'taxa_qf': taxa_qf,
        'economia_pct': round(DESCONTO_QF * 100, 1)
    }


# ─────────────────────────────────────────────────────────────────────────────
# Modo Batch — Lista de Contato
# ─────────────────────────────────────────────────────────────────────────────

def gerar_lista_contato():
    """
    Modo Batch: itera sobre todos os clientes, calcula recomendação CF e anexa
    proposta QF quando o produto recomendado tiver taxa de mercado disponível.

    Faz apenas UMA chamada HTTP por produto (proposta pré-carregada).

    Retorna:
      pandas.DataFrame com colunas:
        Cliente, Produto Recomendado, Score CF,
        Taxa Mercado (min), Proposta QF (−5%), Ação Sugerida
    """
    proposta_credito = gerar_proposta_qf('Crédito Pessoal')
    registros = []

    for nome in clientes:
        recs = getRecomendacoes(nome)
        if not recs:
            continue
        score_cf, produto_rec = recs[0]

        if produto_rec == 'Crédito Pessoal' and proposta_credito:
            taxa_m = proposta_credito['melhor_taxa']
            taxa_q = proposta_credito['taxa_qf']
            acao = 'Oferta Crédito Consignado'
        else:
            taxa_m = taxa_q = None
            acao = 'Oferta Produto'

        registros.append({
            'Cliente': nome,
            'Produto Recomendado': produto_rec,
            'Score CF': round(score_cf, 4),
            'Taxa Mercado (min)': f"{taxa_m * 100:.2f}% a.m." if taxa_m else '—',
            'Proposta QF (−5%)': f"{taxa_q * 100:.4f}% a.m." if taxa_q else '—',
            'Ação Sugerida': acao
        })

    return pd.DataFrame(registros)


# ─────────────────────────────────────────────────────────────────────────────
# Modo Ad-hoc — Recomendação Instantânea
# ─────────────────────────────────────────────────────────────────────────────

def recomendar_adhoc(perfil):
    """
    Modo Ad-hoc: recebe perfil de cliente avulso e retorna recomendação + proposta.

    Parâmetros:
      perfil: dict {produto: score} — produtos que o cliente já possui

    Retorna:
      dict {'recomendacoes': [(score, produto), ...], 'proposta_qf': dict ou None}

    Nota: '_adhoc_' é adicionado/removido do dataset sem efeito colateral.
    O bloco try/finally garante limpeza mesmo em caso de exceção.
    """
    chave = '_adhoc_'
    clientes[chave] = perfil
    try:
        recs = getRecomendacoes(chave)
    finally:
        del clientes[chave]

    proposta = None
    if recs:
        _, prod_top = recs[0]
        if prod_top in ENDPOINTS:
            proposta = gerar_proposta_qf(prod_top)

    return {'recomendacoes': recs, 'proposta_qf': proposta}
