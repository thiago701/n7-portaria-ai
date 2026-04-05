#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Aula 02: Script para criar o banco de dados de moradores

Este script vai:
1. Criar um banco de dados SQLite
2. Criar a tabela de moradores
3. Inserir dados de exemplo
4. Listar todos os moradores

Complete os TODO para fazer funcionar!
"""

import sqlite3
import os

# Caminho do banco de dados (será criado em src/infra/database/)
caminho_banco = "../../src/infra/database/portaria.db"


def conectar_banco():
    """
    Conecta ao banco de dados.
    Se o banco não existir, SQLite cria automaticamente.

    Retorna: conexão com o banco
    """
    conexao = sqlite3.connect(caminho_banco)
    # row_factory permite acessar colunas por nome
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_tabela_moradores(conexao):
    """
    Cria a tabela de moradores no banco.

    TODO: Escreva o comando SQL CREATE TABLE que cria a tabela 'moradores'
    com as seguintes colunas:
    - id (INTEGER, PRIMARY KEY AUTOINCREMENT)
    - nome (TEXT, NOT NULL)
    - cpf (TEXT, UNIQUE, NOT NULL)
    - numero_residencia (TEXT, NOT NULL)
    - bloco (TEXT, DEFAULT 'A')
    - telefone (TEXT)
    - email (TEXT)
    - tipo_morador (TEXT, DEFAULT 'proprietario', CHECK proprietario/inquilino)
    - foto_url (TEXT)
    - dt_foto_validade (TEXT)
    - biometria_hash (TEXT)
    - dt_biometria_validade (TEXT)
    - ativo (INTEGER, DEFAULT 1)
    - dt_criado_em (TEXT, DEFAULT CURRENT_TIMESTAMP)
    - dt_atualizado_em (TEXT, DEFAULT CURRENT_TIMESTAMP)

    Dica: Revise o schema.sql para ver a estrutura!
    """
    cursor = conexao.cursor()

    sql = """
    -- TODO: Escreva o CREATE TABLE aqui
    CREATE TABLE moradores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT UNIQUE NOT NULL,
        numero_residencia TEXT NOT NULL,
        bloco TEXT DEFAULT 'A',
        telefone TEXT,
        email TEXT,
        tipo_morador TEXT DEFAULT 'proprietario' CHECK(tipo_morador IN ('proprietario', 'inquilino')),
        foto_url TEXT,
        dt_foto_validade TEXT,
        biometria_hash TEXT,
        dt_biometria_validade TEXT,
        ativo INTEGER DEFAULT 1,
        dt_criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
        dt_atualizado_em TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """

    try:
        cursor.execute(sql)
        conexao.commit()
        print("✓ Tabela 'moradores' criada com sucesso!")
    except sqlite3.OperationalError as e:
        # Se a tabela já existe, não precisa recriar
        print("ℹ Tabela 'moradores' já existe. Continuando...")


def inserir_morador(conexao, nome, cpf, numero_residencia, bloco, telefone, email):
    """
    Insere um novo morador na tabela.

    TODO: Escreva o comando SQL INSERT INTO que adiciona um registro.
    As colunas são: nome, cpf, numero_residencia, bloco, telefone, email

    Use placeholders (?) para evitar problemas de segurança.
    Exemplo:
        INSERT INTO tabela (coluna1, coluna2) VALUES (?, ?)
    """
    cursor = conexao.cursor()

    sql = """
    -- TODO: Escreva o INSERT INTO aqui
    INSERT INTO moradores (nome, cpf, numero_residencia, bloco, telefone, email)
    VALUES (?, ?, ?, ?, ?, ?)
    """

    try:
        cursor.execute(sql, (nome, cpf, numero_residencia, bloco, telefone, email))
        conexao.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(f"⚠ Erro ao inserir morador: {e}")
        return False


def listar_moradores(conexao):
    """
    Lista todos os moradores da tabela.

    TODO: Escreva o comando SQL SELECT que retorna todos os registros
    de todos os moradores. Use * para selecionar todas as colunas.

    Exemplo:
        SELECT * FROM tabela
    """
    cursor = conexao.cursor()

    sql = """
    -- TODO: Escreva o SELECT aqui
    SELECT * FROM moradores
    """

    try:
        cursor.execute(sql)
        moradores = cursor.fetchall()
        return moradores
    except Exception as e:
        print(f"⚠ Erro ao listar moradores: {e}")
        return []


def main():
    """
    Função principal que executa o fluxo completo.
    """
    print("\n" + "="*60)
    print("🏢 Sistema de Portaria — Criação do Banco de Dados")
    print("="*60 + "\n")

    # Cria a pasta src/infra/database se não existir
    os.makedirs("../../src/infra/database", exist_ok=True)

    print("1️⃣  Conectando ao banco de dados...")
    conexao = conectar_banco()
    print(f"   ✓ Conectado! Banco: {caminho_banco}\n")

    print("2️⃣  Criando tabela 'moradores'...")
    criar_tabela_moradores(conexao)
    print()

    print("3️⃣  Inserindo moradores de exemplo...")

    # Dados dos moradores de exemplo
    moradores_exemplo = [
        ("Ademilson Silva", "123.456.789-00", 102, "A", "(11) 98765-4321", "ademilson@email.com"),
        ("Maria Santos", "987.654.321-00", 205, "A", "(11) 99876-5432", "maria@email.com"),
        ("João Oliveira", "111.222.333-44", 308, "B", "(11) 91234-5678", "joao@email.com"),
    ]

    for nome, cpf, apto, bloco, tel, email in moradores_exemplo:
        if inserir_morador(conexao, nome, cpf, apto, bloco, tel, email):
            print(f"   ✓ {nome} adicionado!")
        else:
            print(f"   ✗ Erro ao adicionar {nome}")

    print()

    print("4️⃣  Listando todos os moradores...")
    print()

    moradores = listar_moradores(conexao)

    if moradores:
        print("┌────────────────────────────────────────────────────┐")
        print("│ MORADORES CADASTRADOS                              │")
        print("├────────────────────────────────────────────────────┤")

        for morador in moradores:
            id_morador = morador['id']
            nome_morador = morador['nome']
            apto_morador = morador['numero_residencia']
            bloco_morador = morador['bloco']
            email_morador = morador['email']

            print(f"│ ID: {id_morador} | {nome_morador:<25} │")
            print(f"│   Apto: {apto_morador} | Bloco: {bloco_morador} | {email_morador:<15} │")
            print("├────────────────────────────────────────────────────┤")

        print("└────────────────────────────────────────────────────┘")
        print()
    else:
        print("⚠ Nenhum morador encontrado no banco.\n")

    # Fecha a conexão
    conexao.close()

    print("✓ Banco de dados criado e populado com sucesso!")
    print(f"✓ Arquivo salvo em: {caminho_banco}")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()
