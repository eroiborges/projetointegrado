# Entregável 4 — Código Fonte
## Especificação dos arquivos Python — Quantum Finance SR

---

## Objetivo deste arquivo

Este documento especifica os **arquivos Python** que implementam o Sistema de Recomendação da Quantum Finance como prova de conceito.
Os arquivos seguem a mesma estrutura modular usada pelo professor nos materiais de aula.

---

## 1. Estrutura de Arquivos

```
/home/sadmin/rs/
├── src/
│   ├── recomendacaoOF.py        ← Módulo 1: Dataset
│   ├── recomendacaoOF2.py       ← Módulo 2: Distância + Similaridade + getSimilares
│   ├── recomendacaoOF3.py       ← Módulo 3: getRecomendacoes (Filtro Colaborativo)
│   ├── recomendacaoOF4.py       ← Módulo 4: Knowledge-Based + SQLite (Abordagem Híbrida)
│   └── recomendacaoOF5.py       ← Módulo 5: Inteligência de Mercado (APIs Open Finance)
└── quantum_finance_sr.ipynb     ← Protótipo (especificado em 03_prototipo.md)
```

> **Alternativa simples (sem subpasta src/):** colocar os 4 arquivos na raiz `/home/sadmin/rs/` — segue o padrão do professor nos materiais de aula.

---

## 2. Módulo 1 — `recomendacaoOF.py`

**Responsabilidade:** Definir o dataset de clientes e produtos Open Finance.

**Arquivo:** `recomendacaoOF.py`

```python
# recomendacaoOF.py
# Quantum Finance — Dataset Open Finance
#
# Estrutura: { cliente: { produto: score_de_uso } }
# Score: valor numérico representando intensidade de uso/interesse (escala 1-7)
# Fonte: Open Finance — dados compartilhados mediante consentimento do cliente
#
# Contexto: clientes da Quantum Finance (Fintech de crédito pessoal/consignado)
# que consentiram compartilhar dados de outras IFs via Open Finance

clientes = {
    'Ana': {
        'Cartão de Crédito': 1,
        'Conta Corrente': 2,
        'Poupança': 3,
        'Renda Fixa': 4,
        'Crédito Pessoal': 5
    },
    'Marcos': {
        'Cartão de Crédito': 2,
        'Conta Corrente': 3,
        'Poupança': 4,
        'Renda Fixa': 5,
        'Renda Variável': 0.6
    },
    'Pedro': {
        'Cartão de Crédito': 3,
        'Conta Corrente': 4,
        'Poupança': 5,
        'Crédito Pessoal': 7
    },
    'Claudia': {
        'Cartão de Crédito': 4,
        'Conta Corrente': 5,
        'Poupança': 6
    }
}
```

**Observações de implementação:**
- Não importa nenhum outro módulo
- É o único módulo que acessa diretamente a variável `clientes`
- Em produção, esse módulo seria substituído por uma função que lê da API do Open Finance ou de um banco de dados

---

## 3. Módulo 2 — `recomendacaoOF2.py`

**Responsabilidade:** Calcular distância euclidiana, similaridade e listar vizinhos similares.
Este módulo replica e consolida as funções ensinadas pelo professor.

**Arquivo:** `recomendacaoOF2.py`

```python
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
```

**Saídas esperadas (para validar):**

```python
# Teste euclidiana
euclidiana('Ana', 'Marcos')   # → 2.0
euclidiana('Ana', 'Pedro')    # → 4.0
euclidiana('Ana', 'Claudia')  # → 5.196...

# Teste similaridade
similaridade('Ana', 'Marcos')   # → 0.3333...
similaridade('Ana', 'Pedro')    # → 0.2
similaridade('Ana', 'Claudia')  # → 0.1614...

# Teste getSimilares
getSimilares('Ana')
# → [(0.3333, 'Marcos'), (0.2, 'Pedro'), (0.1614, 'Claudia')]

getSimilares('Claudia')
# → [(0.3660, 'Pedro'), (0.2240, 'Marcos'), (0.1614, 'Ana')]
```

---

## 4. Módulo 3 — `recomendacaoOF3.py` ★ FUNÇÃO NOVA

**Responsabilidade:** Gerar a lista de produtos recomendados para um cliente, com score ponderado normalizado.

**Arquivo:** `recomendacaoOF3.py`

```python
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
```

**Saídas esperadas (para validar):**

```python
getRecomendacoes('Ana')
# Ana não tem: Renda Variável
# → [(score_renda_variavel, 'Renda Variável')]

getRecomendacoes('Marcos')
# Marcos não tem: Crédito Pessoal
# → [(score, 'Crédito Pessoal')]

getRecomendacoes('Pedro')
# Pedro não tem: Renda Fixa, Renda Variável
# → [(score_renda_fixa, 'Renda Fixa'), (score_renda_variavel, 'Renda Variável')]
# (ordem depende dos scores calculados)

getRecomendacoes('Claudia')
# Claudia não tem: Renda Fixa, Crédito Pessoal, Renda Variável
# → [(maior, 'Crédito Pessoal'), (medio, 'Renda Fixa'), (menor, 'Renda Variável')]
# (Crédito Pessoal lidera pois Pedro — vizinho mais similar de Claudia — tem score 7)
```

---

## 5. Módulo 4 — `recomendacaoOF4.py` ✨ KNOWLEDGE-BASED + SQLite

**Responsabilidade:** Persistir os scores calculados pelo Python em SQLite e aplicar recomendação baseada em conhecimento com ranqueamento por popularidade — conforme Hands-on Aula 2 (PDF p. 100-110).

**Arquivo:** `recomendacaoOF4.py`

```python
# recomendacaoOF4.py
# Quantum Finance — Knowledge-Based + SQLite (Abordagem Híbrida)
#
# Responsabilidade:
#   - Criar e popular o banco SQLite com clientes, produtos e similaridades
#   - Aplicar recomendação via SQL (Filtro Colaborativo + Popularidade)
#   - Simular mecanismo de feedback (likes/dislikes)
#
# Modelo de dados (PDF p. 103):
#   tbCliente, tbProduto (quantidadeLikes), tbClienteProduto, tbClienteSimilaridade

import sqlite3
from recomendacaoOF import clientes
from recomendacaoOF2 import similaridade


def criar_banco():
    """
    Cria o banco SQLite em memória e retorna a conexão.
    Para persistência em arquivo, substituir ':memory:' por 'quantumfinance.db'.
    """
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE tbCliente (
            nomeCliente VARCHAR(50) PRIMARY KEY
        );
        CREATE TABLE tbProduto (
            nomeProduto VARCHAR(50) PRIMARY KEY,
            quantidadeLikes INTEGER DEFAULT 0
        );
        CREATE TABLE tbClienteProduto (
            nomeCliente VARCHAR(50),
            nomeProduto VARCHAR(50),
            valor FLOAT,
            PRIMARY KEY (nomeCliente, nomeProduto)
        );
        CREATE TABLE tbClienteSimilaridade (
            nomeClienteOrigem VARCHAR(50),
            nomeClienteDestino VARCHAR(50),
            similaridade FLOAT,
            PRIMARY KEY (nomeClienteOrigem, nomeClienteDestino)
        );
    """)
    conn.commit()
    return conn


def popular_banco(conn):
    """
    Popula todas as tabelas com dados do dataset Python e scores de similaridade.
    """
    cursor = conn.cursor()

    for nome in clientes:
        cursor.execute("INSERT INTO tbCliente VALUES (?)", (nome,))

    produtos_likes = {
        'Cartão de Crédito': 1,
        'Conta Corrente': 3,
        'Crédito Pessoal': 2,
        'Poupança': 0,
        'Renda Fixa': 1,
        'Renda Variável': 0
    }
    for produto, likes in produtos_likes.items():
        cursor.execute("INSERT INTO tbProduto VALUES (?, ?)", (produto, likes))

    for nome, produtos_cliente in clientes.items():
        for produto, valor in produtos_cliente.items():
            cursor.execute(
                "INSERT INTO tbClienteProduto VALUES (?, ?, ?)",
                (nome, produto, valor)
            )

    # Integração CF → SQL: scores calculados pelo Python são persistidos no BD
    for u1 in clientes:
        for u2 in clientes:
            if u1 != u2:
                sim = round(similaridade(u1, u2), 4)
                cursor.execute(
                    "INSERT INTO tbClienteSimilaridade VALUES (?, ?, ?)",
                    (u1, u2, sim)
                )

    conn.commit()


def recomendar_por_vizinho(conn, usuario):
    """
    Filtro Colaborativo via SQL:
    1. Encontra o vizinho mais similar
    2. Retorna produtos que o vizinho tem e o usuario NÃO tem

    Retorna: (vizinho, [(nomeProduto, valor), ...])
    """
    cursor = conn.cursor()
    row = cursor.execute("""
        SELECT nomeClienteDestino FROM tbClienteSimilaridade
        WHERE nomeClienteOrigem = ?
        ORDER BY similaridade DESC LIMIT 1
    """, (usuario,)).fetchone()

    if not row:
        return None, []

    vizinho = row[0]
    recomendacoes = cursor.execute("""
        SELECT b.nomeProduto, b.valor
        FROM tbClienteProduto b
        WHERE b.nomeCliente = ?
          AND b.nomeProduto NOT IN (
              SELECT nomeProduto FROM tbClienteProduto WHERE nomeCliente = ?
          )
    """, (vizinho, usuario)).fetchall()

    return vizinho, recomendacoes


def listar_por_popularidade(conn):
    """
    Retorna todos os produtos ordenados por popularidade (quantidadeLikes DESC).
    Resolve Cold-Start parcialmente: clientes sem histórico recebem produtos populares.
    """
    cursor = conn.cursor()
    return cursor.execute("""
        SELECT nomeProduto, quantidadeLikes
        FROM tbProduto ORDER BY quantidadeLikes DESC
    """).fetchall()


def registrar_like(conn, produto):
    """Incrementa likes de um produto (feedback positivo do usuário)."""
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tbProduto SET quantidadeLikes = quantidadeLikes + 1 WHERE nomeProduto = ?",
        (produto,)
    )
    conn.commit()


def registrar_dislike(conn, produto):
    """Decrementa likes de um produto. Não permite valor abaixo de 0."""
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tbProduto SET quantidadeLikes = MAX(0, quantidadeLikes - 1) WHERE nomeProduto = ?",
        (produto,)
    )
    conn.commit()
```

**Saídas esperadas (para validar):**

```python
conn = criar_banco()
popular_banco(conn)

vizinho, recs = recomendar_por_vizinho(conn, 'Ana')
# vizinho → 'Marcos'
# recs    → [('Renda Variável', 0.6)]

vizinho, recs = recomendar_por_vizinho(conn, 'Claudia')
# vizinho → 'Pedro'
# recs    → [('Crédito Pessoal', 7)]

listar_por_popularidade(conn)
# → [('Conta Corrente', 3), ('Crédito Pessoal', 2), ('Cartão de Crédito', 1), ...]

registrar_like(conn, 'Cartão de Crédito')
# quantidadeLikes de Cartão de Crédito passa de 1 para 2
```

---

## 6. Módulo 5 — `recomendacaoOF5.py` ✨ INTELIGÊNCIA DE MERCADO

**Responsabilidade:** Consultar APIs Open Finance de 4 IFs, extrair taxas reais de mercado, gerar proposta Quantum Finance (5% abaixo da melhor taxa) e expor os dois modos operacionais: Batch (lista de contato) e Ad-hoc (recomendação instantânea).

**Arquivo:** `recomendacaoOF5.py`

```python
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
# Taxas reais coletadas (Open Finance OpenData, Mar/2025):
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

# ────────────────────────────────────────────────────────────────────────────────
# Configuração: IFs, endpoints e fallback
# ────────────────────────────────────────────────────────────────────────────────

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

# Fallback com taxas reais coletadas em Mar/2025 (caso APIs offline)
TAXAS_FALLBACK = {
    'Crédito Pessoal': {
        'Itaú': 0.0100, 'XP': 0.0100, 'PicPay': 0.0124, 'Caixa': 0.0310
    }
}

DESCONTO_QF = 0.05  # Proposta Quantum Finance: 5% abaixo da melhor taxa

# ────────────────────────────────────────────────────────────────────────────────
# Coleta de taxas de mercado
# ────────────────────────────────────────────────────────────────────────────────

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
      dict {
        'produto': str,
        'taxas_mercado': {banco: float},
        'melhor_taxa': float,
        'banco_referencia': str,
        'taxa_qf': float,
        'economia_pct': float
      }
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


# ────────────────────────────────────────────────────────────────────────────────
# Modo Batch — Lista de Contato
# ────────────────────────────────────────────────────────────────────────────────

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


# ────────────────────────────────────────────────────────────────────────────────
# Modo Ad-hoc — Recomendação Instantânea
# ────────────────────────────────────────────────────────────────────────────────

def recomendar_adhoc(perfil):
    """
    Modo Ad-hoc: recebe perfil de cliente avulso e retorna recomendação + proposta.

    Parâmetros:
      perfil: dict {produto: score} — produtos que o cliente já possui

    Retorna:
      dict {
        'recomendacoes': [(score, produto), ...],
        'proposta_qf': dict ou None
      }

    Nota: '_adhoc_' é adicionado/removido do dataset sem efeito colateral.
    O bloco try/finally garante limpeza mesmo em caso de exceção.
    """
    chave = '_adhoc_'
    clientes[chave] = perfil
    try:
        recs = getRecomendacoes(chave)
    finally:
        del clientes[chave]  # sempre remove — nenhum efeito colateral no dataset

    proposta = None
    if recs:
        _, prod_top = recs[0]
        if prod_top in ENDPOINTS:
            proposta = gerar_proposta_qf(prod_top)

    return {'recomendacoes': recs, 'proposta_qf': proposta}
```

**Saídas esperadas (para validar):**

```python
# Teste buscar_taxas_mercado
taxas = buscar_taxas_mercado('Crédito Pessoal')
# → {'Itaú': 0.01, 'XP': 0.01, 'PicPay': 0.0124, 'Caixa': 0.031}
# (ou fallback com mesmos valores se APIs offline)

# Teste gerar_proposta_qf
p = gerar_proposta_qf('Crédito Pessoal')
# → {
#     'produto': 'Crédito Pessoal',
#     'taxas_mercado': {'Itaú': 0.01, 'XP': 0.01, 'PicPay': 0.0124, 'Caixa': 0.031},
#     'melhor_taxa': 0.01,
#     'banco_referencia': 'Itaú',    # ou 'XP' (empate resolvido por dict ordering)
#     'taxa_qf': 0.0095,
#     'economia_pct': 5.0
# }

# Teste gerar_lista_contato
df = gerar_lista_contato()
# DataFrame com 4 linhas (Ana, Marcos, Pedro, Claudia)
# Marcos e Claudia terão proposta QF (Crédito Pessoal recomendado)
# Ana e Pedro terão '—' (Renda Variável / Renda Fixa — sem taxa)

# Teste recomendar_adhoc
r = recomendar_adhoc({'Cartão de Crédito': 1, 'Conta Corrente': 2, 'Poupança': 3})
# → {'recomendacoes': [(score, 'Crédito Pessoal'), ...], 'proposta_qf': {dict com taxa}}
```

---

## 7. Script de Teste — `testar_recomendacoes.py`

**Responsabilidade:** Script simples para validar os 5 módulos antes de executar o notebook.

**Arquivo:** `testar_recomendacoes.py`

```python
# testar_recomendacoes.py
# Script de validação dos 5 módulos de SR da Quantum Finance

from recomendacaoOF import clientes
from recomendacaoOF2 import euclidiana, similaridade, getSimilares
from recomendacaoOF3 import getRecomendacoes
from recomendacaoOF4 import criar_banco, popular_banco, recomendar_por_vizinho, listar_por_popularidade, registrar_like
from recomendacaoOF5 import buscar_taxas_mercado, gerar_proposta_qf, gerar_lista_contato, recomendar_adhoc

print("=" * 55)
print("QUANTUM FINANCE — Teste do Sistema de Recomendação")
print("=" * 55)

print("\n[1] Dataset carregado:")
for nome, produtos in clientes.items():
    print(f"  {nome}: {list(produtos.keys())}")

print("\n[2] Distâncias a partir de Ana:")
for outro in [c for c in clientes if c != 'Ana']:
    print(f"  Ana → {outro}: {euclidiana('Ana', outro):.4f}")

print("\n[3] Similaridades a partir de Ana:")
for outro in [c for c in clientes if c != 'Ana']:
    print(f"  Ana ↔ {outro}: {similaridade('Ana', outro):.4f}")

print("\n[4] Vizinhos similares por cliente:")
for cliente in clientes:
    print(f"  {cliente}: {getSimilares(cliente)}")

print("\n[5] Recomendações CF (getRecomendacoes):")
for cliente in clientes:
    rec = getRecomendacoes(cliente)
    if rec:
        print(f"  {cliente}:")
        for score, produto in rec:
            print(f"    → {produto} (score: {score})")
    else:
        print(f"  {cliente}: sem novas recomendações")

print("\n[6] Knowledge-Based + SQLite:")
conn = criar_banco()
popular_banco(conn)
for cliente in clientes:
    vizinho, recs = recomendar_por_vizinho(conn, cliente)
    print(f"  {cliente} → vizinho: {vizinho} | recomendações: {[r[0] for r in recs]}")

print("\n[7] Popularidade dos produtos:")
for produto, likes in listar_por_popularidade(conn):
    print(f"  {produto:<22} likes: {likes}")

registrar_like(conn, 'Cartão de Crédito')
print("\n[✓] Like registrado em 'Cartão de Crédito'")

print("\n[8] Inteligência de Mercado (APIs Open Finance):")
taxas = buscar_taxas_mercado('Crédito Pessoal')
print(f"  Taxas coletadas: { {b: f'{t*100:.2f}%' for b, t in taxas.items()} }")
proposta = gerar_proposta_qf('Crédito Pessoal')
if proposta:
    print(f"  Melhor taxa: {proposta['melhor_taxa']*100:.2f}% a.m. ({proposta['banco_referencia']})")
    print(f"  Proposta QF: {proposta['taxa_qf']*100:.4f}% a.m. (−{proposta['economia_pct']}%)")

print("\n[9] Modo Batch — Lista de Contato:")
df = gerar_lista_contato()
print(df.to_string(index=False))

print("\n[10] Modo Ad-hoc — Recomendação para perfil avulso:")
r = recomendar_adhoc({'Cartão de Crédito': 1, 'Conta Corrente': 2, 'Poupança': 3})
for score, prod in r['recomendacoes']:
    print(f"  → {prod} (score: {score:.4f})")
if r['proposta_qf']:
    p = r['proposta_qf']
    print(f"  Proposta QF: {p['taxa_qf']*100:.4f}% a.m.")

print("\n" + "=" * 55)
print("Teste concluído com sucesso.")
```

**Como executar:**
```bash
cd /home/sadmin/rs
python testar_recomendacoes.py
```

---

## 8. Sequência de Implementação

Seguir nesta ordem para evitar erros de importação:

```
1. recomendacaoOF.py         (sem dependências)
2. recomendacaoOF2.py        (importa recomendacaoOF)
3. recomendacaoOF3.py        (importa recomendacaoOF e recomendacaoOF2)
4. recomendacaoOF4.py        (importa recomendacaoOF e recomendacaoOF2 — sqlite3 é built-in)
5. recomendacaoOF5.py        (importa recomendacaoOF e recomendacaoOF3 — requer: requests, pandas)
6. testar_recomendacoes.py   (importa os 5 módulos acima)
7. quantum_finance_sr.ipynb  (integra tudo com visualizações)
```

---

## 9. Decisões de Design

| Decisão | Justificativa |
|---|---|
| 5 módulos separados | Segue a estrutura incremental do professor + camada SQL (Aula 2) + camada API (Market Intelligence) |
| `sqlite3` embutido (':memory:') | Sem dependência externa — sqlite3 é built-in do Python 3 |
| `setdefault` para acumular scores | Mais Pythônico do que verificar `if p in dict` antes de somar |
| Normalização por `total_sim` | Corrige viés de produtos recomendados por muitos vizinhos vs. poucos com alta similaridade |
| Guard `if usuario not in clientes` | Previne KeyError — segue padrão da `euclidiana` com exceptions |
| `round(..., 4)` nos scores | Consistência com o output do professor no `08_TestandoGetSimilares.txt` |
| `MAX(0, quantidadeLikes - 1)` no dislike | Evita likes negativos no banco |
| tbClienteSimilaridade populada pelo Python | Integração explícita CF → SQL: Python calcula, SQL armazena e consulta |
| `verify=False` no requests (Módulo 5) | Equivalente ao `curl -k` — aceitável para Open Data público; NUNCA em APIs com dados de clientes |
| Fallback com taxas reais (Módulo 5) | Garante execução do notebook mesmo sem acesso à internet |
| try/finally em `recomendar_adhoc` | Garante remoção do perfil temporário mesmo em caso de excessão — sem efeito colateral no dataset |
| Proposta QF = melhor_taxa × 0.95 | Regra de negócio: 5% abaixo do mercado; centralizada em `DESCONTO_QF` para fácil ajuste |

---

## 10. Extensões Futuras (não implementar agora)

- **Filtro de elegibilidade:** antes de recomendar Crédito Consignado, verificar se o cliente tem vínculo empregatício ativo (dado disponível no Open Finance — `/consents/v2` com `EMPLOYEES_DATA`)
- **Persistência:** substituir o dict Python por PostgreSQL ou MongoDB
- **API REST:** expor `getRecomendacoes` como endpoint Flask/FastAPI
- **Similaridade de Cosseno:** implementar como função alternativa em `recomendacaoOF2.py` para comparação
- **Avaliação de qualidade:** implementar métricas de Precision@K e Recall@K quando o dataset escalar

---

## Referências
- Material da aula: `material_aula/` (todos os arquivos .txt)
- PDF disciplina: `material_aula/RecommendationSystems.pdf` — p. 100-110 (hands-on SQLite/Knowledge-Based), p. 83-86 (abordagens híbridas)
- Dataset base: `dataset/01_DataSetOpenFinance.txt`
- APIs Open Finance (Open Data, sem autenticação):
  - Participantes: `https://data.directory.openbankingbrasil.org.br/participants`
  - Itaú base: `https://api.itau`
  - Caixa base: `https://api.openbanking.caixa.gov.br`
  - XP base: `https://banking-openfinance.xpi.com.br`
  - PicPay base: `https://resources.openbanking.picpay.com`
- Spec do protótipo: `planejamento./03_prototipo.md`
- Enunciado: `descricao/trabalho.txt`
