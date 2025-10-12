# Catálogo de Dados - Credit Score Classification

## Informações Gerais do Dataset

- **Nome**: Credit Score Classification Dataset
- **Fonte**: Kaggle - https://www.kaggle.com/datasets/parisrohan/credit-score-classification
- **Autor**: Paris Rohan
- **Objetivo**: Classificação de score de crédito baseado em características financeiras e comportamentais
- **Tipo de Problema**: Classificação Multiclasse
- **Formato**: CSV (Comma Separated Values)

## Estrutura do Dataset

- **Arquivo Principal**: `test.csv`
- **Número de Registros**: 50.000 registros (50.001 linhas incluindo cabeçalho)
- **Número de Características**: 27 colunas
- **Tamanho do Arquivo**: ~15.4 MB
- **Moeda de Referência**: USD (Dólares Americanos) para valores monetários

## Dicionário de Dados

### Variáveis de Identificação
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `ID` | String | Identificação única de uma entrada no dataset |
| `Customer_ID` | String | Identificação única de uma pessoa/cliente |
| `Name` | String | Nome da pessoa |
| `SSN` | String | Número de Seguro Social da pessoa |

### Variáveis Demográficas e Temporais
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `Month` | String | Mês do ano de referência dos dados |
| `Age` | Integer | Idade da pessoa |
| `Occupation` | String | Profissão da pessoa |

### Variáveis Financeiras - Renda e Investimentos
| Campo | Tipo | Descrição | Unidade |
|-------|------|-----------|---------|
| `Annual_Income` | Float | Renda anual da pessoa | USD |
| `Monthly_Inhand_Salary` | Float | Salário base mensal da pessoa | USD |
| `Amount_invested_monthly` | Float | Valor mensal investido pelo cliente | USD |
| `Monthly_Balance` | Float | Saldo mensal do cliente | USD |

### Variáveis de Contas Bancárias e Cartões
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `Num_Bank_Accounts` | Integer | Número de contas bancárias que a pessoa possui |
| `Num_Credit_Card` | Integer | Número de outros cartões de crédito mantidos pela pessoa |
| `Interest_Rate` | Float | Taxa de juros do cartão de crédito |
| `Changed_Credit_Limit` | Float | Mudança percentual no limite do cartão de crédito |
| `Num_Credit_Inquiries` | Integer | Número de consultas de cartão de crédito |

### Variáveis de Empréstimos
| Campo | Tipo | Descrição | Unidade |
|-------|------|-----------|---------|
| `Num_of_Loan` | Integer | Número de empréstimos obtidos do banco | - |
| `Type_of_Loan` | String | Tipos de empréstimos obtidos pela pessoa | - |
| `Total_EMI_per_month` | Float | Pagamentos EMI mensais | USD |

### Variáveis de Comportamento de Pagamento
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `Delay_from_due_date` | Integer | Número médio de dias de atraso da data de pagamento |
| `Num_of_Delayed_Payment` | Integer | Número médio de pagamentos atrasados por uma pessoa |
| `Payment_of_Min_Amount` | String | Se apenas o valor mínimo foi pago pela pessoa (Yes/No) |
| `Payment_Behaviour` | String | Comportamento de pagamento do cliente (em USD) |

### Variáveis de Histórico e Utilização de Crédito
| Campo | Tipo | Descrição | Unidade |
|-------|------|-----------|---------|
| `Credit_Mix` | String | Classificação da mistura de créditos | - |
| `Outstanding_Debt` | Float | Dívida restante a ser paga | USD |
| `Credit_Utilization_Ratio` | Float | Taxa de utilização do cartão de crédito | Percentual |
| `Credit_History_Age` | String | Idade do histórico de crédito da pessoa | - |

## Problemas de Qualidade dos Dados Identificados

### 1. **Valores Ausentes**
- Campos com valores vazios ou em branco
- Exemplo: `Monthly_Inhand_Salary` vazio em algumas linhas
- `Num_of_Delayed_Payment` com valores ausentes

### 2. **Valores Inconsistentes/Corrompidos**
- **SSN**: Valores mascarados como "#F%$D@*&8"
- **Age**: Valores com sufixos como "24_"
- **Occupation**: Valores mascarados como "_______"
- **Num_of_Delayed_Payment**: Valores com sufixos como "2_"
- **Credit_Mix**: Valores substituídos por "_"
- **Payment_Behaviour**: Valores corrompidos como "!@9#%8"

### 3. **Formato Inconsistente**
- Diferentes formatos de string para campos numéricos
- Campos categóricos com valores não padronizados

## Variável Target (Não Identificada no Arquivo Atual)

⚠️ **Nota Importante**: O arquivo `test.csv` analisado não contém a variável target (classificação do score de crédito). Tipicamente, em problemas de classificação de score de crédito, as classes seriam:
- Poor/Bad Credit Score
- Standard Credit Score  
- Good Credit Score

É provável que exista um arquivo de treino separado (`train.csv`) que contenha a variável target.

## Recomendações para Pré-processamento

1. **Limpeza de Dados**:
   - Tratar valores mascarados/corrompidos
   - Padronizar formatos de campos numéricos
   - Remover sufixos desnecessários

2. **Tratamento de Valores Ausentes**:
   - Estratégias de imputação baseadas no contexto
   - Análise de padrões de missingness

3. **Engenharia de Features**:
   - Extrair informações numéricas de campos como `Credit_History_Age`
   - Criar variáveis derivadas de razões financeiras
   - Padronizar categorias em campos como `Payment_Behaviour`

4. **Validação de Dados**:
   - Verificar consistência entre campos relacionados
   - Identificar outliers em variáveis financeiras

## Casos de Uso

Este dataset é adequado para:
- **Classificação de Score de Crédito**: Modelo principal
- **Análise de Risco de Crédito**: Identificação de padrões de risco
- **Segmentação de Clientes**: Baseada em comportamento financeiro
- **Detecção de Anomalias**: Identificação de padrões suspeitos
- **Análise Preditiva**: Previsão de comportamento de pagamento

---

**Data de Criação**: 12 de Outubro de 2025  
**Versão**: 1.0  
**Responsável**: Projeto Integrado ML