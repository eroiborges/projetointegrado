# Plano de Execução - Trabalho Final ML

## 📋 Análise do Escopo

### **Contexto do Projeto**
- **Empresa**: Quantum Finance (simulação)
- **Papel**: Time de analistas
- **Dataset**: Credit Score Classification (Kaggle)
- **Objetivo**: Criar sistema de valor através de análise de dados e ML

### **Problema Identificado**
❌ **Issue crítica**: O arquivo disponível (`test.csv`) não contém a variável target (Credit Score). 
- Precisamos da variável de classificação (Poor/Standard/Good Credit Score)
- O trabalho exige treino com `train.csv` que não está disponível

---

## 🎯 Plano de Execução (4 Etapas - 10 pontos)

### **1. Análise Exploratória de Dados (EDA) - 2 pontos**

#### **1.1 Análise Descritiva**
```python
# Estatísticas descritivas
- Shape do dataset
- Tipos de dados
- Valores ausentes
- Distribuições univariadas
- Outliers
```

#### **1.2 Análise Bivariada**
```python
# Correlações e relações
- Matriz de correlação
- Análise por variáveis categóricas (Credit_Mix, Payment_Behaviour)
- Relações entre variáveis financeiras
- Segmentação por ocupação/idade
```

#### **1.3 Visualizações**
```python
# Gráficos exploratórios
- Histogramas das variáveis numéricas
- Box plots para identificar outliers
- Scatter plots das principais relações
- Mapas de calor para correlações
```

### **2. Pipeline de Modelos - 4 pontos**

#### **2.1 Estratégia para Falta de Target**
Duas opções:
1. **Criar target sintético** baseado em regras de negócio
2. **Focar em análise não supervisionada** (clustering de perfis de crédito)

#### **2.2 Implementação dos Modelos**
```python
# Modelos requeridos
1. Random Forest
2. XGBoost  
3. LightGBM

# Com GridSearch para otimização
- Random Forest: n_estimators, max_depth, min_samples_split
- XGBoost: learning_rate, max_depth, n_estimators, reg_alpha
- LightGBM: num_leaves, learning_rate, n_estimators, reg_alpha
```

#### **2.3 Pipeline Completo**
```python
# Pré-processamento
- Tratamento de valores missing
- Encoding de variáveis categóricas
- Normalização/padronização
- Feature engineering

# Validação cruzada
- StratifiedKFold para classificação
- Métricas consistentes
```

### **3. Avaliação e Métricas - 2 pontos**

#### **3.1 Escolha da Métrica Principal**
Para classificação de crédito:
- **F1-Score macro**: Balanceia precision/recall para todas as classes
- **AUC-ROC**: Para análise de probabilidades
- **Justificativa**: Custo balanceado entre falsos positivos/negativos

#### **3.2 Análise Comparativa**
```python
# Comparação dos modelos
- Performance em treino vs validação
- Tempo de treinamento
- Interpretabilidade
- Feature importance
```

### **4. Resultados e Aplicação - 2 pontos**

#### **4.1 Interpretação dos Resultados**
- Principais features que influenciam score de crédito
- Insights de negócio
- Padrões identificados

#### **4.2 Aplicação para Decisões Financeiras**
```python
# Sistema de valor
- Automação de aprovação de crédito
- Definição de limites personalizados
- Identificação de clientes de risco
- Estratégias de retenção
```

---

## 🚨 Ações Imediatas Necessárias

### **Opção 1: Criar Target Sintético**
```python
def create_synthetic_target(df):
    # Regras baseadas em características financeiras
    conditions = [
        (df['Credit_Mix'] == 'Poor') | (df['Payment_Behaviour'].str.contains('Low')),
        (df['Credit_Mix'] == 'Good') & (df['Payment_Behaviour'].str.contains('High')),
    ]
    choices = ['Poor', 'Good']
    return np.select(conditions, choices, default='Standard')
```

### **Opção 2: Baixar Dataset Completo**
- Verificar se existe train.csv no Kaggle
- Fazer download do dataset completo
- Usar API do Kaggle se necessário

### **Opção 3: Abordagem Não-Supervisionada**
```python
# Clustering para segmentação
- K-means para identificar perfis
- DBSCAN para outliers
- Análise de segmentos como proxy para score
```

---

## 📊 Estrutura do Notebook Final

```
1. Introdução e Contexto
2. Carregamento e Primeira Análise
3. EDA Completa
4. Pré-processamento
5. Modelagem e Otimização
6. Avaliação Comparativa
7. Interpretação e Insights
8. Conclusões e Recomendações
```

---

## ⚡ Próximos Passos

1. **Resolver a questão do target** (escolher uma das opções acima)
2. **Implementar EDA detalhada** 
3. **Criar pipeline de pré-processamento**
4. **Treinar os 3 modelos com GridSearch**
5. **Avaliar e comparar resultados**
6. **Documentar insights de negócio**

---

**Estimativa de Tempo**: 6-8 horas de desenvolvimento
**Complexidade**: Média-Alta (devido à falta do target)
**Foco Principal**: Análise exploratória robusta + Modelagem comparativa