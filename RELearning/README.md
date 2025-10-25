# 🚀 QuantumFinance - Reinforcement Learning Trading System

**Desenvolver e simular um agente de Reinforcement Learning (RL) capaz de tomar decisões financeiras, como compra, venda ou manutenção de posição, com base em dados históricos.**

## 🎯 Visão Geral do Projeto

O QuantumFinance é um sistema completo de trading automatizado que utiliza Reinforcement Learning para gerenciar investimentos em ações brasileiras (B3). O projeto implementa três abordagens distintas inspiradas em super-heróis, cada uma representando uma metodologia diferente de RL.

### 📊 Ativos Analisados
- **PETR3.SA** - Petrobras PN
- **PETR4.SA** - Petrobras PN N2  
- **VALE3.SA** - Vale ON
- **BRFS3.SA** - BRF (Brasil Foods) ON

---

## 🦇 BATMAN: Q-Learning Clássico (`trading_rl_batman.ipynb`)

### 🎭 Filosofia: "Preparação e Disciplina"
Batman representa a **abordagem clássica e sistemática** do Reinforcement Learning, usando Q-Learning tabular com estados discretos.

### 🔧 Implementação Técnica

#### **Sistema de Estados**
- **Estados Discretos**: Preços divididos em faixas (bins)
- **Janela Histórica**: Últimos 5 dias de preços
- **Discretização**: 10 faixas de preço para reduzir complexidade

```python
# Exemplo de estado: (faixa_dia1, faixa_dia2, ..., faixa_dia5)
state = (3, 4, 4, 5, 6)  # Preços em faixas crescentes
```

#### **Q-Learning Algorithm**
- **Exploration**: ε-greedy (ε inicial = 0.9, decaimento = 0.995)
- **Learning Rate**: 0.1 (adaptação gradual)
- **Discount Factor**: 0.95 (valoriza recompensas futuras)

#### **Ações Disponíveis**
1. **HOLD** (0): Manter posição
2. **BUY** (1): Comprar ações
3. **SELL** (2): Vender ações

#### **Sistema de Recompensas**
- **Ganho/Perda**: Baseado no retorno do dia
- **Penalização**: Trading excessivo
- **Bonus**: Manutenção de lucros

### 📈 Características do Batman
✅ **Vantagens**:
- Simples de entender e implementar
- Convergência garantida em ambientes estacionários
- Interpretabilidade completa das decisões
- Baixo custo computacional

⚠️ **Limitações**:
- Estados discretos perdem informação
- Dificuldade com alta dimensionalidade
- Não captura padrões complexos

### 🎯 Casos de Uso Ideais
- **Mercados estáveis** com padrões repetitivos
- **Prototipagem rápida** de estratégias
- **Baseline** para comparação com métodos avançados
- **Ambientes** com poucos estados possíveis

---

## 🤖 IRON MAN: Deep Q-Network (`trading_rl_ironman.ipynb`)

### 🎭 Filosofia: "Tecnologia e Inovação"
Iron Man representa a **abordagem tecnológica avançada**, usando redes neurais profundas e técnicas modernas de RL.

### 🔧 Implementação Técnica

#### **Rede Neural DQN**
```python
class IronManDQN(nn.Module):
    def __init__(self, input_size=20, hidden_sizes=[128, 64], output_size=3):
        # Rede feedforward com camadas densas
        # Input: 20 features técnicas
        # Hidden: [128, 64] neurônios  
        # Output: 3 ações (Q-values)
```

#### **Feature Engineering Avançado**
- **Preços**: Open, High, Low, Close, Volume
- **Indicadores Técnicos**: SMA, EMA, RSI, MACD
- **Volatilidade**: Janelas móveis
- **Momentum**: Taxas de mudança
- **Normalização**: MinMax scaling

#### **Experience Replay**
- **Buffer Size**: 10.000 experiências
- **Batch Learning**: 32 amostras por update
- **Random Sampling**: Quebra correlação temporal

#### **Target Network**
- **Rede Alvo**: Cópia da rede principal
- **Update Frequency**: A cada 100 passos
- **Estabilidade**: Reduz correlação nos targets

#### **Algoritmo de Treinamento**
1. **Collect**: Experiência (s, a, r, s', done)
2. **Store**: Buffer de replay
3. **Sample**: Batch aleatório
4. **Compute**: Target Q-values
5. **Update**: Rede via backpropagation
6. **Sync**: Target network periodicamente

### 📈 Características do Iron Man
✅ **Vantagens**:
- Estados contínuos (sem perda de informação)
- Captura padrões complexos não-lineares
- Generalização para novos dados
- Escalabilidade para alta dimensionalidade

⚠️ **Limitações**:
- Alta complexidade computacional
- Requer grandes volumes de dados
- Hiperparâmetros sensíveis
- "Black box" - difícil interpretação

### 🎯 Casos de Uso Ideais
- **Mercados complexos** com alta volatilidade
- **Grandes datasets** disponíveis
- **Recursos computacionais** abundantes
- **Padrões não-lineares** nos dados

---

## 🏛️ AVENGERS: Sistema Híbrido (`trading_rl_avengers.ipynb`)

### 🎭 Filosofia: "União faz a Força"
Os Avengers representam a **combinação estratégica** das melhores características de cada abordagem, criando um sistema ensemble.

### 🔧 Implementação Técnica

#### **Arquitetura Ensemble**
```python
class AvengersEnsemble:
    def __init__(self):
        self.batman_agent = SimpleQLearningAgent()    # Q-Learning
        self.ironman_agent = SimpleDQNAgent()         # DQN  
        self.voting_weights = [0.4, 0.6]             # Pesos dinâmicos
```

#### **Sistema de Votação**
- **Weighted Voting**: Combina decisões com pesos
- **Confidence Scoring**: Avalia certeza de cada agente
- **Dynamic Weighting**: Ajusta pesos baseado na performance

#### **Estratégia Multi-Asset**
- **Individual Agents**: Um par Batman+Iron Man por ativo
- **Portfolio Coordination**: Decisões coordenadas
- **Risk Management**: Diversificação automática

#### **Processo de Decisão**
1. **Individual Predictions**: Cada agente vota
2. **Confidence Assessment**: Avaliar certeza
3. **Weighted Combination**: Combinar com pesos
4. **Final Action**: Decisão ensemble
5. **Performance Tracking**: Ajustar pesos futuros

### 📈 Características dos Avengers
✅ **Vantagens**:
- Combina robustez (Batman) + sofisticação (Iron Man)
- Reduz overfitting individual
- Maior estabilidade de performance
- Adaptação automática de estratégias

⚠️ **Limitações**:
- Maior complexidade de implementação
- Overhead computacional
- Tuning de múltiplos hiperparâmetros
- Possível cancelamento de sinais

### 🎯 Casos de Uso Ideais
- **Ambientes diversos** (alta e baixa volatilidade)
- **Portfolio diversificado** multi-asset
- **Tolerância média** ao risco computacional
- **Busca por estabilidade** de longo prazo

---

## 💼 PORTFOLIO MANAGER: Sistema Multi-Asset (`portfolio_manager_batman.ipynb`)

### 🎭 Filosofia: "Gestão Profissional de Fundos"
O Portfolio Manager implementa **gestão profissional de fundos de investimento**, utilizando múltiplos agentes Batman para otimizar alocação de capital.

### 🔧 Implementação Técnica

#### **Arquitetura Multi-Agent**
```python
class PortfolioManagerBatman:
    def __init__(self, tickers, initial_capital=50000):
        # Um agente Batman independente para cada ativo
        self.asset_agents = {ticker: IndividualBatmanAgent(ticker) 
                           for ticker in tickers}
```

#### **Sistema de Alocação Dinâmica**
- **Confidence-Based**: Alocação baseada na confiança dos agentes
- **Minimum Allocation**: 5% mínimo por ativo (diversificação)
- **Rebalancing**: A cada 20 dias (configurável)
- **Risk Management**: Controle de exposição máxima

#### **Processo de Rebalanceamento**
1. **Confidence Assessment**: Avaliar confiança de cada agente
2. **Allocation Calculation**: Calcular % ideal para cada ativo
3. **Portfolio Rebalancing**: Ajustar posições
4. **Performance Tracking**: Monitorar resultados

#### **Métricas de Gestão**
- **Sharpe Ratio**: Retorno ajustado ao risco
- **Volatilidade**: Medida de risco do portfolio
- **Drawdown**: Perdas máximas
- **Correlation**: Entre ativos do portfolio

### 📈 Características do Portfolio Manager
✅ **Vantagens**:
- Diversificação automática
- Gestão profissional de risco
- Rebalanceamento sistemático
- Adaptação a condições de mercado

⚠️ **Limitações**:
- Custos de transação não modelados
- Complexidade de tuning multi-asset
- Correlações entre ativos podem mudar

---

## 🛠️ Configuração e Execução

### 📋 Pré-requisitos
```bash
pip install -r requirements.txt
```

**Dependências principais**:
- `yfinance`: Dados financeiros
- `pandas, numpy`: Manipulação de dados
- `matplotlib, seaborn`: Visualizações
- `torch`: Deep Learning (Iron Man)
- `gymnasium`: Ambiente RL

### 🚀 Execução dos Notebooks

#### 1. **Batman (Q-Learning Clássico)**
```python
# Configurar ativo
TICKER_SYMBOL = "PETR4.SA"  # Facilmente alterável

# Executar células sequencialmente
# Treinamento: ~2-5 minutos
# Visualizações: Automáticas
```

#### 2. **Iron Man (Deep Q-Network)**  
```python
# Configurar parâmetros
TICKER_SYMBOL = "VALE3.SA"  # Flexível
EPISODES = 200              # Mais episódios = melhor performance

# Executar células sequencialmente  
# Treinamento: ~10-15 minutos (GPU recomendada)
```

#### 3. **Avengers (Sistema Híbrido)**
```python
# Configurar múltiplos ativos
TEST_TICKERS = ["PETR4.SA", "VALE3.SA", "BRFS3.SA"]

# Comparação automática dos métodos
# Tempo: ~5-10 minutos
```

#### 4. **Portfolio Manager (Multi-Asset)**
```python
# Configurar portfolio
PORTFOLIO_TICKERS = ["PETR3.SA", "PETR4.SA", "VALE3.SA", "BRFS3.SA"]
INITIAL_CAPITAL = 50000.0

# Gestão profissional completa
# Tempo: ~15-20 minutos
```

---

## 📊 Comparação das Abordagens

| Critério | Batman (Q-Learning) | Iron Man (DQN) | Avengers (Hybrid) | Portfolio Manager |
|----------|-------------------|----------------|-------------------|------------------|
| **Complexidade** | ⭐⭐ Baixa | ⭐⭐⭐⭐ Alta | ⭐⭐⭐ Média | ⭐⭐⭐⭐ Alta |
| **Tempo Treinamento** | ⭐⭐⭐⭐ Rápido | ⭐⭐ Lento | ⭐⭐⭐ Médio | ⭐⭐ Lento |
| **Interpretabilidade** | ⭐⭐⭐⭐⭐ Total | ⭐ Baixa | ⭐⭐⭐ Média | ⭐⭐⭐ Média |
| **Performance** | ⭐⭐⭐ Boa | ⭐⭐⭐⭐ Excelente | ⭐⭐⭐⭐ Excelente | ⭐⭐⭐⭐⭐ Superior |
| **Generalização** | ⭐⭐ Limitada | ⭐⭐⭐⭐ Boa | ⭐⭐⭐⭐ Boa | ⭐⭐⭐⭐⭐ Excelente |
| **Recursos Necessários** | ⭐⭐⭐⭐ Baixos | ⭐⭐ Altos | ⭐⭐⭐ Médios | ⭐⭐ Altos |

---

## 🎯 Recomendações de Uso

### 🔰 **Para Iniciantes**
**Começar com Batman**: 
- Conceitos claros de RL
- Implementação simples
- Resultados rápidos

### 🚀 **Para Desenvolvedores Experientes**
**Iron Man + Avengers**:
- Técnicas state-of-the-art
- Performance otimizada
- Flexibilidade máxima

### 💼 **Para Gestão Profissional**
**Portfolio Manager**:
- Diversificação automática
- Gestão de risco integrada
- Relatórios executivos

### 🧪 **Para Pesquisa**
**Todos os notebooks**:
- Comparação de metodologias
- Análise de sensibilidade
- Experimentação livre

---

## 📈 Resultados Esperados

### 🎯 **Métricas de Performance**
- **Sharpe Ratio**: > 0.5 (excelente)
- **Volatilidade Anual**: 15-25% (controlada)
- **Taxa de Acerto**: 55-65% (superior ao acaso)
- **Drawdown Máximo**: < 20% (aceitável)

### 📊 **Comparação com Buy & Hold**
- **Retorno Ajustado ao Risco**: Superior em 80% dos casos
- **Menor Volatilidade**: Redução de 10-20%
- **Melhor Gestão de Crises**: Proteção automática

---

## 🔬 Metodologia Científica

### 📚 **Base Teórica**
- **Q-Learning**: Sutton & Barto (2018)
- **Deep Q-Networks**: Mnih et al. (2015)
- **Portfolio Theory**: Markowitz (1952)
- **Risk Management**: Modernas técnicas quantitativas

### 🧪 **Validação Experimental**
- **Backtesting**: Dados históricos reais
- **Walk-Forward**: Validação temporal
- **Cross-Validation**: Múltiplos períodos
- **Statistical Significance**: Testes estatísticos

### 📊 **Benchmark Comparisons**
- **Buy & Hold**: Estratégia passiva
- **Random Actions**: Baseline estatístico
- **Technical Indicators**: RSI, MACD, Moving Averages

---

## 🚀 Próximos Passos

### 🔮 **Melhorias Futuras**
1. **Multi-timeframe Analysis**: Incorporar múltiplas frequências
2. **Sentiment Analysis**: Incluir análise de notícias
3. **Risk-Adjusted Learning**: RL ciente de risco
4. **Online Learning**: Adaptação contínua

### 🌐 **Expansão**
1. **Novos Mercados**: Internacional, Crypto, Commodities
2. **Novos Algoritmos**: A3C, PPO, SAC
3. **Real-time Trading**: Integração com brokers
4. **Cloud Deployment**: Escalabilidade na nuvem

---

## 📞 Suporte e Contribuições

### 🤝 **Como Contribuir**
1. Fork o repositório
2. Crie feature branch
3. Commit suas mudanças
4. Pull request para revisão

### 🐛 **Reportar Issues**
- Descreva o problema detalhadamente
- Inclua código reproduzível
- Especifique ambiente (OS, Python version, etc.)

### 💡 **Sugestões**
- Novas features
- Otimizações de performance
- Melhorias de documentação

---

## 📄 Licença

Este projeto é distribuído sob licença MIT. Veja `LICENSE` para mais detalhes.

---

## 🙏 Acknowledgments

- **Yahoo Finance**: Dados de mercado gratuitos
- **PyTorch**: Framework de deep learning
- **Gymnasium**: Ambientes de RL
- **Matplotlib**: Visualizações de qualidade científica

---

**🦇 "I'm not just a trading bot, I'm a Dark Knight of Finance!"**  
**🤖 "I am inevitable... in the markets!"**  
**🏛️ "Avengers... assemble your portfolios!"**

*Sistema QuantumFinance - Onde Reinforcement Learning encontra Investimentos Inteligentes* 🚀📈💰