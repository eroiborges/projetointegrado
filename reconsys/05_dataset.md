# Entregável — Dataset
## Explicação do Score e Documentação do Dataset de 100 Clientes

---

## O que os scores significam

Os valores no dataset representam o **score de engajamento** do cliente com cada produto — uma proxy do uso real que, em produção, viria do Open Finance (frequência de transações, volume utilizado, tempo de uso):

| Score | Interpretação |
|---|---|
| 1–2 | Uso esporádico/baixo — produto pouco utilizado |
| 3–4 | Uso moderado — parte do portfólio regular |
| 5–6 | Uso intenso — produto principal do cliente |
| 7 | Produto âncora — uso muito intenso, máxima fidelidade |
| **ausente** | **Cliente não possui o produto** → candidato para recomendação |

> O `0.6` do Marcos no dataset original é uma peculiaridade do professor (Renda Variável com engajamento mínimo). No novo dataset foram usados apenas inteiros 1–7 para clareza.

---

## Dataset gerado: `dataset/02_DataSet100Clientes.txt`

**712 linhas · sintaxe Python válida · `random.seed(42)` (reproduzível)**

| Característica | Valor |
|---|---|
| Clientes | 100 |
| Produtos | 7 (`+Crédito Consignado` vs. dataset original) |
| Score médio | 4,12 |
| Média de produtos/cliente | 3,8 |
| Conta Corrente | 96% dos clientes |
| Crédito Consignado | 43% dos clientes ← foco QF |
| Crédito Pessoal | 38% dos clientes ← foco QF |

---

## Perfis de Clientes

| Perfil | Qtd | Características |
|---|---|---|
| Crédito Pessoal | 25 | foco em crédito PF + consignado |
| Conservador | 20 | Conta + Poupança + Cartão |
| Crédito Consignado | 20 | servidor público / aposentado |
| Investidor | 15 | Renda Fixa + Renda Variável |
| Básico | 10 | 2-3 produtos, iniciante |
| Misto | 10 | portfólio diversificado |

---

## Produtos disponíveis (7 total)

| Produto | Presente em |
|---|---|
| Conta Corrente | 96% dos clientes |
| Cartão de Crédito | 88% dos clientes |
| Poupança | 65% dos clientes |
| Crédito Consignado | 43% dos clientes |
| Crédito Pessoal | 38% dos clientes |
| Renda Fixa | 29% dos clientes |
| Renda Variável | 21% dos clientes |

---

## Como usar no notebook

```python
# Opção 1 — carregar diretamente (sem módulo separado)
exec(open('dataset/02_DataSet100Clientes.txt').read())

# Opção 2 — substituir import no recomendacaoOF.py
# Editar recomendacaoOF.py e trocar o dict de 4 clientes pelo de 100
```

---

## Comparação com dataset do professor

| Característica | Dataset Professor | Dataset PoC (100 clientes) |
|---|---|---|
| Clientes | 4 | 100 |
| Produtos | 5 | 7 |
| Crédito Consignado | ✗ | ✓ |
| Scores | 0.6–7 (float) | 1–7 (inteiro) |
| Perfis | implícitos | explícitos (6 perfis) |
| Reproduzível | N/A | `random.seed(42)` |

---

## Referências
- Dataset original do professor: `dataset/01_DataSetOpenFinance.txt`
- Dataset gerado: `dataset/02_DataSet100Clientes.txt`
- Enunciado: `descricao/trabalho.txt`
