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
  Na semana você criou o banco portaria.db com SQL puro.
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
  (criado pela tarefa antecipada com projeto_portaria_completo.sql)
"""

import sqlite3
import os
from datetime import datetime


# ============================================================
# CONFIGURAÇÃO DO BANCO
# ============================================================
# Caminho até o banco que você criou na semana:
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
    Muito mais legível!
    """
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    # Ativa verificação de chaves estrangeiras (FOREIGN KEY)
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
    Entrada : '12345678901'
    Saída   : '123.456.789-01'
    """
    cpf = str(cpf).strip()
    if len(cpf) == 11 and cpf.isdigit():
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return cpf  # retorna como veio se não conseguir formatar


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

    Conceito SQL usado:
      INSERT INTO moradores (coluna1, coluna2, ...) VALUES (?, ?, ...)

    O '?' é um PLACEHOLDER — o Python substitui pelo valor real.
    Isso evita problemas de segurança (SQL Injection).
    """
    separador("CADASTRAR NOVO MORADOR")

    try:
        # ── Coleta de dados ──────────────────────────────
        nome = input("  Nome completo       : ").strip()
        if not nome:
            print("  ✗  Nome é obrigatório!")
            return

        cpf = input("  CPF (só números)    : ").strip()
        if not validar_cpf(cpf):
            return

        numero_residencia = input("  Apartamento (ex:101): ").strip()
        if not numero_residencia:
            print("  ✗  Apartamento é obrigatório!")
            return

        bloco = input("  Bloco [A]           : ").strip() or "A"
        telefone = input("  Telefone            : ").strip()
        email = input("  E-mail              : ").strip()

        print()
        print("  Tipo de morador:")
        print("    1. Proprietário")
        print("    2. Inquilino")
        opcao_tipo = input("  Escolha [1]         : ").strip() or "1"
        tipo_morador = "inquilino" if opcao_tipo == "2" else "proprietario"

        # ── Verificação de CPF duplicado ─────────────────
        # TODO: Entenda o que acontece aqui — buscamos no banco ANTES de inserir.
        #       Se já existir um morador com esse CPF, recusamos o cadastro.
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT nome FROM moradores WHERE cpf = ?", (cpf,))
        existente = cursor.fetchone()

        if existente:
            print(f"\n  ✗  CPF {formatar_cpf(cpf)} já está cadastrado.")
            print(f"     Morador: {existente['nome']}")
            fechar(conexao)
            return

        # ── INSERT no banco ───────────────────────────────
        # TODO: Observe que passamos os valores com '?' — nunca concatene
        #       strings diretamente no SQL (ex: f"VALUES ('{nome}')") !
        cursor.execute(
            """
            INSERT INTO moradores
                (nome, cpf, numero_residencia, bloco, telefone, email, tipo_morador)
            VALUES
                (?, ?, ?, ?, ?, ?, ?)
            """,
            (nome, cpf, numero_residencia, bloco, telefone or None, email or None, tipo_morador)
        )

        # IMPORTANTE: sem commit(), a inserção NÃO é salva no disco!
        conexao.commit()

        novo_id = cursor.lastrowid  # pega o ID gerado automaticamente

        print(f"\n  ✓  Morador cadastrado com sucesso! (ID: {novo_id})")
        print(f"     {nome} — Apto {numero_residencia}/{bloco} — {tipo_morador}")

    except sqlite3.IntegrityError as e:
        print(f"\n  ✗  Erro de integridade: {e}")
        print("     Verifique se o CPF já está cadastrado.")
    except Exception as e:
        print(f"\n  ✗  Erro inesperado: {e}")
    finally:
        # 'finally' executa SEMPRE — mesmo se der erro
        fechar(conexao)


# ============================================================
# R — READ: LISTAR MORADORES
# ============================================================

def listar_moradores():
    """
    Busca e exibe todos os moradores ativos.

    Conceito SQL usado:
      SELECT coluna1, coluna2 FROM tabela WHERE condicao ORDER BY coluna
    """
    separador("LISTA DE MORADORES ATIVOS")

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # TODO: Esta consulta traz apenas moradores ATIVOS (ativo = 1),
        #       ordenados por bloco e depois por numero_residencia.
        #       Veja como o SQL é quase "inglês"!
        cursor.execute(
            """
            SELECT id, nome, cpf, numero_residencia, bloco, tipo_morador, telefone
            FROM   moradores
            WHERE  ativo = 1
            ORDER  BY bloco, numero_residencia
            """
        )

        moradores = cursor.fetchall()  # fetchall() = pegar TODOS os resultados

        if not moradores:
            print("\n  Nenhum morador ativo encontrado.")
            return

        print(f"\n  Total de moradores ativos: {len(moradores)}\n")
        print(f"  {'ID':<4}  {'Nome':<28}  {'CPF':<15}  {'Apto':<6}  {'Bl':<3}  {'Tipo':<13}  Telefone")
        print(f"  {'─'*4}  {'─'*28}  {'─'*15}  {'─'*6}  {'─'*3}  {'─'*13}  {'─'*14}")

        for m in moradores:
            tipo_label = "Proprietário" if m['tipo_morador'] == "proprietario" else "Inquilino   "
            tel = m['telefone'] or "—"
            print(
                f"  {m['id']:<4}  {m['nome']:<28}  {formatar_cpf(m['cpf']):<15}  "
                f"{m['numero_residencia']:<6}  {m['bloco']:<3}  {tipo_label:<13}  {tel}"
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

    Conceito SQL usado:
      WHERE nome LIKE '%texto%'

    O '%' é o coringa — substitui qualquer sequência de caracteres.
    Exemplos:
      '%Silva'   → termina com "Silva"
      'Maria%'   → começa com "Maria"
      '%ar%'     → contém "ar" em qualquer posição
    """
    separador("BUSCAR MORADOR POR NOME")

    try:
        termo = input("  Digite parte do nome : ").strip()
        if not termo:
            print("  ✗  Digite ao menos uma letra para buscar.")
            return

        conexao = conectar()
        cursor = conexao.cursor()

        # TODO: O '?' recebe '%termo%' — os % ficam FORA das aspas no SQL,
        #       mas dentro do valor Python. O sqlite3 monta tudo direitinho.
        cursor.execute(
            """
            SELECT id, nome, cpf, numero_residencia, bloco, tipo_morador,
                   telefone, email, ativo
            FROM   moradores
            WHERE  nome LIKE ?
            ORDER  BY nome
            """,
            (f"%{termo}%",)   # <- note a vírgula: é uma tupla de 1 elemento!
        )

        resultados = cursor.fetchall()

        if not resultados:
            print(f"\n  Nenhum morador encontrado com '{termo}'.")
            return

        print(f"\n  {len(resultados)} resultado(s) para '{termo}':\n")

        for m in resultados:
            status = "✓ Ativo" if m['ativo'] == 1 else "✗ Inativo"
            tipo = "Proprietário" if m['tipo_morador'] == "proprietario" else "Inquilino"
            print(f"  ┌── ID {m['id']} ─────────────────────────────")
            print(f"  │  Nome       : {m['nome']}")
            print(f"  │  CPF        : {formatar_cpf(m['cpf'])}")
            print(f"  │  Apto/Bloco : {m['numero_residencia']} / {m['bloco']}")
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
    Atualiza os dados de um morador já cadastrado.

    Conceito SQL usado:
      UPDATE tabela SET coluna = valor WHERE id = ?

    ATENÇÃO: sem WHERE o UPDATE muda TODOS os registros!
    Sempre filtre pelo ID para ter certeza de alterar só um.
    """
    separador("ATUALIZAR MORADOR")

    listar_moradores()  # mostra a lista para o usuário escolher

    try:
        id_str = input("\n  ID do morador a atualizar: ").strip()
        try:
            id_morador = int(id_str)
        except ValueError:
            print("  ✗  ID deve ser um número inteiro.")
            return

        conexao = conectar()
        cursor = conexao.cursor()

        # Verificar se o morador existe
        cursor.execute("SELECT * FROM moradores WHERE id = ? AND ativo = 1", (id_morador,))
        m = cursor.fetchone()

        if not m:
            print(f"  ✗  Morador ID {id_morador} não encontrado ou inativo.")
            fechar(conexao)
            return

        # Mostra dados atuais
        print(f"\n  Dados atuais de {m['nome']}:")
        print(f"  Telefone : {m['telefone'] or '—'}")
        print(f"  E-mail   : {m['email'] or '—'}")
        print(f"  Apto/Bl  : {m['numero_residencia']} / {m['bloco']}")
        print()
        print("  (Deixe em branco para manter o valor atual)\n")

        novo_telefone  = input(f"  Novo telefone  [{m['telefone'] or '—'}] : ").strip() or m['telefone']
        novo_email     = input(f"  Novo e-mail    [{m['email']    or '—'}] : ").strip() or m['email']
        novo_apartamento = input(f"  Novo apto      [{m['numero_residencia']}]  : ").strip() or m['numero_residencia']
        novo_bloco     = input(f"  Novo bloco     [{m['bloco']}]        : ").strip() or m['bloco']

        # TODO: Veja o SET com vírgulas entre as colunas.
        #       'dt_atualizado_em' recebe a data/hora atual automaticamente.
        cursor.execute(
            """
            UPDATE moradores
            SET    telefone     = ?,
                   email        = ?,
                   numero_residencia  = ?,
                   bloco        = ?,
                   dt_atualizado_em = ?
            WHERE  id = ?
            """,
            (novo_telefone, novo_email, novo_apartamento, novo_bloco, agora(), id_morador)
        )
        conexao.commit()

        linhas = cursor.rowcount  # quantas linhas foram alteradas?
        if linhas > 0:
            print(f"\n  ✓  Dados de '{m['nome']}' atualizados com sucesso!")
        else:
            print("\n  ⚠  Nenhuma alteração registrada.")

    except Exception as e:
        print(f"\n  ✗  Erro ao atualizar: {e}")
    finally:
        fechar(conexao)


# ============================================================
# D — DELETE (macio): DESATIVAR MORADOR
# ============================================================

def desativar_morador():
    """
    Marca o morador como inativo (ativo = 0).

    SOFT DELETE: NÃO apagamos o registro — apenas "escondemos".
    Isso é muito importante:
      - Histórico de acessos continua íntegro
      - Podemos reativar se precisar
      - Auditoria: sempre sabemos que aquela pessoa morou lá

    Conceito SQL usado:
      UPDATE moradores SET ativo = 0 WHERE id = ?
    """
    separador("DESATIVAR MORADOR (Soft Delete)")

    print("  ⚠  O morador NÃO será apagado — apenas marcado como inativo.")
    print("     Seus dados ficam preservados no banco.\n")

    listar_moradores()

    try:
        id_str = input("\n  ID do morador a desativar: ").strip()
        try:
            id_morador = int(id_str)
        except ValueError:
            print("  ✗  ID deve ser um número inteiro.")
            return

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT nome, numero_residencia, bloco FROM moradores WHERE id = ? AND ativo = 1", (id_morador,))
        m = cursor.fetchone()

        if not m:
            print(f"  ✗  Morador ID {id_morador} não encontrado ou já está inativo.")
            fechar(conexao)
            return

        print(f"\n  Morador: {m['nome']} — Apto {m['numero_residencia']}/{m['bloco']}")
        confirmacao = input("  Confirma desativação? (s/N) : ").strip().lower()

        if confirmacao != "s":
            print("  ✗  Operação cancelada.")
            fechar(conexao)
            return

        # TODO: Observe que apenas 'ativo' muda — todo o resto permanece.
        cursor.execute(
            """
            UPDATE moradores
            SET    ativo        = 0,
                   dt_atualizado_em = ?
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
# BÔNUS — CONSULTA RÁPIDA DE STATUS
# ============================================================

def resumo_moradores():
    """
    Exibe um resumo rápido: totais de ativos, proprietários e inquilinos.

    Conceito SQL usado:
      SELECT COUNT(*) — conta registros
      GROUP BY        — agrupa por valor de coluna
    """
    separador("RESUMO DO CONDOMÍNIO")

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # Subconsultas dentro de um único SELECT
        cursor.execute(
            """
            SELECT
                (SELECT COUNT(*) FROM moradores WHERE ativo = 1)                              AS ativos,
                (SELECT COUNT(*) FROM moradores WHERE ativo = 1 AND tipo_morador='proprietario') AS proprietarios,
                (SELECT COUNT(*) FROM moradores WHERE ativo = 1 AND tipo_morador='inquilino')    AS inquilinos,
                (SELECT COUNT(*) FROM moradores WHERE ativo = 0)                              AS inativos,
                (SELECT COUNT(*) FROM moradores WHERE foto_url IS NULL AND ativo = 1)         AS sem_foto,
                (SELECT COUNT(*) FROM moradores WHERE biometria_hash IS NULL AND ativo = 1)   AS sem_biometria
            """
        )

        r = cursor.fetchone()

        print(f"""
  ╔══════════════════════════════════════╗
  ║  MORADORES                           ║
  ╠══════════════════════════════════════╣
  ║  Ativos    : {str(r['ativos']):<25}║
  ║    Proprietários : {str(r['proprietarios']):<20}║
  ║    Inquilinos    : {str(r['inquilinos']):<20}║
  ║  Inativos  : {str(r['inativos']):<25}║
  ╠══════════════════════════════════════╣
  ║  CADASTROS PENDENTES                 ║
  ╠══════════════════════════════════════╣
  ║  Sem foto       : {str(r['sem_foto']):<20}║
  ║  Sem biometria  : {str(r['sem_biometria']):<20}║
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
  5. Desativar morador            (D - Delete macio)
  ─────────────────────────────────────────────
  6. Resumo do condomínio
  ─────────────────────────────────────────────
  0. Sair
    """)
    return input("  Escolha uma opção: ").strip()


def main():
    """Loop principal do programa."""

    # Verifica se o banco existe antes de começar
    caminho = os.path.normpath(CAMINHO_BANCO)
    if not os.path.exists(caminho):
        print(f"\n  ✗  Banco não encontrado em: {caminho}")
        print("     Execute primeiro a tarefa antecipada:")
        print("     sqlite3 portaria.db < projeto_portaria_completo.sql")
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
            print("  Até a próxima aula! Continue praticando! 👋")
            separador()
            break
        else:
            print("  ✗  Opção inválida. Digite um número entre 0 e 6.")

        pausar()


if __name__ == "__main__":
    main()
