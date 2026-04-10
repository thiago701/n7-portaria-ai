-- ============================================================================
-- PROJETO PORTARIA INTELIGENTE — BANCO DE DADOS COMPLETO (v1.0)
-- ============================================================================
-- Aluno: Ademilson
-- Aula 02 (Ampliada) — Banco de Dados + Estrutura Completa do Projeto
-- Data da Aula: 09/04/2026
-- Criado em: 04/04/2026 (contribuicao de Ademilson + Thiago)
--
-- COMO EXECUTAR:
--   sqlite3 portaria.db < projeto_portaria_completo.sql
--
--   Ou no Python:
--   import sqlite3
--   conn = sqlite3.connect('portaria.db')
--   with open('projeto_portaria_completo.sql', 'r') as f:
--       conn.executescript(f.read())
-- ============================================================================

PRAGMA foreign_keys = ON;
-- Ativa verificacao de chaves estrangeiras no SQLite.
-- Por padrao o SQLite NAO verifica FKs — este PRAGMA ativa!
-- MUITO IMPORTANTE para garantir integridade dos dados.

-- ============================================================================
-- PARTE 1: CRIACAO DAS TABELAS (DROP primeiro para re-executar com seguranca)
-- ============================================================================

DROP TABLE IF EXISTS acessos;
DROP TABLE IF EXISTS morador_residencia;
DROP TABLE IF EXISTS config_acesso_morador;
DROP TABLE IF EXISTS veiculos;
DROP TABLE IF EXISTS assinatura_condominio;
DROP TABLE IF EXISTS visitantes;
DROP TABLE IF EXISTS funcionarios;
DROP TABLE IF EXISTS residencias;
DROP TABLE IF EXISTS moradores;

-- ======================================================================
--  TABELA 1: moradores
--  Guarda os dados PESSOAIS de cada morador.
--  Dados da UNIDADE estao em 'residencias' (tabela separada).
-- ======================================================================
--
-- MUDANCA v8.0: Os campos de unidade (numero_residencia, bloco, andar...)
-- foram movidos para 'residencias'. Um morador pode ter N unidades.
-- A relacao morador <-> unidade esta em 'morador_residencia'.
--
-- LGPD (Lei 13.709/2018):
--   O sistema coleta dados pessoais dos moradores. Por lei, precisamos:
--   - Informar o morador sobre o uso dos dados (termos de uso)
--   - Guardar a prova de aceite (bytes do documento + timestamp)
--   'termos_lgpd' = bytes do PDF dos termos que o morador recebeu e aceitou
--   'dt_aceite_lgpd' = quando ele aceitou (prova juridica)

CREATE TABLE moradores (
    id                    INTEGER   PRIMARY KEY AUTOINCREMENT,
    -- Identificador unico. O banco cria sozinho: 1, 2, 3...

    nome                  TEXT      NOT NULL,
    -- Nome completo. Obrigatorio.

    cpf                   TEXT      UNIQUE NOT NULL
                                    CHECK(length(cpf) = 11),
    -- CPF sem pontos (so numeros: 12345678901).
    -- UNIQUE = nao pode repetir. CHECK = exige exatamente 11 digitos.
    -- POR QUE TEXT? CPF pode comecar com zero — INTEGER perderia o zero!

    telefone              TEXT,
    -- Telefone de contato (opcional).

    email                 TEXT      CHECK(email LIKE '%@%.%'),
    -- Email (opcional). CHECK valida formato basico: precisa ter '@' e '.'.

    dt_nascimento         DATE,
    -- Data de nascimento. Formato: 'AAAA-MM-DD' (ex: '1985-03-22').
    -- Util para verificar maioridade e gerar relatorios demograficos.

    foto                  BLOB,
    -- Foto do morador armazenada como bytes binarios.
    -- Em producao: with open('foto.jpg','rb') as f: foto_bytes = f.read()

    dt_foto_validade      DATE,
    -- Validade da foto. Renovar a cada 2 anos (pessoas mudam!).

    biometria             BLOB,
    -- Bytes da impressao digital (template biometrico).
    -- Gerado pelo leitor, nunca reconstruivel para a digital original.

    dt_biometria_validade DATE,
    -- Validade da biometria. Renovar a cada 2 anos. --- 4 a 5 anos
    --- Se por acusa houver um acidente (tipo corte na digital) que possa produzir uma cicatriz aí diminue o tempo de validade

    -- ══════════════════════════════════════════════════════════
    -- CAMPOS LGPD (v8.0) — conformidade com Lei 13.709/2018
    -- ══════════════════════════════════════════════════════════

    termos_lgpd           BLOB,
    -- Bytes do PDF dos Termos de Uso e Politica de Privacidade
    -- que o morador recebeu no momento do cadastro.
    -- Guardamos o DOCUMENTO EXATO que ele aceitou — nao so um flag!
    -- Isso e evidencia juridica em caso de auditoria da ANPD.
    --
    -- Em producao:
    --   with open('termos_v2.pdf', 'rb') as f:
    --       termos_bytes = f.read()
    --   cursor.execute('UPDATE moradores SET termos_lgpd = ? WHERE id = ?',
    --                  (termos_bytes, id))

    dt_aceite_lgpd        DATETIME,
    -- Timestamp do momento em que o morador aceitou os termos.
    -- NULL = termos ainda nao formalizados (morador antigo sem aceite digital).
    -- Em producao: dt_aceite_lgpd = datetime.now().isoformat()

    ativo                 BOOLEAN   DEFAULT 1
                                    CHECK(ativo IN (0, 1)),
    -- 1 = morador ativo. 0 = desativado (soft delete — dado preservado!).
    -- NAO usamos DELETE — isso se chama "exclusao logica".

    -- ══════════════════════════════════════════════════════════
    -- CORRELATION_ID (v8.0) — sincronizacao com nuvem
    -- ══════════════════════════════════════════════════════════

    correlation_id        TEXT      UNIQUE NOT NULL,
    -- Hash SHA-256 de 64 caracteres hex. Gerado no Python:
    --   import hashlib
    --   cid = hashlib.sha256(f'moradores:{cpf}'.encode()).hexdigest()
    -- Unico globalmente. Usado para sync SQLite <-> nuvem sem duplicatas.
    -- Ver secao 5.8 para explicacao completa de idempotencia.

    dt_criado_em          DATETIME  DEFAULT CURRENT_TIMESTAMP,
    -- Criado automaticamente no INSERT.

    dt_atualizado_em      DATETIME  DEFAULT CURRENT_TIMESTAMP
    -- Atualizado manualmente no UPDATE (o banco nao faz isso sozinho).
);


-- ======================================================================
--  TABELA 2: residencias
--  Guarda os dados de cada UNIDADE HABITACIONAL do condominio.
-- ======================================================================
--
-- ANALOGIA: Na prefeitura existem dois cadastros separados:
--   - Cadastro de PESSOA (CPF, nome, telefone...)
--   - Cadastro de IMOVEL (numero, bloco, andar, tipo...)
-- Nossa tabela segue o mesmo principio.

CREATE TABLE residencias (
    id                    INTEGER   PRIMARY KEY AUTOINCREMENT,

    codigo_condominio     TEXT      NOT NULL,
    -- Codigo do condominio ao qual esta unidade pertence.
    -- Ex: 'COND-001' (referencia ao codigo em assinatura_condominio).
    -- Texto livre — nao e FK para evitar dependencia circular.

    numero_residencia     TEXT      NOT NULL,
    -- Numero da unidade. TEXT porque pode ser '101', '101-A', '12' (lote).

    -- ══════════════════════════════════════════════════════════
    -- LOCALIZACAO — varia por tipo de condominio
    -- ══════════════════════════════════════════════════════════
    --
    --   VERTICAL (apartamentos):  bloco + andar + numero_residencia
    --   HORIZONTAL (casas/lotes): quadra + numero_residencia
    --   SIMPLES (predinho unico): andar + numero_residencia

    bloco                 TEXT,
    -- Ex: 'A', 'B', 'Torre 1'. NULL em condominios horizontais.

    quadra                TEXT,
    -- Ex: '01', '05'. NULL em condominios verticais.

    andar                 INTEGER,
    -- Numero do andar. NULL em casas (condominio horizontal).

    tipo_moradia          TEXT      DEFAULT 'apartamento'
                                    CHECK(tipo_moradia IN ('apartamento','casa','comercial','outro')),
    -- Tipo fisico da unidade.
    -- SUGESTAO DO ADEMILSON (v5.0) — agora no lugar correto!

    interfone             TEXT,
    -- Codigo do interfone desta unidade (ex: '101', '1-A').
    -- SUGESTAO DO ADEMILSON (v5.0) — agora no lugar correto!

    observacao            TEXT,
    -- Observacoes sobre a unidade (ex: 'Cobertura — acesso especial').
    -- SUGESTAO DO ADEMILSON (v5.0) — agora no lugar correto!

    ativo                 BOOLEAN   DEFAULT 1
                                    CHECK(ativo IN (0, 1)),

    correlation_id        TEXT      UNIQUE NOT NULL,

    dt_criado_em          DATETIME  DEFAULT CURRENT_TIMESTAMP,
    dt_atualizado_em      DATETIME  DEFAULT CURRENT_TIMESTAMP
);


-- ======================================================================
--  TABELA 3: morador_residencia (TABELA DE ASSOCIACAO / JUNCTION TABLE)
--  Conecta moradores a residencias. Permite N:N (muitos para muitos).
-- ======================================================================
--
-- POR QUE ESSA TABELA EXISTE?
--
--   Problema: Um morador pode TER VARIAS unidades (proprietario de
--   varios apartamentos). E uma unidade pode TER VARIOS moradores
--   (casal, familia). Isso e uma relacao MUITOS PARA MUITOS (N:N).
--
--   Em SQL, relacoes N:N nao cabem em 2 tabelas — precisam de uma
--   TERCEIRA tabela no meio. Essa e a 'morador_residencia'.
--
--   ANALOGIA: Pense em um hospital.
--     - Um paciente pode ter varios medicos.
--     - Um medico pode ter varios pacientes.
--     - A tabela 'consultas' conecta os dois (paciente_id + medico_id).
--   Aqui: 'morador_residencia' conecta moradores e residencias.
--
-- EXEMPLO DE USO:
--   Ana Paula (id=4) e proprietaria de 2 unidades:
--     INSERT INTO morador_residencia (morador_id, residencia_id, tipo_morador)
--     VALUES (4, 4, 'proprietario');  -- Apto 104 (dela)
--     INSERT INTO morador_residencia (morador_id, residencia_id, tipo_morador)
--     VALUES (4, 1, 'proprietario');  -- Apto 101 (herdou do pai)

CREATE TABLE morador_residencia (
    id                    INTEGER   PRIMARY KEY AUTOINCREMENT,

    morador_id            INTEGER   NOT NULL,
    -- FK para moradores.id

    residencia_id         INTEGER   NOT NULL,
    -- FK para residencias.id

    tipo_morador          TEXT      DEFAULT 'proprietario'
                                    CHECK(tipo_morador IN ('proprietario', 'inquilino')),
    -- O morador e dono ou inquilino DESTA unidade especifica.
    -- Um mesmo morador pode ser proprietario de uma e inquilino de outra!

    dt_inicio             DATE      NOT NULL DEFAULT (DATE('now')),
    -- Data em que o morador passou a ocupar esta unidade.

    dt_fim                DATE,
    -- Data em que saiu. NULL = ainda mora aqui.
    -- CHECK: se preenchido, deve ser >= dt_inicio.

    ativo                 BOOLEAN   DEFAULT 1
                                    CHECK(ativo IN (0, 1)),

    correlation_id        TEXT      UNIQUE NOT NULL,

    dt_criado_em          DATETIME  DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (morador_id)    REFERENCES moradores(id),
    FOREIGN KEY (residencia_id) REFERENCES residencias(id),
    UNIQUE (morador_id, residencia_id, dt_inicio)
    -- Evita duplicata: mesma combinacao morador+unidade+data so uma vez.
    -- Permite historico: Ana pode ter saido e voltado (dt_inicio diferente).
);


-- ======================================================================
--  TABELA 4: visitantes
--  Guarda os dados de pessoas que visitam o condominio.
-- ======================================================================

CREATE TABLE visitantes (
    id                    INTEGER   PRIMARY KEY AUTOINCREMENT,

    nome                  TEXT      NOT NULL,
    documento             TEXT      NOT NULL,

    tipo_documento        TEXT      DEFAULT 'RG'
                                    CHECK(tipo_documento IN ('RG', 'CNH', 'PASSAPORTE', 'OUTRO')),

    telefone              TEXT,

    foto                  BLOB,
    -- Foto do visitante. Util para reconhecimento facial futuro com IA.

    bloqueado             BOOLEAN   DEFAULT 0
                                    CHECK(bloqueado IN (0, 1)),
    -- 0 = visitante normal. 1 = bloqueado (porta nao abre sem autorizacao manual).

    motivo_bloqueio       TEXT,
    -- Se bloqueado = 1, por que? Registra o historico da ocorrencia.

    -- ══════════════════════════════════════════════════════════
    -- JANELA DE ACESSO (opcional)
    -- ══════════════════════════════════════════════════════════
    -- Define um periodo em que o visitante tem acesso autorizado.
    -- NULL em ambos = sem restricao de data.

    dt_validade_inicio    DATE,
    -- A partir desta data o visitante pode entrar.
    -- NULL = sem restricao de data de inicio.

    dt_validade_fim       DATE      CHECK(
                                        dt_validade_fim IS NULL OR
                                        dt_validade_fim >= dt_validade_inicio),
    -- Ate esta data o visitante pode entrar.
    -- NULL = sem data de corte.
    -- CHECK garante que o fim nao e anterior ao inicio.

    correlation_id        TEXT      UNIQUE NOT NULL,

    dt_criado_em          DATETIME  DEFAULT CURRENT_TIMESTAMP
);


-- ======================================================================
--  TABELA 5: funcionarios
--  Porteiros, zeladores, administradores do condominio.
-- ======================================================================
--
-- CONTRIBUICAO DO ADEMILSON (v3.0): Ele identificou que o sistema
-- precisava distinguir quem registrou cada acesso — origem desta tabela!

CREATE TABLE funcionarios (
    id                    INTEGER   PRIMARY KEY AUTOINCREMENT,
    nome                  TEXT      NOT NULL,
    cpf                   TEXT      UNIQUE NOT NULL  CHECK(length(cpf) = 11),
    cargo                 TEXT      DEFAULT 'porteiro'
                                    CHECK(cargo IN ('porteiro','zelador','administrador','outro')),
    setor                 TEXT,
    -- Texto livre: 'portaria', 'administracao', 'limpeza', 'manutencao'...

    login                 TEXT      UNIQUE NOT NULL,
    senha_hash            TEXT      NOT NULL  CHECK(length(senha_hash) = 64),
    -- Hash SHA-256 da senha (64 hex chars). NUNCA armazenar senha em texto!
    -- Python: hashlib.sha256('senha'.encode()).hexdigest()

    ativo                 BOOLEAN   DEFAULT 1  CHECK(ativo IN (0, 1)),

    correlation_id        TEXT      UNIQUE NOT NULL,

    dt_criado_em          DATETIME  DEFAULT CURRENT_TIMESTAMP
);


-- ======================================================================
--  TABELA 6: veiculos
--  Veiculos de moradores, funcionarios e visitantes.
-- ======================================================================
--
-- CONTRIBUICAO DO ADEMILSON (v3.0): "Carro e placa" foi sugestao dele!
-- Um veiculo pertence a UM dos tres tipos: morador, funcionario ou visitante.
-- Apenas um dos tres campos FK deve estar preenchido (os outros ficam NULL).

CREATE TABLE veiculos (
    id                    INTEGER   PRIMARY KEY AUTOINCREMENT,
    placa                 TEXT      UNIQUE NOT NULL  CHECK(length(placa) >= 7),
    -- Formato: 'ABC-1234' (Mercosul: 'ABC1D23'). Minimo 7 chars.

    modelo                TEXT,
    cor                   TEXT,

    morador_id            INTEGER,
    funcionario_id        INTEGER,
    visitante_id          INTEGER,
    -- Apenas UM deve ser preenchido. Os outros ficam NULL.
    -- Em producao, validar no Python antes de inserir.

    ativo                 BOOLEAN   DEFAULT 1  CHECK(ativo IN (0, 1)),

    correlation_id        TEXT      UNIQUE NOT NULL,

    dt_criado_em          DATETIME  DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (morador_id)      REFERENCES moradores(id),
    FOREIGN KEY (funcionario_id)  REFERENCES funcionarios(id),
    FOREIGN KEY (visitante_id)    REFERENCES visitantes(id)
);


-- ======================================================================
--  TABELA 7: acessos
--  Log de cada entrada e saida no condominio. Nunca deletar!
-- ======================================================================
--
-- ESTA TABELA E O CORACAO DO SISTEMA.
-- Cada linha representa um evento: alguem entrou (ou saiu).
-- O porteiro registra o acesso; o sistema guarda para sempre.
--
-- FATORES DE AUTENTICACAO (2FA):
--   auth_senha   = porteiro digitou senha manual de liberacao
--   auth_digital = leitor biometrico confirmou digital
--   auth_facial  = camera reconheceu o rosto
-- Pelo menos 1 dos tres deve ser verdadeiro (CHECK garante isso).

CREATE TABLE acessos (
    id                    INTEGER   PRIMARY KEY AUTOINCREMENT,

    visitante_id          INTEGER   NOT NULL,
    morador_id            INTEGER,
    -- Morador visitado. NULL em casos de servicos gerais sem morador especifico.

    funcionario_id        INTEGER,
    -- Porteiro que registrou este acesso (quem estava de plantao).

    veiculo_id            INTEGER,
    -- Veiculo usado no acesso (NULL se veio a pe).

    tipo_acesso           TEXT      DEFAULT 'pedestre'
                                    CHECK(tipo_acesso IN ('pedestre', 'garagem')),
    -- 'pedestre' = portao principal (pessoas a pe, entregas, prestadores)
    -- 'garagem'  = cancela do estacionamento (veiculos)

    auth_senha            BOOLEAN   DEFAULT 0  CHECK(auth_senha IN (0,1)),
    auth_digital          BOOLEAN   DEFAULT 0  CHECK(auth_digital IN (0,1)),
    auth_facial           BOOLEAN   DEFAULT 0  CHECK(auth_facial IN (0,1)),

    motivo                TEXT      NOT NULL,
    -- Razao da visita: 'Visita familiar', 'Entrega', 'Manutencao'...

    dt_entrada_em         DATETIME  NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    dt_saida_em           DATETIME,
    -- NULL = pessoa ainda esta dentro do condominio.
    -- Ao sair: UPDATE acessos SET dt_saida_em = CURRENT_TIMESTAMP WHERE id = ?

    porteiro              TEXT,
    -- Nome do porteiro em texto livre (campo legado de compatibilidade).

    observacoes           TEXT,

    correlation_id        TEXT      UNIQUE NOT NULL,

    -- Pelo menos 1 fator de autenticacao deve ser verdadeiro:
    CHECK(auth_senha + auth_digital + auth_facial >= 1),

    FOREIGN KEY (visitante_id)   REFERENCES visitantes(id),
    FOREIGN KEY (morador_id)     REFERENCES moradores(id),
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id),
    FOREIGN KEY (veiculo_id)     REFERENCES veiculos(id)
);


-- ======================================================================
--  TABELA 8: config_acesso_morador
--  Politica de seguranca individual por morador.
-- ======================================================================
--
-- Cada morador pode ter uma politica personalizada de autenticacao.
-- Quantos fatores sao exigidos? Quais tipos sao permitidos?
-- Quando ausente, o sistema usa o padrao do condominio (1 fator, qualquer tipo).

CREATE TABLE config_acesso_morador (
    id                    INTEGER   PRIMARY KEY AUTOINCREMENT,

    morador_id            INTEGER   UNIQUE NOT NULL,
    -- UNIQUE: cada morador tem no maximo 1 config. Relacao 1:1.

    fatores_requeridos    INTEGER   DEFAULT 1  CHECK(fatores_requeridos IN (1, 2)),
    -- 1 = qualquer fator aceito (senha OU digital OU facial)
    -- 2 = dois fatores obrigatorios (ex: digital + facial)

    permite_senha         BOOLEAN   DEFAULT 1  CHECK(permite_senha IN (0, 1)),
    permite_digital       BOOLEAN   DEFAULT 1  CHECK(permite_digital IN (0, 1)),
    permite_facial        BOOLEAN   DEFAULT 0  CHECK(permite_facial IN (0, 1)),

    correlation_id        TEXT      UNIQUE NOT NULL,

    dt_criado_em          DATETIME  DEFAULT CURRENT_TIMESTAMP,
    dt_atualizado_em      DATETIME  DEFAULT CURRENT_TIMESTAMP,

    -- Pelo menos 1 tipo de autenticacao deve estar habilitado:
    CHECK(permite_senha + permite_digital + permite_facial >= 1),

    FOREIGN KEY (morador_id) REFERENCES moradores(id)
);


-- ======================================================================
--  TABELA 9: assinatura_condominio
--  Contrato do CONDOMINIO com o servico n7-portaria-ai.
-- ======================================================================
--
-- MUDANCA IMPORTANTE v8.0:
--   Antes: cada morador tinha seu proprio contrato (N linhas por condo).
--   Agora: cada CONDOMINIO tem UMA assinatura (UNIQUE codigo_condominio).
--
--   Esta tabela representa o contrato do condominio como ORGANIZACAO
--   com o sistema n7-portaria-ai — nao contratos individuais de moradores.
--
--   'responsavel_id' = sindico ou administrador que assinou o contrato.
--   O historico de contratos de moradores individuais (inquilinos)
--   deve ir em outra tabela se necessario (fora do escopo desta versao).
--
-- EXEMPLO: O "Residencial Parque das Flores" assina o n7-portaria-ai.
--   Todos os moradores do condominio passam a usar o sistema.
--   Um so registro representa essa assinatura.

CREATE TABLE assinatura_condominio (
    id                    INTEGER   PRIMARY KEY AUTOINCREMENT,

    codigo_condominio     TEXT      UNIQUE NOT NULL,
    -- Codigo interno unico do condominio. UNIQUE = 1 assinatura por condo!
    -- Ex: 'COND-001', 'PQ-FLORES', 'ED-CENTRAL'

    nome_condominio       TEXT      NOT NULL,
    -- Nome comercial do condominio.

    endereco              TEXT,
    -- Endereco completo do condominio.

    responsavel_id        INTEGER,
    -- FK → moradores.id (o sindico ou representante que assinou o contrato).
    -- Nullable: pode ser preenchido apos o INSERT inicial.

    numero_contrato       TEXT      UNIQUE NOT NULL,
    -- Numero unico do contrato firmado. Ex: '2026/0001-N7'

    contrato              BLOB,
    -- Bytes do PDF do contrato digitalizado e assinado.
    -- NULL nos dados de exemplo (em producao: bytes do arquivo).

    dt_ativacao           DATE,
    -- Data em que o sistema foi ativado para uso.
    -- NULL enquanto status = 'pendente' (ainda nao ativado).

    dt_vigencia_inicio    DATE      NOT NULL,
    -- Inicio da vigencia contratual.

    dt_vigencia_fim       DATE      CHECK(
                                        dt_vigencia_fim IS NULL OR
                                        dt_vigencia_fim >= dt_vigencia_inicio),
    -- Fim da vigencia. NULL = contrato por prazo indeterminado.

    status                TEXT      DEFAULT 'ativo'
                                    CHECK(status IN ('ativo','pendente','vencido','cancelado')),

    observacoes           TEXT,

    correlation_id        TEXT      UNIQUE NOT NULL,

    dt_criado_em          DATETIME  DEFAULT CURRENT_TIMESTAMP,
    dt_atualizado_em      DATETIME  DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (responsavel_id) REFERENCES moradores(id)
);


-- ============================================================================
-- PARTE 2: INDICES DE DESEMPENHO
-- ============================================================================
-- Indices aceleram buscas do banco de dados.
-- Sem indice = banco le TODAS as linhas (lento para tabelas grandes).
-- Com indice = banco pula direto para as linhas certas (log2(N) — muito rapido).

-- moradores — buscas frequentes por nome e CPF (UNIQUE ja tem indice automatico)
CREATE INDEX idx_moradores_nome        ON moradores(nome);
CREATE INDEX idx_moradores_ativo       ON moradores(ativo);

-- residencias — buscas por condominio e numero
CREATE INDEX idx_residencias_cond      ON residencias(codigo_condominio);
CREATE INDEX idx_residencias_num       ON residencias(numero_residencia);

-- morador_residencia — JOINs frequentes por morador ou por residencia
CREATE INDEX idx_mr_morador            ON morador_residencia(morador_id);
CREATE INDEX idx_mr_residencia         ON morador_residencia(residencia_id);
CREATE INDEX idx_mr_ativo              ON morador_residencia(ativo);

-- visitantes — busca por documento (nao tem UNIQUE, precisa de indice)
CREATE INDEX idx_visitantes_documento  ON visitantes(documento);
CREATE INDEX idx_visitantes_bloqueado  ON visitantes(bloqueado);

-- funcionarios — busca por cargo e setor
CREATE INDEX idx_funcionarios_cargo    ON funcionarios(cargo);

-- veiculos — FKs sao campos frequentes em JOIN
CREATE INDEX idx_veiculos_morador      ON veiculos(morador_id);

-- acessos — campo mais consultado: data/hora de entrada (relatorios)
CREATE INDEX idx_acessos_entrada       ON acessos(dt_entrada_em);
CREATE INDEX idx_acessos_visitante     ON acessos(visitante_id);
CREATE INDEX idx_acessos_morador       ON acessos(morador_id);
CREATE INDEX idx_acessos_funcionario   ON acessos(funcionario_id);
CREATE INDEX idx_acessos_veiculo       ON acessos(veiculo_id);

-- correlation_id — busca por hash para sync com nuvem
CREATE INDEX idx_cor_moradores         ON moradores(correlation_id);
CREATE INDEX idx_cor_residencias       ON residencias(correlation_id);
CREATE INDEX idx_cor_visitantes        ON visitantes(correlation_id);
CREATE INDEX idx_cor_funcionarios      ON funcionarios(correlation_id);
CREATE INDEX idx_cor_veiculos          ON veiculos(correlation_id);
CREATE INDEX idx_cor_acessos           ON acessos(correlation_id);

-- assinatura_condominio — status e vigencia (ja tem UNIQUE em codigo_condominio)
CREATE INDEX idx_assinatura_status     ON assinatura_condominio(status);
CREATE INDEX idx_assinatura_vig_fim    ON assinatura_condominio(dt_vigencia_fim);


-- ============================================================================
-- PARTE 3: DADOS DE EXEMPLO
-- ============================================================================
-- INSERT INTO = "inserir dentro da tabela"
-- correlation_id: hash SHA-256 gerado no Python:
--   import hashlib
--   cid = hashlib.sha256(f'moradores:{cpf}'.encode()).hexdigest()
-- ============================================================================

-- ──────────────────────────────────────────────
-- 3.1 — Moradores
-- ──────────────────────────────────────────────
--
-- MUDANCA v8.0: sem numero_residencia, bloco, andar, tipo_morador.
-- Esses dados estao em 'residencias' e 'morador_residencia'.

-- Moradores (10 registros — dados pessoais sem residencia)
-- correlation_id = SHA-256 de 'moradores:{cpf}'

-- Morador 1: Joao Carlos da Silva
INSERT INTO moradores (nome, cpf, telefone, email, ativo, termos_lgpd, dt_aceite_lgpd, correlation_id)
VALUES (
    'Joao Carlos da Silva',
    '11122233344',
    '83999001122',
    'joao.silva@email.com',
    1,
    NULL,      -- BLOB: NULL no exemplo (em producao: bytes do PDF dos termos)
    '2026-04-09 10:00:00',
    '72104cb9e6cf2f1ac722a5513d1145b32a94fdc216e2ff09c991f88e5e343e8a'
);
-- Morador 2: Maria Aparecida Santos
INSERT INTO moradores (nome, cpf, telefone, email, ativo, termos_lgpd, dt_aceite_lgpd, correlation_id)
VALUES (
    'Maria Aparecida Santos',
    '55566677788',
    '83988112233',
    'maria.santos@email.com',
    1,
    NULL,      -- BLOB: NULL no exemplo (em producao: bytes do PDF dos termos)
    '2026-04-09 10:00:00',
    'acec16f37ddd60d6ab79d892a5e2b6d8c5fed2e7c7d23a28eebc9fc84205f8bb'
);
-- Morador 3: Pedro Henrique Oliveira
INSERT INTO moradores (nome, cpf, telefone, email, ativo, termos_lgpd, dt_aceite_lgpd, correlation_id)
VALUES (
    'Pedro Henrique Oliveira',
    '99988877766',
    '83977223344',
    'pedro.oliveira@email.com',
    1,
    NULL,      -- BLOB: NULL no exemplo (em producao: bytes do PDF dos termos)
    NULL,
    '16b60edc33103400e13f71c96d9b69d2c70c1592938e42586e68f2dc1eddba49'
);
-- Morador 4: Ana Paula Ferreira
INSERT INTO moradores (nome, cpf, telefone, email, ativo, termos_lgpd, dt_aceite_lgpd, correlation_id)
VALUES (
    'Ana Paula Ferreira',
    '44433322211',
    '83966334455',
    'ana.ferreira@email.com',
    1,
    NULL,      -- BLOB: NULL no exemplo (em producao: bytes do PDF dos termos)
    '2026-04-09 10:00:00',
    '33d18f4959453b7f40ec89b81f289fcfbe9853c0b6ff55723696994f24470690'
);
-- Morador 5: Carlos Eduardo Lima
INSERT INTO moradores (nome, cpf, telefone, email, ativo, termos_lgpd, dt_aceite_lgpd, correlation_id)
VALUES (
    'Carlos Eduardo Lima',
    '77788899900',
    '83955445566',
    NULL,
    1,
    NULL,      -- BLOB: NULL no exemplo (em producao: bytes do PDF dos termos)
    NULL,
    'c65ef5d5e73cb4f14ccac8d2e158f28b7a12370964116e8229929095b91fbc37'
);
-- Morador 6: Lucia Fernandes Gomes
INSERT INTO moradores (nome, cpf, telefone, email, ativo, termos_lgpd, dt_aceite_lgpd, correlation_id)
VALUES (
    'Lucia Fernandes Gomes',
    '12312312300',
    '83922001133',
    'lucia.gomes@email.com',
    1,
    NULL,      -- BLOB: NULL no exemplo (em producao: bytes do PDF dos termos)
    '2026-04-09 10:00:00',
    'd34026bfb80b7750340269732c5f9df2311bd0f2e4345512d377e68c64d3b3ad'
);
-- Morador 7: Rafael Souza Mendes
INSERT INTO moradores (nome, cpf, telefone, email, ativo, termos_lgpd, dt_aceite_lgpd, correlation_id)
VALUES (
    'Rafael Souza Mendes',
    '45645645600',
    '83911009988',
    NULL,
    1,
    NULL,      -- BLOB: NULL no exemplo (em producao: bytes do PDF dos termos)
    NULL,
    'a7171fb127844865bf7ea8807e3ddcf7592ed5a0c9a3d36759d5469ce5358be0'
);
-- Morador 8: Dona Teresa Albuquerque
INSERT INTO moradores (nome, cpf, telefone, email, ativo, termos_lgpd, dt_aceite_lgpd, correlation_id)
VALUES (
    'Dona Teresa Albuquerque',
    '78978978700',
    '83900112233',
    'teresa.albuquerque@email.com',
    1,
    NULL,      -- BLOB: NULL no exemplo (em producao: bytes do PDF dos termos)
    '2026-04-09 10:00:00',
    '302d4921ec2a44f2638ae243de0d9bf18953658719d3fe6d74d3dc30df923f6b'
);
-- Morador 9: Bruno Martins Costa
INSERT INTO moradores (nome, cpf, telefone, email, ativo, termos_lgpd, dt_aceite_lgpd, correlation_id)
VALUES (
    'Bruno Martins Costa',
    '14725836900',
    '83988776655',
    'bruno.martins@email.com',
    1,
    NULL,      -- BLOB: NULL no exemplo (em producao: bytes do PDF dos termos)
    NULL,
    '0bc2e0e60c01f6c0f042f1ffced27dfdaa9a37a100d3bd942b03832d45e1594e'
);
-- Morador 10: Sergio Ramos Pereira
INSERT INTO moradores (nome, cpf, telefone, email, ativo, termos_lgpd, dt_aceite_lgpd, correlation_id)
VALUES (
    'Sergio Ramos Pereira',
    '96385274100',
    '83977665544',
    'sergio.ramos@email.com',
    0,
    NULL,      -- BLOB: NULL no exemplo (em producao: bytes do PDF dos termos)
    NULL,
    '9607837e767aaf6dd26683a4f4a4729c9828d6646157c9d0cd513218aef2d64a'
);

-- Sergio (id=10) e um ex-morador desativado. ativo=0 = soft delete.
-- O registro PERMANECE no banco — historico preservado.

-- Atualizando fotos e biometrias dos moradores que as possuem:
UPDATE moradores SET foto = NULL, dt_foto_validade = '2028-04-09',
    biometria = NULL, dt_biometria_validade = '2028-04-09'
    WHERE cpf = '11122233344';  -- Joao (foto + biometria)
UPDATE moradores SET foto = NULL, dt_foto_validade = '2028-04-09'
    WHERE cpf = '55566677788';  -- Maria (so foto)
UPDATE moradores SET foto = NULL, dt_foto_validade = '2028-04-09',
    biometria = NULL, dt_biometria_validade = '2028-04-09'
    WHERE cpf = '44433322211';  -- Ana Paula
UPDATE moradores SET biometria = NULL, dt_biometria_validade = '2028-04-09'
    WHERE cpf = '12312312300';  -- Lucia (so biometria)
UPDATE moradores SET foto = NULL, dt_foto_validade = '2028-04-09',
    biometria = NULL, dt_biometria_validade = '2028-04-09'
    WHERE cpf = '78978978700';  -- Dona Teresa
UPDATE moradores SET foto = NULL, dt_foto_validade = '2025-03-15'
    WHERE cpf = '14725836900';  -- Bruno (FOTO VENCIDA!)
-- Bruno: foto venceu em mar/2025 — a consulta de fotos vencidas vai encontra-lo!


-- ──────────────────────────────────────────────
-- 3.2 — Residencias (unidades habitacionais)
-- ──────────────────────────────────────────────
--
-- Tipos de condominio cobertos:
--   [V] VERTICAL   — bloco + andar + numero_residencia
--   [H] HORIZONTAL — quadra + numero_residencia
--   [S] SIMPLES    — so andar + numero_residencia (predinho unico)

-- [V] Joao, Bloco A 1o andar
INSERT INTO residencias (codigo_condominio, numero_residencia, bloco, quadra, andar, tipo_moradia, interfone, observacao, correlation_id)
VALUES ('COND-001', '101', 'A', NULL, 1, 'apartamento', '101', NULL, '1ccd150e2b552bc7bb71a6bec19ff9110ce1a8a76cf0a1a81db6eaad16685b08');
-- [V] Maria, Bloco A 2o andar
INSERT INTO residencias (codigo_condominio, numero_residencia, bloco, quadra, andar, tipo_moradia, interfone, observacao, correlation_id)
VALUES ('COND-001', '202', 'A', NULL, 2, 'apartamento', '202', NULL, 'f7e5a6c9f4e8156d0de4d6fdbe5a73d776ef5dfa76b62258fbc8d2a86f2782bc');
-- [V] Pedro, Bloco B 3o andar
INSERT INTO residencias (codigo_condominio, numero_residencia, bloco, quadra, andar, tipo_moradia, interfone, observacao, correlation_id)
VALUES ('COND-001', '303', 'B', NULL, 3, 'apartamento', '303', NULL, '2f9251ab6a5c4338f485b4ac1e01e4ae7a811454b54ab5d999519c0f10ca24ab');
-- [V] Ana Paula, Bloco A 1o andar
INSERT INTO residencias (codigo_condominio, numero_residencia, bloco, quadra, andar, tipo_moradia, interfone, observacao, correlation_id)
VALUES ('COND-001', '104', 'A', NULL, 1, 'apartamento', '104', NULL, 'f132abc2f047e8f15468d8f9dbcce0973edfa50544aa4555addb37e79a6e5a1a');
-- [V] Carlos, Bloco C 5o andar
INSERT INTO residencias (codigo_condominio, numero_residencia, bloco, quadra, andar, tipo_moradia, interfone, observacao, correlation_id)
VALUES ('COND-001', '501', 'C', NULL, 5, 'apartamento', '501', NULL, '826ae84e9c67b31c5a1bd069ea68bf5089dec85286e0b63253bd1ed3a48fee92');
-- [V] Lucia, Bloco A 1o andar
INSERT INTO residencias (codigo_condominio, numero_residencia, bloco, quadra, andar, tipo_moradia, interfone, observacao, correlation_id)
VALUES ('COND-001', '102', 'A', NULL, 1, 'apartamento', '102', NULL, '1d362ac2452307e641e0e1aaa50783160346042b7af3ca948905e71d3f4dead5');
-- [H] Rafael, Quadra 03 Lote 08
INSERT INTO residencias (codigo_condominio, numero_residencia, bloco, quadra, andar, tipo_moradia, interfone, observacao, correlation_id)
VALUES ('COND-001', '08', NULL, '03', NULL, 'casa', NULL, 'Lote 08 da Quadra 03', '3cb2c94dddc8eca081e06b962525ffdb72bb8f30582dcc64b077f48b8ff8997d');
-- [H] Dona Teresa, Quadra 07 Lote 14
INSERT INTO residencias (codigo_condominio, numero_residencia, bloco, quadra, andar, tipo_moradia, interfone, observacao, correlation_id)
VALUES ('COND-001', '14', NULL, '07', NULL, 'casa', NULL, 'Lote 14 da Quadra 07', '639310841f7f3c153c7f2d2d7733e5b83af825c8ee2fc440468132d1e5649f08');
-- [S] Bruno, 3o andar sem bloco
INSERT INTO residencias (codigo_condominio, numero_residencia, bloco, quadra, andar, tipo_moradia, interfone, observacao, correlation_id)
VALUES ('COND-001', '301', NULL, NULL, 3, 'apartamento', '301', 'Predinho sem bloco', '99814f834cc117b151dcc7d9c0cf5de717730bcc93c7b3782f82793e94e098f6');
-- [V] Sergio, Bloco B 4o andar
INSERT INTO residencias (codigo_condominio, numero_residencia, bloco, quadra, andar, tipo_moradia, interfone, observacao, correlation_id)
VALUES ('COND-001', '402', 'B', NULL, 4, 'apartamento', '402', NULL, '921dfc608b24288ec61a9459b0090030708a5725f116a2d9b679121316b77b7e');


-- ──────────────────────────────────────────────
-- 3.3 — morador_residencia (quem mora onde)
-- ──────────────────────────────────────────────
--
-- ANA PAULA (id=4) DEMO DE N:N:
-- Ela e proprietaria de 2 apartamentos — 104 (dela) e 101 (herdou).
-- O 101 tambem pertence ao Joao (id=1), demonstrando que uma unidade
-- pode ter mais de um proprietario (condominio, herdeiros, etc.).

-- Joao → Apto 101
INSERT INTO morador_residencia (morador_id, residencia_id, tipo_morador, dt_inicio, dt_fim, correlation_id)
VALUES (1, 1, 'proprietario', '2024-01-10', NULL, 'e2fa727090a47afdcad043747f94d378b6e5865fed0291e72e417a7cddd63076');
-- Maria → Apto 202
INSERT INTO morador_residencia (morador_id, residencia_id, tipo_morador, dt_inicio, dt_fim, correlation_id)
VALUES (2, 2, 'inquilino', '2025-06-01', NULL, 'd89c2b30b2ebd21654705b470d34ee61a829fbaf34ab464e21e5f61e0bbbff65');
-- Pedro → Apto 303
INSERT INTO morador_residencia (morador_id, residencia_id, tipo_morador, dt_inicio, dt_fim, correlation_id)
VALUES (3, 3, 'proprietario', '2020-03-01', NULL, '2f78470e823125ec48c0efa7c236e06343889f11ed0d0c17b3ab42039fc6d6e3');
-- Ana Paula → Apto 104
INSERT INTO morador_residencia (morador_id, residencia_id, tipo_morador, dt_inicio, dt_fim, correlation_id)
VALUES (4, 4, 'proprietario', '2023-03-15', NULL, '55bb9b3615a4ff69272decbaf4789c5ee904d6c6d502c98282dea2196dd3eb90');
-- Ana Paula → Apto 101 (co-proprietaria)
INSERT INTO morador_residencia (morador_id, residencia_id, tipo_morador, dt_inicio, dt_fim, correlation_id)
VALUES (4, 1, 'proprietario', '2023-03-15', NULL, '5ac08b755649dcc7553b83815f556035832125d27cc1881afb0dfb6027ded2f0');
-- Carlos → Apto 501
INSERT INTO morador_residencia (morador_id, residencia_id, tipo_morador, dt_inicio, dt_fim, correlation_id)
VALUES (5, 5, 'inquilino', '2024-01-01', NULL, 'a438b5a0d51a66dd3e83bc0c395b6dfe0ec47d25e5d29c6b5182df490cff0ac9');
-- Lucia → Apto 102
INSERT INTO morador_residencia (morador_id, residencia_id, tipo_morador, dt_inicio, dt_fim, correlation_id)
VALUES (6, 6, 'proprietario', '2019-07-01', NULL, '1eb61a8d188a66874d4d50c07e5b69183f8fe9619a995c22b51f1caa11fd85da');
-- Rafael → Lote 08 Quadra 03
INSERT INTO morador_residencia (morador_id, residencia_id, tipo_morador, dt_inicio, dt_fim, correlation_id)
VALUES (7, 7, 'inquilino', '2022-01-15', NULL, '8405f971c1b79ece97e6e88d5fe2189d0adf83b6d29e0852f5bea905a273773f');
-- Dona Teresa → Lote 14 Quadra 07
INSERT INTO morador_residencia (morador_id, residencia_id, tipo_morador, dt_inicio, dt_fim, correlation_id)
VALUES (8, 8, 'proprietario', '2015-05-20', NULL, '96a31d2a2fefc87023b794eecab354a99acc6c6a63568623befed1e10b8e2d49');
-- Bruno → Apto 301
INSERT INTO morador_residencia (morador_id, residencia_id, tipo_morador, dt_inicio, dt_fim, correlation_id)
VALUES (9, 9, 'inquilino', '2023-08-01', NULL, '2c89679220a21413f72b162d1eb92863595b98023c15210e811f734f57d0ee5c');
-- Sergio → Apto 402 (desativado)
INSERT INTO morador_residencia (morador_id, residencia_id, tipo_morador, dt_inicio, dt_fim, correlation_id)
VALUES (10, 10, 'proprietario', '2018-02-01', NULL, '64d312cb302fe239bf564dee91d13fd2439761b612725d5bdddd7007c1fe1a6c');


-- ──────────────────────────────────────────────
-- 3.4 — Config de seguranca por morador
-- ──────────────────────────────────────────────

-- Joao (id=1): 2 fatores — digital + facial (maximo de seguranca)
INSERT INTO config_acesso_morador (morador_id, fatores_requeridos, permite_senha, permite_digital, permite_facial, correlation_id)
VALUES (1, 2, 0, 1, 1, '7914898478adf525bea855df16a9e21de09414e23ce6427055e58a2e86ffe469');
-- Joao desabilitou senha — so biometria. Exige 2 fatores simultaneos.

-- Maria (id=2): 1 fator — senha ou digital (sem camera facial)
INSERT INTO config_acesso_morador (morador_id, fatores_requeridos, permite_senha, permite_digital, permite_facial, correlation_id)
VALUES (2, 1, 1, 1, 0, '567b4719ccd83efc64aff16183c623c2bcf6fc23d7913028d97c793dee84b468');

-- Ana (id=4): 2 fatores — senha + digital (sem facial)
INSERT INTO config_acesso_morador (morador_id, fatores_requeridos, permite_senha, permite_digital, permite_facial, correlation_id)
VALUES (4, 2, 1, 1, 0, '38a70f6ccfeb329e09f4ba260c405c7dba364102fbc50550cfce0c7b35db48e6');

-- Lucia (id=6): 1 fator — so digital (sem senha)
INSERT INTO config_acesso_morador (morador_id, fatores_requeridos, permite_senha, permite_digital, permite_facial, correlation_id)
VALUES (6, 1, 0, 1, 0, '72e2a5065a1d5925210cb88d22901a47079fa6313e68f1ae26bd5670a040b344');

-- Dona Teresa (id=8): 2 fatores — digital + facial
INSERT INTO config_acesso_morador (morador_id, fatores_requeridos, permite_senha, permite_digital, permite_facial, correlation_id)
VALUES (8, 2, 0, 1, 1, 'cc9aa65e2281a5d90bb3321d46c21ffebdaab2cbfc08ab83ba73ca1160797c2b');
-- Moradores 3, 5, 7, 9, 10 sem config → sistema usa padrao do condominio.


-- ──────────────────────────────────────────────
-- 3.5 — Assinatura do condominio (1 registro!)
-- ──────────────────────────────────────────────
--
-- MUDANCA v8.0: Antes havia N contratos (um por morador).
-- Agora ha 1 linha por condominio = assinatura do SERVICO n7-portaria-ai.
-- UNIQUE(codigo_condominio) impede duplicatas no banco.
--
-- 'responsavel_id' sera atualizado para apontar para o sindico
-- apos o INSERT dos moradores (similar ao padrao de FK circular anterior).

INSERT INTO assinatura_condominio (
    codigo_condominio, nome_condominio, endereco,
    responsavel_id, numero_contrato, contrato,
    dt_ativacao, dt_vigencia_inicio, dt_vigencia_fim,
    status, observacoes, correlation_id
)
VALUES (
    'COND-001',
    'Residencial Parque das Flores',
    'Rua das Palmeiras, 100, Jardim Botanico, Joao Pessoa - PB, CEP 58000-000',
    NULL,              -- sera atualizado para o id da sindica (Claudia)
    '2026/0001-N7',    -- numero do contrato com a Neural Tech (n7)
    NULL,              -- BLOB: NULL no exemplo (em producao: bytes do PDF)
    '2026-04-09',      -- data de ativacao do sistema
    '2026-04-09',      -- inicio da vigencia
    NULL,              -- vigencia indeterminada (contrato de servico SaaS)
    'ativo',
    'Assinatura inicial do sistema n7-portaria-ai para este condominio',
    'b56eecd6260a748dce8f10f79c8aaa842d747df24febaff8898524403493fb61'
);
-- A sindica (Claudia Regina, funcionaria id=3) vai ser referenciada
-- via UPDATE apos o INSERT dos funcionarios.
-- NOTA: responsavel_id aponta para moradores.id, nao funcionarios.id.
-- Se a sindica tambem e moradora, adicionar ela como moradora e atualizar aqui.


-- ──────────────────────────────────────────────
-- 3.6 — Visitantes (8 registros)
-- ──────────────────────────────────────────────

-- Roberto: amigo do Joao — visita avulsa (sem restricao de periodo)
INSERT INTO visitantes (nome, documento, tipo_documento, telefone, correlation_id)
VALUES ('Roberto Almeida', '1234567', 'RG', '83911112222', 'd360fb29c4b740ce5b14d469aa8e3a14046613ca036dd68109801f458eef1546');

-- Fernanda: amiga da Maria — visita avulsa
INSERT INTO visitantes (nome, documento, tipo_documento, telefone, correlation_id)
VALUES ('Fernanda Costa', '98765432101', 'CNH', '83933334444', '2756d6698f27a08436d28a30b331edffc8094bb2d9be424481dd2094c24c916c');

-- Marcos Delivery: entregador recorrente
INSERT INTO visitantes (nome, documento, tipo_documento, telefone, correlation_id)
VALUES ('Marcos Delivery Pizza', '7654321', 'RG', '83955556666', '35167da0662e1e665997b3b5d2716a7dd5e4867aca241c17cc9851b07d8e2c33');

-- Jose Suspeito: BLOQUEADO — tentativa de acesso nao autorizado
INSERT INTO visitantes (nome, documento, tipo_documento, bloqueado, motivo_bloqueio, correlation_id)
VALUES ('Jose Suspeito', '0000000', 'RG', 1,
        'Tentativa de acesso nao autorizado em 01/04/2026', '4cccf53242e8b9d552f85b4fd9fc042874bd8d4e277cb31eda76a4f4fb55b305');

-- Jean Pierre: tecnico estrangeiro — autorizado apenas durante obras (10/04 a 30/04)
INSERT INTO visitantes (nome, documento, tipo_documento, telefone,
                        dt_validade_inicio, dt_validade_fim, correlation_id)
VALUES ('Jean Pierre Dubois', 'FR12345678', 'PASSAPORTE', '83900998877',
        '2026-04-10', '2026-04-30', '8e5715b82bfe3bf182c6961f229103bcb564e61ff8af25a42185f410e4ed4eb8');

-- Camila: sobrinha da Lucia — morando temporariamente (mai a jul/2026)
INSERT INTO visitantes (nome, documento, tipo_documento, telefone,
                        dt_validade_inicio, dt_validade_fim, correlation_id)
VALUES ('Camila Rodrigues', '55544433322', 'CNH', '83944223311',
        '2026-05-01', '2026-07-31', 'a34e5818f646f09aecfa6ab44fb48a1bcaa04e5eb492cd1fa8f0324f5d21f041');

-- Sandra: irma do Pedro — acesso permanente a partir de abr/2026
INSERT INTO visitantes (nome, documento, tipo_documento, telefone,
                        dt_validade_inicio, correlation_id)
VALUES ('Sandra Oliveira', '3216549', 'RG', '83966778899',
        '2026-04-09', '3a9849432fc688c6abfcd27d87027896ca130a32d88ba05606a52f359b0121e6');

-- Ricardo: BLOQUEADO — comportamento inadequado
INSERT INTO visitantes (nome, documento, tipo_documento, bloqueado, motivo_bloqueio, correlation_id)
VALUES ('Ricardo Problema', '1111111', 'RG', 1,
        'Comportamento agressivo com porteiro em 28/03/2026', '8ddfcbd949ce5cfb72b7b33bb036bd6c0e9cbd3b72ce326845f115e86df79e24');


-- ──────────────────────────────────────────────
-- 3.7 — Funcionarios (5 registros)
-- ──────────────────────────────────────────────
-- senha_hash: SHA-256 de string vazia '' — usar senha real em producao!

INSERT INTO funcionarios (nome, cpf, cargo, setor, login, senha_hash, correlation_id)
VALUES ('Jose Silva Santos', '10120230340', 'porteiro', 'portaria', 'porteiro.silva',
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '3512b07f74959acbc82083dd5ad4ea7a9d0e293657a12aea779e1b0ee669a1d1');

INSERT INTO funcionarios (nome, cpf, cargo, setor, login, senha_hash, correlation_id)
VALUES ('Marcos Pereira Lima', '20230340450', 'porteiro', 'portaria', 'porteiro.marcos',
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '0950793ef7057529925913bf35327653887776ac4deccd0ae0324e9d2f9bf511');

INSERT INTO funcionarios (nome, cpf, cargo, setor, login, senha_hash, correlation_id)
VALUES ('Claudia Regina Borges', '30340450560', 'administrador', 'administracao', 'admin.claudia',
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'd0a8c15332ea1a0cf3a96e6cf6c59b8b30c791afb13826029315178d027db5b5');

INSERT INTO funcionarios (nome, cpf, cargo, setor, login, senha_hash, correlation_id)
VALUES ('Fatima Souza Andrade', '40450560670', 'outro', 'limpeza', 'limpeza.fatima',
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '6cb3dd614b4225c71bde78364cb46342a76820bd150ca7cff218b9c311d3841b');

INSERT INTO funcionarios (nome, cpf, cargo, setor, login, senha_hash, correlation_id)
VALUES ('Paulo Oliveira Neto', '50560670780', 'zelador', 'manutencao', 'zelador.paulo',
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '679f4960f88cbb170c2c6cc18653dd8203684d50ba3eda0ad2a82de474957df4');


-- ──────────────────────────────────────────────
-- 3.8 — Veiculos (5 registros)
-- ──────────────────────────────────────────────

INSERT INTO veiculos (placa, modelo, cor, morador_id, correlation_id)
VALUES ('ABC-1234', 'Honda Civic', 'Prata', 1, '69f472ffd51e61a0f489498fc339c9d299d90b9f268855a0b4431e4fcc484346');

INSERT INTO veiculos (placa, modelo, cor, morador_id, correlation_id)
VALUES ('DEF-5678', 'Fiat Pulse', 'Branco', 4, '0b2f8b037a2b1e18d722e27bef0fac999c51a92c4a451b93f54aa71492465c4e');

INSERT INTO veiculos (placa, modelo, cor, morador_id, correlation_id)
VALUES ('GHI-9012', 'Toyota Corolla', 'Preto', 8, 'bce468b6569f90ae6a1de439c8316554cf524d1f12f3e5caf7f49dec4921c14b');

INSERT INTO veiculos (placa, modelo, cor, funcionario_id, correlation_id)
VALUES ('JKL-3456', 'Moto Honda CG', 'Vermelha', 2, '334f1c4e400e74b3b6fa2571981c4fe28b409b09a44af724e4d9a9dbf66b3f5c');

INSERT INTO veiculos (placa, modelo, cor, visitante_id, correlation_id)
VALUES ('QRS-5678', 'VW Polo', 'Cinza', 2, 'bbfeb3ba1b9a3a309c5afc21a2e3303258b46e6472367537262797de7faedfa1');


-- ──────────────────────────────────────────────
-- 3.9 — Registros de acesso (10 registros)
-- ──────────────────────────────────────────────

INSERT INTO acessos (visitante_id, morador_id, funcionario_id, tipo_acesso, auth_senha, auth_digital, auth_facial, motivo, dt_entrada_em, dt_saida_em, porteiro, observacoes, correlation_id)
VALUES (1, 1, 1, 'pedestre', 0, 1, 0, 'Visita familiar', '2026-04-08 14:00:00', '2026-04-08 17:30:00', 'Porteiro Silva', 'Tio do morador', '5a47affa6f1366945900e72987634b19331ad301b904ada6bcba20a4c1e24e45');

INSERT INTO acessos (visitante_id, morador_id, funcionario_id, veiculo_id, tipo_acesso, auth_senha, auth_digital, auth_facial, motivo, dt_entrada_em, dt_saida_em, porteiro, correlation_id)
VALUES (2, 2, 1, 5, 'garagem', 0, 1, 1, 'Visita social', '2026-04-09 10:00:00', '2026-04-09 12:00:00', 'Porteiro Silva', '9b4dac4acd0b5a8736ec3f1e20033f7145c02c4c005760705fb49afd2e75cb4f');

INSERT INTO acessos (visitante_id, morador_id, funcionario_id, tipo_acesso, auth_senha, auth_digital, auth_facial, motivo, dt_entrada_em, dt_saida_em, porteiro, observacoes, correlation_id)
VALUES (3, 3, 2, 'pedestre', 1, 0, 0, 'Entrega - Pizza', '2026-04-09 19:45:00', '2026-04-09 19:52:00', 'Porteiro Marcos', 'Delivery de moto', '15d13f5672421e32bebf4f400df0a93b73c3c00440b721d09786d45a00e59ee5');

INSERT INTO acessos (visitante_id, morador_id, funcionario_id, tipo_acesso, auth_senha, auth_digital, auth_facial, motivo, porteiro, correlation_id)
VALUES (1, 4, 1, 'pedestre', 0, 1, 0, 'Manutencao do ar-condicionado', 'Porteiro Silva', 'ce1922f0c1c846498028c0f3503f64da67a1e70a5248c8843184b93d1955c808');
-- Roberto esta dentro agora — dt_saida_em = NULL

INSERT INTO acessos (visitante_id, morador_id, funcionario_id, tipo_acesso, auth_senha, auth_digital, auth_facial, motivo, dt_entrada_em, dt_saida_em, porteiro, correlation_id)
VALUES (5, 2, 2, 'pedestre', 1, 0, 0, 'Visita social - amiga', '2026-04-07 15:00:00', '2026-04-07 18:30:00', 'Porteiro Marcos', '34a4f87d0ec41ace7d168c5233ce7f7cf4dcd201a5e9cae47ad600a213aa634d');

INSERT INTO acessos (visitante_id, morador_id, funcionario_id, tipo_acesso, auth_senha, auth_digital, auth_facial, motivo, dt_entrada_em, dt_saida_em, porteiro, observacoes, correlation_id)
VALUES (6, 8, 1, 'pedestre', 1, 1, 0, 'Manutencao - Ar condicionado', '2026-04-08 09:00:00', '2026-04-08 11:45:00', 'Porteiro Silva', 'Tecnico autorizado', 'ab432261a712123cda4f57c7c1177ab393e9ab07c4482e7d1bda7408931244cd');

INSERT INTO acessos (visitante_id, morador_id, funcionario_id, tipo_acesso, auth_senha, auth_digital, auth_facial, motivo, dt_entrada_em, dt_saida_em, porteiro, correlation_id)
VALUES (7, 3, 2, 'pedestre', 0, 1, 0, 'Visita familiar - irma', '2026-04-06 10:00:00', '2026-04-06 13:00:00', 'Porteiro Marcos', '7a5370ca54a979745ee52be36df94ae72a6d115484010e525aacf28a24769a54');

INSERT INTO acessos (visitante_id, morador_id, funcionario_id, tipo_acesso, auth_senha, auth_digital, auth_facial, motivo, dt_entrada_em, dt_saida_em, porteiro, observacoes, correlation_id)
VALUES (7, 3, 1, 'pedestre', 0, 1, 0, 'Visita familiar - irma', '2026-04-09 16:00:00', '2026-04-09 20:00:00', 'Porteiro Silva', 'Trouxe bolo de aniversario', '2c687ce34224518bffee47db0034995073d4a1246bf89e633b97072ce36390b8');

INSERT INTO acessos (visitante_id, morador_id, funcionario_id, tipo_acesso, auth_senha, auth_digital, auth_facial, motivo, dt_entrada_em, dt_saida_em, porteiro, observacoes, correlation_id)
VALUES (3, 8, 2, 'pedestre', 1, 0, 0, 'Entrega - Restaurante Japones', '2026-04-09 12:30:00', '2026-04-09 12:38:00', 'Porteiro Marcos', 'Delivery de moto', '00de89a3b6947f1054e60d4785498310a48b18d9728cf9bae81765e70d34f98f');

INSERT INTO acessos (visitante_id, morador_id, funcionario_id, veiculo_id, tipo_acesso, auth_senha, auth_digital, auth_facial, motivo, porteiro, observacoes, correlation_id)
VALUES (2, 6, 1, 5, 'garagem', 0, 1, 1, 'Reuniao de condominio informal', 'Porteiro Silva', 'Veio de carro, placa QRS-5678', '6cd1121564ac10c292b20fecd66b646283ffcc68a14096fcc310564c74a26db7');
-- Fernanda esta dentro agora — dt_saida_em = NULL


-- ============================================================================
-- PARTE 4: CONSULTAS DE ESTUDO (SELECT)
-- ============================================================================
-- Configure a exibicao bonita no SQLite:
--   .mode column
--   .headers on
-- ============================================================================

-- ──────────────────────────────────────────────
-- 4.1 — CONSULTAS BASICAS
-- ──────────────────────────────────────────────

-- Listar todos os moradores ativos:
SELECT id, nome, cpf, telefone, ativo FROM moradores WHERE ativo = 1;

-- Contar moradores ativos:
SELECT COUNT(*) AS total_moradores_ativos FROM moradores WHERE ativo = 1;

-- Moradores sem aceite LGPD formalizado:
SELECT nome, cpf FROM moradores WHERE dt_aceite_lgpd IS NULL AND ativo = 1;


-- ──────────────────────────────────────────────
-- 4.2 — CONSULTAS COM RESIDENCIAS (JOIN N:N)
-- ──────────────────────────────────────────────

-- Listar morador + unidade (visao completa):
SELECT
    m.nome,
    r.numero_residencia,
    r.bloco,
    r.quadra,
    r.andar,
    r.tipo_moradia,
    mr.tipo_morador,
    r.codigo_condominio
FROM moradores m
    JOIN morador_residencia mr ON m.id = mr.morador_id
    JOIN residencias r         ON mr.residencia_id = r.id
WHERE m.ativo = 1 AND mr.ativo = 1
ORDER BY r.bloco, r.numero_residencia;

-- Moradores com MAIS DE UMA unidade (proprietarios multiplos):
SELECT
    m.nome,
    COUNT(mr.residencia_id) AS total_unidades
FROM moradores m
    JOIN morador_residencia mr ON m.id = mr.morador_id
WHERE m.ativo = 1 AND mr.ativo = 1
GROUP BY m.id
HAVING COUNT(mr.residencia_id) > 1
ORDER BY total_unidades DESC;

-- Todas as unidades do Bloco A:
SELECT
    r.numero_residencia,
    r.andar,
    m.nome,
    mr.tipo_morador
FROM residencias r
    JOIN morador_residencia mr ON r.id = mr.residencia_id
    JOIN moradores m           ON mr.morador_id = m.id
WHERE r.bloco = 'A' AND r.ativo = 1 AND mr.ativo = 1
ORDER BY r.andar, r.numero_residencia;

-- Proprietarios vs Inquilinos por tipo de moradia:
SELECT
    r.tipo_moradia,
    mr.tipo_morador,
    COUNT(*) AS quantidade
FROM morador_residencia mr
    JOIN residencias r ON mr.residencia_id = r.id
WHERE mr.ativo = 1
GROUP BY r.tipo_moradia, mr.tipo_morador;


-- ──────────────────────────────────────────────
-- 4.3 — CONSULTAS DE BIOMETRIA E FOTO
-- ──────────────────────────────────────────────

-- Moradores sem foto:
SELECT m.nome FROM moradores m WHERE m.foto IS NULL AND m.ativo = 1;

-- Moradores com foto ou biometria VENCIDA:
SELECT m.nome, m.dt_foto_validade, m.dt_biometria_validade
FROM moradores m
WHERE m.ativo = 1
  AND (m.dt_foto_validade < DATE('now') OR m.dt_biometria_validade < DATE('now'));


-- ──────────────────────────────────────────────
-- 4.4 — ACESSOS COM JOIN
-- ──────────────────────────────────────────────

-- Todos os acessos com nomes completos:
SELECT
    a.id            AS registro,
    v.nome          AS visitante,
    m.nome          AS morador_visitado,
    a.motivo,
    a.tipo_acesso,
    a.dt_entrada_em,
    a.dt_saida_em,
    a.porteiro
FROM acessos a
    JOIN visitantes v ON a.visitante_id = v.id
    JOIN moradores  m ON a.morador_id   = m.id
ORDER BY a.dt_entrada_em DESC;

-- Quem esta DENTRO agora? (saida = NULL)
SELECT v.nome AS visitante, m.nome AS morador, a.motivo, a.dt_entrada_em
FROM acessos a
    JOIN visitantes v ON a.visitante_id = v.id
    JOIN moradores  m ON a.morador_id   = m.id
WHERE a.dt_saida_em IS NULL;


-- ──────────────────────────────────────────────
-- 4.5 — VEICULOS E FUNCIONARIOS
-- ──────────────────────────────────────────────

-- Todos os veiculos com nome do proprietario:
SELECT
    v.placa, v.modelo, v.cor,
    CASE
        WHEN v.morador_id    IS NOT NULL THEN 'Morador: '     || m.nome
        WHEN v.funcionario_id IS NOT NULL THEN 'Funcionario: ' || f.nome
        WHEN v.visitante_id  IS NOT NULL THEN 'Visitante: '   || vis.nome
        ELSE 'Sem proprietario'
    END AS proprietario
FROM veiculos v
    LEFT JOIN moradores    m   ON v.morador_id     = m.id
    LEFT JOIN funcionarios f   ON v.funcionario_id  = f.id
    LEFT JOIN visitantes   vis ON v.visitante_id    = vis.id
WHERE v.ativo = 1;


-- ──────────────────────────────────────────────
-- 4.6 — ASSINATURA DO CONDOMINIO
-- ──────────────────────────────────────────────

-- Status da assinatura do condominio:
SELECT
    codigo_condominio,
    nome_condominio,
    numero_contrato,
    dt_ativacao,
    dt_vigencia_inicio,
    dt_vigencia_fim,
    status
FROM assinatura_condominio;

-- Quantos dias faltam para o contrato vencer? (NULL = sem prazo)
SELECT
    nome_condominio,
    status,
    CASE
        WHEN dt_vigencia_fim IS NULL THEN 'Prazo indeterminado'
        ELSE CAST(JULIANDAY(dt_vigencia_fim) - JULIANDAY(DATE('now')) AS INTEGER) || ' dias'
    END AS vigencia
FROM assinatura_condominio;


-- ──────────────────────────────────────────────
-- 4.7 — LGPD: CONFORMIDADE
-- ──────────────────────────────────────────────

-- Moradores com e sem aceite LGPD formalizado:
SELECT
    (SELECT COUNT(*) FROM moradores WHERE dt_aceite_lgpd IS NOT NULL AND ativo = 1) AS com_aceite,
    (SELECT COUNT(*) FROM moradores WHERE dt_aceite_lgpd IS NULL     AND ativo = 1) AS sem_aceite,
    (SELECT COUNT(*) FROM moradores WHERE termos_lgpd IS NOT NULL    AND ativo = 1) AS com_documento;

-- Listar moradores com aceite pendente (precisam assinar os termos):
SELECT nome, cpf, telefone, email
FROM moradores
WHERE dt_aceite_lgpd IS NULL AND ativo = 1
ORDER BY nome;


-- ──────────────────────────────────────────────
-- 4.8 — IDEMPOTENCIA COM CORRELATION_ID (v8.0)
-- ──────────────────────────────────────────────
--
-- O QUE E IDEMPOTENCIA?
-- Uma operacao e IDEMPOTENTE quando executar ela N vezes
-- tem o mesmo resultado de executar 1 vez.
--
-- POR QUE IMPORTA?
-- Em sincronizacao com nuvem (Local SQLite <-> Cloud DB), podem
-- ocorrer falhas de rede. O sistema precisa reenviar dados com
-- seguranca — sem criar duplicatas.
--
-- COMO FUNCIONA O CORRELATION_ID?
-- Antes de INSERT, geramos um hash SHA-256 dos dados unicos:
--
--   import hashlib
--   cid = hashlib.sha256(f'moradores:{cpf}'.encode()).hexdigest()
--
-- Este hash e DETERMINISTICO: o mesmo CPF sempre gera o mesmo hash.
-- Se o INSERT falhar e repetirmos, o banco rejeita silenciosamente
-- a duplicata (gracas ao UNIQUE no correlation_id).
--
-- PADRAO 1 — INSERT idempotente (ignora se ja existe):
--   INSERT OR IGNORE INTO moradores
--       (nome, cpf, ativo, correlation_id)
--   VALUES ('Joao Carlos', '11122233344', 1, 'hash-aqui');
--   → Se o hash ja existir: nao faz nada, nao gera erro.
--   → Se for novo: insere normalmente.
--
-- PADRAO 2 — UPSERT (atualiza se existir, insere se nao):
--   INSERT INTO moradores (nome, cpf, ativo, correlation_id)
--   VALUES ('Joao Carlos', '11122233344', 1, 'hash-aqui')
--   ON CONFLICT(correlation_id) DO UPDATE SET
--       nome             = excluded.nome,
--       dt_atualizado_em = CURRENT_TIMESTAMP;
--   → Se o hash ja existir: atualiza os dados.
--   → Se for novo: insere normalmente.
--
-- QUAL USAR?
-- INSERT OR IGNORE: para dados imutaveis (acessos historicos, logs).
-- UPSERT:           para dados mutaveis (moradores, visitantes).

-- Consultar moradores por correlation_id (busca por hash):
SELECT nome, cpf, correlation_id FROM moradores WHERE correlation_id LIKE '72%';

-- Verificar duplicatas (nunca deveria ter resultado — UNIQUE garante):
SELECT correlation_id, COUNT(*) AS contagem
FROM moradores
GROUP BY correlation_id
HAVING COUNT(*) > 1;


-- ============================================================================
-- PARTE 5: EXERCICIOS PARA PRATICAR
-- ============================================================================

-- EXERCICIO 1: Insira um novo morador chamado 'Luiza Barbosa',
--   CPF '22233344455', telefone '83944556677'.
--   Gere o correlation_id com: hashlib.sha256('moradores:22233344455'.encode()).hexdigest()
-- Sua resposta aqui:

-- RESPOSTA 1:
-- INSERT INTO moradores (nome, cpf, telefone, correlation_id)
-- VALUES ('Luiza Barbosa', '22233344455', '83944556677',
--         hashlib.sha256('moradores:22233344455'.encode()).hexdigest());
-- (Na pratica, substitua pela string hex do hash calculado no Python)


-- EXERCICIO 2: Adicione uma residencia para a Luiza (apartamento 401, Bloco B).
-- Dica: Primeiro INSERT em residencias, depois INSERT em morador_residencia.
-- Sua resposta aqui:

-- RESPOSTA 2:
-- INSERT INTO residencias (codigo_condominio, numero_residencia, bloco, andar, tipo_moradia, correlation_id)
-- VALUES ('COND-001', '401', 'B', 4, 'apartamento', '<hash>');
-- INSERT INTO morador_residencia (morador_id, residencia_id, tipo_morador, correlation_id)
-- VALUES (11, 11, 'inquilino', '<hash>');  -- id 11 porque tem 10 moradores


-- EXERCICIO 3: Registre a SAIDA do Roberto (acesso id=4, ainda dentro).
-- Dica: UPDATE acessos SET dt_saida_em = ... WHERE id = 4
-- Sua resposta aqui:

-- RESPOSTA 3:
-- UPDATE acessos SET dt_saida_em = '2026-04-09 16:00:00' WHERE id = 4;


-- EXERCICIO 4: Quais moradores tem fotos vencidas?
-- Dica: dt_foto_validade < DATE('now')
-- Sua resposta aqui:

-- RESPOSTA 4:
-- SELECT nome, dt_foto_validade FROM moradores
-- WHERE dt_foto_validade < DATE('now') AND ativo = 1;


-- EXERCICIO 5: Liste todos os proprietarios de mais de uma unidade.
-- Dica: JOIN morador_residencia + GROUP BY + HAVING COUNT > 1
-- Sua resposta aqui:

-- RESPOSTA 5:
-- SELECT m.nome, COUNT(mr.residencia_id) AS unidades
-- FROM moradores m JOIN morador_residencia mr ON m.id = mr.morador_id
-- WHERE mr.tipo_morador = 'proprietario' AND mr.ativo = 1
-- GROUP BY m.id HAVING COUNT(mr.residencia_id) > 1;


-- EXERCICIO 6 (DESAFIO): Quantos moradores de cada tipo (proprietario/inquilino)
-- existem no Bloco A?
-- Dica: JOIN moradores + morador_residencia + residencias WHERE bloco='A'
-- Sua resposta aqui:

-- RESPOSTA 6:
-- SELECT mr.tipo_morador, COUNT(*) AS total
-- FROM moradores m
--     JOIN morador_residencia mr ON m.id = mr.morador_id
--     JOIN residencias r ON mr.residencia_id = r.id
-- WHERE r.bloco = 'A' AND m.ativo = 1 AND mr.ativo = 1
-- GROUP BY mr.tipo_morador;


-- EXERCICIO 7 (DESAFIO LGPD): Qual porcentagem de moradores ativos
-- ainda nao formalizou o aceite dos termos LGPD?
-- Dica: SUM(CASE WHEN...) / COUNT(*) * 100.0
-- Sua resposta aqui:

-- RESPOSTA 7:
-- SELECT
--     COUNT(*) AS total,
--     SUM(CASE WHEN dt_aceite_lgpd IS NULL THEN 1 ELSE 0 END) AS sem_aceite,
--     ROUND(SUM(CASE WHEN dt_aceite_lgpd IS NULL THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1) AS pct_pendente
-- FROM moradores WHERE ativo = 1;


-- ============================================================================
-- GLOSSARIO RAPIDO
-- ============================================================================
-- PRIMARY KEY   — numero unico do registro (como RG — nunca repete)
-- AUTOINCREMENT — banco cria o numero sozinho (1, 2, 3...)
-- NOT NULL      — campo obrigatorio (nao pode ficar em branco)
-- UNIQUE        — nao pode repetir na tabela
-- DEFAULT       — valor automatico se nao informado
-- CHECK(...)    — regra de validacao — banco RECUSA dados invalidos
-- FOREIGN KEY   — chave estrangeira: link entre tabelas
-- BLOB          — dados binarios (foto, PDF, biometria, bytes de arquivo)
-- DATE          — apenas data: 'AAAA-MM-DD' (ex: '2026-04-09')
-- DATETIME      — data e hora: 'AAAA-MM-DD HH:MM:SS'
-- BOOLEAN       — verdadeiro/falso, armazenado como 0 ou 1 no SQLite
-- INDEX         — estrutura de busca rapida (como indice de livro)
-- LEFT JOIN     — retorna todos da tabela da esquerda, mesmo sem correspondencia
-- SHA-256       — funcao que transforma qualquer texto em hash de 64 hex chars
-- IDEMPOTENCIA  — operacao que pode ser repetida sem efeito colateral
-- CORRELATION_ID — hash usado como identificador global para sync entre bancos
-- LGPD          — Lei Geral de Protecao de Dados (Lei 13.709/2018)
-- SOFT DELETE   — desativar (ativo=0) em vez de deletar — preserva historico
-- ============================================================================
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 