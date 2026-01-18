#!/bin/bash
# Script de instalação para ambiente do protótipo FNN
# Uso: bash setup.sh

# Atualiza pip
python3 -m pip install --upgrade pip

# Instala dependências Python
pip install -r requirements.txt

# Instala Graphviz no sistema (necessário para plot_model)
if command -v apt-get &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y graphviz
elif command -v yum &> /dev/null; then
    sudo yum install -y graphviz
else
    echo "Instale o Graphviz manualmente para seu sistema."
fi
pip install pydot

echo "\nAmbiente configurado! Execute o notebook normalmente."
