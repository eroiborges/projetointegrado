# recomendacaoOF4.py
# Quantum Finance — Knowledge-Based + SQLite (Abordagem Híbrida)
#
# Responsabilidade:
#   - Criar e popular o banco SQLite com clientes, produtos e similaridades
#   - Aplicar recomendação via SQL (Filtro Colaborativo + Popularidade)
#   - Simular mecanismo de feedback (likes/dislikes)
#
# Modelo de dados (PDF p. 103):
#   tbCliente, tbProduto (quantidadeLikes), tbClienteProduto, tbClienteSimilaridade

import sqlite3
from recomendacaoOF import clientes
from recomendacaoOF2 import similaridade


def criar_banco():
    """
    Cria o banco SQLite em memória e retorna a conexão.
    Para persistência em arquivo, substituir ':memory:' por 'quantumfinance.db'.
    """
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE tbCliente (
            nomeCliente VARCHAR(50) PRIMARY KEY
        );
        CREATE TABLE tbProduto (
            nomeProduto VARCHAR(50) PRIMARY KEY,
            quantidadeLikes INTEGER DEFAULT 0
        );
        CREATE TABLE tbClienteProduto (
            nomeCliente VARCHAR(50),
            nomeProduto VARCHAR(50),
            valor FLOAT,
            PRIMARY KEY (nomeCliente, nomeProduto)
        );
        CREATE TABLE tbClienteSimilaridade (
            nomeClienteOrigem VARCHAR(50),
            nomeClienteDestino VARCHAR(50),
            similaridade FLOAT,
            PRIMARY KEY (nomeClienteOrigem, nomeClienteDestino)
        );
    """)
    conn.commit()
    return conn


def popular_banco(conn):
    """
    Popula todas as tabelas com dados do dataset Python e scores de similaridade.
    """
    cursor = conn.cursor()

    for nome in clientes:
        cursor.execute("INSERT INTO tbCliente VALUES (?)", (nome,))

    produtos_likes = {
        'Cartão de Crédito': 1,
        'Conta Corrente': 3,
        'Crédito Pessoal': 2,
        'Poupança': 0,
        'Renda Fixa': 1,
        'Renda Variável': 0
    }
    for produto, likes in produtos_likes.items():
        cursor.execute("INSERT INTO tbProduto VALUES (?, ?)", (produto, likes))

    for nome, produtos_cliente in clientes.items():
        for produto, valor in produtos_cliente.items():
            cursor.execute(
                "INSERT INTO tbClienteProduto VALUES (?, ?, ?)",
                (nome, produto, valor)
            )

    for u1 in clientes:
        for u2 in clientes:
            if u1 != u2:
                sim = round(similaridade(u1, u2), 4)
                cursor.execute(
                    "INSERT INTO tbClienteSimilaridade VALUES (?, ?, ?)",
                    (u1, u2, sim)
                )

    conn.commit()


def recomendar_por_vizinho(conn, usuario):
    """
    Filtro Colaborativo via SQL:
    1. Encontra o vizinho mais similar
    2. Retorna produtos que o vizinho tem e o usuario NÃO tem

    Retorna: (vizinho, [(nomeProduto, valor), ...])
    """
    cursor = conn.cursor()
    row = cursor.execute("""
        SELECT nomeClienteDestino FROM tbClienteSimilaridade
        WHERE nomeClienteOrigem = ?
        ORDER BY similaridade DESC LIMIT 1
    """, (usuario,)).fetchone()

    if not row:
        return None, []

    vizinho = row[0]
    recomendacoes = cursor.execute("""
        SELECT b.nomeProduto, b.valor
        FROM tbClienteProduto b
        WHERE b.nomeCliente = ?
          AND b.nomeProduto NOT IN (
              SELECT nomeProduto FROM tbClienteProduto WHERE nomeCliente = ?
          )
    """, (vizinho, usuario)).fetchall()

    return vizinho, recomendacoes


def listar_por_popularidade(conn):
    """
    Retorna todos os produtos ordenados por popularidade (quantidadeLikes DESC).
    Resolve Cold-Start parcialmente: clientes sem histórico recebem produtos populares.
    """
    cursor = conn.cursor()
    return cursor.execute("""
        SELECT nomeProduto, quantidadeLikes
        FROM tbProduto ORDER BY quantidadeLikes DESC
    """).fetchall()


def registrar_like(conn, produto):
    """Incrementa likes de um produto (feedback positivo do usuário)."""
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tbProduto SET quantidadeLikes = quantidadeLikes + 1 WHERE nomeProduto = ?",
        (produto,)
    )
    conn.commit()


def registrar_dislike(conn, produto):
    """Decrementa likes de um produto. Não permite valor abaixo de 0."""
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tbProduto SET quantidadeLikes = MAX(0, quantidadeLikes - 1) WHERE nomeProduto = ?",
        (produto,)
    )
    conn.commit()
