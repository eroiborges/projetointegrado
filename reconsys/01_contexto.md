# Entregável 1 — Slide de Contexto
## Especificação para Quantum Finance — Recommendation System

---

## Objetivo deste arquivo

Este documento é o guia de referência para a construção do **slide de contexto** do trabalho.
Ele descreve a narrativa da Fintech, o problema que o SR resolve e a estrutura sugerida para os slides.

---

## 1. Narrativa da Quantum Finance

### Quem é a Quantum Finance?

A **Quantum Finance** é uma Fintech brasileira fundada em 2021, especializada em **crédito pessoal e consignado**.
Seu público-alvo são trabalhadores com carteira assinada e servidores públicos que buscam condições melhores de crédito do que as oferecidas pelos bancos tradicionais.

**Diferenciais da empresa:**
- Processo 100% digital de contratação de crédito
- Taxa de juros competitivas via análise de risco proprietária
- Integração com o Open Finance para obter visão completa do perfil financeiro do cliente

**Missão:** Democratizar o acesso ao crédito justo e personalizado no Brasil.

---

## 2. O Problema

Com a adesão ao **Open Finance**, a Quantum Finance passou a ter acesso (mediante consentimento do cliente) a dados financeiros consolidados de múltiplas instituições.

**Dores identificadas:**
- O cliente possui produtos em diferentes bancos, mas cada banco enxerga apenas parte do perfil
- A oferta de produtos é genérica — todos recebem as mesmas sugestões
- Clientes com perfil de investidor leve recebem ofertas de crédito inadequadas e vice-versa
- Taxa de conversão de ofertas proativas é baixa (< 5%)

**Pergunta-chave:** Como usar os dados do Open Finance para recomendar produtos financeiros **relevantes e personalizados** a cada cliente?

---

## 3. A Solução — Sistema de Recomendação (Abordagem Híbrida + Market Intelligence)

A Quantum Finance propõe um **Motor de Recomendação com três camadas de inteligência**:

**Camada 1 — Quem recomendar?** (Filtro Colaborativo / Knowledge-Based)
- Identifica quais clientes têm maior propensão para contratar Crédito Pessoal, Cartão de Crédito ou Seguro com base no perfil de clientes similares

**Camada 2 — O que oferecer?** (Open Finance Market Intelligence)
- Consulta em tempo real as APIs públicas do Open Finance de 4 instituições: **Itaú, Caixa Econômica, XP e PicPay**
- Coleta taxas e condições de mercado para os produtos recomendados
- Exibe a **melhor e a pior proposta do mercado**

**Camada 3 — Qual a proposta da Quantum Finance?**
- Gera automaticamente uma proposta com taxa **5% abaixo da melhor taxa de mercado**
- Diferencial competitivo claro e mensurável para o cliente

**Dois modos de uso:**
1. **Batch** — Lista de contato priorizada: todos os clientes ranqueados por propensão a cada produto, com a proposta da QF já calculada (entregue ao time comercial)
2. **Ad-hoc** — Interface de entrada de perfil: operador preenche dados de um potencial cliente → sistema gera recomendação personalizada + comparativo de mercado instantâneo

**Produtos cobertos:**
| Produto | Endpoint Open Finance | Métrica de comparação |
|---|---|---|
| Crédito Pessoal / Consignado | `opendata-loans/v1/personal-loans` | Taxa de juros (% a.m.) |
| Cartão de Crédito | `opendata-creditcards/v1/personal-credit-cards` | Anuidade + limite |
| Seguro de Vida | `opendata-insurance/v2/personals` | Modalidade + cobertura |

**Valor gerado:**
- Time comercial recebe todos os dias uma lista de contato priorizada com a proposta já pronta
- Atendimento ad-hoc oferece comparativo de mercado em segundos, sem pesquisa manual
- Cliente percebe que a Quantum Finance já pesquisou o mercado por ele → aumento de conversão

---

## 4. Desafios Específicos do SR Financeiro

O professor destaca (PDF p. 88) que SRs no setor financeiro têm características únicas que impactam o design da solução — importante mencionar no slide para demonstrar maturidade técnica:

| Desafio | Impacto no SR da Quantum Finance |
|---|---|
| **Comprometimento de longo prazo** | Crédito consignado é uma decisão de meses/anos — a recomendação deve ser cautelosa |
| **Impacto financeiro direto na vida do usuário** | Uma recomendação ruim de crédito pode endividar o cliente |
| **Poucas métricas de feedback** | Diferente de e-commerce, cliente não "curte" ou "devolve" um produto financeiro |
| **Regulamentações** | BACEN, LGPD, Open Finance obrigam privacidade e consentimento explícito |
| **Cold-start acentuado** | LGPD limita coleta histórica — novos clientes chegam sem histórico acessível |

Esses desafios **justificam** a abordagem híbrida: Filtro Colaborativo resolve similaridade, popularidade resolve cold-start parcialmente.

---

## 5. Conexão com o Open Finance

| Dado do Open Finance | Uso no SR |
|---|---|
| Produtos contratados em outras IFs | Composição do vetor de perfil do cliente |
| Score/uso de cada produto | Peso do produto no cálculo de distância (Euclidiana) |
| Dados cadastrais (renda, vínculo) | Enriquecimento futuro para filtragem por elegibilidade |

**Referências do Open Finance Brasil:**
- Portal do desenvolvedor: https://openfinancebrasil.atlassian.net/wiki/spaces/OF/overview
- Diretório de participantes: https://data.directory.openbankingbrasil.org.br/participants

---

## 6. Estrutura Sugerida de Slides

### Slide 1 — Capa
- Título: "Quantum Finance — Sistema de Recomendação com Open Finance"
- Subtítulo: "Personalização de crédito baseada em Filtragem Colaborativa"
- Logo fictícia + ícone de Open Finance

### Slide 2 — Quem somos
- 3 bullets: missão, público-alvo, diferenciais
- Destaque: "100% digital | Open Finance | Crédito justo"

### Slide 3 — O Problema
- Diagrama: cliente no centro, múltiplos bancos ao redor (dados fragmentados)
- Seta convergindo para a Quantum via Open Finance
- Texto: "Sem visão consolidada, a oferta é genérica e ineficiente"

### Slide 4 — A Oportunidade
- Gráfico fictício: "Taxa de conversão: oferta genérica 4% vs oferta personalizada 18%"
- Fonte: benchmarks de mercado (pode citar casos de Nubank, Inter, etc.)

### Slide 5 — A Solução: SR Híbrido + Market Intelligence
- Diagrama do fluxo completo em 3 camadas: CF (quem?) → Open Finance APIs (o quê?) → Proposta QF (como?)
- Técnicas: User-Based CF + Knowledge-Based + Market Intelligence via Open Finance
- Dois modos de saída: Batch (lista de contato) + Ad-hoc (atendimento instantâneo)
- Frase de impacto: "5% abaixo do mercado, automaticamente"

### Slide 6 — Exemplo Real: Lista de Contato (Demo Batch)
- Tabela com clientes, produto recomendado, score de propensão e proposta QF
- Ex: "Claudia → Crédito Pessoal → propensão 3.61 → QF: 1.71% a.m. vs mercado 1.80% a.m."

### Slide 7 — Exemplo Real: Atendimento Ad-hoc (Demo)
- Print do Jupyter Notebook mostrando interface de entrada de perfil
- Output: produtos recomendados + tabela comparativa Itaú / Caixa / XP / PicPay / QF

### Slide 8 — Próximos Passos
- Integrar às APIs fechadas do Open Finance (com consentimento — dados reais do cliente)
- Expandir dataset com mais clientes e produtos
- Automatizar envio da lista de contato via CRM diariamente
- Adicionar filtro de elegibilidade (renda, score de crédito, vínculo empregatício)

---

## 7. Mensagem-Chave para o Slide

> "Com o Open Finance, a Quantum Finance não apenas processa dados — ela transforma dados em relacionamentos personalizados, consultando o mercado em tempo real e entregando a proposta certa, para a pessoa certa, 5% abaixo do mercado."

---

## Referências Úteis para Construção do Slide
- Dataset do professor: `dataset/01_DataSetOpenFinance.txt`
- Enunciado oficial: `descricao/trabalho.txt`
- PDF da disciplina: `material_aula/RecommendationSystems.pdf` — especialmente p. 29-31 (propriedades), p. 33-35 (problemas), p. 88 (desafios financeiros), p. 89-99 (estudo de Caso Santander/Open Finance)
- Banco Central — Open Finance: https://openfinancebrasil.atlassian.net/wiki/spaces/OF/overview
