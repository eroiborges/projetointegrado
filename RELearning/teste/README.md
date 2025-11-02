# Quantum Finance - Agente de Reinforcement Learning para Trading

## 📊 Visão Geral do Projeto

Este projeto implementa um agente de **Reinforcement Learning (RL)** utilizando o algoritmo **Deep Q-Network (DQN)** para operar automaticamente em 3 ativos da bolsa brasileira (B3): Vale (VALE3.SA), Petrobras (PETR4.SA) e BRF (BRFS3.SA).

**Objetivo:** Maximizar o lucro em um período de 6 meses com um capital inicial de R$ 10.000,00.

---

## 🎯 Estrutura do Projeto

O projeto está dividido em 5 fases principais:

### Fase 1: Preparação e Configuração
- Instalação e importação de bibliotecas
- Download de dados históricos via `yfinance`
- Preparação e limpeza dos dados
- Divisão entre conjunto de treino (2018-2022) e teste (primeiros 6 meses de 2023)

### Fase 2: Modelagem do Problema
- Criação de ambiente customizado `StockTradingEnv` (Gymnasium)
- Definição de **Estados**, **Ações** e **Recompensas**

### Fase 3: Implementação do Algoritmo
- Implementação do agente **DQN (Deep Q-Network)**
- Rede neural para aproximar função Q
- Experience Replay e Target Network
- Loop de treinamento

### Fase 4: Avaliação do Desempenho
- Comparação com estratégias baseline:
  - **Buy and Hold**: Compra e mantém ações
  - **Agente Aleatório**: Decisões aleatórias
- Métricas de avaliação:
  - Lucro/Prejuízo Total
  - Retorno Percentual
  - Sharpe Ratio (métrica avançada)
- Visualizações comparativas

### Fase 5: Documentação
- Explicação detalhada da modelagem
- Análise de resultados
- Insights e melhorias futuras

---

## 🔧 Requisitos

### Bibliotecas Necessárias

```bash
pip install yfinance gymnasium tensorflow pandas numpy matplotlib seaborn
```

### Principais Dependências
- **Python 3.8+**
- **TensorFlow 2.x**: Deep Learning
- **Gymnasium**: Ambiente de RL
- **yfinance**: Download de dados financeiros
- **pandas, numpy**: Manipulação de dados
- **matplotlib, seaborn**: Visualizações

---

## 📈 Modelagem do Problema

### Estados (State)
Vetor de 7 dimensões:
1. Saldo em dinheiro
2. Quantidade de ações da Vale
3. Quantidade de ações da Petrobras
4. Quantidade de ações da BRF
5. Preço atual da Vale
6. Preço atual da Petrobras
7. Preço atual da BRF

### Ações (Actions)
Espaço discreto com 7 ações:
- `0`: Manter (não fazer nada)
- `1`: Comprar 10 ações da Vale
- `2`: Vender 10 ações da Vale
- `3`: Comprar 10 ações da Petrobras
- `4`: Vender 10 ações da Petrobras
- `5`: Comprar 10 ações da BRF
- `6`: Vender 10 ações da BRF

### Recompensa (Reward)
Mudança no valor total do portfólio entre um dia e o próximo:
```
Recompensa = Valor_Portfólio_D - Valor_Portfólio_{D-1}
```

---

## 🚀 Como Usar

### Execução no Google Colab (Recomendado)

1. Abra o arquivo `quantum_finance.ipynb` no Google Colab
2. Execute as células sequencialmente
3. O notebook baixará os dados automaticamente e treinará o agente

### Execução Local

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute o notebook:
```bash
jupyter notebook quantum_finance.ipynb
```

### Parâmetros Configuráveis

No notebook, você pode ajustar:
- `episodes`: Número de episódios de treinamento (padrão: 50)
- `capital_inicial`: Capital inicial (padrão: R$ 10.000)
- `quantidade_acoes`: Quantidade fixa de ações por operação (padrão: 10)
- `learning_rate`: Taxa de aprendizado da rede neural (padrão: 0.001)
- `episodes` no treinamento: Aumentar para melhor desempenho (recomendado: 100-200)

---

## 📊 Resultados Esperados

O notebook gera:
1. **Gráficos de evolução do portfólio** durante o treinamento
2. **Comparação visual** entre DQN, Buy and Hold e Agente Aleatório
3. **Tabela resumo** com métricas de desempenho
4. **Sharpe Ratio** para análise de risco-retorno

---

## 🔍 Estrutura dos Arquivos

```
quantum_finance/
│
├── quantum_finance.ipynb    # Notebook principal com todo o código
├── README.md                 # Este arquivo
└── requirements.txt          # Lista de dependências (opcional)
```

---

## 🎓 Características Técnicas

### Arquitetura DQN
- **Camadas**: 3 camadas densas (128-128-64 neurônios)
- **Ativação**: ReLU com Dropout (0.2) para regularização
- **Experience Replay**: Buffer de 10.000 transições
- **Target Network**: Atualizado a cada 5 episódios
- **Epsilon-Greedy**: Exploração inicial 100%, decaindo até 1%

### Ambiente Customizado
- Herda de `gymnasium.Env`
- Implementa métodos: `reset()`, `step()`, `render()`
- Validação de ações (saldo suficiente, ações suficientes para venda)

---

## 💡 Melhorias Futuras

1. **Feature Engineering**: Adicionar indicadores técnicos (RSI, MACD, médias móveis)
2. **Ações Contínuas**: Permitir quantidades variáveis em vez de fixas
3. **Custos de Transação**: Incluir taxas e impostos (IR, corretagem)
4. **Algoritmos Avançados**: Testar Dueling DQN, Double DQN, PPO, A3C
5. **Risk Management**: Implementar stop-loss e take-profit
6. **Multi-timeframe**: Considerar dados de diferentes períodos
7. **Múltiplos Ativos**: Expandir para mais ações simultaneamente

---

## 📝 Notas Importantes

- ⚠️ **Este é um projeto acadêmico**. Não use para trading real sem extensivos testes e validações.
- 📊 Os dados são históricos e não garantem desempenho futuro.
- 🔄 O treinamento pode levar alguns minutos dependendo do número de episódios.
- 🎲 Sementes aleatórias estão fixas para reprodutibilidade dos resultados.

---

## 📚 Referências

- **Gymnasium**: https://gymnasium.farama.org/
- **Deep Q-Learning (DQN)**: Mnih et al., 2015
- **yfinance**: https://github.com/ranaroussi/yfinance
- **TensorFlow**: https://www.tensorflow.org/

---

## 👤 Autor

Projeto desenvolvido para o **MBA em Data Science e Analytics**.

---

## 📄 Licença

Este projeto é apenas para fins educacionais e acadêmicos.

---

**Desenvolvido com ❤️ usando Reinforcement Learning e Python**

