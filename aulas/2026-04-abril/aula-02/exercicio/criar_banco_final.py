"""
criar_banco_final.py — Cria o portaria.db completo na raiz do projeto
======================================================================
Aluno:  Ademilson
Aula:   02 — Banco de Dados na Prática: DBeaver + SQLite + Python
Data:   09/04/2026

COMO USAR:
    python criar_banco_final.py

O script:
  1. Cria (ou recria) o arquivo  portaria.db  na RAIZ do projeto n7-portaria-ai
  2. Executa TODO o DDL (CREATE TABLE, CREATE INDEX)
  3. Insere os dados de exemplo (10 moradores, 10 residências, etc.)
  4. Imprime um resumo do que foi criado

Depois é só abrir o portaria.db no DBeaver e explorar!

GABARITO:
  As respostas dos exercícios estão COMENTADAS no final deste arquivo.
  Tente resolver sozinho antes de olhar!
======================================================================
"""

import sqlite3
import os
import hashlib
from pathlib import Path
from datetime import datetime


# ============================================================================
# LOCALIZAR A RAIZ DO PROJETO
# ============================================================================
# O script está em:  n7-portaria-ai/aulas/2026-04-abril/aula-02/exercicio/
# A raiz é:          n7-portaria-ai/  (onde mora a pasta .git)
#
# Em vez de contar ".parent" varias vezes (frágil!), subimos a árvore
# procurando a pasta .git — assim o script funciona mesmo se for movido.

def _achar_raiz_projeto() -> Path:
    """Sobe a partir do script ate achar a pasta .git (raiz do repositorio)."""
    atual = Path(__file__).resolve().parent
    for pasta in [atual, *atual.parents]:
        if (pasta / ".git").exists():
            return pasta
    # Plano B: 4 niveis acima (estrutura conhecida do projeto)
    return Path(__file__).resolve().parents[4]

SCRIPT_DIR = Path(__file__).resolve().parent
RAIZ_PROJETO = _achar_raiz_projeto()
DB_PATH = RAIZ_PROJETO / "portaria.db"


def gerar_correlation_id(tabela: str, chave: str) -> str:
    """
    Gera um correlation_id usando SHA-256.
    Exemplo: gerar_correlation_id('moradores', '11122233344')
             → hashlib.sha256('moradores:11122233344'.encode()).hexdigest()
    """
    texto = f"{tabela}:{chave}"
    return hashlib.sha256(texto.encode()).hexdigest()


def criar_banco():
    """Cria o portaria.db do zero com todas as 9 tabelas."""

    # Se já existe, remove para recriar do zero
    if DB_PATH.exists():
        DB_PATH.unlink()
        print(f"♻  Banco anterior removido: {DB_PATH}")

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    print(f"📦 Criando banco em: {DB_PATH}\n")

    # ========================================================================
    # PARTE 1: CRIAÇÃO DAS TABELAS (DDL)
    # ========================================================================

    # ── TABELA 1: moradores ─────────────────────────────────────────────────
    # Dados PESSOAIS de cada morador (CPF, foto, biometria, LGPD).
    # Dados da UNIDADE estão em 'residencias'.
    cur.execute("""
    CREATE TABLE moradores (
        id                    INTEGER   PRIMARY KEY AUTOINCREMENT,
        nome                  TEXT      NOT NULL,
        cpf                   TEXT      UNIQUE NOT NULL CHECK(length(cpf) = 11),
        telefone              TEXT,
        email                 TEXT      CHECK(email LIKE '%@%.%'),
        dt_nascimento         DATE,
        foto                  BLOB,
        dt_foto_validade      DATE,
        biometria             BLOB,
        dt_biometria_validade DATE,
        termos_lgpd           BLOB,
        dt_aceite_lgpd        DATETIME,
        ativo                 BOOLEAN   DEFAULT 1 CHECK(ativo IN (0, 1)),
        correlation_id        TEXT      UNIQUE NOT NULL,
        dt_criado_em          DATETIME  DEFAULT CURRENT_TIMESTAMP,
        dt_atualizado_em      DATETIME  DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ── TABELA 2: residencias ───────────────────────────────────────────────
    # Dados de cada UNIDADE HABITACIONAL do condomínio.
    # Campos do Ademilson: tipo_moradia, interfone, observacao
    cur.execute("""
    CREATE TABLE residencias (
        id                    INTEGER   PRIMARY KEY AUTOINCREMENT,
        codigo_condominio     TEXT      NOT NULL,
        numero_residencia     TEXT      NOT NULL,
        bloco                 TEXT,
        quadra                TEXT,
        andar                 INTEGER,
        tipo_moradia          TEXT      DEFAULT 'apartamento'
                                        CHECK(tipo_moradia IN ('apartamento','casa','comercial','outro')),
        interfone             TEXT,
        observacao            TEXT,
        ativo                 BOOLEAN   DEFAULT 1 CHECK(ativo IN (0, 1)),
        correlation_id        TEXT      UNIQUE NOT NULL,
        dt_criado_em          DATETIME  DEFAULT CURRENT_TIMESTAMP,
        dt_atualizado_em      DATETIME  DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ── TABELA 3: morador_residencia (JUNCTION TABLE — relação N:N) ────────
    # Conecta moradores a residências.
    # Um morador pode ter várias unidades. Uma unidade pode ter vários moradores.
    cur.execute("""
    CREATE TABLE morador_residencia (
        id                    INTEGER   PRIMARY KEY AUTOINCREMENT,
        morador_id            INTEGER   NOT NULL,
        residencia_id         INTEGER   NOT NULL,
        tipo_morador          TEXT      DEFAULT 'proprietario'
                                        CHECK(tipo_morador IN ('proprietario', 'inquilino')),
        dt_inicio             DATE      NOT NULL DEFAULT (DATE('now')),
        dt_fim                DATE,
        ativo                 BOOLEAN   DEFAULT 1 CHECK(ativo IN (0, 1)),
        correlation_id        TEXT      UNIQUE NOT NULL,
        dt_criado_em          DATETIME  DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (morador_id)    REFERENCES moradores(id),
        FOREIGN KEY (residencia_id) REFERENCES residencias(id),
        UNIQUE (morador_id, residencia_id, dt_inicio)
    )
    """)

    # ── TABELA 4: visitantes ────────────────────────────────────────────────
    # Pessoas que visitam o condomínio.
    cur.execute("""
    CREATE TABLE visitantes (
        id                    INTEGER   PRIMARY KEY AUTOINCREMENT,
        nome                  TEXT      NOT NULL,
        documento             TEXT      NOT NULL,
        tipo_documento        TEXT      DEFAULT 'RG'
                                        CHECK(tipo_documento IN ('RG', 'CNH', 'PASSAPORTE', 'OUTRO')),
        telefone              TEXT,
        foto                  BLOB,
        bloqueado             BOOLEAN   DEFAULT 0 CHECK(bloqueado IN (0, 1)),
        motivo_bloqueio       TEXT,
        dt_validade_inicio    DATE,
        dt_validade_fim       DATE      CHECK(
                                            dt_validade_fim IS NULL OR
                                            dt_validade_fim >= dt_validade_inicio),
        correlation_id        TEXT      UNIQUE NOT NULL,
        dt_criado_em          DATETIME  DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ── TABELA 5: funcionarios ──────────────────────────────────────────────
    # Porteiros, zeladores, administradores.
    # Contribuição do Ademilson: ele identificou que o sistema precisava saber
    # QUEM registrou cada acesso.
    cur.execute("""
    CREATE TABLE funcionarios (
        id                    INTEGER   PRIMARY KEY AUTOINCREMENT,
        nome                  TEXT      NOT NULL,
        cpf                   TEXT      UNIQUE NOT NULL CHECK(length(cpf) = 11),
        cargo                 TEXT      DEFAULT 'porteiro'
                                        CHECK(cargo IN ('porteiro','zelador','administrador','outro')),
        setor                 TEXT,
        login                 TEXT      UNIQUE NOT NULL,
        senha_hash            TEXT      NOT NULL CHECK(length(senha_hash) = 64),
        ativo                 BOOLEAN   DEFAULT 1 CHECK(ativo IN (0, 1)),
        correlation_id        TEXT      UNIQUE NOT NULL,
        dt_criado_em          DATETIME  DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ── TABELA 6: veiculos ──────────────────────────────────────────────────
    # Carros e motos de moradores, funcionários e visitantes.
    # Contribuição do Ademilson: ele sugeriu 'carro' e 'placa' diretamente em
    # moradores — o raciocínio estava certo! Refinamos para tabela separada.
    cur.execute("""
    CREATE TABLE veiculos (
        id                    INTEGER   PRIMARY KEY AUTOINCREMENT,
        placa                 TEXT      UNIQUE NOT NULL CHECK(length(placa) >= 7),
        modelo                TEXT,
        cor                   TEXT,
        morador_id            INTEGER,
        funcionario_id        INTEGER,
        visitante_id          INTEGER,
        ativo                 BOOLEAN   DEFAULT 1 CHECK(ativo IN (0, 1)),
        correlation_id        TEXT      UNIQUE NOT NULL,
        dt_criado_em          DATETIME  DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (morador_id)      REFERENCES moradores(id),
        FOREIGN KEY (funcionario_id)  REFERENCES funcionarios(id),
        FOREIGN KEY (visitante_id)    REFERENCES visitantes(id)
    )
    """)

    # ── TABELA 7: acessos ───────────────────────────────────────────────────
    # Log de entradas e saídas. NUNCA deletar registros desta tabela!
    # 2FA: auth_senha + auth_digital + auth_facial (pelo menos 1 obrigatório).
    cur.execute("""
    CREATE TABLE acessos (
        id                    INTEGER   PRIMARY KEY AUTOINCREMENT,
        visitante_id          INTEGER   NOT NULL,
        morador_id            INTEGER,
        funcionario_id        INTEGER,
        veiculo_id            INTEGER,
        tipo_acesso           TEXT      DEFAULT 'pedestre'
                                        CHECK(tipo_acesso IN ('pedestre', 'garagem')),
        auth_senha            BOOLEAN   DEFAULT 0 CHECK(auth_senha IN (0,1)),
        auth_digital          BOOLEAN   DEFAULT 0 CHECK(auth_digital IN (0,1)),
        auth_facial           BOOLEAN   DEFAULT 0 CHECK(auth_facial IN (0,1)),
        motivo                TEXT      NOT NULL,
        dt_entrada_em         DATETIME  NOT NULL DEFAULT CURRENT_TIMESTAMP,
        dt_saida_em           DATETIME,
        porteiro              TEXT,
        observacoes           TEXT,
        correlation_id        TEXT      UNIQUE NOT NULL,
        CHECK(auth_senha + auth_digital + auth_facial >= 1),
        FOREIGN KEY (visitante_id)   REFERENCES visitantes(id),
        FOREIGN KEY (morador_id)     REFERENCES moradores(id),
        FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id),
        FOREIGN KEY (veiculo_id)     REFERENCES veiculos(id)
    )
    """)

    # ── TABELA 8: config_acesso_morador ─────────────────────────────────────
    # Política de autenticação individual por morador.
    cur.execute("""
    CREATE TABLE config_acesso_morador (
        id                    INTEGER   PRIMARY KEY AUTOINCREMENT,
        morador_id            INTEGER   UNIQUE NOT NULL,
        fatores_requeridos    INTEGER   DEFAULT 1 CHECK(fatores_requeridos IN (1, 2)),
        permite_senha         BOOLEAN   DEFAULT 1 CHECK(permite_senha IN (0, 1)),
        permite_digital       BOOLEAN   DEFAULT 1 CHECK(permite_digital IN (0, 1)),
        permite_facial        BOOLEAN   DEFAULT 0 CHECK(permite_facial IN (0, 1)),
        correlation_id        TEXT      UNIQUE NOT NULL,
        dt_criado_em          DATETIME  DEFAULT CURRENT_TIMESTAMP,
        dt_atualizado_em      DATETIME  DEFAULT CURRENT_TIMESTAMP,
        CHECK(permite_senha + permite_digital + permite_facial >= 1),
        FOREIGN KEY (morador_id) REFERENCES moradores(id)
    )
    """)

    # ── TABELA 9: assinatura_condominio ─────────────────────────────────────
    # Contrato do CONDOMÍNIO com o sistema n7-portaria-ai.
    cur.execute("""
    CREATE TABLE assinatura_condominio (
        id                    INTEGER   PRIMARY KEY AUTOINCREMENT,
        codigo_condominio     TEXT      UNIQUE NOT NULL,
        nome_condominio       TEXT      NOT NULL,
        endereco              TEXT,
        responsavel_id        INTEGER,
        numero_contrato       TEXT      UNIQUE NOT NULL,
        contrato              BLOB,
        dt_ativacao           DATE,
        dt_vigencia_inicio    DATE      NOT NULL,
        dt_vigencia_fim       DATE      CHECK(
                                            dt_vigencia_fim IS NULL OR
                                            dt_vigencia_fim >= dt_vigencia_inicio),
        status                TEXT      DEFAULT 'ativo'
                                        CHECK(status IN ('ativo','pendente','vencido','cancelado')),
        observacoes           TEXT,
        correlation_id        TEXT      UNIQUE NOT NULL,
        dt_criado_em          DATETIME  DEFAULT CURRENT_TIMESTAMP,
        dt_atualizado_em      DATETIME  DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (responsavel_id) REFERENCES moradores(id)
    )
    """)

    print("✅ 9 tabelas criadas!\n")

    # ========================================================================
    # PARTE 2: ÍNDICES DE DESEMPENHO
    # ========================================================================
    # Sem índice = banco lê TODAS as linhas (lento).
    # Com índice = banco vai direto (log2 N — muito rápido).

    indices = [
        "CREATE INDEX idx_moradores_nome        ON moradores(nome)",
        "CREATE INDEX idx_moradores_ativo       ON moradores(ativo)",
        "CREATE INDEX idx_residencias_cond      ON residencias(codigo_condominio)",
        "CREATE INDEX idx_residencias_num       ON residencias(numero_residencia)",
        "CREATE INDEX idx_residencias_tipo      ON residencias(tipo_moradia)",
        "CREATE INDEX idx_mr_morador            ON morador_residencia(morador_id)",
        "CREATE INDEX idx_mr_residencia         ON morador_residencia(residencia_id)",
        "CREATE INDEX idx_mr_ativo              ON morador_residencia(ativo)",
        "CREATE INDEX idx_visitantes_documento  ON visitantes(documento)",
        "CREATE INDEX idx_visitantes_bloqueado  ON visitantes(bloqueado)",
        "CREATE INDEX idx_funcionarios_cargo    ON funcionarios(cargo)",
        "CREATE INDEX idx_veiculos_morador      ON veiculos(morador_id)",
        "CREATE INDEX idx_acessos_entrada       ON acessos(dt_entrada_em)",
        "CREATE INDEX idx_acessos_visitante     ON acessos(visitante_id)",
        "CREATE INDEX idx_acessos_morador       ON acessos(morador_id)",
        "CREATE INDEX idx_acessos_funcionario   ON acessos(funcionario_id)",
        "CREATE INDEX idx_acessos_veiculo       ON acessos(veiculo_id)",
        "CREATE INDEX idx_assinatura_status     ON assinatura_condominio(status)",
        "CREATE INDEX idx_assinatura_vig_fim    ON assinatura_condominio(dt_vigencia_fim)",
    ]
    for idx in indices:
        cur.execute(idx)

    print(f"✅ {len(indices)} índices criados!\n")

    # ========================================================================
    # PARTE 3: DADOS DE EXEMPLO
    # ========================================================================

    # ── 3.1 — Moradores (10 registros) ──────────────────────────────────────
    moradores = [
        ('Joao Carlos da Silva',    '11122233344', '83999001122', 'joao.silva@email.com',      1, '2026-04-09 10:00:00'),
        ('Maria Aparecida Santos',  '55566677788', '83988112233', 'maria.santos@email.com',    1, '2026-04-09 10:00:00'),
        ('Pedro Henrique Oliveira', '99988877766', '83977223344', 'pedro.oliveira@email.com',  1, None),
        ('Ana Paula Ferreira',      '44433322211', '83966334455', 'ana.ferreira@email.com',    1, '2026-04-09 10:00:00'),
        ('Carlos Eduardo Lima',     '77788899900', '83955445566', None,                        1, None),
        ('Lucia Fernandes Gomes',   '12312312300', '83922001133', 'lucia.gomes@email.com',     1, '2026-04-09 10:00:00'),
        ('Rafael Souza Mendes',     '45645645600', '83911009988', None,                        1, None),
        ('Dona Teresa Albuquerque', '78978978700', '83900112233', 'teresa.albuquerque@email.com', 1, '2026-04-09 10:00:00'),
        ('Bruno Martins Costa',     '14725836900', '83988776655', 'bruno.martins@email.com',   1, None),
        ('Sergio Ramos Pereira',    '96385274100', '83977665544', 'sergio.ramos@email.com',    0, None),  # soft delete
    ]

    for nome, cpf, telefone, email, ativo, lgpd in moradores:
        cid = gerar_correlation_id('moradores', cpf)
        cur.execute("""
            INSERT INTO moradores (nome, cpf, telefone, email, ativo, dt_aceite_lgpd, correlation_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nome, cpf, telefone, email, ativo, lgpd, cid))

    # Atualizar fotos e biometrias
    cur.execute("UPDATE moradores SET foto=NULL, dt_foto_validade='2028-04-09', biometria=NULL, dt_biometria_validade='2028-04-09' WHERE cpf='11122233344'")
    cur.execute("UPDATE moradores SET foto=NULL, dt_foto_validade='2028-04-09' WHERE cpf='55566677788'")
    cur.execute("UPDATE moradores SET foto=NULL, dt_foto_validade='2028-04-09', biometria=NULL, dt_biometria_validade='2028-04-09' WHERE cpf='44433322211'")
    cur.execute("UPDATE moradores SET biometria=NULL, dt_biometria_validade='2028-04-09' WHERE cpf='12312312300'")
    cur.execute("UPDATE moradores SET foto=NULL, dt_foto_validade='2028-04-09', biometria=NULL, dt_biometria_validade='2028-04-09' WHERE cpf='78978978700'")
    cur.execute("UPDATE moradores SET foto=NULL, dt_foto_validade='2025-03-15' WHERE cpf='14725836900'")
    # Bruno: foto VENCIDA em mar/2025 — a consulta de fotos vencidas vai encontrá-lo!

    print(f"  👤 {len(moradores)} moradores inseridos")

    # ── 3.2 — Residências (10 unidades) ─────────────────────────────────────
    # Tipos: [V] VERTICAL (bloco+andar), [H] HORIZONTAL (quadra), [S] SIMPLES
    residencias = [
        # (codigo, numero, bloco, quadra, andar, tipo, interfone, obs, correlation_key)
        ('COND-001', '101', 'A',    None,  1, 'apartamento', '101', None,                    'res_101_A'),
        ('COND-001', '202', 'A',    None,  2, 'apartamento', '202', None,                    'res_202_A'),
        ('COND-001', '303', 'B',    None,  3, 'apartamento', '303', None,                    'res_303_B'),
        ('COND-001', '104', 'A',    None,  1, 'apartamento', '104', None,                    'res_104_A'),
        ('COND-001', '501', 'C',    None,  5, 'apartamento', '501', None,                    'res_501_C'),
        ('COND-001', '102', 'A',    None,  1, 'apartamento', '102', None,                    'res_102_A'),
        ('COND-001', '08',  None,   '03',  None, 'casa',     None,  'Lote 08 da Quadra 03',  'res_lote08_Q03'),
        ('COND-001', '14',  None,   '07',  None, 'casa',     None,  'Lote 14 da Quadra 07',  'res_lote14_Q07'),
        ('COND-001', '301', None,   None,  3, 'apartamento', '301', 'Predinho sem bloco',    'res_301_simples'),
        ('COND-001', '402', 'B',    None,  4, 'apartamento', '402', None,                    'res_402_B'),
    ]

    for cod, num, bloco, quadra, andar, tipo, inter, obs, ckey in residencias:
        cid = gerar_correlation_id('residencias', ckey)
        cur.execute("""
            INSERT INTO residencias (codigo_condominio, numero_residencia, bloco, quadra, andar,
                                     tipo_moradia, interfone, observacao, correlation_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (cod, num, bloco, quadra, andar, tipo, inter, obs, cid))

    print(f"  🏠 {len(residencias)} residências inseridas")

    # ── 3.3 — morador_residencia (quem mora onde) ──────────────────────────
    # DEMO N:N: Ana Paula (id=4) é proprietária de 2 unidades!
    vinculos = [
        # (morador_id, residencia_id, tipo_morador, dt_inicio, correlation_key)
        (1,  1,  'proprietario', '2024-01-10', 'mr_1_1'),
        (2,  2,  'inquilino',    '2025-06-01', 'mr_2_2'),
        (3,  3,  'proprietario', '2020-03-01', 'mr_3_3'),
        (4,  4,  'proprietario', '2023-03-15', 'mr_4_4'),
        (4,  1,  'proprietario', '2023-03-15', 'mr_4_1'),   # Ana Paula co-proprietária do 101!
        (5,  5,  'inquilino',    '2024-01-01', 'mr_5_5'),
        (6,  6,  'proprietario', '2019-07-01', 'mr_6_6'),
        (7,  7,  'inquilino',    '2022-01-15', 'mr_7_7'),
        (8,  8,  'proprietario', '2015-05-20', 'mr_8_8'),
        (9,  9,  'inquilino',    '2023-08-01', 'mr_9_9'),
        (10, 10, 'proprietario', '2018-02-01', 'mr_10_10'),
    ]

    for mid, rid, tipo, dt, ckey in vinculos:
        cid = gerar_correlation_id('morador_residencia', ckey)
        cur.execute("""
            INSERT INTO morador_residencia (morador_id, residencia_id, tipo_morador, dt_inicio, correlation_id)
            VALUES (?, ?, ?, ?, ?)
        """, (mid, rid, tipo, dt, cid))

    print(f"  🔗 {len(vinculos)} vínculos morador↔residência")

    # ── 3.4 — Config de segurança por morador (5 registros) ────────────────
    configs = [
        # (morador_id, fatores, senha, digital, facial, correlation_key)
        (1, 2, 0, 1, 1, 'cfg_1'),  # João: 2 fatores, só biometria
        (2, 1, 1, 1, 0, 'cfg_2'),  # Maria: 1 fator, senha ou digital
        (4, 2, 1, 1, 0, 'cfg_4'),  # Ana: 2 fatores, senha + digital
        (6, 1, 0, 1, 0, 'cfg_6'),  # Lucia: 1 fator, só digital
        (8, 2, 0, 1, 1, 'cfg_8'),  # Dona Teresa: 2 fatores, digital + facial
    ]

    for mid, fatores, senha, digital, facial, ckey in configs:
        cid = gerar_correlation_id('config_acesso_morador', ckey)
        cur.execute("""
            INSERT INTO config_acesso_morador
                (morador_id, fatores_requeridos, permite_senha, permite_digital, permite_facial, correlation_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (mid, fatores, senha, digital, facial, cid))

    print(f"  🔐 {len(configs)} configurações de segurança")

    # ── 3.5 — Assinatura do condomínio ──────────────────────────────────────
    cid = gerar_correlation_id('assinatura_condominio', 'COND-001')
    cur.execute("""
        INSERT INTO assinatura_condominio
            (codigo_condominio, nome_condominio, endereco, numero_contrato,
             dt_ativacao, dt_vigencia_inicio, status, observacoes, correlation_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        'COND-001',
        'Residencial Parque das Flores',
        'Rua das Palmeiras, 100, Jardim Botanico, Joao Pessoa - PB',
        '2026/0001-N7',
        '2026-04-09',
        '2026-04-09',
        'ativo',
        'Assinatura inicial do sistema n7-portaria-ai',
        cid,
    ))
    print("  📝 1 assinatura de condomínio")

    # ── 3.6 — Visitantes (8 registros) ──────────────────────────────────────
    visitantes = [
        # (nome, documento, tipo_doc, telefone, bloqueado, motivo_bloq, val_inicio, val_fim, ckey)
        ('Roberto Almeida',       '1234567',     'RG',         '83911112222', 0, None, None, None,         'vis_roberto'),
        ('Fernanda Costa',        '98765432101', 'CNH',        '83933334444', 0, None, None, None,         'vis_fernanda'),
        ('Marcos Delivery Pizza', '7654321',     'RG',         '83955556666', 0, None, None, None,         'vis_marcos'),
        ('Jose Suspeito',         '0000000',     'RG',         None,          1, 'Tentativa de acesso nao autorizado em 01/04/2026', None, None, 'vis_jose'),
        ('Jean Pierre Dubois',   'FR12345678',  'PASSAPORTE', '83900998877', 0, None, '2026-04-10', '2026-04-30', 'vis_jean'),
        ('Camila Rodrigues',      '55544433322', 'CNH',        '83944223311', 0, None, '2026-05-01', '2026-07-31', 'vis_camila'),
        ('Sandra Oliveira',       '3216549',     'RG',         '83966778899', 0, None, '2026-04-09', None,         'vis_sandra'),
        ('Ricardo Problema',      '1111111',     'RG',         None,          1, 'Comportamento agressivo com porteiro em 28/03/2026', None, None, 'vis_ricardo'),
    ]

    for nome, doc, tdoc, tel, bloq, motivo, vi, vf, ckey in visitantes:
        cid = gerar_correlation_id('visitantes', ckey)
        cur.execute("""
            INSERT INTO visitantes (nome, documento, tipo_documento, telefone,
                                    bloqueado, motivo_bloqueio, dt_validade_inicio, dt_validade_fim,
                                    correlation_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (nome, doc, tdoc, tel, bloq, motivo, vi, vf, cid))

    print(f"  🚶 {len(visitantes)} visitantes inseridos")

    # ── 3.7 — Funcionários (5 registros) ────────────────────────────────────
    # senha_hash = SHA-256 de '' (string vazia) — trocar em produção!
    SENHA_VAZIA_HASH = hashlib.sha256(b'').hexdigest()

    funcionarios = [
        # (nome, cpf, cargo, setor, login, ckey)
        ('Jose Silva Santos',      '10120230340', 'porteiro',       'portaria',       'porteiro.silva',  'func_jose'),
        ('Marcos Pereira Lima',    '20230340450', 'porteiro',       'portaria',       'porteiro.marcos', 'func_marcos'),
        ('Claudia Regina Borges',  '30340450560', 'administrador',  'administracao',  'admin.claudia',   'func_claudia'),
        ('Fatima Souza Andrade',   '40450560670', 'outro',          'limpeza',        'limpeza.fatima',  'func_fatima'),
        ('Paulo Oliveira Neto',    '50560670780', 'zelador',        'manutencao',     'zelador.paulo',   'func_paulo'),
    ]

    for nome, cpf, cargo, setor, login, ckey in funcionarios:
        cid = gerar_correlation_id('funcionarios', ckey)
        cur.execute("""
            INSERT INTO funcionarios (nome, cpf, cargo, setor, login, senha_hash, correlation_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nome, cpf, cargo, setor, login, SENHA_VAZIA_HASH, cid))

    print(f"  👷 {len(funcionarios)} funcionários inseridos")

    # ── 3.8 — Veículos (5 registros) ────────────────────────────────────────
    veiculos = [
        # (placa, modelo, cor, morador_id, func_id, visit_id, ckey)
        ('ABC-1234', 'Honda Civic',     'Prata',    1,    None, None, 'veic_abc'),
        ('DEF-5678', 'Fiat Pulse',      'Branco',   4,    None, None, 'veic_def'),
        ('GHI-9012', 'Toyota Corolla',  'Preto',    8,    None, None, 'veic_ghi'),
        ('JKL-3456', 'Moto Honda CG',   'Vermelha', None, 2,    None, 'veic_jkl'),
        ('QRS-5678', 'VW Polo',         'Cinza',    None, None, 2,    'veic_qrs'),
    ]

    for placa, modelo, cor, mid, fid, vid, ckey in veiculos:
        cid = gerar_correlation_id('veiculos', ckey)
        cur.execute("""
            INSERT INTO veiculos (placa, modelo, cor, morador_id, funcionario_id, visitante_id, correlation_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (placa, modelo, cor, mid, fid, vid, cid))

    print(f"  🚗 {len(veiculos)} veículos inseridos")

    # ── 3.9 — Registros de acesso (10 registros) ───────────────────────────
    acessos = [
        # (visit_id, morador_id, func_id, veic_id, tipo, s, d, f, motivo, entrada, saida, porteiro, obs, ckey)
        (1, 1, 1, None, 'pedestre', 0, 1, 0, 'Visita familiar',                    '2026-04-08 14:00:00', '2026-04-08 17:30:00', 'Porteiro Silva',  'Tio do morador',              'ac_1'),
        (2, 2, 1, 5,    'garagem',  0, 1, 1, 'Visita social',                      '2026-04-09 10:00:00', '2026-04-09 12:00:00', 'Porteiro Silva',  None,                          'ac_2'),
        (3, 3, 2, None, 'pedestre', 1, 0, 0, 'Entrega - Pizza',                    '2026-04-09 19:45:00', '2026-04-09 19:52:00', 'Porteiro Marcos', 'Delivery de moto',            'ac_3'),
        (1, 4, 1, None, 'pedestre', 0, 1, 0, 'Manutencao do ar-condicionado',      '2026-04-09 14:00:00', None,                  'Porteiro Silva',  None,                          'ac_4'),  # DENTRO!
        (5, 2, 2, None, 'pedestre', 1, 0, 0, 'Visita social - amiga',              '2026-04-07 15:00:00', '2026-04-07 18:30:00', 'Porteiro Marcos', None,                          'ac_5'),
        (6, 8, 1, None, 'pedestre', 1, 1, 0, 'Manutencao - Ar condicionado',       '2026-04-08 09:00:00', '2026-04-08 11:45:00', 'Porteiro Silva',  'Tecnico autorizado',          'ac_6'),
        (7, 3, 2, None, 'pedestre', 0, 1, 0, 'Visita familiar - irma',             '2026-04-06 10:00:00', '2026-04-06 13:00:00', 'Porteiro Marcos', None,                          'ac_7'),
        (7, 3, 1, None, 'pedestre', 0, 1, 0, 'Visita familiar - irma',             '2026-04-09 16:00:00', '2026-04-09 20:00:00', 'Porteiro Silva',  'Trouxe bolo de aniversario',  'ac_8'),
        (3, 8, 2, None, 'pedestre', 1, 0, 0, 'Entrega - Restaurante Japones',      '2026-04-09 12:30:00', '2026-04-09 12:38:00', 'Porteiro Marcos', 'Delivery de moto',            'ac_9'),
        (2, 6, 1, 5,    'garagem',  0, 1, 1, 'Reuniao de condominio informal',     '2026-04-09 18:00:00', None,                  'Porteiro Silva',  'Veio de carro, placa QRS-5678', 'ac_10'),  # DENTRO!
    ]

    for vid, mid, fid, vecid, tipo, s, d, f, motivo, entrada, saida, porteiro, obs, ckey in acessos:
        cid = gerar_correlation_id('acessos', ckey)
        cur.execute("""
            INSERT INTO acessos (visitante_id, morador_id, funcionario_id, veiculo_id,
                                 tipo_acesso, auth_senha, auth_digital, auth_facial,
                                 motivo, dt_entrada_em, dt_saida_em, porteiro, observacoes,
                                 correlation_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (vid, mid, fid, vecid, tipo, s, d, f, motivo, entrada, saida, porteiro, obs, cid))

    print(f"  🚪 {len(acessos)} registros de acesso\n")

    # ========================================================================
    # COMMIT E RESUMO
    # ========================================================================
    conn.commit()

    # Resumo final
    print("=" * 60)
    print("  RESUMO DO BANCO CRIADO")
    print("=" * 60)

    tabelas = cur.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """).fetchall()

    for (tabela,) in tabelas:
        count = cur.execute(f"SELECT COUNT(*) FROM {tabela}").fetchone()[0]
        print(f"  {tabela:30s} → {count:>3} registros")

    # Contagem de índices
    idx_count = cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'").fetchone()[0]
    print(f"\n  {'ÍNDICES':30s} → {idx_count:>3} criados")

    # Quem está dentro agora?
    dentro = cur.execute("""
        SELECT v.nome, m.nome, a.motivo
        FROM acessos a
            JOIN visitantes v ON a.visitante_id = v.id
            JOIN moradores m ON a.morador_id = m.id
        WHERE a.dt_saida_em IS NULL
    """).fetchall()

    if dentro:
        print(f"\n  ⚠️  {len(dentro)} pessoa(s) DENTRO do condomínio agora:")
        for vis, mor, motivo in dentro:
            print(f"     → {vis} visitando {mor} ({motivo})")

    print(f"\n✅ Banco pronto: {DB_PATH}")
    print("   Abra no DBeaver: File → New → SQLite → selecione portaria.db")

    conn.close()


# ============================================================================
# EXECUÇÃO
# ============================================================================
if __name__ == "__main__":
    criar_banco()


# ============================================================================
# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                    GABARITO — RESPOSTAS DOS EXERCÍCIOS                  ║
# ║            Ademilson, tente resolver ANTES de olhar aqui!              ║
# ╚══════════════════════════════════════════════════════════════════════════╝
# ============================================================================
#
# Para testar as respostas abaixo, descomente e rode no Python interativo:
#   conn = sqlite3.connect('portaria.db')
#   conn.row_factory = sqlite3.Row
#   cur = conn.cursor()
#
# ────────────────────────────────────────────────────────────────────────────
# EXERCÍCIO 1: Insira um novo morador chamado 'Luiza Barbosa',
#   CPF '22233344455', telefone '83944556677'.
# ────────────────────────────────────────────────────────────────────────────
#
# RESPOSTA 1:
# cur.execute("""
#     INSERT INTO moradores (nome, cpf, telefone, correlation_id)
#     VALUES ('Luiza Barbosa', '22233344455', '83944556677',
#             'gabarito_resp1_luiza_barbosa_22233344455')
# """)
# conn.commit()
#
# # Conferir:
# cur.execute("SELECT id, nome, cpf, telefone FROM moradores WHERE cpf = '22233344455'")
# print(cur.fetchone())
#
#
# ────────────────────────────────────────────────────────────────────────────
# EXERCÍCIO 2: Adicione uma residência para a Luiza (Apto 401, Bloco B).
#   Dica: primeiro INSERT em residencias, depois em morador_residencia.
# ────────────────────────────────────────────────────────────────────────────
#
# RESPOSTA 2:
# cur.execute("""
#     INSERT INTO residencias (codigo_condominio, numero_residencia, bloco, andar,
#                              tipo_moradia, interfone, correlation_id)
#     VALUES ('COND-001', '401', 'B', 4, 'apartamento', '401',
#             'gabarito_resp2_residencia_401_bloco_b')
# """)
#
# # Buscar IDs dinamicamente (melhor prática!):
# luiza_id = cur.execute("SELECT id FROM moradores WHERE cpf = '22233344455'").fetchone()[0]
# res_id = cur.execute("SELECT id FROM residencias WHERE numero_residencia = '401' AND bloco = 'B'").fetchone()[0]
#
# cur.execute("""
#     INSERT INTO morador_residencia (morador_id, residencia_id, tipo_morador, correlation_id)
#     VALUES (?, ?, 'inquilino', 'gabarito_resp2_vinculo_luiza_401b')
# """, (luiza_id, res_id))
# conn.commit()
#
# # Conferir:
# cur.execute("""
#     SELECT m.nome, r.numero_residencia, r.bloco, mr.tipo_morador
#     FROM moradores m
#         JOIN morador_residencia mr ON m.id = mr.morador_id
#         JOIN residencias r ON mr.residencia_id = r.id
#     WHERE m.cpf = '22233344455'
# """)
# print(cur.fetchone())
#
#
# ────────────────────────────────────────────────────────────────────────────
# EXERCÍCIO 3: Registre a SAÍDA do Roberto (acesso id=4, ainda dentro).
#   Dica: UPDATE acessos SET dt_saida_em = ... WHERE id = 4
# ────────────────────────────────────────────────────────────────────────────
#
# RESPOSTA 3:
# cur.execute("UPDATE acessos SET dt_saida_em = '2026-04-09 16:00:00' WHERE id = 4")
# conn.commit()
#
# # Conferir:
# cur.execute("SELECT id, dt_entrada_em, dt_saida_em FROM acessos WHERE id = 4")
# print(cur.fetchone())
#
#
# ────────────────────────────────────────────────────────────────────────────
# EXERCÍCIO 4: Liste todos os moradores do Bloco A com seus interfones.
#   Dica: JOIN moradores + morador_residencia + residencias WHERE bloco='A'
# ────────────────────────────────────────────────────────────────────────────
#
# RESPOSTA 4:
# cur.execute("""
#     SELECT m.nome, r.numero_residencia, r.interfone, mr.tipo_morador
#     FROM moradores m
#         JOIN morador_residencia mr ON m.id = mr.morador_id
#         JOIN residencias r ON mr.residencia_id = r.id
#     WHERE r.bloco = 'A' AND m.ativo = 1
#     ORDER BY r.numero_residencia
# """)
# for row in cur.fetchall():
#     print(row)
#
#
# ────────────────────────────────────────────────────────────────────────────
# EXERCÍCIO 5 (DESAFIO): Quantos moradores de cada tipo_moradia existem?
#   Dica: JOIN + GROUP BY tipo_moradia
# ────────────────────────────────────────────────────────────────────────────
#
# RESPOSTA 5:
# cur.execute("""
#     SELECT r.tipo_moradia, COUNT(DISTINCT m.id) AS total_moradores
#     FROM moradores m
#         JOIN morador_residencia mr ON m.id = mr.morador_id
#         JOIN residencias r ON mr.residencia_id = r.id
#     WHERE m.ativo = 1 AND mr.ativo = 1
#     GROUP BY r.tipo_moradia
# """)
# for row in cur.fetchall():
#     print(row)
#
#
# ────────────────────────────────────────────────────────────────────────────
# EXERCÍCIO 6 (DESAFIO): Quem tem MAIS de uma unidade? (demo N:N)
#   Dica: GROUP BY m.id + HAVING COUNT > 1
# ────────────────────────────────────────────────────────────────────────────
#
# RESPOSTA 6:
# cur.execute("""
#     SELECT m.nome, COUNT(mr.residencia_id) AS unidades
#     FROM moradores m
#         JOIN morador_residencia mr ON m.id = mr.morador_id
#     WHERE mr.tipo_morador = 'proprietario' AND mr.ativo = 1
#     GROUP BY m.id
#     HAVING COUNT(mr.residencia_id) > 1
# """)
# for row in cur.fetchall():
#     print(row)
#
#
# ────────────────────────────────────────────────────────────────────────────
# EXERCÍCIO 7 (DESAFIO LGPD): Qual % de moradores ainda não aceitou os termos?
#   Dica: SUM(CASE WHEN...) / COUNT(*) * 100.0
# ────────────────────────────────────────────────────────────────────────────
#
# RESPOSTA 7:
# cur.execute("""
#     SELECT
#         COUNT(*) AS total,
#         SUM(CASE WHEN dt_aceite_lgpd IS NULL THEN 1 ELSE 0 END) AS sem_aceite,
#         ROUND(
#             SUM(CASE WHEN dt_aceite_lgpd IS NULL THEN 1.0 ELSE 0 END)
#             / COUNT(*) * 100, 1
#         ) AS pct_pendente
#     FROM moradores
#     WHERE ativo = 1
# """)
# print(cur.fetchone())
#
# ============================================================================
# FIM DO GABARITO
# ============================================================================
