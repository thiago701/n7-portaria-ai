#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  SISTEMA DE PORTARIA — CRUD de Moradores
  Aula 02 | 09/04/2026
============================================================

Aluno : Ademilson
Prof  : Thiago

O QUE VAMOS FAZER HOJE:
  Você já criou o banco portaria.db usando o DBeaver.
  Agora vamos fazer o Python CONVERSAR com esse banco!

  CRUD = as 4 operações que TODO sistema do mundo usa:
    C — Create  (cadastrar)
    R — Read    (listar / buscar)
    U — Update  (atualizar)
    D — Delete  (desativar — "soft delete")

COMO EXECUTAR:
  No terminal, dentro desta pasta:
    python moradores_crud.py

PRÉ-REQUISITO:
  O arquivo portaria.db já deve existir na pasta:
    src/infra/database/portaria.db
  (criado pelo DBeaver com projeto_portaria_completo.sql)
"""

import sqlite3
import os
import hashlib
from datetime import datetime


# ============================================================
# CONFIGURAÇÃO DO BANCO
# ============================================================
# Caminho até o banco que você criou no DBeaver:
CAMINHO_BANCO = os.path.join(
    os.path.dirname(__file__),  # pasta deste arquivo
    "..", "..", "..", "..",     # sobe até a raiz do projeto
    "src", "infra", "database", "portaria.db"
)


# ============================================================
# FUNÇÕES DE CONEXÃO
# ============================================================

def conectar():
    """
    Abre a conexão com o banco portaria.db.

    row_factory = sqlite3.Row permite acessar colunas pelo NOME:
      morador['nome']  em vez de  morador[1]
    Muito mais fácil de entender!
    """
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    # Ativa verificação de chaves estrangeiras
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def fechar(conexao):
    """Fecha a conexão com o banco de forma segura."""
    if conexao:
        conexao.close()


# ============================================================
# FUNÇÕES AUXILIARES (já prontas — use à vontade!)
# ============================================================

def separador(titulo=""):
    """Imprime uma linha separadora com título opcional."""
    print()
    if titulo:
        print(f"  {'═' * 50}")
        print(f"  {titulo.center(50)}")
        print(f"  {'═' * 50}")
    else:
        print(f"  {'─' * 50}")


def formatar_cpf(cpf):
    """
    Formata CPF para exibição bonita.
    '12345678901' → '123.456.789-01'
    """
    cpf = str(cpf).strip()
    if len(cpf) == 11 and cpf.isdigit():
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return cpf


def validar_cpf(cpf):
    """
    Validação básica: CPF deve ter exatamente 11 dígitos numéricos.
    Retorna True se válido, False se inválido.
    """
    cpf = cpf.strip()
    if not cpf.isdigit():
        print("  ⚠  CPF deve conter apenas números (sem pontos ou traços).")
        return False
    if len(cpf) != 11:
        print(f"  ⚠  CPF deve ter 11 dígitos. Você digitou {len(cpf)}.")
        return False
    return True


def gerar_correlation_id(tabela, valor_unico):
    """
    Gera um correlation_id usando SHA-256.
    É como um "RG digital" único para cada registro.

    Exemplo:
      gerar_correlation_id('moradores', '11122233344')
      → 'a1b2c3d4...' (64 caracteres)
    """
    texto = f"{tabela}:{valor_unico}"
    return hashlib.sha256(texto.encode()).hexdigest()


def agora():
    """Retorna data e hora atual no formato do banco."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def pausar():
    """Aguarda o usuário pressionar ENTER antes de continuar."""
    input("\n  Pressione ENTER para continuar...")


# ============================================================
# C — CREATE: CADASTRAR MORADOR
# ============================================================

def cadastrar_morador():
    """
    Pede os dados do morador e insere no banco de dados.

    ATENÇÃO: A tabela 'moradores' guarda dados PESSOAIS.
    O endereço (apartamento/bloco) fica na tabela 'residencias',
    conectado pela tabela 'morador_residencia'.

    Nesta versão simplificada, cadastramos apenas o morador.
    A associação com a residência será feita depois!
    """
    separador("CADASTRAR NOVO MORADOR")

    conexao = None
    try:
        # ── Coleta de dados ──────────────────────────────
        nome = input("  Nome completo       : ").strip()
        if not nome:
            print("  ✗  Nome é obrigatório!")
            return

        cpf = input("  CPF (só números)    : ").strip()
        if not validar_cpf(cpf):
            return

        telefone = input("  Telefone            : ").strip() or None
        email = input("  E-mail              : ").strip() or None

        # ── Verificação de CPF duplicado ─────────────────
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT nome FROM moradores WHERE cpf = ?", (cpf,))
        existente = cursor.fetchone()

        if existente:
            print(f"\n  ✗  CPF {formatar_cpf(cpf)} já está cadastrado.")
            print(f"     Morador: {existente['nome']}")
            return

        # ── INSERT no banco ───────────────────────────────
        # Gera o correlation_id automaticamente
        correlation = gerar_correlation_id("moradores", cpf)

        cursor.execute(
            """
            INSERT INTO moradores (nome, cpf, telefone, email, correlation_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (nome, cpf, telefone, email, correlation)
        )

        # IMPORTANTE: sem commit(), a inserção NÃO é salva!
        conexao.commit()

        novo_id = cursor.lastrowid
        print(f"\n  ✓  Morador cadastrado com sucesso! (ID: {novo_id})")
        print(f"     {nome} — CPF: {formatar_cpf(cpf)}")

    except sqlite3.IntegrityError as e:
        print(f"\n  ✗  Erro de integridade: {e}")
    except Exception as e:
        print(f"\n  ✗  Erro inesperado: {e}")
    finally:
        fechar(conexao)


# ============================================================
# R — READ: LISTAR MORADORES
# ============================================================

def listar_moradores():
    """
    Busca e exibe todos os moradores ativos.

    Usa JOIN para trazer o endereço de cada morador
    (dados que estão nas tabelas residencias e morador_residencia).
    """
    separador("LISTA DE MORADORES ATIVOS")

    conexao = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # JOIN traz dados de 3 tabelas de uma vez!
        # moradores ← morador_residencia → residencias
        cursor.execute(
            """
            SELECT m.id,
                   m.nome,
                   m.cpf,
                   m.telefone,
                   r.numero_residencia,
                   r.bloco,
                   mr.tipo_morador
            FROM   moradores m
            LEFT JOIN morador_residencia mr ON m.id = mr.morador_id AND mr.ativo = 1
            LEFT JOIN residencias r         ON mr.residencia_id = r.id
            WHERE  m.ativo = 1
            ORDER  BY r.bloco, r.numero_residencia, m.nome
            """
        )

        moradores = cursor.fetchall()

        if not moradores:
            print("\n  Nenhum morador ativo encontrado.")
            return

        print(f"\n  Total de moradores ativos: {len(moradores)}\n")
        print(f"  {'ID':<4}  {'Nome':<28}  {'CPF':<15}  {'Apto':<6}  {'Bl':<3}  {'Tipo':<13}  Telefone")
        print(f"  {'─'*4}  {'─'*28}  {'─'*15}  {'─'*6}  {'─'*3}  {'─'*13}  {'─'*14}")

        for m in moradores:
            tipo_raw = m['tipo_morador'] or "—"
            tipo_label = "Proprietário" if tipo_raw == "proprietario" else (
                "Inquilino" if tipo_raw == "inquilino" else "—"
            )
            apto = m['numero_residencia'] or "—"
            bloco = m['bloco'] or "—"
            tel = m['telefone'] or "—"
            print(
                f"  {m['id']:<4}  {m['nome']:<28}  {formatar_cpf(m['cpf']):<15}  "
                f"{apto:<6}  {bloco:<3}  {tipo_label:<13}  {tel}"
            )

    except Exception as e:
        print(f"\n  ✗  Erro ao listar moradores: {e}")
    finally:
        fechar(conexao)


# ============================================================
# R — READ: BUSCAR MORADOR POR NOME
# ============================================================

def buscar_morador():
    """
    Procura moradores cujo nome contenha o texto digitado.

    O '%' no SQL é o coringa — substitui qualquer texto.
    '%Silva' = termina com Silva
    'Maria%' = começa com Maria
    '%ar%'   = contém 'ar' em qualquer posição
    """
    separador("BUSCAR MORADOR POR NOME")

    conexao = None
    try:
        termo = input("  Digite parte do nome : ").strip()
        if not termo:
            print("  ✗  Digite ao menos uma letra para buscar.")
            return

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT m.id, m.nome, m.cpf, m.telefone, m.email, m.ativo,
                   r.numero_residencia, r.bloco,
                   mr.tipo_morador
            FROM   moradores m
            LEFT JOIN morador_residencia mr ON m.id = mr.morador_id AND mr.ativo = 1
            LEFT JOIN residencias r         ON mr.residencia_id = r.id
            WHERE  m.nome LIKE ?
            ORDER  BY m.nome
            """,
            (f"%{termo}%",)
        )

        resultados = cursor.fetchall()

        if not resultados:
            print(f"\n  Nenhum morador encontrado com '{termo}'.")
            return

        print(f"\n  {len(resultados)} resultado(s) para '{termo}':\n")

        for m in resultados:
            status = "Ativo" if m['ativo'] == 1 else "Inativo"
            tipo = m['tipo_morador'] or "—"
            if tipo == "proprietario":
                tipo = "Proprietário"
            elif tipo == "inquilino":
                tipo = "Inquilino"
            apto = m['numero_residencia'] or "—"
            bloco = m['bloco'] or "—"

            print(f"  ┌── ID {m['id']} ─────────────────────────────")
            print(f"  │  Nome       : {m['nome']}")
            print(f"  │  CPF        : {formatar_cpf(m['cpf'])}")
            print(f"  │  Apto/Bloco : {apto} / {bloco}")
            print(f"  │  Tipo       : {tipo}")
            print(f"  │  Telefone   : {m['telefone'] or '—'}")
            print(f"  │  E-mail     : {m['email'] or '—'}")
            print(f"  │  Status     : {status}")
            print(f"  └─────────────────────────────────────────")
            print()

    except Exception as e:
        print(f"\n  ✗  Erro ao buscar: {e}")
    finally:
        fechar(conexao)


# ============================================================
# U — UPDATE: ATUALIZAR MORADOR
# ============================================================

def atualizar_morador():
    """
    Atualiza os dados pessoais de um morador.

    ATENÇÃO: sem WHERE o UPDATE muda TODOS os registros!
    Sempre filtre pelo ID para ter certeza de alterar só um.
    """
    separador("ATUALIZAR MORADOR")

    listar_moradores()

    conexao = None
    try:
        id_str = input("\n  ID do morador a atualizar: ").strip()
        try:
            id_morador = int(id_str)
        except ValueError:
            print("  ✗  ID deve ser um número inteiro.")
            return

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT * FROM moradores WHERE id = ? AND ativo = 1", (id_morador,))
        m = cursor.fetchone()

        if not m:
            print(f"  ✗  Morador ID {id_morador} não encontrado ou inativo.")
            return

        print(f"\n  Dados atuais de {m['nome']}:")
        print(f"  Telefone : {m['telefone'] or '—'}")
        print(f"  E-mail   : {m['email'] or '—'}")
        print()
        print("  (Deixe em branco para manter o valor atual)\n")

        novo_telefone = input(f"  Novo telefone [{m['telefone'] or '—'}] : ").strip() or m['telefone']
        novo_email = input(f"  Novo e-mail   [{m['email'] or '—'}] : ").strip() or m['email']

        cursor.execute(
            """
            UPDATE moradores
            SET    telefone         = ?,
                   email            = ?,
                   dt_atualizado_em = ?
            WHERE  id = ?
            """,
            (novo_telefone, novo_email, agora(), id_morador)
        )
        conexao.commit()

        linhas = cursor.rowcount
        if linhas > 0:
            print(f"\n  ✓  Dados de '{m['nome']}' atualizados com sucesso!")
        else:
            print("\n  ⚠  Nenhuma alteração registrada.")

    except Exception as e:
        print(f"\n  ✗  Erro ao atualizar: {e}")
    finally:
        fechar(conexao)


# ============================================================
# D — DELETE (soft): DESATIVAR MORADOR
# ============================================================

def desativar_morador():
    """
    Marca o morador como inativo (ativo = 0).

    SOFT DELETE: NÃO apagamos o registro — apenas "escondemos".
    Isso preserva o histórico de acessos e permite reativar depois.
    """
    separador("DESATIVAR MORADOR (Soft Delete)")

    print("  ⚠  O morador NÃO será apagado — apenas marcado como inativo.")
    print("     Seus dados ficam preservados no banco.\n")

    listar_moradores()

    conexao = None
    try:
        id_str = input("\n  ID do morador a desativar: ").strip()
        try:
            id_morador = int(id_str)
        except ValueError:
            print("  ✗  ID deve ser um número inteiro.")
            return

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT nome FROM moradores WHERE id = ? AND ativo = 1",
            (id_morador,)
        )
        m = cursor.fetchone()

        if not m:
            print(f"  ✗  Morador ID {id_morador} não encontrado ou já está inativo.")
            return

        print(f"\n  Morador: {m['nome']}")
        confirmacao = input("  Confirma desativação? (s/N) : ").strip().lower()

        if confirmacao != "s":
            print("  ✗  Operação cancelada.")
            return

        cursor.execute(
            """
            UPDATE moradores
            SET    ativo = 0, dt_atualizado_em = ?
            WHERE  id = ?
            """,
            (agora(), id_morador)
        )
        conexao.commit()

        print(f"\n  ✓  {m['nome']} desativado. Dados preservados no banco.")

    except Exception as e:
        print(f"\n  ✗  Erro ao desativar: {e}")
    finally:
        fechar(conexao)


# ============================================================
# BÔNUS — RESUMO DO CONDOMÍNIO
# ============================================================

def resumo_moradores():
    """
    Exibe um resumo rápido: totais de ativos, proprietários e inquilinos.
    """
    separador("RESUMO DO CONDOMÍNIO")

    conexao = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT
                (SELECT COUNT(*) FROM moradores WHERE ativo = 1) AS ativos,
                (SELECT COUNT(*) FROM moradores WHERE ativo = 0) AS inativos,
                (SELECT COUNT(*) FROM morador_residencia WHERE tipo_morador='proprietario' AND ativo=1) AS proprietarios,
                (SELECT COUNT(*) FROM morador_residencia WHERE tipo_morador='inquilino' AND ativo=1) AS inquilinos,
                (SELECT COUNT(*) FROM residencias WHERE ativo = 1) AS residencias,
                (SELECT COUNT(*) FROM visitantes) AS visitantes
            """
        )

        r = cursor.fetchone()

        print(f"""
  ╔══════════════════════════════════════╗
  ║  MORADORES                           ║
  ╠══════════════════════════════════════╣
  ║  Ativos         : {str(r['ativos']):<19}║
  ║    Proprietários : {str(r['proprietarios']):<19}║
  ║    Inquilinos    : {str(r['inquilinos']):<19}║
  ║  Inativos       : {str(r['inativos']):<19}║
  ╠══════════════════════════════════════╣
  ║  CONDOMÍNIO                          ║
  ╠══════════════════════════════════════╣
  ║  Residências    : {str(r['residencias']):<19}║
  ║  Visitantes     : {str(r['visitantes']):<19}║
  ╚══════════════════════════════════════╝""")

    except Exception as e:
        print(f"\n  ✗  Erro ao gerar resumo: {e}")
    finally:
        fechar(conexao)


# ============================================================
# MENU PRINCIPAL
# ============================================================

def menu():
    """Exibe o menu e retorna a opção escolhida."""
    separador("SISTEMA DE PORTARIA — MORADORES")
    print("""
  1. Cadastrar novo morador       (C - Create)
  2. Listar moradores             (R - Read)
  3. Buscar morador por nome      (R - Read)
  4. Atualizar dados do morador   (U - Update)
  5. Desativar morador            (D - Delete Soft)
  ─────────────────────────────────────────────
  6. Resumo do condomínio
  ─────────────────────────────────────────────
  0. Sair
    """)
    return input("  Escolha uma opção: ").strip()


def main():
    """Loop principal do programa."""

    caminho = os.path.normpath(CAMINHO_BANCO)
    if not os.path.exists(caminho):
        print(f"\n  ✗  Banco não encontrado em: {caminho}")
        print("     Primeiro, crie o banco pelo DBeaver:")
        print("     1. Abra o DBeaver")
        print("     2. Crie uma conexão SQLite apontando para portaria.db")
        print("     3. Execute o arquivo projeto_portaria_completo.sql")
        return

    print("\n  Bem-vindo ao Sistema de Portaria, Ademilson!")
    print(f"  Banco de dados: {os.path.basename(caminho)}")

    while True:
        opcao = menu()

        if   opcao == "1": cadastrar_morador()
        elif opcao == "2": listar_moradores()
        elif opcao == "3": buscar_morador()
        elif opcao == "4": atualizar_morador()
        elif opcao == "5": desativar_morador()
        elif opcao == "6": resumo_moradores()
        elif opcao == "0":
            separador()
            print("  Até a próxima aula! Continue praticando!")
            separador()
            break
        else:
            print("  ✗  Opção inválida. Digite um número entre 0 e 6.")

        pausar()


if __name__ == "__main__":
    main()
