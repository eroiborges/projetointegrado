# Quantum Finance — Sistema de Recomendação Open Finance

**PoC · User-Based Collaborative Filtering + Knowledge-Based (SQLite) + Market Intelligence (Open Finance APIs)**

---

## Visão Geral

A Quantum Finance é uma Fintech especializada em **crédito pessoal e consignado**. Este protótipo demonstra um **Sistema de Recomendação** híbrido em 3 camadas que utiliza dados do Open Finance para recomendar produtos financeiros personalizados e gerar propostas de taxa 5% abaixo do mercado.

```
┌─────────────────────────────────────────────────────────┐
│           QUANTUM FINANCE — SR HÍBRIDO                  │
├─────────────────────────────────────────────────────────┤
│  Camada 1: User-Based CF  (Distância Euclidiana)        │
│  Camada 2: Knowledge-Based (SQLite + Popularidade)      │
│  Camada 3: Market Intelligence (APIs Open Finance)      │
│            → Proposta QF: melhor_taxa × 0.95 (−5%)      │
└─────────────────────────────────────────────────────────┘
```

---

## Estrutura do Projeto

```
./rs/
├── quantum_finance_sr.ipynb          ← Notebook principal (4 clientes, pedagógico)
├── quantum_finance_sr_100.ipynb      ← Notebook escala (100 clientes, 7 produtos)
├── quantum_finance_lista_contato_100.csv  ← Exportação batch gerada pelo 2º notebook
├── README.md                         ← Este arquivo
├── src/
│   ├── recomendacaoOF.py             ← Módulo 1: Dataset (4 clientes)
│   ├── recomendacaoOF2.py            ← Módulo 2: euclidiana + similaridade + getSimilares
│   ├── recomendacaoOF3.py            ← Módulo 3: getRecomendacoes (CF)
│   ├── recomendacaoOF4.py            ← Módulo 4: Knowledge-Based + SQLite
│   └── recomendacaoOF5.py            ← Módulo 5: APIs Open Finance + Batch + Ad-hoc
├── dataset/
    ├── 01_DataSetOpenFinance.txt     ← Dataset original do professor (4 clientes)
    └── 02_DataSet100Clientes.txt     ← Dataset gerado (100 clientes, 6 perfis, seed=42)

```

---

## Pré-requisitos

```bash
# Python 3.10+
pip install jupyter pandas matplotlib seaborn requests
# sqlite3 já vem na biblioteca padrão do Python
```

---

## Como Executar os Notebooks

```bash
cd ./rs/

# ── Notebook principal (4 clientes) ──────────────────────────────────────
# Opção A — Jupyter Notebook clássico
jupyter notebook quantum_finance_sr.ipynb

# Opção B — Headless (executar e salvar com outputs)
jupyter nbconvert --to notebook --execute quantum_finance_sr.ipynb \
  --output quantum_finance_sr.ipynb

# ── Notebook de escala (100 clientes) ─────────────────────────────────────
# Opção A — Jupyter Notebook clássico
jupyter notebook quantum_finance_sr_100.ipynb

# Opção B — Headless
jupyter nbconvert --to notebook --execute quantum_finance_sr_100.ipynb \
  --output quantum_finance_sr_100.ipynb
```

No Jupyter: **Cell → Run All** para executar todas as células em sequência.

---

## Dataset

O dataset usa um **score de engajamento** por produto (escala 1–7):

| Score | Interpretação |
|---|---|
| 1–2 | Uso esporádico / baixo engajamento |
| 3–4 | Uso moderado |
| 5–6 | Uso intenso — produto principal |
| 7 | Produto âncora — máxima fidelidade |
| **ausente** | **Não possui → candidato à recomendação** |

**Dataset do professor** (`01_DataSetOpenFinance.txt`): 4 clientes · 5 produtos  
**Dataset PoC** (`02_DataSet100Clientes.txt`): 100 clientes · 7 produtos · `random.seed(42)`

---

## APIs Open Finance Utilizadas

| IF | Base URL | Endpoint |
|---|---|---|
| Itaú | `https://api.itau` | `/open-banking/opendata-loans/v1/personal-loans` |
| Caixa | `https://api.openbanking.caixa.gov.br` | `/open-banking/opendata-loans/v1/personal-loans` |
| XP | `https://banking-openfinance.xpi.com.br` | `/open-banking/opendata-loans/v1/personal-loans` |
| PicPay | `https://resources.openbanking.picpay.com` | `/open-banking/opendata-loans/v1/personal-loans` |

**Taxas reais coletadas (Mar/2026) — Crédito Pessoal Consignado PRE_FIXADO:**

| IF | Taxa mínima |
|---|---|
| Itaú | 1,00% a.m. |
| XP | 1,00% a.m. |
| PicPay | 1,24% a.m. |
| Caixa | 3,10% a.m. |

**Proposta Quantum Finance:** `1,00% × 0,95 = 0,95% a.m.`

> As APIs são Open Data públicas (sem autenticação). O fallback garante funcionamento mesmo sem internet.

---

## Exemplos de Teste

### Exemplo 1 — Distância e Similaridade entre clientes

```python
from math import sqrt

# Dataset
clientes = {
    'Ana':   {'Cartão de Crédito': 1, 'Conta Corrente': 2, 'Poupança': 3, 'Renda Fixa': 4, 'Crédito Pessoal': 5},
    'Marcos':{'Cartão de Crédito': 2, 'Conta Corrente': 3, 'Poupança': 4, 'Renda Fixa': 5, 'Renda Variável': 0.6},
    'Pedro': {'Cartão de Crédito': 3, 'Conta Corrente': 4, 'Poupança': 5, 'Crédito Pessoal': 7},
    'Claudia':{'Cartão de Crédito': 4, 'Conta Corrente': 5, 'Poupança': 6}
}

def euclidiana(u1, u2):
    si = {i: 1 for i in clientes[u1] if i in clientes[u2]}
    if not si: return -3
    return sqrt(sum(pow(clientes[u1][i] - clientes[u2][i], 2) for i in si))

def similaridade(u1, u2):
    d = euclidiana(u1, u2)
    return 0 if d < 0 else 1 / (1 + d)

# Resultados esperados:
print(euclidiana('Ana', 'Marcos'))   # → 2.0
print(euclidiana('Ana', 'Pedro'))    # → 4.0
print(euclidiana('Ana', 'Claudia'))  # → 5.196

print(similaridade('Ana', 'Marcos'))   # → 0.3333
print(similaridade('Ana', 'Pedro'))    # → 0.2000
print(similaridade('Ana', 'Claudia'))  # → 0.1614
```

**Output esperado:**
```
2.0
4.0
5.196152422706632
0.3333333333333333
0.2
0.16130...
```

---

### Exemplo 2 — Recomendação por Filtro Colaborativo

```python
def getSimilares(usuario):
    lista = [(round(similaridade(usuario, o), 4), o) for o in clientes if o != usuario]
    lista.sort(reverse=True)
    return lista

def getRecomendacoes(usuario):
    scores, total_sim = {}, {}
    for sim, vizinho in getSimilares(usuario):
        for produto, rating in clientes[vizinho].items():
            if produto not in clientes[usuario]:
                scores.setdefault(produto, 0)
                total_sim.setdefault(produto, 0)
                scores[produto] += sim * rating
                total_sim[produto] += sim
    recs = [(round(scores[p] / total_sim[p], 4), p) for p in scores]
    recs.sort(reverse=True)
    return recs

# Testar para Claudia (só tem Cartão, Conta, Poupança)
print(getRecomendacoes('Claudia'))
```

**Output esperado:**
```
[(score, 'Crédito Pessoal'), (score, 'Renda Fixa'), (score, 'Renda Variável')]
# Crédito Pessoal lidera pois Pedro (vizinho mais similar, sim=0.37) tem score 7
```

---

### Exemplo 3 — SQLite: Recomendação via SQL + Popularidade

```python
import sqlite3

conn = sqlite3.connect(':memory:')
# (após criar e popular as tabelas conforme Seção 9 do notebook)

# Vizinho mais similar a Claudia (via SQL)
row = conn.execute("""
    SELECT nomeClienteDestino, similaridade
    FROM tbClienteSimilaridade
    WHERE nomeClienteOrigem = 'Claudia'
    ORDER BY similaridade DESC LIMIT 1
""").fetchone()
print(f"Vizinho de Claudia: {row[0]} (sim={row[1]})")
# → Vizinho de Claudia: Pedro (sim=0.366)

# Produto mais popular (cold-start)
popular = conn.execute("""
    SELECT nomeProduto, quantidadeLikes FROM tbProduto
    ORDER BY quantidadeLikes DESC LIMIT 1
""").fetchone()
print(f"Produto mais popular: {popular[0]} ({popular[1]} likes)")
# → Produto mais popular: Conta Corrente (3 likes)
```

---

### Exemplo 4 — Consulta às APIs Open Finance

```python
import requests, warnings
warnings.filterwarnings('ignore')

BANCOS = {
    'Itaú':   'https://api.itau',
    'XP':     'https://banking-openfinance.xpi.com.br',
    'PicPay': 'https://resources.openbanking.picpay.com',
    'Caixa':  'https://api.openbanking.caixa.gov.br',
}
ENDPOINT = '/open-banking/opendata-loans/v1/personal-loans'
TIPO     = 'EMPRESTIMO_CREDITO_PESSOAL_CONSIGNADO'
FALLBACK = {'Itaú': 0.01, 'XP': 0.01, 'PicPay': 0.0124, 'Caixa': 0.031}

taxas = {}
for banco, url in BANCOS.items():
    try:
        resp = requests.get(url + ENDPOINT, verify=False, timeout=8)
        for item in resp.json().get('data', []):
            if item.get('type') == TIPO:
                for r in item.get('interestRates', []):
                    mn = float(r.get('minimumRate', '0'))
                    if mn > 0:
                        taxas[banco] = mn
                        break
    except:
        pass

taxas = taxas or FALLBACK

melhor = min(taxas.values())
print(f"Melhor taxa de mercado: {melhor*100:.2f}% a.m.")
print(f"Proposta QF (−5%)     : {melhor*0.95*100:.4f}% a.m.")
```

**Output esperado:**
```
Melhor taxa de mercado: 1.00% a.m.
Proposta QF (−5%)     : 0.9500% a.m.
```

---

### Exemplo 5 — Modo Ad-hoc: Novo Cliente durante Atendimento

```python
# Simula novo cliente com perfil de iniciante (similar a Claudia)
perfil_novo_cliente = {
    'Conta Corrente':    3,
    'Cartão de Crédito': 2,
    'Poupança':          4,
}

# Adicionar temporariamente e recomendar
chave = '_adhoc_'
clientes[chave] = perfil_novo_cliente
try:
    recomendacoes = getRecomendacoes(chave)
finally:
    del clientes[chave]  # sempre remove — sem efeito colateral

print("Perfil do novo cliente:", list(perfil_novo_cliente.keys()))
print("\nRecomendações:")
for score, produto in recomendacoes:
    print(f"  → {produto:<25} score: {score:.4f}")

# Proposta QF se Crédito Pessoal for o top
if recomendacoes and recomendacoes[0][1] == 'Crédito Pessoal':
    melhor = min(taxas.values())
    print(f"\nProposta Quantum Finance: {melhor*0.95*100:.4f}% a.m. (vs {melhor*100:.2f}% mercado)")
```

**Output esperado:**
```
Perfil do novo cliente: ['Conta Corrente', 'Cartão de Crédito', 'Poupança']

Recomendações:
  → Crédito Pessoal          score: 3.xxxx
  → Renda Fixa               score: 2.xxxx
  → Renda Variável           score: 0.xxxx

Proposta Quantum Finance: 0.9500% a.m. (vs 1.00% mercado)
```

---

### Exemplo 6 — Modo Batch: Lista de Contato Completa

```python
import pandas as pd

# Gerar lista de contato com todos os clientes (executa direto no notebook)
# Após executar as seções 10 e a função gerar_lista_contato():

df = gerar_lista_contato()
print(df.to_string(index=False))
```

**Output esperado:**
```
  Cliente Produto Recomendado  Score CF Taxa Mercado (min) Proposta QF (−5%)          Ação Sugerida
     Ana      Renda Variável    0.3752                 —                 —          📧 Oferta Produto
  Marcos     Crédito Pessoal    3.275        1.00% a.m.    0.9500% a.m.  📞 Oferta Crédito Consignado
   Pedro          Renda Fixa    3.750                 —                 —          📧 Oferta Produto
 Claudia     Crédito Pessoal    3.100        1.00% a.m.    0.9500% a.m.  📞 Oferta Crédito Consignado
```

---

---

## Notebook com 100 Clientes (`quantum_finance_sr_100.ipynb`)

Complemento do notebook principal que aplica o **mesmo algoritmo CF** ao dataset
de 100 clientes / 7 produtos (inclui *Crédito Consignado*) e demonstra o
comportamento do sistema em escala.

| Aspecto                    | `quantum_finance_sr.ipynb` | `quantum_finance_sr_100.ipynb` |
|----------------------------|----------------------------|----------------------------------|
| Clientes                   | 4                          | 100                              |
| Produtos                   | 6                          | 7 (+ Crédito Consignado)          |
| Perfis de cliente          | Manual                     | 6 perfis gerados (`seed=42`)      |
| Heatmap similaridade       | 4 × 4                      | 10 × 10 (amostra estratificada)  |
| Grid de barras             | 2 × 2 (4 clientes)         | 2 × 4 (8 clientes)               |
| Distribuição top-1         | —                          | ✔ (Counter sobre 100 clientes)   |
| Modo Batch / CSV export    | ✔ (4 registros)            | ✔ (100 registros → `*_100.csv`)  |
| Modo Ad-hoc                | ✔ (3 cenários)             | ✔ (3 perfis arquetípicos)        |

### Seções do notebook (17 células)

1. **Dataset 100 clientes** — carrega `02_DataSet100Clientes.txt`, exibe estatísticas e presença por produto  
2. **Funções CF** — mesmas funções com `getSimilares(top_n=None)` para suportar base maior  
3. **Top-5 Vizinhos** — amostra de 5 clientes com seus 5 vizinhos mais similares  
4. **Heatmap 10 × 10** — matriz de similaridade para 10 clientes estratificados  
5. **Grid 2 × 4** — recomendações em barras horizontais para 8 clientes  
6. **Distribuição top-1** — frequência do produto mais recomendado na base completa  
7. **Modo Batch** — proposta QF para todos os 100 clientes → exporta CSV  
8. **Modo Ad-hoc** — 3 perfis arquetípicos (Conservador, Investidor, Consignado)  
9. **Conclusão** — tabela comparativa + próximos passos  

### Exemplo de uso rápido

```python
# Após executar Cell 2 (carrega dataset) e Cell 4 (define funções):
getRecomendacoes('João')   # → [(score, produto), ...]

# Verificar distribuição top-1 (Cell 12):
from collections import Counter
top1 = [getRecomendacoes(c)[0][1] for c in clientes if getRecomendacoes(c)]
print(Counter(top1).most_common(3))
# Ex: [('Crédito Pessoal', 28), ('Renda Fixa', 22), ('Crédito Consignado', 19)]
```

### CSV exportado

O modo batch salva `quantum_finance_lista_contato_100.csv` com as colunas:
`cliente, produto_sugerido, score_cf, melhor_banco, taxa_mercado_am, proposta_qf_am`

```
cliente,produto_sugerido,score_cf,melhor_banco,taxa_mercado_am,proposta_qf_am
Ana,Renda Fixa,4.1599,XP,0.0085,0.008075
Marcos,Crédito Consignado,5.1018,Itaú,0.018,0.0171
Pedro,Crédito Consignado,4.9976,Itaú,0.018,0.0171
...
```

---

## Referências

- Dataset original: `dataset/01_DataSetOpenFinance.txt` (professor)
- Dataset PoC 100 clientes: `dataset/02_DataSet100Clientes.txt`
- PDF da disciplina: `material_aula/RecommendationSystems.pdf` — p. 83-110
- Open Finance OpenData: [https://openfinancebrasil.org.br](https://openfinancebrasil.org.br)
- Diretório de participantes: `https://data.directory.openbankingbrasil.org.br/participants`
