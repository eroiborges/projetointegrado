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
