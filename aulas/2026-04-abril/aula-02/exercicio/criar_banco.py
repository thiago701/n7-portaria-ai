#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
n7-portaria-ai — Aula 02: Banco de Dados na Prática
=====================================================

Neste exercício, você vai:
1. Criar o banco de dados a partir do SQL completo
2. Fazer consultas divertidas aos moradores do condomínio
3. Cadastrar novos personagens na portaria
4. Descobrir quem está DENTRO do condomínio agora!

O arquivo 'projeto_portaria_completo.sql' (na mesma pasta) já tem
todas as tabelas, índices e dados de exemplo. Você vai interagir
com esse banco usando Python!

Complete os TODOs — cada um é uma mini-missão! 🎯
"""

import sqlite3
import os
import hashlib
from datetime import datetime


# ============================================
# PASSO 1: CRIAR O BANCO A PARTIR DO SQL
# ============================================

def criar_banco() -> sqlite3.Connection:
    """
    Lê o arquivo SQL completo e cria o banco de dados.

    Returns:
        Conexão ativa com o banco SQLite
    """
    # Caminho do arquivo SQL (mesma pasta deste script)
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    arquivo_sql = os.path.join(pasta_atual, "projeto_portaria_completo.sql")

    # Banco de dados em memória (perfeito para aprender, sem criar arquivo)
    conn = sqlite3.connect(":memory:")

    # Ativa modo de dicionário: resultado vem com nome das colunas!
    conn.row_factory = sqlite3.Row

    # Lê o SQL completo e executa apenas até a PARTE 4 (consultas de estudo)
    with open(arquivo_sql, "r", encoding="utf-8") as f:
        sql_completo = f.read()

    # Corta o SQL antes da seção de consultas de estudo
    marcador = "-- PARTE 4: CONSULTAS DE ESTUDO"
    if marcador in sql_completo:
        sql_criacao = sql_completo[:sql_completo.index(marcador)]
    else:
        sql_criacao = sql_completo

    conn.executescript(sql_criacao)
    print("✅ Banco de dados criado com sucesso!")
    return conn


def gerar_correlation_id(texto: str) -> str:
    """
    Gera um correlation_id usando SHA-256.

    Toda tabela do nosso sistema precisa de um correlation_id.
    É como um "RG digital" único para cada registro.

    Args:
        texto: string base para gerar o hash

    Returns:
        Hash SHA-256 de 64 caracteres
    """
    return hashlib.sha256(texto.encode()).hexdigest()


# ============================================
# PASSO 2: MISSÕES DE CONSULTA (SELECT)
# ============================================

def missao_1_conhecer_moradores(conn: sqlite3.Connection) -> None:
    """
    🏠 MISSÃO 1: Conheça os moradores do condomínio!
    Vamos ver quem mora aqui.
    """
    print("\n" + "=" * 60)
    print("🏠 MISSÃO 1: Quem mora no Residencial Parque das Flores?")
    print("=" * 60)

    cursor = conn.execute("""
        SELECT nome, cpf, telefone, ativo
        FROM moradores
        WHERE ativo = 1
        ORDER BY nome
    """)

    moradores = cursor.fetchall()
    print(f"\n📋 Total de moradores ativos: {len(moradores)}\n")

    for m in moradores:
        # Mostra apenas os 3 primeiros e últimos dígitos do CPF (privacidade!)
        cpf_mask = m["cpf"][:3] + ".***.***" + m["cpf"][-2:]
        print(f"   👤 {m['nome']:<30} Tel: {m['telefone'] or 'Não informado'}")

    print(f"\n✅ Missão 1 completa! Você conheceu {len(moradores)} moradores.")


def missao_2_quem_mora_onde(conn: sqlite3.Connection) -> None:
    """
    🔑 MISSÃO 2: Descubra quem mora em cada apartamento!
    Aqui usamos JOIN — o super-poder do SQL!
    """
    print("\n" + "=" * 60)
    print("🔑 MISSÃO 2: Quem mora onde? (JOIN em ação!)")
    print("=" * 60)

    # TODO 1 — SUA PRIMEIRA CONSULTA JOIN! 🎯
    #
    # Complete a consulta abaixo para trazer:
    #   - nome do morador (da tabela moradores)
    #   - numero_residencia (da tabela residencias)
    #   - bloco (da tabela residencias)
    #   - tipo_morador (da tabela morador_residencia: 'proprietario' ou 'inquilino')
    #
    # As tabelas se conectam assim:
    #   moradores ←→ morador_residencia ←→ residencias
    #       m.id  =  mr.morador_id
    #                 mr.residencia_id  =  r.id
    #
    # Dica: copie este modelo e preencha os ___:
    #
    #   SELECT m.nome, r.numero_residencia, r.bloco, mr.tipo_morador
    #   FROM moradores m
    #       JOIN morador_residencia mr ON m.id = mr.___
    #       JOIN residencias r ON mr.___ = r.id
    #   WHERE m.ativo = 1
    #   ORDER BY r.bloco, r.numero_residencia
    #
    # Escreva sua consulta aqui dentro das aspas triplas:

    consulta = """
        SELECT 'Complete o TODO 1!' AS nome, '' AS numero_residencia, '' AS bloco, '' AS tipo_morador
    """

    cursor = conn.execute(consulta)
    resultados = cursor.fetchall()

    print(f"\n📋 Moradores e suas residências:\n")
    for r in resultados:
        bloco_str = f"Bloco {r['bloco']}" if r['bloco'] else "Sem bloco"
        tipo = "🏡 Proprietário" if r["tipo_morador"] == "proprietario" else "📝 Inquilino"
        print(f"   {tipo} {r['nome']:<30} Apto {r['numero_residencia']:<5} {bloco_str}")


def missao_3_detetive_portaria(conn: sqlite3.Connection) -> None:
    """
    🔍 MISSÃO 3: Quem está DENTRO do condomínio agora?
    Registros de acesso sem dt_saida_em = pessoa ainda dentro!
    """
    print("\n" + "=" * 60)
    print("🔍 MISSÃO 3: Detetive da Portaria — quem está aqui agora?")
    print("=" * 60)

    # TODO 2 — CONSULTA DE SEGURANÇA! 🎯
    #
    # Descubra quem está DENTRO do condomínio neste momento.
    # A "sacada": se dt_saida_em é NULL, a pessoa NÃO SAIU ainda!
    #
    # Complete a consulta:
    #
    #   SELECT v.nome AS visitante, m.nome AS morador, a.motivo
    #   FROM acessos a
    #       JOIN visitantes v ON a.visitante_id = v.id
    #       JOIN moradores m  ON a.morador_id = m.id
    #   WHERE a.___ IS NULL
    #
    # Qual campo indica que a pessoa ainda não saiu?
    # Dica: começa com "dt_saida"...

    consulta = """
        SELECT 'Complete o TODO 2!' AS visitante, '' AS morador, '' AS motivo
    """

    cursor = conn.execute(consulta)
    dentro = cursor.fetchall()

    print(f"\n🚨 Pessoas dentro do condomínio agora: {len(dentro)}\n")
    for d in dentro:
        print(f"   🚶 {d['visitante']:<25} visitando {d['morador']:<25} Motivo: {d['motivo']}")

    if len(dentro) == 0:
        print("   (Ninguém dentro agora — verifique o TODO 2)")


def missao_4_visitantes_bloqueados(conn: sqlite3.Connection) -> None:
    """
    ⛔ MISSÃO 4: Lista negra — quem está BLOQUEADO?
    """
    print("\n" + "=" * 60)
    print("⛔ MISSÃO 4: Lista negra da portaria")
    print("=" * 60)

    # TODO 3 — FILTRO SIMPLES! 🎯
    #
    # Encontre todos os visitantes BLOQUEADOS.
    # Um visitante bloqueado tem bloqueado = 1.
    #
    # Complete a consulta:
    #
    #   SELECT nome, documento, motivo_bloqueio
    #   FROM visitantes
    #   WHERE ___ = 1
    #
    # Qual campo você precisa filtrar?
    # Dica: o nome do campo é "bloqueado"

    consulta = """
        SELECT 'Complete o TODO 3!' AS nome, '' AS documento, '' AS motivo_bloqueio
    """

    cursor = conn.execute(consulta)
    bloqueados = cursor.fetchall()

    print(f"\n🚫 Visitantes na lista negra: {len(bloqueados)}\n")
    for b in bloqueados:
        print(f"   ⛔ {b['nome']:<25} Doc: {b['documento']:<15}")
        print(f"      Motivo: {b['motivo_bloqueio']}")
        print()


# ============================================
# PASSO 3: MISSÕES DE INSERÇÃO (INSERT)
# ============================================

def missao_5_novo_morador(conn: sqlite3.Connection) -> None:
    """
    ✨ MISSÃO 5: Cadastre um morador novo no condomínio!
    """
    print("\n" + "=" * 60)
    print("✨ MISSÃO 5: Cadastrar novo morador")
    print("=" * 60)

    # TODO 4 — INSERIR UM MORADOR! 🎯
    #
    # Cadastre "Ademilson Programador" no condomínio!
    # É o nosso aluno entrando para o sistema. 😄
    #
    # Complete o INSERT:
    #
    #   INSERT INTO moradores (nome, cpf, telefone, email, ativo, correlation_id)
    #   VALUES (
    #       'Ademilson Programador',
    #       '99999999999',
    #       '83912345678',
    #       'ademilson@n7tech.com',
    #       1,
    #       ___
    #   )
    #
    # O último campo (correlation_id) precisa ser um hash SHA-256.
    # Use a função que já temos: gerar_correlation_id('moradores:99999999999')
    #
    # Preencha o ___ com o resultado da função!

    corr_id = gerar_correlation_id("moradores:99999999999")

    insert_morador = """
        SELECT 'Complete o TODO 4!' AS resultado
    """
    # Quando completar, troque o SELECT acima pelo INSERT correto.
    # Depois descomente as linhas abaixo:

    # conn.execute(insert_morador, ...)  # ou sem parâmetros se inline
    # conn.commit()
    # print("✅ Ademilson Programador cadastrado com sucesso!")

    # Verifica se o cadastro funcionou:
    cursor = conn.execute("SELECT nome FROM moradores WHERE cpf = '99999999999'")
    resultado = cursor.fetchone()
    if resultado:
        print(f"✅ Morador cadastrado: {resultado['nome']}")
        print(f"   correlation_id: {corr_id[:16]}...")
    else:
        print("⏳ Complete o TODO 4 para cadastrar o Ademilson!")


def missao_6_novo_visitante(conn: sqlite3.Connection) -> None:
    """
    🎉 MISSÃO 6: Registre a visita de alguém ao Ademilson!
    """
    print("\n" + "=" * 60)
    print("🎉 MISSÃO 6: Registrar um visitante")
    print("=" * 60)

    # TODO 5 — INSERIR UM VISITANTE! 🎯
    #
    # O Thiago (professor) vai visitar o Ademilson!
    # Cadastre o Thiago como visitante.
    #
    # Complete o INSERT:
    #
    #   INSERT INTO visitantes (nome, documento, tipo_documento, telefone, correlation_id)
    #   VALUES (
    #       '___',                  ← Nome completo
    #       '12345678900',          ← Documento
    #       '___',                  ← Tipo: 'RG', 'CNH', 'PASSAPORTE' ou 'OUTRO'
    #       '83900001111',          ← Telefone
    #       ___                     ← correlation_id (use gerar_correlation_id)
    #   )
    #
    # Dica:
    #   corr_id = gerar_correlation_id('visitantes:12345678900')
    #   conn.execute(""" INSERT INTO ... """)
    #   conn.commit()

    # Escreva seu código aqui:


    # Verifica se funcionou:
    cursor = conn.execute("SELECT nome FROM visitantes WHERE documento = '12345678900'")
    resultado = cursor.fetchone()
    if resultado:
        print(f"✅ Visitante cadastrado: {resultado['nome']}")
    else:
        print("⏳ Complete o TODO 5 para cadastrar o visitante!")


# ============================================
# PASSO 4: MISSÃO ESPECIAL — RELATÓRIO!
# ============================================

def missao_7_relatorio_condominio(conn: sqlite3.Connection) -> None:
    """
    📊 MISSÃO 7: Gere o relatório do condomínio!
    O síndico precisa de um resumo rápido.
    """
    print("\n" + "=" * 60)
    print("📊 MISSÃO 7: Relatório para o Síndico")
    print("=" * 60)

    # TODO 6 — CONSULTAS DE CONTAGEM! 🎯
    #
    # O síndico quer saber:
    # a) Quantos moradores ativos existem?
    # b) Quantos visitantes estão cadastrados?
    # c) Quantos acessos foram registrados?
    # d) Quantos veículos estão no sistema?
    #
    # Complete cada consulta com COUNT(*):
    #
    # total_moradores  = conn.execute("SELECT COUNT(*) AS total FROM moradores WHERE ativo = 1").fetchone()["total"]
    # total_visitantes = conn.execute("SELECT COUNT(*) AS total FROM ___").fetchone()["total"]
    # total_acessos    = conn.execute("SELECT COUNT(*) AS total FROM ___").fetchone()["total"]
    # total_veiculos   = conn.execute("SELECT COUNT(*) AS total FROM ___").fetchone()["total"]
    #
    # Dica: só troque ___ pelo nome da tabela!

    total_moradores = conn.execute("SELECT COUNT(*) AS total FROM moradores WHERE ativo = 1").fetchone()["total"]

    # Descomente e complete estas linhas:
    # total_visitantes = conn.execute("SELECT COUNT(*) AS total FROM ___").fetchone()["total"]
    # total_acessos    = conn.execute("SELECT COUNT(*) AS total FROM ___").fetchone()["total"]
    # total_veiculos   = conn.execute("SELECT COUNT(*) AS total FROM ___").fetchone()["total"]

    # Quando completar, troque os zeros abaixo pelas variáveis:
    total_visitantes = 0  # ← troque por total_visitantes
    total_acessos = 0     # ← troque por total_acessos
    total_veiculos = 0    # ← troque por total_veiculos

    print(f"""
    ┌─────────────────────────────────────────┐
    │   RESIDENCIAL PARQUE DAS FLORES         │
    │   Relatório do Sistema de Portaria      │
    ├─────────────────────────────────────────┤
    │   👤 Moradores ativos:    {total_moradores:>5}         │
    │   🚶 Visitantes:          {total_visitantes:>5}         │
    │   🚪 Total de acessos:    {total_acessos:>5}         │
    │   🚗 Veículos:            {total_veiculos:>5}         │
    ├─────────────────────────────────────────┤
    │   📅 Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}       │
    └─────────────────────────────────────────┘
    """)

    if total_visitantes == 0:
        print("   ⏳ Complete o TODO 6 para ver os números reais!")


# ============================================
# MISSÃO BÔNUS: PARA QUEM QUER MAIS!
# ============================================

def missao_bonus_ranking(conn: sqlite3.Connection) -> None:
    """
    🏆 MISSÃO BÔNUS: Ranking dos moradores mais visitados!
    """
    print("\n" + "=" * 60)
    print("🏆 MISSÃO BÔNUS: Ranking de visitas (GROUP BY + ORDER BY)")
    print("=" * 60)

    # TODO 7 (BÔNUS) — RANKING COM GROUP BY! 🎯
    #
    # Quem é o morador mais popular (mais visitado)?
    #
    # Complete a consulta:
    #
    #   SELECT m.nome, COUNT(a.id) AS total_visitas
    #   FROM acessos a
    #       JOIN moradores m ON a.___ = m.id
    #   GROUP BY m.id
    #   ORDER BY total_visitas DESC
    #
    # Qual campo de 'acessos' referencia o morador visitado?
    # Dica: morador_id

    consulta = """
        SELECT 'Complete o TODO 7!' AS nome, 0 AS total_visitas
    """

    cursor = conn.execute(consulta)
    ranking = cursor.fetchall()

    print(f"\n🥇 Ranking dos mais visitados:\n")
    medalhas = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    for i, r in enumerate(ranking):
        medalha = medalhas[i] if i < len(medalhas) else f"  {i+1}."
        barra = "█" * r["total_visitas"]
        print(f"   {medalha} {r['nome']:<30} {barra} ({r['total_visitas']} visitas)")


# ============================================
# FUNÇÃO PRINCIPAL
# ============================================

def main() -> None:
    """
    Executa todas as missões em sequência.
    O banco é criado em memória — sem precisar instalar nada!
    """
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║   n7-portaria-ai — Aula 02: Banco de Dados          ║
    ║                                                       ║
    ║   7 missões para dominar o SQL!                       ║
    ║   Cada TODO completado = 1 missão cumprida 🎯        ║
    ╚═══════════════════════════════════════════════════════╝
    """)

    # Cria o banco a partir do SQL completo
    conn = criar_banco()

    # Conta as tabelas criadas (pra mostrar que funcionou!)
    tabelas = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()
    print(f"📦 Tabelas criadas: {len(tabelas)}")
    for t in tabelas:
        print(f"   📋 {t['name']}")

    # ---- MISSÕES DE CONSULTA (mais fáceis → mais difíceis) ----
    missao_1_conhecer_moradores(conn)     # Pronta! Só rode e veja
    missao_2_quem_mora_onde(conn)         # TODO 1: JOIN
    missao_3_detetive_portaria(conn)      # TODO 2: WHERE ... IS NULL
    missao_4_visitantes_bloqueados(conn)  # TODO 3: WHERE ... = 1

    # ---- MISSÕES DE INSERÇÃO ----
    missao_5_novo_morador(conn)           # TODO 4: INSERT morador
    missao_6_novo_visitante(conn)         # TODO 5: INSERT visitante

    # ---- RELATÓRIO ----
    missao_7_relatorio_condominio(conn)   # TODO 6: COUNT(*)

    # ---- BÔNUS ----
    missao_bonus_ranking(conn)            # TODO 7: GROUP BY + ORDER BY

    # Fecha a conexão
    conn.close()

    print("\n" + "=" * 60)
    print("🎉 Parabéns, Ademilson!")
    print("   Você interagiu com um banco de 9 tabelas usando Python!")
    print("   Na Aula 03, vamos fazer o CRUD completo: criar, ler,")
    print("   atualizar e deletar registros — tudo pelo terminal!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()


# ============================================================================
# GABARITO — RESPOSTAS DOS TODOs
# ============================================================================
# Ademilson, só olhe aqui DEPOIS de tentar sozinho!
# Aprender é errar, corrigir e tentar de novo. 💪
# ============================================================================

"""
═══════════════════════════════════════════════════════════════
TODO 1 — JOIN de 3 tabelas (Missão 2)
═══════════════════════════════════════════════════════════════

    consulta = \"""
        SELECT m.nome, r.numero_residencia, r.bloco, mr.tipo_morador
        FROM moradores m
            JOIN morador_residencia mr ON m.id = mr.morador_id
            JOIN residencias r ON mr.residencia_id = r.id
        WHERE m.ativo = 1
        ORDER BY r.bloco, r.numero_residencia
    \"""

Explicação:
  - morador_residencia é a tabela "ponte" que conecta moradores a residências
  - mr.morador_id aponta para moradores.id
  - mr.residencia_id aponta para residencias.id
  - É como uma corrente: moradores ↔ morador_residencia ↔ residencias


═══════════════════════════════════════════════════════════════
TODO 2 — WHERE ... IS NULL (Missão 3)
═══════════════════════════════════════════════════════════════

    consulta = \"""
        SELECT v.nome AS visitante, m.nome AS morador, a.motivo
        FROM acessos a
            JOIN visitantes v ON a.visitante_id = v.id
            JOIN moradores m  ON a.morador_id = m.id
        WHERE a.dt_saida_em IS NULL
    \"""

Explicação:
  - Se dt_saida_em é NULL, a pessoa ainda NÃO registrou saída
  - NULL em SQL significa "sem valor" — usamos IS NULL (nunca = NULL)
  - É a mesma lógica de "se não carimbou a saída, ainda está aqui"


═══════════════════════════════════════════════════════════════
TODO 3 — Filtro simples (Missão 4)
═══════════════════════════════════════════════════════════════

    consulta = \"""
        SELECT nome, documento, motivo_bloqueio
        FROM visitantes
        WHERE bloqueado = 1
    \"""

Explicação:
  - bloqueado = 1 significa "sim, está bloqueado"
  - bloqueado = 0 significa "não está bloqueado"
  - Em banco de dados, usamos 0 e 1 para representar falso/verdadeiro


═══════════════════════════════════════════════════════════════
TODO 4 — INSERT de morador (Missão 5)
═══════════════════════════════════════════════════════════════

    corr_id = gerar_correlation_id("moradores:99999999999")

    conn.execute(\"""
        INSERT INTO moradores (nome, cpf, telefone, email, ativo, correlation_id)
        VALUES (?, ?, ?, ?, ?, ?)
    \""", (
        'Ademilson Programador',
        '99999999999',
        '83912345678',
        'ademilson@n7tech.com',
        1,
        corr_id
    ))
    conn.commit()
    print("✅ Ademilson Programador cadastrado com sucesso!")

Explicação:
  - Usamos ? como "placeholders" — o Python preenche com os valores da tupla
  - Isso se chama "prepared statement" e protege contra SQL Injection!
  - conn.commit() salva de verdade no banco (sem commit, nada é gravado)


═══════════════════════════════════════════════════════════════
TODO 5 — INSERT de visitante (Missão 6)
═══════════════════════════════════════════════════════════════

    corr_id = gerar_correlation_id("visitantes:12345678900")

    conn.execute(\"""
        INSERT INTO visitantes (nome, documento, tipo_documento, telefone, correlation_id)
        VALUES (?, ?, ?, ?, ?)
    \""", (
        'Thiago Professor',
        '12345678900',
        'CNH',
        '83900001111',
        corr_id
    ))
    conn.commit()
    print("✅ Visitante Thiago cadastrado com sucesso!")

Explicação:
  - tipo_documento aceita: 'RG', 'CNH', 'PASSAPORTE' ou 'OUTRO'
  - O CHECK no banco garante que valores inválidos são rejeitados
  - Se tentar 'CARTEIRINHA', o banco dá erro — isso é validação na fonte!


═══════════════════════════════════════════════════════════════
TODO 6 — COUNT(*) para relatório (Missão 7)
═══════════════════════════════════════════════════════════════

    total_moradores  = conn.execute("SELECT COUNT(*) AS total FROM moradores WHERE ativo = 1").fetchone()["total"]
    total_visitantes = conn.execute("SELECT COUNT(*) AS total FROM visitantes").fetchone()["total"]
    total_acessos    = conn.execute("SELECT COUNT(*) AS total FROM acessos").fetchone()["total"]
    total_veiculos   = conn.execute("SELECT COUNT(*) AS total FROM veiculos").fetchone()["total"]

Explicação:
  - COUNT(*) conta quantas linhas existem na tabela
  - "AS total" dá um apelido para a coluna (senão fica "COUNT(*)" — feio!)
  - fetchone()["total"] pega o primeiro resultado e acessa pelo nome da coluna


═══════════════════════════════════════════════════════════════
TODO 7 (BÔNUS) — GROUP BY + ORDER BY (Missão Bônus)
═══════════════════════════════════════════════════════════════

    consulta = \"""
        SELECT m.nome, COUNT(a.id) AS total_visitas
        FROM acessos a
            JOIN moradores m ON a.morador_id = m.id
        GROUP BY m.id, m.nome
        ORDER BY total_visitas DESC
    \"""

Explicação:
  - GROUP BY agrupa todos os acessos por morador
  - COUNT(a.id) conta quantos acessos cada morador recebeu
  - ORDER BY total_visitas DESC ordena do mais visitado para o menos
  - É como fazer uma "contagem de votos" — quem tem mais, aparece primeiro!
"""
