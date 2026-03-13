# Entregável 2 — Desenho Técnico da Arquitetura
## Especificação para Quantum Finance — Recommendation System

---

## Objetivo deste arquivo

Este documento é o guia de referência para a construção do **desenho técnico de arquitetura** da solução de SR.
Descreve as camadas, componentes, fluxo de dados e justificativas técnicas para serem usadas como base no draw.io, Lucidchart, PowerPoint ou qualquer ferramenta de diagramação.

---

## 1. Visão Geral da Arquitetura (Abordagem Híbrida + Market Intelligence)

A solução é composta por **5 camadas**, adicionando Market Intelligence via APIs reais do Open Finance:

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                          QUANTUM FINANCE — SR HÍBRIDO + MARKET INTELLIGENCE              │
│                                                                                          │
│ ┌─────────────┐  ┌───────────────────┐  ┌────────────────────┐  ┌──────────────────────┐│
│ │ DATA LAYER  │─▶│  PROCESSING L1    │─▶│  PROCESSING L2     │─▶│  PROCESSING L3       ││
│ │ (Dataset    │  │  Python · CF      │  │  SQLite · Knowledge│  │  Open Finance APIs   ││
│ │  OFin)      │  │  Propensidade     │  │  Based+Popularidade│  │  Market Intelligence ││
│ └─────────────┘  └───────────────────┘  └────────────────────┘  └──────────┬───────────┘│
│                                                                             │            │
│                                          ┌──────────────────────────────────▼──────────┐│
│                                          │         PRESENTATION LAYER                  ││
│                                          │  BATCH: Lista de Contato (DataFrame)         ││
│                                          │  AD-HOC: Perfil → Recomendação + Comparativo││
│                                          └─────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Camadas Detalhadas

### Camada 1 — DATA LAYER (Dados de Entrada)

**Responsabilidade:** Armazenar e fornecer o dataset de clientes e produtos.

**Componentes:**

| Componente | Descrição | Arquivo/Módulo |
|---|---|---|
| Dataset Open Finance | Dicionário Python com clientes e seus produtos com scores de uso | `recomendacaoOF.py` |
| Clientes | Ana, Marcos, Pedro, Claudia (representam correntistas com dados via Open Finance) | `clientes = {...}` |
| Produtos Financeiros | Cartão de Crédito, Conta Corrente, Poupança, Renda Fixa, Crédito Pessoal, Renda Variável | chaves do dicionário |
| Score de Uso | Valor numérico que representa a intensidade de uso/interesse do cliente pelo produto (1–7) | valores do dicionário |

**Diagrama desta camada:**

```
Open Finance (consentimento do cliente)
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  Dataset (Python dict)                                   │
│                                                          │
│  'Ana':    { Cartão: 1, Conta: 2, Poupança: 3,          │
│              Renda Fixa: 4, Crédito Pessoal: 5 }        │
│  'Marcos': { Cartão: 2, Conta: 3, Poupança: 4,          │
│              Renda Fixa: 5, Renda Variável: 0.6 }       │
│  'Pedro':  { Cartão: 3, Conta: 4, Poupança: 5,          │
│              Crédito Pessoal: 7 }                        │
│  'Claudia':{ Cartão: 4, Conta: 5, Poupança: 6 }         │
└─────────────────────────────────────────────────────────┘
```

---

### Camada 2 — PROCESSING LAYER 1: Python · Filtro Colaborativo

**Responsabilidade:** Calcular similaridade entre usuários e gerar as recomendações ponderadas.

**Componentes e Funções:**

```
┌──────────────────────────────────────────────────────────────────┐
│              PROCESSING LAYER 1 — Python                         │
│                                                                  │
│   euclidiana()   →   similaridade()   →   getSimilares()        │
│                                              │                   │
│                                              ▼                   │
│                                    getRecomendacoes()           │
│                                    (weighted score)             │
│                                              │                   │
│                              Exporta scores para BD SQLite ──▶  │
└──────────────────────────────────────────────────────────────────┘
```

**Algoritmo de `getRecomendacoes()` — passo a passo:**

```
1. Obter lista de vizinhos ordenados por similaridade via getSimilares(usuario)
2. Para cada vizinho (sim, outro):
   a. Para cada produto que o vizinho possui:
      - Se o usuario-alvo NÃO possui esse produto:
        * Acumula: scores[produto] += sim * rating_do_vizinho
        * Acumula: total_sim[produto] += sim
3. Para cada produto acumulado:
   - weighted_score[produto] = scores[produto] / total_sim[produto]
4. Ordenar produtos por weighted_score (decrescente)
5. Retornar lista: [(weighted_score, produto), ...]
6. Persistir scores de similaridade no SQLite (tbClienteSimilaridade)
```

---

### Camada 3 — PROCESSING LAYER 2: SQLite · Knowledge-Based + Popularidade

**Responsabilidade:** Persistir os scores de similaridade calculados pelo Python e aplicar recomendação baseada em conhecimento com ranqueamento por popularidade — conforme Hands-on Aula 2.

**Modelo de dados (SQLite):**

```
┌──────────────────────────────────────────────────────────────────────┐
│                        MODELO DE DADOS                               │
│                                                                      │
│  tbCliente              tbProduto                                    │
│  ┌───────────┐          ┌───────────────────┬──────────────┐        │
│  │nomeCliente│          │ nomeProduto       │quantidadeLikes│       │
│  └───────────┘          └───────────────────┴──────────────┘        │
│        │                          │                                  │
│        ▼                          ▼                                  │
│  tbClienteProduto          tbClienteSimilaridade                     │
│  ┌────────────┬────────────┬──────┐  ┌──────────┬──────────┬──────┐ │
│  │nomeCliente │nomeProduto │valor │  │ origem   │ destino  │ sim  │ │
│  └────────────┴────────────┴──────┘  └──────────┴──────────┴──────┘ │
└──────────────────────────────────────────────────────────────────────┘
```

**Queries SQL para recomendação:**

```sql
-- Passo 1: Encontrar o cliente mais similar ao cliente-alvo (ex: 'Ana')
SELECT * FROM tbClienteSimilaridade
WHERE nomeClienteOrigem = 'Ana'
ORDER BY similaridade DESC
LIMIT 1;

-- Passo 2: Recomendar produto que o vizinho possui e o cliente-alvo NÃO possui
SELECT b.* FROM tbCliente a, tbClienteProduto b, tbProduto c
WHERE a.nomeCliente = b.nomeCliente AND b.nomeProduto = c.nomeProduto
  AND b.nomeCliente = 'Marcos'   -- vizinho mais similar de Ana
  AND b.nomeProduto NOT IN (
    SELECT b.nomeProduto FROM tbClienteProduto b
    WHERE b.nomeCliente = 'Ana'
  );

-- Passo 3: Ranquear produtos por Popularidade (quantidadeLikes)
SELECT * FROM tbProduto ORDER BY quantidadeLikes DESC;

-- Passo 4 (feedback): Incrementar/decrementar likes
UPDATE tbProduto SET quantidadeLikes = quantidadeLikes + 1
WHERE nomeProduto = 'Cartão de Crédito';
```

---

### Camada 4 — PROCESSING LAYER 3: Open Finance APIs · Market Intelligence ★ NOVO

**Responsabilidade:** Consultar taxas de mercado reais de 4 IFs, gerar proposta QF 5% abaixo da melhor taxa.

**Mapeamento Produto SR → Endpoint Open Finance:**

| Produto SR | Endpoint | IFs consultadas |
|---|---|---|
| Crédito Pessoal | `/open-banking/opendata-loans/v1/personal-loans` | Itaú, Caixa, XP, PicPay |
| Cartão de Crédito | `/open-banking/opendata-creditcards/v1/personal-credit-cards` | Itaú, Caixa, XP, PicPay |
| Seguro | `/open-banking/opendata-insurance/v2/personals` | Itaú, Caixa, XP, PicPay |

**URLs reais (confirmadas no diretório Open Finance):**
```python
BANCOS = {
    'Itaú':   'https://api.itau',
    'Caixa':  'https://api.openbanking.caixa.gov.br',
    'XP':     'https://banking-openfinance.xpi.com.br',
    'PicPay': 'https://resources.openbanking.picpay.com'
}
```

**Estrutura real de resposta — personal-loans (XP, verificado):**
```json
{
  "data": [{
    "participant": { "brand": "Banco XP" },
    "type": "EMPRESTIMO_CREDITO_PESSOAL_CONSIGNADO",
    "interestRates": [{
      "referentialRateIndexer": "PRE_FIXADO",
      "minimumRate": "0.010000",
      "maximumRate": "0.040000"
    }]
  }]
}
```
> `minimumRate: 0.01` = 1% a.m. | `maximumRate: 0.04` = 4% a.m.

**Lógica de proposta QF:**
```
taxa_qf = min(minimumRates_coletadas) * 0.95   # 5% abaixo da melhor taxa de mercado
```

**Fallback:** Se a API não responder em 8s → usar mock data com taxas fictícias realistas.

---

### Camada 5 — PRESENTATION LAYER (Dois Modos de Saída) ★ NOVO

**Responsabilidade:** Apresentar as recomendações em dois modos operacionais.

**Modo 1 — BATCH: Lista de Contato (time comercial)**

```
┌─────────────┬─────────────────────┬────────────┬────────────────┬──────────────┬──────────┐
│ Cliente     │ Produto Recomendado │ Propensão  │ Melhor Mercado │ Proposta QF  │Prioridade│
├─────────────┼─────────────────────┼────────────┼────────────────┼──────────────┼──────────┤
│ Claudia     │ Crédito Pessoal     │ 3.61       │ 1.80% a.m.     │ 1.71% a.m.   │ ALTA     │
│ Pedro       │ Renda Fixa          │ 4.41       │ CDI + 1%       │ CDI + 0.95%  │ ALTA     │
│ Ana         │ Renda Variável      │ 0.25       │ -              │ -            │ BAIXA    │
│ Marcos      │ Crédito Pessoal     │ 2.80       │ 1.80% a.m.     │ 1.71% a.m.   │ MÉDIA    │
└─────────────┴─────────────────────┴────────────┴────────────────┴──────────────┴──────────┘
```

**Modo 2 — AD-HOC: Perfil → Recomendação Instantânea**
```
Input: { 'Cartão de Crédito': 1, 'Conta Corrente': 2, 'Poupança': 3 }
   → CF calcula: cliente mais parecido com Claudia
   → Output: "Recomendamos Crédito Pessoal"
   → Busca mercado: Itaú 2.1% | Caixa 1.9% | XP 1.8% | PicPay 2.3%
   → Proposta QF: 1.71% a.m. (5% abaixo da XP)
   → Tabela comparativa exibida no notebook
```

---

## 3. Fluxo Completo de Dados

```
┌──────────────┐
│  CLIENTE     │  Ex: "Claudia"
│  (Input)     │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────────────────┐
│  DATA LAYER                                          │
│  Buscar perfil de Claudia no dataset                 │
│  Claudia: { Cartão: 4, Conta: 5, Poupança: 6 }      │
└──────┬───────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────┐
│  PROCESSING LAYER 1 — Python · Filtro Colaborativo   │
│  euclidiana('Claudia', 'Pedro')  = 2.73              │
│  similaridade('Claudia', 'Pedro') = 0.37 (maior)     │
│  getRecomendacoes('Claudia') →                       │
│    1. Crédito Pessoal (score ponderado maior)        │
│    2. Renda Fixa                                     │
│    3. Renda Variável                                 │
│  → Persiste scores em tbClienteSimilaridade (SQLite) │
└──────┬───────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────┐
│  PROCESSING LAYER 2 — SQLite · Knowledge-Based       │
│  Query: vizinho mais similar = Pedro                 │
│  Produtos de Pedro que Claudia NÃO tem:              │
│    → Crédito Pessoal (valor: 7)                      │
│  Ranqueamento por popularidade (quantidadeLikes):    │
│    → Conta Corrente: 3 likes (mais popular)          │
│    → Crédito Pessoal: 2 likes                        │
│    → Cartão de Crédito: 1 like                       │
└──────┬───────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────┐
│  PRESENTATION LAYER                                  │
│  CF recomenda: [Crédito Pessoal, Renda Fixa]         │
│  Knowledge-Based ranqueia por popularidade           │
│  Recomendação final apresentada no Jupyter Notebook  │
└──────────────────────────────────────────────────────┘
```

---

## 4. Justificativa Técnica das Escolhas

### Por que Abordagem Híbrida (CF + Knowledge-Based)?

Conforme PDF da disciplina (p. 83-86), a abordagem híbrida equilibra os pontos fracos de técnicas isoladas:

| Problema isolado | Técnica que resolve |
|---|---|
| Cold Start (cliente novo sem histórico) | Popularidade (`quantidadeLikes`) — Knowledge-Based |
| Previsibilidade (sempre o mesmo produto) | CF diversifica por perfis de vizinhos |
| Falta de conhecimento do usuário | CF usa comportamento implícito de vizinhos similares |

### Por que User-Based Collaborative Filtering?

| Critério | Justificativa |
|---|---|
| **Natureza dos dados** | Dados de comportamento de consumo de produtos (implícito ao perfil via Open Finance) — CF é nativo para esse tipo |
| **Tamanho do dataset** | Dataset pequeno (PoC) — User-Based CF não exige grande volume para funcionar |
| **Interpretabilidade** | "Clientes com perfil similar ao seu também usam X" — discurso natural para o cliente final |
| **Alinhamento com aula** | Técnica ensinada pelo professor com os exemplos de dataset idênticos |
| **Custo de implementação** | Implementável em Python puro (math.sqrt), sem dependências externas críticas |

### Por que Distância Euclidiana?

| Critério | Justificativa |
|---|---|
| **Espaço de features** | Os scores de produtos são valores contínuos em escala comparável — Euclidiana é adequada |
| **Intuição geométrica** | Fácil de explicar: "distância no espaço de produtos financeiros" |
| **Base do professor** | Garante alinhamento com o material da disciplina |
| **Limitação conhecida** | Sensível à escala — mitigado pelo fato de que os scores já estão em escala similar (0–7) |

### Alternativas consideradas (e por que não usamos agora)

| Técnica | Motivo de não usar nesta PoC |
|---|---|
| Pearson Correlation | Boa para rating explícito — exigiria mais dados por par de usuário |
| Cosine Similarity | Melhor quando a escala varia muito — dataset atual é pequeno e bem calibrado |
| Matrix Factorization (SVD) | Exige biblioteca (scikit-learn/surprise) e dataset maior para convergir |
| Content-Based Filtering | Necessita features dos produtos (taxa, prazo, risco) — não disponíveis no dataset atual |

---

## 5. Guia para Criar o Desenho no draw.io / PowerPoint

### Elementos visuais recomendados:

- **4 caixas em sequência horizontal** (Data Layer → Python CF → SQLite Knowledge-Based → Output)
- **Setas direcionais** entre camadas (esquerda → direita)
- **Cores sugeridas:**
  - Data Layer: azul (#1E3A5F ou similar a azul Open Finance)
  - Python CF Layer: cinza escuro / roxo tecnológico
  - SQLite Knowledge-Based: laranja / amber (diferencia da camada Python)
  - Output: verde (#1B5E20) representando resultado
- **Ícones sugeridos:** banco/card (Data), Python logo (CF), banco de dados (SQLite), gráfico (Output)
- **Legenda das técnicas:**
  - Camada Python: `euclidiana`, `similaridade`, `getSimilares`, `getRecomendacoes`
  - Camada SQLite: `tbCliente`, `tbProduto`, `tbClienteProduto`, `tbClienteSimilaridade`, `quantidadeLikes`

### Referência visual: Estudo de Caso do Professor (Santander — PDF p. 92)
O professor apresentou um diagrama com 3 componentes numerados (1, 2, 3) para o caso Santander/Open Finance — use como referência de nível de detalhe esperado pelo professor para o desenho técnico.

### Estrutura sugerida para o slide de arquitetura:
1. Título: "Arquitetura do Sistema de Recomendação — Quantum Finance"
2. Diagrama das 4 camadas (horizontal, da esquerda para direita)
3. Caixa de destaque: "Abordagem Híbrida: User-Based CF + Knowledge-Based"
4. Sub-nota: "Implementado em Python + SQLite como Prova de Conceito"

---

## Referências
- Material da aula: `material_aula/` (todos os arquivos .txt)
- PDF disciplina: `material_aula/RecommendationSystems.pdf` — p. 83-86 (abordagens híbridas), p. 100-110 (hands-on SQLite), p. 92 (arquitetura Santander)
- Dataset: `dataset/01_DataSetOpenFinance.txt`
- Spec do protótipo: `planejamento./03_prototipo.md`
- Enunciado: `descricao/trabalho.txt`

