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

## Dicionário de Dados

### Variáveis de Identificação
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `ID` | String | Identificador único do registro (formato: 0x160a, 0x160b, etc.) |
| `Customer_ID` | String | Identificador único do cliente (formato: CUS_0xd40, etc.) |
| `Name` | String | Nome do cliente |
| `SSN` | String | Número de Seguro Social (com possíveis valores mascarados/corrompidos) |

### Variáveis Demográficas
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `Age` | Integer/String | Idade do cliente (alguns valores com sufixos como "24_") |
| `Occupation` | String | Profissão do cliente (Scientist, Teacher, Engineer, etc.) |
| `Month` | String | Mês de referência dos dados (September, October, November, December) |

### Variáveis Financeiras - Renda
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `Annual_Income` | Float | Renda anual do cliente (em unidade monetária não especificada) |
| `Monthly_Inhand_Salary` | Float | Salário líquido mensal |
| `Amount_invested_monthly` | Float | Valor investido mensalmente |
| `Monthly_Balance` | Float | Saldo mensal |

### Variáveis de Contas e Cartões
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `Num_Bank_Accounts` | Integer | Número de contas bancárias |
| `Num_Credit_Card` | Integer | Número de cartões de crédito |
| `Interest_Rate` | Float | Taxa de juros |
| `Changed_Credit_Limit` | Float | Alteração no limite de crédito |
| `Num_Credit_Inquiries` | Float | Número de consultas de crédito |

### Variáveis de Empréstimos
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `Num_of_Loan` | Integer | Número de empréstimos |
| `Type_of_Loan` | String | Tipos de empréstimos (Auto Loan, Credit-Builder Loan, Personal Loan, Home Equity Loan) |
| `Total_EMI_per_month` | Float | Total de EMI (Equated Monthly Installment) por mês |

### Variáveis de Comportamento de Pagamento
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `Delay_from_due_date` | Integer | Dias de atraso da data de vencimento |
| `Num_of_Delayed_Payment` | Integer/String | Número de pagamentos atrasados (alguns valores com sufixos) |
| `Payment_of_Min_Amount` | String | Se paga o valor mínimo (Yes/No) |
| `Payment_Behaviour` | String | Comportamento de pagamento (Low_spent_Small_value_payments, High_spent_Medium_value_payments, etc.) |

### Variáveis de Histórico e Utilização de Crédito
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `Credit_Mix` | String | Mix de crédito (Good, Bad, Standard) |
| `Outstanding_Debt` | Float | Dívida pendente |
| `Credit_Utilization_Ratio` | Float | Taxa de utilização do crédito (em percentual) |
| `Credit_History_Age` | String | Idade do histórico de crédito (formato: "X Years and Y Months") |

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