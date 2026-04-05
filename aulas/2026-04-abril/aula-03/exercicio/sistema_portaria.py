#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  SISTEMA DE PORTARIA — Completo
  Aula 03 | 16/04/2026
============================================================

Aluno : Ademilson
Prof  : Thiago

O QUE VAMOS FAZER HOJE:
  Na Aula 02 você fez o CRUD de moradores.
  Hoje vamos EXPANDIR o sistema com:

    - CRUD de Visitantes  (padrão idêntico ao de moradores!)
    - Registro de Acessos (entrada e saída de visitantes)
    - Consultas com JOIN  (cruzar dados de tabelas diferentes)
    - Relatório geral     (resumo completo do condomínio)

  O CRUD de moradores já está PRONTO aqui como referência.
  Seus TODO estão nas seções de VISITANTES e ACESSOS.

COMO EXECUTAR:
  python sistema_portaria.py

PRÉ-REQUISITO:
  portaria.db criado e com dados (feito na tarefa antecipada).
  CRUD de moradores da Aula 02 funcionando.
"""

import sqlite3
import os
from datetime import datetime


# ============================================================
# CONFIGURAÇÃO DO BANCO
# ============================================================

CAMINHO_BANCO = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "..", "..",
    "src", "infra", "database", "portaria.db"
)


# ============================================================
# FUNÇÕES DE CONEXÃO E AUXILIARES
# ============================================================

def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao

def fechar(conexao):
    if conexao:
        conexao.close()

def separador(titulo=""):
    print()
    if titulo:
        print(f"  {'═' * 52}")
        print(f"  {titulo.center(52)}")
        print(f"  {'═' * 52}")
    else:
        print(f"  {'─' * 52}")

def formatar_cpf(cpf):
    cpf = str(cpf).strip()
    if len(cpf) == 11 and cpf.isdigit():
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return cpf

def agora():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def pausar():
    input("\n  Pressione ENTER para continuar...")


# ============================================================
# CRUD DE MORADORES — PRONTO (referência da Aula 02)
# ============================================================

def listar_moradores(apenas_ativos=True):
    """Lista moradores. Parâmetro apenas_ativos controla o filtro."""
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        filtro = "WHERE ativo = 1" if apenas_ativos else ""
        cursor.execute(
            f"""
            SELECT id, nome, numero_residencia, bloco, tipo_morador, telefone
            FROM   moradores
            {filtro}
            ORDER  BY bloco, numero_residencia
            """
        )
        moradores = cursor.fetchall()
        if not moradores:
            print("\n  Nenhum morador encontrado.")
            return []

        print(f"\n  {'ID':<4}  {'Nome':<28}  {'Apto':<6}  {'Bl':<3}  {'Tipo':<13}  Telefone")
        print(f"  {'─'*4}  {'─'*28}  {'─'*6}  {'─'*3}  {'─'*13}  {'─'*14}")
        for m in moradores:
            tipo = "Proprietário" if m['tipo_morador'] == "proprietario" else "Inquilino   "
            print(f"  {m['id']:<4}  {m['nome']:<28}  {m['numero_residencia']:<6}  {m['bloco']:<3}  {tipo}  {m['telefone'] or '—'}")
        return list(moradores)
    except Exception as e:
        print(f"\n  ✗  Erro: {e}")
        return []
    finally:
        fechar(conexao)


def cadastrar_morador():
    """CRUD de moradores — igual à Aula 02 (aqui como referência)."""
    separador("CADASTRAR NOVO MORADOR")
    try:
        nome = input("  Nome completo       : ").strip()
        cpf  = input("  CPF (só números)    : ").strip()
        apto = input("  Apartamento         : ").strip()
        bloco = input("  Bloco [A]           : ").strip() or "A"
        telefone = input("  Telefone            : ").strip()
        email    = input("  E-mail              : ").strip()
        tipo = "inquilino" if input("  Tipo (1=Prop/2=Inq) [1]: ").strip() == "2" else "proprietario"

        if not nome or not cpf or not apto:
            print("  ✗  Nome, CPF e Apartamento são obrigatórios.")
            return

        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT nome FROM moradores WHERE cpf = ?", (cpf,))
        if cursor.fetchone():
            print(f"  ✗  CPF {formatar_cpf(cpf)} já cadastrado.")
            fechar(conexao); return

        cursor.execute(
            "INSERT INTO moradores (nome, cpf, numero_residencia, bloco, telefone, email, tipo_morador) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (nome, cpf, apto, bloco, telefone or None, email or None, tipo)
        )
        conexao.commit()
        print(f"\n  ✓  {nome} cadastrado! ID: {cursor.lastrowid}")
    except Exception as e:
        print(f"\n  ✗  Erro: {e}")
    finally:
        fechar(conexao)


# ============================================================
# CRUD DE VISITANTES
# ============================================================
# Perceba que o padrão é IDÊNTICO ao de moradores!
# A diferença: visitantes usam 'bloqueado' em vez de 'ativo'.

def listar_visitantes():
    """
    READ: Lista todos os visitantes cadastrados.

    Conceito SQL:
      SELECT ... FROM visitantes ORDER BY nome

    Diferença do morador: mostramos se está BLOQUEADO (🚫) ou LIBERADO (✓).
    """
    separador("LISTA DE VISITANTES")

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # TODO: Execute um SELECT trazendo todas as colunas úteis de visitantes.
        #       Ordene pelo nome.
        #       Colunas sugeridas: id, nome, documento, tipo_documento, telefone, bloqueado
        cursor.execute(
            """
            SELECT id, nome, documento, tipo_documento, telefone, bloqueado
            FROM   visitantes
            ORDER  BY nome
            """
        )

        visitantes = cursor.fetchall()

        if not visitantes:
            print("\n  Nenhum visitante cadastrado.")
            return []

        print(f"\n  Total: {len(visitantes)} visitante(s)\n")
        print(f"  {'ID':<4}  {'Nome':<28}  {'Documento':<12}  {'Tipo':<10}  Status")
        print(f"  {'─'*4}  {'─'*28}  {'─'*12}  {'─'*10}  {'─'*12}")

        for v in visitantes:
            # TODO: Mostre '🚫 Bloqueado' se bloqueado=1, '✓ Liberado' se bloqueado=0
            status = "🚫 Bloqueado" if v['bloqueado'] == 1 else "✓ Liberado"
            print(
                f"  {v['id']:<4}  {v['nome']:<28}  {v['documento']:<12}  "
                f"{v['tipo_documento']:<10}  {status}"
            )

        return list(visitantes)

    except Exception as e:
        print(f"\n  ✗  Erro ao listar visitantes: {e}")
        return []
    finally:
        fechar(conexao)


def cadastrar_visitante():
    """
    CREATE: Adiciona um novo visitante ao banco.

    Conceito SQL:
      INSERT INTO visitantes (nome, documento, tipo_documento, telefone)
      VALUES (?, ?, ?, ?)

    Diferença do morador: pedimos DOCUMENTO em vez de CPF.
    Tipos aceitos: RG, CNH, PASSAPORTE, OUTRO  (restrição CHECK no banco!)
    """
    separador("CADASTRAR NOVO VISITANTE")

    try:
        # TODO: Peça os dados ao usuário
        nome = input("  Nome completo          : ").strip()
        if not nome:
            print("  ✗  Nome é obrigatório!"); return

        documento = input("  Número do documento    : ").strip()
        if not documento:
            print("  ✗  Documento é obrigatório!"); return

        print("\n  Tipo de documento:")
        print("    1. RG          2. CNH")
        print("    3. PASSAPORTE  4. OUTRO")
        opcao = input("  Escolha [1]            : ").strip()
        tipos = {"1": "RG", "2": "CNH", "3": "PASSAPORTE", "4": "OUTRO"}
        tipo_documento = tipos.get(opcao, "RG")

        telefone = input("  Telefone               : ").strip()

        conexao = conectar()
        cursor = conexao.cursor()

        # TODO: Verifique se o documento já está cadastrado
        #       (evita cadastrar a mesma pessoa duas vezes)
        cursor.execute(
            "SELECT nome FROM visitantes WHERE documento = ?", (documento,)
        )
        existente = cursor.fetchone()
        if existente:
            print(f"\n  ⚠  Documento já cadastrado para: {existente['nome']}")
            print("     Deseja cadastrar mesmo assim? (s/N) ", end="")
            if input().strip().lower() != "s":
                fechar(conexao); return

        # TODO: Insira o visitante no banco
        #       Colunas: nome, documento, tipo_documento, telefone
        cursor.execute(
            """
            INSERT INTO visitantes (nome, documento, tipo_documento, telefone)
            VALUES (?, ?, ?, ?)
            """,
            (nome, documento, tipo_documento, telefone or None)
        )
        conexao.commit()

        print(f"\n  ✓  {nome} cadastrado como visitante! ID: {cursor.lastrowid}")

    except Exception as e:
        print(f"\n  ✗  Erro ao cadastrar visitante: {e}")
    finally:
        fechar(conexao)


def buscar_visitante():
    """
    READ: Busca visitante por nome (parcial com LIKE).

    Mesmo padrão do buscar_morador() da Aula 02!
    """
    separador("BUSCAR VISITANTE POR NOME")

    try:
        termo = input("  Digite parte do nome : ").strip()
        if not termo:
            print("  ✗  Digite ao menos uma letra."); return

        conexao = conectar()
        cursor = conexao.cursor()

        # TODO: Use SELECT com LIKE — mesmo padrão da Aula 02!
        cursor.execute(
            """
            SELECT id, nome, documento, tipo_documento, telefone, bloqueado, motivo_bloqueio
            FROM   visitantes
            WHERE  nome LIKE ?
            ORDER  BY nome
            """,
            (f"%{termo}%",)
        )

        resultados = cursor.fetchall()

        if not resultados:
            print(f"\n  Nenhum visitante encontrado com '{termo}'."); return

        print(f"\n  {len(resultados)} resultado(s):\n")
        for v in resultados:
            status = "🚫 BLOQUEADO" if v['bloqueado'] == 1 else "✓ Liberado"
            print(f"  ┌── ID {v['id']} ───────────────────────────────")
            print(f"  │  Nome       : {v['nome']}")
            print(f"  │  Documento  : {v['documento']} ({v['tipo_documento']})")
            print(f"  │  Telefone   : {v['telefone'] or '—'}")
            print(f"  │  Status     : {status}")
            if v['bloqueado']:
                print(f"  │  Motivo     : {v['motivo_bloqueio'] or '—'}")
            print(f"  └─────────────────────────────────────────────")
            print()

    except Exception as e:
        print(f"\n  ✗  Erro ao buscar: {e}")
    finally:
        fechar(conexao)


def bloquear_visitante():
    """
    DELETE macio de visitantes: marca como bloqueado (bloqueado = 1).

    Conceito SQL:
      UPDATE visitantes SET bloqueado = 1, motivo_bloqueio = ? WHERE id = ?

    Diferença do soft-delete de moradores:
      moradores → ativo = 0
      visitantes → bloqueado = 1

    Por que guardar o MOTIVO? Segurança! O porteiro do próximo
    turno precisa saber POR QUE aquela pessoa não pode entrar.
    """
    separador("BLOQUEAR VISITANTE")

    listar_visitantes()

    try:
        id_str = input("\n  ID do visitante a bloquear: ").strip()
        try:
            id_visitante = int(id_str)
        except ValueError:
            print("  ✗  ID deve ser um número."); return

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT nome, bloqueado FROM visitantes WHERE id = ?", (id_visitante,)
        )
        v = cursor.fetchone()

        if not v:
            print(f"  ✗  Visitante ID {id_visitante} não encontrado.")
            fechar(conexao); return

        if v['bloqueado'] == 1:
            print(f"  ⚠  {v['nome']} já está bloqueado!")
            fechar(conexao); return

        motivo = input(f"  Motivo do bloqueio de {v['nome']}: ").strip()
        if not motivo:
            print("  ✗  O motivo é obrigatório para registrar o bloqueio."); return

        # TODO: Atualize o banco — bloqueado = 1 e salve o motivo
        cursor.execute(
            """
            UPDATE visitantes
            SET    bloqueado       = 1,
                   motivo_bloqueio = ?
            WHERE  id = ?
            """,
            (motivo, id_visitante)
        )
        conexao.commit()

        print(f"\n  ✓  {v['nome']} bloqueado. Motivo registrado.")
        print("     Ele não poderá mais entrar no condomínio.")

    except Exception as e:
        print(f"\n  ✗  Erro ao bloquear: {e}")
    finally:
        fechar(conexao)


# ============================================================
# REGISTRO DE ACESSOS (ENTRADA E SAÍDA)
# ============================================================
# Esta é a tabela mais importante do sistema:
# cada vez que alguém entra ou sai, registramos aqui.

def registrar_entrada():
    """
    Registra a ENTRADA de um visitante no condomínio.

    Fluxo real da portaria:
      1. Visitante chega e diz para quem vai
      2. Porteiro verifica se não está BLOQUEADO
      3. Se liberado: registra a entrada (INSERT em acessos)
      4. dt_saida_em fica NULL enquanto o visitante ainda está dentro

    Conceito SQL:
      INSERT INTO acessos (visitante_id, morador_id, motivo, porteiro) VALUES (?, ?, ?, ?)
    """
    separador("REGISTRAR ENTRADA DE VISITANTE")

    try:
        # Mostrar lista de visitantes para escolher
        print("  Visitantes cadastrados:\n")
        listar_visitantes()

        id_str = input("\n  ID do visitante que chegou: ").strip()
        try:
            id_visitante = int(id_str)
        except ValueError:
            print("  ✗  ID deve ser um número."); return

        conexao = conectar()
        cursor = conexao.cursor()

        # TODO: Busque o visitante e verifique se está BLOQUEADO
        cursor.execute(
            "SELECT nome, bloqueado, motivo_bloqueio FROM visitantes WHERE id = ?",
            (id_visitante,)
        )
        v = cursor.fetchone()

        if not v:
            print(f"  ✗  Visitante ID {id_visitante} não encontrado."); fechar(conexao); return

        # VERIFICAÇÃO DE SEGURANÇA: bloqueado não pode entrar!
        if v['bloqueado'] == 1:
            print(f"\n  🚫  ACESSO NEGADO — {v['nome']} está BLOQUEADO!")
            print(f"     Motivo: {v['motivo_bloqueio'] or 'sem motivo registrado'}")
            fechar(conexao); return

        print(f"\n  ✓  {v['nome']} — Entrada liberada.")

        # Mostrar moradores para escolher quem autorizou
        print("\n  Moradores ativos:\n")
        listar_moradores(apenas_ativos=True)

        id_morador_str = input("\n  ID do morador que autorizou: ").strip()
        try:
            id_morador = int(id_morador_str)
        except ValueError:
            print("  ✗  ID do morador deve ser número."); fechar(conexao); return

        # Confirma que o morador existe
        cursor.execute("SELECT nome, numero_residencia FROM moradores WHERE id = ? AND ativo = 1", (id_morador,))
        m = cursor.fetchone()
        if not m:
            print(f"  ✗  Morador ID {id_morador} não encontrado."); fechar(conexao); return

        motivo  = input("  Motivo da visita : ").strip() or "Visita"
        porteiro = input("  Nome do porteiro : ").strip() or "Porteiro"

        # TODO: Insira o registro de entrada na tabela 'acessos'
        #       A dt_entrada_em e preenchida automaticamente (DEFAULT CURRENT_TIMESTAMP)
        #       A dt_saida_em fica NULL por enquanto — o visitante ainda está dentro!
        cursor.execute(
            """
            INSERT INTO acessos (visitante_id, morador_id, motivo, porteiro)
            VALUES (?, ?, ?, ?)
            """,
            (id_visitante, id_morador, motivo, porteiro)
        )
        conexao.commit()

        print(f"\n  ✓  Entrada registrada!")
        print(f"     {v['nome']} → Apto {m['numero_residencia']} de {m['nome']}")
        print(f"     Motivo: {motivo}")

    except Exception as e:
        print(f"\n  ✗  Erro ao registrar entrada: {e}")
    finally:
        fechar(conexao)


def registrar_saida():
    """
    Registra a SAÍDA de um visitante — preenche 'dt_saida_em' no acesso.

    Conceito SQL:
      UPDATE acessos SET dt_saida_em = CURRENT_TIMESTAMP WHERE id = ?

    Antes de registrar, mostramos quem ainda está DENTRO (dt_saida_em IS NULL).
    """
    separador("REGISTRAR SAÍDA DE VISITANTE")

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # TODO: Busque os acessos onde dt_saida_em IS NULL
        #       (essas são as pessoas que ainda estão dentro)
        #       Use JOIN para mostrar o nome do visitante e do morador.
        cursor.execute(
            """
            SELECT
                a.id          AS acesso_id,
                v.nome        AS visitante,
                m.nome        AS morador,
                m.numero_residencia AS numero_residencia,
                a.motivo,
                a.dt_entrada_em
            FROM  acessos a
                  JOIN visitantes v ON a.visitante_id = v.id
                  JOIN moradores  m ON a.morador_id   = m.id
            WHERE a.dt_saida_em IS NULL
            ORDER BY a.dt_entrada_em
            """
        )
        dentro = cursor.fetchall()

        if not dentro:
            print("\n  Não há ninguém dentro do condomínio no momento.")
            fechar(conexao); return

        print(f"\n  Visitantes dentro agora ({len(dentro)}):\n")
        print(f"  {'ID':<4}  {'Visitante':<28}  {'Apto':<6}  {'Motivo':<20}  Entrada")
        print(f"  {'─'*4}  {'─'*28}  {'─'*6}  {'─'*20}  {'─'*16}")

        for a in dentro:
            print(
                f"  {a['acesso_id']:<4}  {a['visitante']:<28}  "
                f"{a['numero_residencia']:<6}  {a['motivo']:<20}  {a['dt_entrada_em']}"
            )

        id_str = input("\n  ID do registro de acesso (coluna ID): ").strip()
        try:
            acesso_id = int(id_str)
        except ValueError:
            print("  ✗  ID deve ser número."); fechar(conexao); return

        # TODO: Atualize a coluna dt_saida_em com CURRENT_TIMESTAMP
        cursor.execute(
            """
            UPDATE acessos
            SET    dt_saida_em = CURRENT_TIMESTAMP
            WHERE  id = ? AND dt_saida_em IS NULL
            """,
            (acesso_id,)
        )
        conexao.commit()

        if cursor.rowcount == 0:
            print("  ✗  Registro não encontrado ou saída já registrada.")
        else:
            print(f"\n  ✓  Saída registrada para o acesso ID {acesso_id}.")

    except Exception as e:
        print(f"\n  ✗  Erro ao registrar saída: {e}")
    finally:
        fechar(conexao)


# ============================================================
# CONSULTAS COM JOIN
# ============================================================
# JOIN = cruzar dados de tabelas diferentes.
# É como fazer PROCV no Excel, mas muito mais poderoso!

def quem_esta_dentro():
    """
    Lista quem está atualmente dentro do condomínio.

    Conceito SQL:
      JOIN para cruzar acessos + visitantes + moradores
      WHERE dt_saida_em IS NULL → ainda está dentro!
    """
    separador("QUEM ESTÁ DENTRO AGORA?")

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # TODO: Entenda este JOIN:
        #   - Partimos da tabela 'acessos' (a)
        #   - JOIN com 'visitantes' (v) para pegar o nome do visitante
        #   - JOIN com 'moradores'  (m) para pegar o nome e apto do morador
        #   - WHERE dt_saida_em IS NULL filtra quem ainda está dentro
        cursor.execute(
            """
            SELECT
                v.nome          AS visitante,
                m.nome          AS morador,
                m.numero_residencia   AS numero_residencia,
                m.bloco         AS bloco,
                a.motivo,
                a.dt_entrada_em,
                a.porteiro
            FROM  acessos a
                  JOIN visitantes v ON a.visitante_id = v.id
                  JOIN moradores  m ON a.morador_id   = m.id
            WHERE a.dt_saida_em IS NULL
            ORDER BY a.dt_entrada_em
            """
        )

        dentro = cursor.fetchall()

        if not dentro:
            print("\n  ✓  Nenhum visitante dentro no momento.")
            return

        print(f"\n  {len(dentro)} visitante(s) dentro:\n")
        for a in dentro:
            print(f"  ┌── {a['visitante']}")
            print(f"  │  Visita  : {a['morador']} — Apto {a['numero_residencia']}/{a['bloco']}")
            print(f"  │  Motivo  : {a['motivo']}")
            print(f"  │  Entrou  : {a['dt_entrada_em']}")
            print(f"  │  Porteiro: {a['porteiro'] or '—'}")
            print(f"  └──────────────────────────────────────────")
            print()

    except Exception as e:
        print(f"\n  ✗  Erro: {e}")
    finally:
        fechar(conexao)


def historico_acessos():
    """
    Exibe os últimos 10 acessos registrados (entradas e saídas).

    Conceito SQL:
      ORDER BY dt_entrada_em DESC → mais recentes primeiro
      LIMIT 10                 → só os 10 últimos
    """
    separador("HISTÓRICO DE ACESSOS (Últimos 10)")

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # TODO: Mesmo padrão de JOIN — mas agora sem filtro IS NULL
        #       Mostramos TODOS os acessos, ordenados do mais recente.
        cursor.execute(
            """
            SELECT
                a.id            AS id,
                v.nome          AS visitante,
                m.nome          AS morador,
                m.numero_residencia,
                a.motivo,
                a.dt_entrada_em,
                a.dt_saida_em,
                a.porteiro
            FROM  acessos a
                  JOIN visitantes v ON a.visitante_id = v.id
                  JOIN moradores  m ON a.morador_id   = m.id
            ORDER BY a.dt_entrada_em DESC
            LIMIT 10
            """
        )

        acessos = cursor.fetchall()

        if not acessos:
            print("\n  Nenhum acesso registrado ainda."); return

        print(f"\n  {'ID':<4}  {'Visitante':<22}  {'Apto':<6}  {'Entrada':<17}  {'Saída':<17}  Motivo")
        print(f"  {'─'*4}  {'─'*22}  {'─'*6}  {'─'*17}  {'─'*17}  {'─'*20}")

        for a in acessos:
            saida = a['dt_saida_em'] or "Ainda dentro 🟡"
            print(
                f"  {a['id']:<4}  {a['visitante']:<22}  "
                f"{a['numero_residencia']:<6}  {a['dt_entrada_em']:<17}  "
                f"{saida:<17}  {a['motivo']}"
            )

    except Exception as e:
        print(f"\n  ✗  Erro: {e}")
    finally:
        fechar(conexao)


# ============================================================
# RELATÓRIO GERAL DO CONDOMÍNIO
# ============================================================

def relatorio_condominio():
    """
    Resumo completo: moradores, visitantes e acessos.

    Conceito SQL:
      Subconsultas — SELECT dentro de SELECT
      COUNT(*)     — contar linhas
      SUM(CASE WHEN ...) — soma condicional
    """
    separador("RELATÓRIO DO CONDOMÍNIO")

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # TODO: Entenda este SELECT com subconsultas.
        #       Cada linha entre parênteses é uma query separada
        #       que retorna um único número. Chamamos isso de "subconsulta escalar".
        cursor.execute(
            """
            SELECT
                (SELECT COUNT(*) FROM moradores WHERE ativo = 1)
                    AS moradores_ativos,
                (SELECT COUNT(*) FROM moradores WHERE ativo = 1 AND tipo_morador = 'proprietario')
                    AS proprietarios,
                (SELECT COUNT(*) FROM moradores WHERE ativo = 1 AND tipo_morador = 'inquilino')
                    AS inquilinos,
                (SELECT COUNT(*) FROM moradores WHERE ativo = 1 AND foto_url IS NOT NULL)
                    AS com_foto,
                (SELECT COUNT(*) FROM moradores WHERE ativo = 1 AND biometria_hash IS NOT NULL)
                    AS com_biometria,
                (SELECT COUNT(*) FROM visitantes)
                    AS total_visitantes,
                (SELECT COUNT(*) FROM visitantes WHERE bloqueado = 1)
                    AS visitantes_bloqueados,
                (SELECT COUNT(*) FROM acessos)
                    AS total_acessos,
                (SELECT COUNT(*) FROM acessos WHERE dt_saida_em IS NULL)
                    AS dentro_agora
            """
        )

        r = cursor.fetchone()

        print(f"""
  ╔══════════════════════════════════════════╗
  ║  MORADORES                               ║
  ╠══════════════════════════════════════════╣
  ║  Ativos total   : {str(r['moradores_ativos']):<24}║
  ║    Proprietários : {str(r['proprietarios']):<23}║
  ║    Inquilinos    : {str(r['inquilinos']):<23}║
  ╠══════════════════════════════════════════╣
  ║  CADASTROS DE SEGURANÇA                  ║
  ╠══════════════════════════════════════════╣
  ║  Com foto       : {str(r['com_foto']):<24}║
  ║  Com biometria  : {str(r['com_biometria']):<24}║
  ╠══════════════════════════════════════════╣
  ║  VISITANTES                              ║
  ╠══════════════════════════════════════════╣
  ║  Total           : {str(r['total_visitantes']):<23}║
  ║  Bloqueados      : {str(r['visitantes_bloqueados']):<23}║
  ╠══════════════════════════════════════════╣
  ║  ACESSOS                                 ║
  ╠══════════════════════════════════════════╣
  ║  Total de acessos: {str(r['total_acessos']):<23}║
  ║  Dentro agora    : {str(r['dentro_agora']):<23}║
  ╚══════════════════════════════════════════╝""")

    except Exception as e:
        print(f"\n  ✗  Erro ao gerar relatório: {e}")
    finally:
        fechar(conexao)


# ============================================================
# MENU PRINCIPAL EXPANDIDO
# ============================================================

def menu():
    """Exibe o menu completo e retorna a opção escolhida."""
    separador("SISTEMA DE PORTARIA — COMPLETO")
    print("""
  ── MORADORES ──────────────────────────────
  1. Cadastrar morador
  2. Listar moradores
  ── VISITANTES ─────────────────────────────
  3. Cadastrar visitante
  4. Listar visitantes
  5. Buscar visitante por nome
  6. Bloquear visitante
  ── ACESSOS ────────────────────────────────
  7. Registrar entrada de visitante
  8. Registrar saída de visitante
  9. Quem está dentro agora?
  10. Histórico de acessos
  ── RELATÓRIO ──────────────────────────────
  11. Relatório geral do condomínio
  ───────────────────────────────────────────
  0. Sair
    """)
    return input("  Escolha uma opção: ").strip()


def main():
    """Loop principal do programa."""
    caminho = os.path.normpath(CAMINHO_BANCO)
    if not os.path.exists(caminho):
        print(f"\n  ✗  Banco não encontrado: {caminho}")
        print("     Certifique-se de que portaria.db existe.")
        return

    print("\n  Sistema de Portaria — Aula 03")
    print(f"  Banco: {os.path.basename(caminho)}")

    while True:
        opcao = menu()

        if   opcao == "1":  cadastrar_morador()
        elif opcao == "2":  listar_moradores()
        elif opcao == "3":  cadastrar_visitante()
        elif opcao == "4":  listar_visitantes()
        elif opcao == "5":  buscar_visitante()
        elif opcao == "6":  bloquear_visitante()
        elif opcao == "7":  registrar_entrada()
        elif opcao == "8":  registrar_saida()
        elif opcao == "9":  quem_esta_dentro()
        elif opcao == "10": historico_acessos()
        elif opcao == "11": relatorio_condominio()
        elif opcao == "0":
            separador()
            print("  Até a próxima aula! Você está evoluindo muito! 🚀")
            separador()
            break
        else:
            print("  ✗  Opção inválida. Digite um número entre 0 e 11.")

        pausar()


if __name__ == "__main__":
    main()
