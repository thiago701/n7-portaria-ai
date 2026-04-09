-- ============================================================================
-- PROJETO PORTARIA INTELIGENTE — BANCO DE DADOS COMPLETO (v1.0 - FINAL)
-- SQL SERVER COMPATIBLE VERSION
-- ============================================================================
-- Aluno: Ademilson
-- Aula 02 (Ampliada) — Banco de Dados + Estrutura Completa do Projeto
-- Data da Aula: 09/04/2026
--
-- CONVERSAO SQLITE -> SQL SERVER:
-- Este arquivo foi convertido da versao SQLite original para ser executado em SQL Server.
-- Todas as estruturas, dados e comentarios foram preservados.
--
-- COMO EXECUTAR:
--   No SQL Server Management Studio (SSMS):
--     1. Abra um novo Query Window
--     2. Cole o conteudo deste arquivo
--     3. Pressione F5 ou Ctrl+E para executar
--
--   Ou via sqlcmd:
--     sqlcmd -S servidor -U usuario -P senha -d database -i projeto_portaria_sqlserver.sql
-- ============================================================================


-- ============================================================================
-- LIMPEZA: DROP TABLE IF EXISTS na ordem correta (filhas antes das maes)
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

-- ============================================================================
-- PARTE 1: CRIACAO DAS TABELAS
-- ============================================================================

-- ======================================================================
--  TABELA 1: moradores
--  Dados PESSOAIS de cada morador (CPF, foto, biometria, LGPD).
--  Dados da UNIDADE estao em 'residencias'.
-- ======================================================================
CREATE TABLE moradores (
    id INT IDENTITY(1,1) PRIMARY KEY,

    nome                  NVARCHAR(255)      NOT NULL,
    -- Nome completo. Obrigatorio.

    cpf NVARCHAR(11)      UNIQUE NOT NULL
                                    CHECK(LEN(cpf) = 11),
    -- CPF sem pontos (11 digitos). UNIQUE = nao repete. NVARCHAR(255) = preserva zero inicial.

    telefone              NVARCHAR(255),
    email                 NVARCHAR(255)      CHECK(email LIKE '%@%.%'),
    dt_nascimento         DATE,

    foto                  VARBINARY(MAX),
    -- Bytes da foto (JPG/PNG). Em producao: open('foto.jpg','rb').read()

    dt_foto_validade      DATE,
    -- Renovar a cada 2 anos — pessoas mudam com o tempo!

    biometria             VARBINARY(MAX),
    -- Bytes do template biometrico (impressao digital).

    dt_biometria_validade DATE,
    -- Renovar a cada 2 anos.

    -- LGPD (Lei 13.709/2018) ---------------------------------------------------
    termos_lgpd           VARBINARY(MAX),
    -- Bytes do PDF dos Termos de Uso aceitos pelo morador.
    -- Guardamos o DOCUMENTO EXATO — evidencia juridica.

    dt_aceite_lgpd        DATETIME2,
    -- Timestamp do aceite. NULL = ainda nao formalizado.
    -- ---------------------------------------------------------------------------

    ativo                 BIT   DEFAULT 1
                                    CHECK(ativo IN (0, 1)),
    -- 1 = ativo. 0 = soft delete (dado preservado, morador "invisivel").

    correlation_id        NVARCHAR(255)      UNIQUE NOT NULL,
    -- SHA-256 de 'moradores:{cpf}'. Usado para sync sem duplicatas.

    dt_criado_em          DATETIME2 DEFAULT GETDATE(),
    dt_atualizado_em      DATETIME2 DEFAULT GETDATE()
);


-- ======================================================================
--  TABELA 2: residencias
--  Dados de cada UNIDADE HABITACIONAL do condominio.
--
--  >> CAMPOS DO ADEMILSON: tipo_moradia, interfone, observacao (v5.0)
-- ======================================================================
CREATE TABLE residencias (
    id INT IDENTITY(1,1) PRIMARY KEY,

    codigo_condominio     NVARCHAR(255)      NOT NULL,
    -- Codigo do condominio. Ex: 'COND-001'.

    numero_residencia     NVARCHAR(255)      NOT NULL,
    -- Numero da unidade: '101', '101-A', '08' (lote), 'Cobertura'.

    bloco                 NVARCHAR(255),
    -- Ex: 'A', 'B', 'Torre 1'. NULL em condominios horizontais (casas).

    quadra                NVARCHAR(255),
    -- Ex: '01', '05'. NULL em condominios verticais (predios).

    andar                 INT,
    -- Numero do andar. NULL em casas.

    -- >> SUGESTAO DO ADEMILSON (v5.0) -----------------------------------------
    tipo_moradia          NVARCHAR(255)      DEFAULT 'apartamento'
                                    CHECK(tipo_moradia IN ('apartamento','casa','comercial','outro')),
    -- Tipo fisico da unidade.
    -- SUGESTAO DO ADEMILSON: ele percebeu que o sistema precisa saber
    -- se e casa ou apartamento para o porteiro saber como chamar o morador!

    interfone             NVARCHAR(255),
    -- Codigo do interfone desta unidade. Ex: '101', '1-A'.
    -- SUGESTAO DO ADEMILSON: campo fundamental para a portaria chamar o morador!

    observacao            NVARCHAR(255),
    -- Observacoes sobre a unidade. Ex: 'Cobertura — acesso especial'.
    -- SUGESTAO DO ADEMILSON: anotacoes livres que o porteiro precisa ver.
    -- --------------------------------------------------------------------------

    ativo                 BIT   DEFAULT 1
                                    CHECK(ativo IN (0, 1)),

    correlation_id        NVARCHAR(255)      UNIQUE NOT NULL,

    dt_criado_em          DATETIME2 DEFAULT GETDATE(),
    dt_atualizado_em      DATETIME2 DEFAULT GETDATE()
);


-- ======================================================================
--  TABELA 3: morador_residencia (JUNCTION TABLE — relacao N:N)
--  Conecta moradores a residencias.
--
--  POR QUE EXISTE?
--  Um morador pode ser proprietario de varias unidades.
--  Uma unidade pode ter varios moradores (familia, herdeiros).
--  Isso e relacao MUITOS PARA MUITOS (N:N) — precisa de tabela intermediaria.
--
--  ANALOGIA: Em um hospital, 'consultas' conecta pacientes a medicos.
--  Aqui, 'morador_residencia' conecta moradores a residencias.
-- ======================================================================
CREATE TABLE morador_residencia (
    id INT IDENTITY(1,1) PRIMARY KEY,

    morador_id            INT   NOT NULL,
    residencia_id         INT   NOT NULL,

    tipo_morador          NVARCHAR(255)      DEFAULT 'proprietario'
                                    CHECK(tipo_morador IN ('proprietario', 'inquilino')),
    -- O mesmo morador pode ser proprietario de uma unidade e inquilino de outra!

    dt_inicio             DATE      NOT NULL DEFAULT (CAST(GETDATE() AS DATE)),
    dt_fim                DATE,
    -- NULL = ainda mora aqui.

    ativo                 BIT   DEFAULT 1
                                    CHECK(ativo IN (0, 1)),

    correlation_id        NVARCHAR(255)      UNIQUE NOT NULL,

    dt_criado_em          DATETIME2 DEFAULT GETDATE(),

    FOREIGN KEY (morador_id)    REFERENCES moradores(id),
    FOREIGN KEY (residencia_id) REFERENCES residencias(id),
    UNIQUE (morador_id, residencia_id, dt_inicio)
    -- Evita duplicata. Permite historico (mesmo morador pode sair e voltar).
);


-- ======================================================================
--  TABELA 4: visitantes
--  Pessoas que visitam o condominio.
-- ======================================================================
CREATE TABLE visitantes (
    id INT IDENTITY(1,1) PRIMARY KEY,

    nome                  NVARCHAR(255)      NOT NULL,
    documento             NVARCHAR(255)      NOT NULL,

    tipo_documento        NVARCHAR(255)      DEFAULT 'RG'
                                    CHECK(tipo_documento IN ('RG', 'CNH', 'PASSAPORTE', 'OUTRO')),

    telefone              NVARCHAR(255),

    foto                  VARBINARY(MAX),
    -- Foto do visitante. Util para reconhecimento facial futuro.

    bloqueado             BIT   DEFAULT 0
                                    CHECK(bloqueado IN (0, 1)),
    -- 1 = bloqueado — porta nao abre, porteiro e alertado.

    motivo_bloqueio       NVARCHAR(255),
    -- Se bloqueado = 1, por que? Registra o historico.

    dt_validade_inicio    DATE,
    -- A partir desta data o visitante pode entrar. NULL = sem restricao.

    dt_validade_fim       DATE      CHECK(
                                        dt_validade_fim IS NULL OR
                                        dt_validade_fim >= dt_validade_inicio),
    -- Ate esta data. NULL = sem prazo. CHECK evita datas invertidas.

    correlation_id        NVARCHAR(255)      UNIQUE NOT NULL,

    dt_criado_em          DATETIME2 DEFAULT GETDATE()
);


-- ======================================================================
--  TABELA 5: funcionarios
--  Porteiros, zeladores, administradores.
--
--  >> CONTRIBUICAO DO ADEMILSON (v3.0): ele identificou que o sistema
--     precisava saber QUEM registrou cada acesso — origem desta tabela!
-- ======================================================================
CREATE TABLE funcionarios (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nome                  NVARCHAR(255)      NOT NULL,
    cpf NVARCHAR(11)      UNIQUE NOT NULL  CHECK(LEN(cpf) = 11),
    cargo                 NVARCHAR(255)      DEFAULT 'porteiro'
                                    CHECK(cargo IN ('porteiro','zelador','administrador','outro')),
    setor                 NVARCHAR(255),
    -- Texto livre: 'portaria', 'administracao', 'limpeza', 'manutencao'

    login                 NVARCHAR(255)      UNIQUE NOT NULL,
    senha_hash            NVARCHAR(255)      NOT NULL  CHECK(LEN(senha_hash) = 64),
    -- SHA-256 da senha (64 hex chars). NUNCA armazenar senha em texto puro!
    -- Python: import hashlib; hashlib.sha256('senha'.encode()).hexdigest()

    ativo                 BIT   DEFAULT 1  CHECK(ativo IN (0, 1)),
    correlation_id        NVARCHAR(255)      UNIQUE NOT NULL,
    dt_criado_em          DATETIME2 DEFAULT GETDATE()
);


-- ======================================================================
--  TABELA 6: veiculos
--  Carros e motos de moradores, funcionarios e visitantes.
--
--  >> CONTRIBUICAO DO ADEMILSON (v3.0): ele sugeriu 'carro' e 'placa'
--     diretamente em moradores — o raciocinio estava certo!
--     Refinamos para uma tabela separada, que tambem serve funcionarios
--     e visitantes. Excelente instinto de modelagem!
-- ======================================================================
CREATE TABLE veiculos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    placa                 NVARCHAR(255)      UNIQUE NOT NULL  CHECK(LEN(placa) >= 7),
    -- Formato: 'ABC-1234' (antigo) ou 'ABC1D23' (Mercosul). Minimo 7 chars.

    modelo                NVARCHAR(255),
    cor                   NVARCHAR(255),

    morador_id            INT,
    funcionario_id        INT,
    visitante_id          INT,
    -- Apenas UM deve ser preenchido — os outros ficam NULL.

    ativo                 BIT   DEFAULT 1  CHECK(ativo IN (0, 1)),
    correlation_id        NVARCHAR(255)      UNIQUE NOT NULL,
    dt_criado_em          DATETIME2 DEFAULT GETDATE(),

    FOREIGN KEY (morador_id)      REFERENCES moradores(id),
    FOREIGN KEY (funcionario_id)  REFERENCES funcionarios(id),
    FOREIGN KEY (visitante_id)    REFERENCES visitantes(id)
);


-- ======================================================================
--  TABELA 7: acessos
--  Log de entradas e saidas. NUNCA deletar registros desta tabela!
--
--  FATORES DE AUTENTICACAO (2FA):
--    auth_senha   = porteiro liberou com senha manual
--    auth_digital = leitor biometrico confirmou digital
--    auth_facial  = camera reconheceu o rosto
--  Pelo menos 1 dos tres deve ser verdadeiro (CHECK garante isso).
-- ======================================================================
CREATE TABLE acessos (
    id INT IDENTITY(1,1) PRIMARY KEY,

    visitante_id          INT   NOT NULL,
    morador_id            INT,
    -- Morador visitado. NULL = servico geral sem morador especifico.

    funcionario_id        INT,
    -- Porteiro que registrou este acesso.

    veiculo_id            INT,
    -- Veiculo usado. NULL = veio a pe.

    tipo_acesso           NVARCHAR(255)      DEFAULT 'pedestre'
                                    CHECK(tipo_acesso IN ('pedestre', 'garagem')),
    -- 'pedestre' = portao principal
    -- 'garagem'  = cancela do estacionamento

    auth_senha            BIT   DEFAULT 0  CHECK(auth_senha IN (0,1)),
    auth_digital          BIT   DEFAULT 0  CHECK(auth_digital IN (0,1)),
    auth_facial           BIT   DEFAULT 0  CHECK(auth_facial IN (0,1)),

    motivo                NVARCHAR(255)      NOT NULL,
    dt_entrada_em         DATETIME2  NOT NULL  DEFAULT GETDATE(),
    dt_saida_em           DATETIME2,
    -- NULL = pessoa AINDA ESTA DENTRO do condominio.

    porteiro              NVARCHAR(255),
    -- Nome do porteiro em texto livre (compatibilidade).

    observacoes           NVARCHAR(255),
    correlation_id        NVARCHAR(255)      UNIQUE NOT NULL,

    CHECK(auth_senha + auth_digital + auth_facial >= 1),
    -- Nenhum acesso pode ser registrado sem autenticacao!

    FOREIGN KEY (visitante_id)   REFERENCES visitantes(id),
    FOREIGN KEY (morador_id)     REFERENCES moradores(id),
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id),
    FOREIGN KEY (veiculo_id)     REFERENCES veiculos(id)
);


-- ======================================================================
--  TABELA 8: config_acesso_morador
--  Politica de autenticacao individual por morador.
--  Quando ausente, o sistema aplica o padrao do condominio (1 fator).
-- ======================================================================
CREATE TABLE config_acesso_morador (
    id INT IDENTITY(1,1) PRIMARY KEY,
    morador_id            INTEGER   UNIQUE NOT NULL,
    -- UNIQUE: cada morador tem no maximo 1 config (relacao 1:1).

    fatores_requeridos    INT   DEFAULT 1  CHECK(fatores_requeridos IN (1, 2)),
    -- 1 = qualquer fator aceito
    -- 2 = dois fatores obrigatorios (ex: digital + facial)

    permite_senha         BIT   DEFAULT 1  CHECK(permite_senha IN (0, 1)),
    permite_digital       BIT   DEFAULT 1  CHECK(permite_digital IN (0, 1)),
    permite_facial        BIT   DEFAULT 0  CHECK(permite_facial IN (0, 1)),
    -- DEFAULT 0 para facial: exige hardware de camera especial.

    correlation_id        NVARCHAR(255)      UNIQUE NOT NULL,
    dt_criado_em          DATETIME2 DEFAULT GETDATE(),
    dt_atualizado_em      DATETIME2 DEFAULT GETDATE(),

    CHECK(permite_senha + permite_digital + permite_facial >= 1),
    -- Pelo menos 1 tipo de autenticacao deve estar habilitado.

    FOREIGN KEY (morador_id) REFERENCES moradores(id)
);


-- ======================================================================
--  TABELA 9: assinatura_condominio
--  Contrato do CONDOMINIO com o sistema n7-portaria-ai.
--  1 registro por condominio (UNIQUE codigo_condominio).
-- ======================================================================
CREATE TABLE assinatura_condominio (
    id INT IDENTITY(1,1) PRIMARY KEY,

    codigo_condominio     NVARCHAR(255)      UNIQUE NOT NULL,
    -- Codigo interno. UNIQUE = 1 assinatura por condominio. Ex: 'COND-001'

    nome_condominio       NVARCHAR(255)      NOT NULL,
    endereco              NVARCHAR(255),

    responsavel_id        INT,
    -- FK → moradores.id (sindico que assinou o contrato).

    numero_contrato       NVARCHAR(255)      UNIQUE NOT NULL,
    contrato              VARBINARY(MAX),
    -- Bytes do PDF do contrato assinado.

    dt_ativacao           DATE,
    dt_vigencia_inicio    DATE      NOT NULL,
    dt_vigencia_fim       DATE      CHECK(
                                        dt_vigencia_fim IS NULL OR
                                        dt_vigencia_fim >= dt_vigencia_inicio),

    status                NVARCHAR(255)      DEFAULT 'ativo'
                                    CHECK(status IN ('ativo','pendente','vencido','cancelado')),

    observacoes           NVARCHAR(255),
    correlation_id        NVARCHAR(255)      UNIQUE NOT NULL,
    dt_criado_em          DATETIME2 DEFAULT GETDATE(),
    dt_atualizado_em      DATETIME2 DEFAULT GETDATE(),

    FOREIGN KEY (responsavel_id) REFERENCES moradores(id)
);


-- ============================================================================
-- PARTE 2: INDICES DE DESEMPENHO
-- ============================================================================
-- Sem indice = banco le TODAS as linhas (lento).
-- Com indice = banco vai direto (log2 N — muito rapido).
-- PRIMARY KEY e UNIQUE ja criam indices automaticamente — nao precisam de CREATE INDEX.

CREATE INDEX idx_moradores_nome        ON moradores(nome);
CREATE INDEX idx_moradores_ativo       ON moradores(ativo);

CREATE INDEX idx_residencias_cond      ON residencias(codigo_condominio);
CREATE INDEX idx_residencias_num       ON residencias(numero_residencia);
CREATE INDEX idx_residencias_tipo      ON residencias(tipo_moradia);

CREATE INDEX idx_mr_morador            ON morador_residencia(morador_id);
CREATE INDEX idx_mr_residencia         ON morador_residencia(residencia_id);
CREATE INDEX idx_mr_ativo              ON morador_residencia(ativo);

CREATE INDEX idx_visitantes_documento  ON visitantes(documento);
CREATE INDEX idx_visitantes_bloqueado  ON visitantes(bloqueado);

CREATE INDEX idx_funcionarios_cargo    ON funcionarios(cargo);

CREATE INDEX idx_veiculos_morador      ON veiculos(morador_id);

CREATE INDEX idx_acessos_entrada       ON acessos(dt_entrada_em);
CREATE INDEX idx_acessos_visitante     ON acessos(visitante_id);
CREATE INDEX idx_acessos_morador       ON acessos(morador_id);
CREATE INDEX idx_acessos_funcionario   ON acessos(funcionario_id);
CREATE INDEX idx_acessos_veiculo       ON acessos(veiculo_id);

CREATE INDEX idx_assinatura_status     ON assinatura_condominio(status);
CREATE INDEX idx_assinatura_vig_fim    ON assinatura_condominio(dt_vigencia_fim);


-- ============================================================================
-- PARTE 3: DADOS DE EXEMPLO
-- ============================================================================

-- ──────────────────────────────────────────────
-- 3.1 — Moradores (10 registros)
-- ──────────────────────────────────────────────
-- correlation_id = SHA-256 de 'moradores:{cpf}' calculado no Python.
-- Em producao: hashlib.sha256(f'moradores:{cpf}'.encode()).hexdigest()

INSERT INTO moradores (nome, cpf, telefone, email, ativo, dt_aceite_lgpd, correlation_id)
VALUES ('Joao Carlos da Silva','11122233344','83999001122','joao.silva@email.com',1,'2026-04-09 10:00:00','72104cb9e6cf2f1ac722a5513d1145b32a94fdc216e2ff09c991f88e5e343e8a');

INSERT INTO moradores (nome, cpf, telefone, email, ativo, dt_aceite_lgpd, correlation_id)
VALUES ('Maria Aparecida Santos','55566677788','83988112233','maria.santos@email.com',1,'2026-04-09 10:00:00','acec16f37ddd60d6ab79d892a5e2b6d8c5fed2e7c7d23a28eebc9fc84205f8bb');

INSERT INTO moradores (nome, cpf, telefone, email, ativo, correlation_id)
VALUES ('Pedro Henrique Oliveira','99988877766','83977223344','pedro.oliveira@email.com',1,'16b60edc33103400e13f71c96d9b69d2c70c1592938e42586e68f2dc1eddba49');

INSERT INTO moradores (nome, cpf, telefone, email, ativo, dt_aceite_lgpd, correlation_id)
VALUES ('Ana Paula Ferreira','44433322211','83966334455','ana.ferreira@email.com',1,'2026-04-09 10:00:00','33d18f4959453b7f40ec89b81f289fcfbe9853c0b6ff55723696994f24470690');

INSERT INTO moradores (nome, cpf, telefone, ativo, correlation_id)
VALUES ('Carlos Eduardo Lima','77788899900','83955445566',1,'c65ef5d5e73cb4f14ccac8d2e158f28b7a12370964116e8229929095b91fbc37');

INSERT INTO moradores (nome, cpf, telefone, email, ativo, dt_aceite_lgpd, correlation_id)
VALUES ('Lucia Fernandes Gomes','12312312300','83922001133','lucia.gomes@email.com',1,'2026-04-09 10:00:00','d34026bfb80b7750340269732c5f9df2311bd0f2e4345512d377e68c64d3b3ad');

INSERT INTO moradores (nome, cpf, telefone, ativo, correlation_id)
VALUES ('Rafael Souza Mendes','45645645600','83911009988',1,'a7171fb127844865bf7ea8807e3ddcf7592ed5a0c9a3d36759d5469ce5358be0');

INSERT INTO moradores (nome, cpf, telefone, email, ativo, dt_aceite_lgpd, correlation_id)
VALUES ('Dona Teresa Albuquerque','78978978700','83900112233','teresa.albuquerque@email.com',1,'2026-04-09 10:00:00','302d4921ec2a44f2638ae243de0d9bf18953658719d3fe6d74d3dc30df923f6b');

INSERT INTO moradores (nome, cpf, telefone, email, ativo, correlation_id)
VALUES ('Bruno Martins Costa','14725836900','83988776655','bruno.martins@email.com',1,'0bc2e0e60c01f6c0f042f1ffced27dfdaa9a37a100d3bd942b03832d45e1594e');

INSERT INTO moradores (nome, cpf, telefone, email, ativo, correlation_id)
VALUES ('Sergio Ramos Pereira','96385274100','83977665544','sergio.ramos@email.com',0,'9607837e767aaf6dd26683a4f4a4729c9828d6646157c9d0cd513218aef2d64a');
-- Sergio: ativo=0 = soft delete (ex-morador que se mudou)

-- Atualizar fotos e biometrias dos moradores que as possuem:
UPDATE moradores SET foto=NULL, dt_foto_validade='2028-04-09', biometria=NULL, dt_biometria_validade='2028-04-09' WHERE cpf='11122233344';
UPDATE moradores SET foto=NULL, dt_foto_validade='2028-04-09' WHERE cpf='55566677788';
UPDATE moradores SET foto=NULL, dt_foto_validade='2028-04-09', biometria=NULL, dt_biometria_validade='2028-04-09' WHERE cpf='44433322211';
UPDATE moradores SET biometria=NULL, dt_biometria_validade='2028-04-09' WHERE cpf='12312312300';
UPDATE moradores SET foto=NULL, dt_foto_validade='2028-04-09', biometria=NULL, dt_biometria_validade='2028-04-09' WHERE cpf='78978978700';
UPDATE moradores SET foto=NULL, dt_foto_validade='2025-03-15' WHERE cpf='14725836900';
-- Bruno: foto VENCIDA em mar/2025 — a consulta de fotos vencidas vai encontra-lo!


-- ──────────────────────────────────────────────
-- 3.2 — Residencias (10 unidades)
-- ──────────────────────────────────────────────
-- Tipos cobertos:
--   [V] VERTICAL   — bloco + andar (apartamentos)
--   [H] HORIZONTAL — quadra (casas/lotes)
--   [S] SIMPLES    — so andar (predinho unico sem bloco)

-- [V] Apto 101 — Bloco A, 1o andar
INSERT INTO residencias (codigo_condominio, numero_residencia, bloco, andar, tipo_moradia, interfone, correlation_id)
VALUES ('COND-001','101','A',1,'apartamento','101','1ccd150e2b552bc7bb71a6bec19ff9110ce1a8a76cf0a1a81db6eaad16685b08');

-- [V] Apto 202 — Bloco A, 2o andar
INSERT INTO residencias (codigo_condominio, numero_residencia, bloco, andar, tipo_moradia, interfone, correlation_id)
VALUES ('COND-001','202','A',2,'apartamento','202','f7e5a6c9f4e8156d0de4d6fdbe5a73d776ef5dfa76b62258fbc8d2a86f2782bc');

-- [V] Apto 303 — Bloco B, 3o andar
INSERT INTO residencias (codigo_condominio, numero_residencia, bloco, andar, tipo_moradia, interfone, correlation_id)
VALUES ('COND-001','303','B',3,'apartamento','303','2f9251ab6a5c4338f485b4ac1e01e4ae7a811454b54ab5d999519c0f10ca24ab');

-- [V] Apto 104 — Bloco A, 1o andar
INSERT INTO residencias (codigo_condominio, numero_residencia, bloco, andar, tipo_moradia, interfone, correlation_id)
VALUES ('COND-001','104','A',1,'apartamento','104','f132abc2f047e8f15468d8f9dbcce0973edfa50544aa4555addb37e79a6e5a1a');

-- [V] Apto 501 — Bloco C, 5o andar
INSERT INTO residencias (codigo_condominio, numero_residencia, bloco, andar, tipo_moradia, interfone, correlation_id)
VALUES ('COND-001','501','C',5,'apartamento','501','826ae84e9c67b31c5a1bd069ea68bf5089dec85286e0b63253bd1ed3a48fee92');

-- [V] Apto 102 — Bloco A, 1o andar
INSERT INTO residencias (codigo_condominio, numero_residencia, bloco, andar, tipo_moradia, interfone, correlation_id)
VALUES ('COND-001','102','A',1,'apartamento','102','1d362ac2452307e641e0e1aaa50783160346042b7af3ca948905e71d3f4dead5');

-- [H] Lote 08 — Quadra 03 (condominio de casas)
INSERT INTO residencias (codigo_condominio, numero_residencia, quadra, tipo_moradia, observacao, correlation_id)
VALUES ('COND-001','08','03','casa','Lote 08 da Quadra 03','3cb2c94dddc8eca081e06b962525ffdb72bb8f30582dcc64b077f48b8ff8997d');

-- [H] Lote 14 — Quadra 07 (condominio de casas)
INSERT INTO residencias (codigo_condominio, numero_residencia, quadra, tipo_moradia, observacao, correlation_id)
VALUES ('COND-001','14','07','casa','Lote 14 da Quadra 07','639310841f7f3c153c7f2d2d7733e5b83af825c8ee2fc440468132d1e5649f08');

-- [S] Apto 301 — predinho unico sem bloco
INSERT INTO residencias (codigo_condominio, numero_residencia, andar, tipo_moradia, interfone, observacao, correlation_id)
VALUES ('COND-001','301',3,'apartamento','301','Predinho sem bloco','99814f834cc117b151dcc7d9c0cf5de717730bcc93c7b3782f82793e94e098f6');

-- [V] Apto 402 — Bloco B, 4o andar (ex-morador Sergio)
INSERT INTO residencias (codigo_condominio, numero_residencia, bloco, andar, tipo_moradia, interfone, correlation_id)
VALUES ('COND-001','402','B',4,'apartamento','402','921dfc608b24288ec61a9459b0090030708a5725f116a2d9b679121316b77b7e');


-- ──────────────────────────────────────────────
-- 3.3 — morador_residencia (quem mora onde)
-- ──────────────────────────────────────────────
-- DEMO N:N: Ana Paula (id=4) e proprietaria de 2 unidades!

INSERT INTO morador_residencia (morador_id,residencia_id,tipo_morador,dt_inicio,correlation_id) VALUES (1,1,'proprietario','2024-01-10','e2fa727090a47afdcad043747f94d378b6e5865fed0291e72e417a7cddd63076');
INSERT INTO morador_residencia (morador_id,residencia_id,tipo_morador,dt_inicio,correlation_id) VALUES (2,2,'inquilino','2025-06-01','d89c2b30b2ebd21654705b470d34ee61a829fbaf34ab464e21e5f61e0bbbff65');
INSERT INTO morador_residencia (morador_id,residencia_id,tipo_morador,dt_inicio,correlation_id) VALUES (3,3,'proprietario','2020-03-01','2f78470e823125ec48c0efa7c236e06343889f11ed0d0c17b3ab42039fc6d6e3');
INSERT INTO morador_residencia (morador_id,residencia_id,tipo_morador,dt_inicio,correlation_id) VALUES (4,4,'proprietario','2023-03-15','55bb9b3615a4ff69272decbaf4789c5ee904d6c6d502c98282dea2196dd3eb90');
INSERT INTO morador_residencia (morador_id,residencia_id,tipo_morador,dt_inicio,correlation_id) VALUES (4,1,'proprietario','2023-03-15','5ac08b755649dcc7553b83815f556035832125d27cc1881afb0dfb6027ded2f0');
-- Ana Paula tambem e co-proprietaria do Apto 101 (herdou do pai)!
INSERT INTO morador_residencia (morador_id,residencia_id,tipo_morador,dt_inicio,correlation_id) VALUES (5,5,'inquilino','2024-01-01','a438b5a0d51a66dd3e83bc0c395b6dfe0ec47d25e5d29c6b5182df490cff0ac9');
INSERT INTO morador_residencia (morador_id,residencia_id,tipo_morador,dt_inicio,correlation_id) VALUES (6,6,'proprietario','2019-07-01','1eb61a8d188a66874d4d50c07e5b69183f8fe9619a995c22b51f1caa11fd85da');
INSERT INTO morador_residencia (morador_id,residencia_id,tipo_morador,dt_inicio,correlation_id) VALUES (7,7,'inquilino','2022-01-15','8405f971c1b79ece97e6e88d5fe2189d0adf83b6d29e0852f5bea905a273773f');
INSERT INTO morador_residencia (morador_id,residencia_id,tipo_morador,dt_inicio,correlation_id) VALUES (8,8,'proprietario','2015-05-20','96a31d2a2fefc87023b794eecab354a99acc6c6a63568623befed1e10b8e2d49');
INSERT INTO morador_residencia (morador_id,residencia_id,tipo_morador,dt_inicio,correlation_id) VALUES (9,9,'inquilino','2023-08-01','2c89679220a21413f72b162d1eb92863595b98023c15210e811f734f57d0ee5c');
INSERT INTO morador_residencia (morador_id,residencia_id,tipo_morador,dt_inicio,correlation_id) VALUES (10,10,'proprietario','2018-02-01','64d312cb302fe239bf564dee91d13fd2439761b612725d5bdddd7007c1fe1a6c');


-- ──────────────────────────────────────────────
-- 3.4 — Config de seguranca por morador (5 registros)
-- ──────────────────────────────────────────────
-- Moradores sem config usam o padrao: 1 fator, qualquer tipo.

INSERT INTO config_acesso_morador (morador_id,fatores_requeridos,permite_senha,permite_digital,permite_facial,correlation_id)
VALUES (1,2,0,1,1,'7914898478adf525bea855df16a9e21de09414e23ce6427055e58a2e86ffe469');
-- Joao: 2 fatores obrigatorios, so biometria (sem senha)

INSERT INTO config_acesso_morador (morador_id,fatores_requeridos,permite_senha,permite_digital,permite_facial,correlation_id)
VALUES (2,1,1,1,0,'567b4719ccd83efc64aff16183c623c2bcf6fc23d7913028d97c793dee84b468');
-- Maria: 1 fator, senha ou digital (sem camera)

INSERT INTO config_acesso_morador (morador_id,fatores_requeridos,permite_senha,permite_digital,permite_facial,correlation_id)
VALUES (4,2,1,1,0,'38a70f6ccfeb329e09f4ba260c405c7dba364102fbc50550cfce0c7b35db48e6');
-- Ana: 2 fatores, senha + digital

INSERT INTO config_acesso_morador (morador_id,fatores_requeridos,permite_senha,permite_digital,permite_facial,correlation_id)
VALUES (6,1,0,1,0,'72e2a5065a1d5925210cb88d22901a47079fa6313e68f1ae26bd5670a040b344');
-- Lucia: 1 fator, so digital (sem senha por preferencia)

INSERT INTO config_acesso_morador (morador_id,fatores_requeridos,permite_senha,permite_digital,permite_facial,correlation_id)
VALUES (8,2,0,1,1,'cc9aa65e2281a5d90bb3321d46c21ffebdaab2cbfc08ab83ba73ca1160797c2b');
-- Dona Teresa: 2 fatores, digital + facial (maximo de seguranca)


-- ──────────────────────────────────────────────
-- 3.5 — Assinatura do condominio (1 registro)
-- ──────────────────────────────────────────────
INSERT INTO assinatura_condominio (
    codigo_condominio, nome_condominio, endereco,
    numero_contrato, dt_ativacao, dt_vigencia_inicio,
    status, observacoes, correlation_id
) VALUES (
    'COND-001',
    'Residencial Parque das Flores',
    'Rua das Palmeiras, 100, Jardim Botanico, Joao Pessoa - PB',
    '2026/0001-N7',
    '2026-04-09',
    '2026-04-09',
    'ativo',
    'Assinatura inicial do sistema n7-portaria-ai',
    'b56eecd6260a748dce8f10f79c8aaa842d747df24febaff8898524403493fb61'
);


-- ──────────────────────────────────────────────
-- 3.6 — Visitantes (8 registros)
-- ──────────────────────────────────────────────

-- Roberto: amigo do Joao — visita avulsa
INSERT INTO visitantes (nome,documento,tipo_documento,telefone,correlation_id)
VALUES ('Roberto Almeida','1234567','RG','83911112222','d360fb29c4b740ce5b14d469aa8e3a14046613ca036dd68109801f458eef1546');

-- Fernanda: amiga da Maria — visita avulsa
INSERT INTO visitantes (nome,documento,tipo_documento,telefone,correlation_id)
VALUES ('Fernanda Costa','98765432101','CNH','83933334444','2756d6698f27a08436d28a30b331edffc8094bb2d9be424481dd2094c24c916c');

-- Marcos: entregador recorrente
INSERT INTO visitantes (nome,documento,tipo_documento,telefone,correlation_id)
VALUES ('Marcos Delivery Pizza','7654321','RG','83955556666','35167da0662e1e665997b3b5d2716a7dd5e4867aca241c17cc9851b07d8e2c33');

-- Jose: BLOQUEADO — tentativa de acesso nao autorizado
INSERT INTO visitantes (nome,documento,tipo_documento,bloqueado,motivo_bloqueio,correlation_id)
VALUES ('Jose Suspeito','0000000','RG',1,'Tentativa de acesso nao autorizado em 01/04/2026','4cccf53242e8b9d552f85b4fd9fc042874bd8d4e277cb31eda76a4f4fb55b305');

-- Jean Pierre: tecnico estrangeiro — autorizado apenas durante obras (10/04 a 30/04)
INSERT INTO visitantes (nome,documento,tipo_documento,telefone,dt_validade_inicio,dt_validade_fim,correlation_id)
VALUES ('Jean Pierre Dubois','FR12345678','PASSAPORTE','83900998877','2026-04-10','2026-04-30','8e5715b82bfe3bf182c6961f229103bcb564e61ff8af25a42185f410e4ed4eb8');

-- Camila: sobrinha da Lucia — morando temporariamente (mai a jul/2026)
INSERT INTO visitantes (nome,documento,tipo_documento,telefone,dt_validade_inicio,dt_validade_fim,correlation_id)
VALUES ('Camila Rodrigues','55544433322','CNH','83944223311','2026-05-01','2026-07-31','a34e5818f646f09aecfa6ab44fb48a1bcaa04e5eb492cd1fa8f0324f5d21f041');

-- Sandra: irma do Pedro — acesso permanente a partir de abr/2026
INSERT INTO visitantes (nome,documento,tipo_documento,telefone,dt_validade_inicio,correlation_id)
VALUES ('Sandra Oliveira','3216549','RG','83966778899','2026-04-09','3a9849432fc688c6abfcd27d87027896ca130a32d88ba05606a52f359b0121e6');

-- Ricardo: BLOQUEADO — comportamento inadequado
INSERT INTO visitantes (nome,documento,tipo_documento,bloqueado,motivo_bloqueio,correlation_id)
VALUES ('Ricardo Problema','1111111','RG',1,'Comportamento agressivo com porteiro em 28/03/2026','8ddfcbd949ce5cfb72b7b33bb036bd6c0e9cbd3b72ce326845f115e86df79e24');


-- ──────────────────────────────────────────────
-- 3.7 — Funcionarios (5 registros)
-- ──────────────────────────────────────────────
-- senha_hash abaixo = SHA-256 de '' (string vazia) — trocar em producao!

INSERT INTO funcionarios (nome,cpf,cargo,setor,login,senha_hash,correlation_id)
VALUES ('Jose Silva Santos','10120230340','porteiro','portaria','porteiro.silva','e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855','3512b07f74959acbc82083dd5ad4ea7a9d0e293657a12aea779e1b0ee669a1d1');

INSERT INTO funcionarios (nome,cpf,cargo,setor,login,senha_hash,correlation_id)
VALUES ('Marcos Pereira Lima','20230340450','porteiro','portaria','porteiro.marcos','e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855','0950793ef7057529925913bf35327653887776ac4deccd0ae0324e9d2f9bf511');

INSERT INTO funcionarios (nome,cpf,cargo,setor,login,senha_hash,correlation_id)
VALUES ('Claudia Regina Borges','30340450560','administrador','administracao','admin.claudia','e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855','d0a8c15332ea1a0cf3a96e6cf6c59b8b30c791afb13826029315178d027db5b5');

INSERT INTO funcionarios (nome,cpf,cargo,setor,login,senha_hash,correlation_id)
VALUES ('Fatima Souza Andrade','40450560670','outro','limpeza','limpeza.fatima','e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855','6cb3dd614b4225c71bde78364cb46342a76820bd150ca7cff218b9c311d3841b');

INSERT INTO funcionarios (nome,cpf,cargo,setor,login,senha_hash,correlation_id)
VALUES ('Paulo Oliveira Neto','50560670780','zelador','manutencao','zelador.paulo','e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855','679f4960f88cbb170c2c6cc18653dd8203684d50ba3eda0ad2a82de474957df4');


-- ──────────────────────────────────────────────
-- 3.8 — Veiculos (5 registros)
-- ──────────────────────────────────────────────

INSERT INTO veiculos (placa,modelo,cor,morador_id,correlation_id)
VALUES ('ABC-1234','Honda Civic','Prata',1,'69f472ffd51e61a0f489498fc339c9d299d90b9f268855a0b4431e4fcc484346');

INSERT INTO veiculos (placa,modelo,cor,morador_id,correlation_id)
VALUES ('DEF-5678','Fiat Pulse','Branco',4,'0b2f8b037a2b1e18d722e27bef0fac999c51a92c4a451b93f54aa71492465c4e');

INSERT INTO veiculos (placa,modelo,cor,morador_id,correlation_id)
VALUES ('GHI-9012','Toyota Corolla','Preto',8,'bce468b6569f90ae6a1de439c8316554cf524d1f12f3e5caf7f49dec4921c14b');

INSERT INTO veiculos (placa,modelo,cor,funcionario_id,correlation_id)
VALUES ('JKL-3456','Moto Honda CG','Vermelha',2,'334f1c4e400e74b3b6fa2571981c4fe28b409b09a44af724e4d9a9dbf66b3f5c');

INSERT INTO veiculos (placa,modelo,cor,visitante_id,correlation_id)
VALUES ('QRS-5678','VW Polo','Cinza',2,'bbfeb3ba1b9a3a309c5afc21a2e3303258b46e6472367537262797de7faedfa1');


-- ──────────────────────────────────────────────
-- 3.9 — Registros de acesso (10 registros)
-- ──────────────────────────────────────────────

-- Roberto visitou Joao (ja saiu):
INSERT INTO acessos (visitante_id,morador_id,funcionario_id,tipo_acesso,auth_senha,auth_digital,auth_facial,motivo,dt_entrada_em,dt_saida_em,porteiro,observacoes,correlation_id)
VALUES (1,1,1,'pedestre',0,1,0,'Visita familiar','2026-04-08 14:00:00','2026-04-08 17:30:00','Porteiro Silva','Tio do morador','5a47affa6f1366945900e72987634b19331ad301b904ada6bcba20a4c1e24e45');

-- Fernanda visitou Maria — entrou de carro pela garagem:
INSERT INTO acessos (visitante_id,morador_id,funcionario_id,veiculo_id,tipo_acesso,auth_senha,auth_digital,auth_facial,motivo,dt_entrada_em,dt_saida_em,porteiro,correlation_id)
VALUES (2,2,1,5,'garagem',0,1,1,'Visita social','2026-04-09 10:00:00','2026-04-09 12:00:00','Porteiro Silva','9b4dac4acd0b5a8736ec3f1e20033f7145c02c4c005760705fb49afd2e75cb4f');

-- Marcos entregou pizza (portao de pedestres):
INSERT INTO acessos (visitante_id,morador_id,funcionario_id,tipo_acesso,auth_senha,auth_digital,auth_facial,motivo,dt_entrada_em,dt_saida_em,porteiro,observacoes,correlation_id)
VALUES (3,3,2,'pedestre',1,0,0,'Entrega - Pizza','2026-04-09 19:45:00','2026-04-09 19:52:00','Porteiro Marcos','Delivery de moto','15d13f5672421e32bebf4f400df0a93b73c3c00440b721d09786d45a00e59ee5');

-- Roberto esta dentro agora (manutencao na Ana — sem saida):
INSERT INTO acessos (visitante_id,morador_id,funcionario_id,tipo_acesso,auth_senha,auth_digital,auth_facial,motivo,porteiro,correlation_id)
VALUES (1,4,1,'pedestre',0,1,0,'Manutencao do ar-condicionado','Porteiro Silva','ce1922f0c1c846498028c0f3503f64da67a1e70a5248c8843184b93d1955c808');

-- Camila visitou Maria (ja saiu):
INSERT INTO acessos (visitante_id,morador_id,funcionario_id,tipo_acesso,auth_senha,auth_digital,auth_facial,motivo,dt_entrada_em,dt_saida_em,porteiro,correlation_id)
VALUES (5,2,2,'pedestre',1,0,0,'Visita social - amiga','2026-04-07 15:00:00','2026-04-07 18:30:00','Porteiro Marcos','34a4f87d0ec41ace7d168c5233ce7f7cf4dcd201a5e9cae47ad600a213aa634d');

-- Jean Pierre fez manutencao na Dona Teresa (ja saiu):
INSERT INTO acessos (visitante_id,morador_id,funcionario_id,tipo_acesso,auth_senha,auth_digital,auth_facial,motivo,dt_entrada_em,dt_saida_em,porteiro,observacoes,correlation_id)
VALUES (6,8,1,'pedestre',1,1,0,'Manutencao - Ar condicionado','2026-04-08 09:00:00','2026-04-08 11:45:00','Porteiro Silva','Tecnico autorizado','ab432261a712123cda4f57c7c1177ab393e9ab07c4482e7d1bda7408931244cd');

-- Sandra visitou Pedro (1a visita — ja saiu):
INSERT INTO acessos (visitante_id,morador_id,funcionario_id,tipo_acesso,auth_senha,auth_digital,auth_facial,motivo,dt_entrada_em,dt_saida_em,porteiro,correlation_id)
VALUES (7,3,2,'pedestre',0,1,0,'Visita familiar - irma','2026-04-06 10:00:00','2026-04-06 13:00:00','Porteiro Marcos','7a5370ca54a979745ee52be36df94ae72a6d115484010e525aacf28a24769a54');

-- Sandra visitou Pedro (2a visita — ja saiu):
INSERT INTO acessos (visitante_id,morador_id,funcionario_id,tipo_acesso,auth_senha,auth_digital,auth_facial,motivo,dt_entrada_em,dt_saida_em,porteiro,observacoes,correlation_id)
VALUES (7,3,1,'pedestre',0,1,0,'Visita familiar - irma','2026-04-09 16:00:00','2026-04-09 20:00:00','Porteiro Silva','Trouxe bolo de aniversario','2c687ce34224518bffee47db0034995073d4a1246bf89e633b97072ce36390b8');

-- Marcos fez entrega de restaurante (ja saiu):
INSERT INTO acessos (visitante_id,morador_id,funcionario_id,tipo_acesso,auth_senha,auth_digital,auth_facial,motivo,dt_entrada_em,dt_saida_em,porteiro,observacoes,correlation_id)
VALUES (3,8,2,'pedestre',1,0,0,'Entrega - Restaurante Japones','2026-04-09 12:30:00','2026-04-09 12:38:00','Porteiro Marcos','Delivery de moto','00de89a3b6947f1054e60d4785498310a48b18d9728cf9bae81765e70d34f98f');

-- Fernanda esta visitando Lucia AGORA (sem saida):
INSERT INTO acessos (visitante_id,morador_id,funcionario_id,veiculo_id,tipo_acesso,auth_senha,auth_digital,auth_facial,motivo,porteiro,observacoes,correlation_id)
VALUES (2,6,1,5,'garagem',0,1,1,'Reuniao de condominio informal','Porteiro Silva','Veio de carro, placa QRS-5678','6cd1121564ac10c292b20fecd66b646283ffcc68a14096fcc310564c74a26db7');


-- ============================================================================
-- PARTE 4: CONSULTAS DE ESTUDO
-- ============================================================================
-- Configure o SQLite para exibicao bonita:
--   .mode column
--   .headers on

-- 4.1 — BASICAS -------------------------------------------------------------

-- Todos os moradores ativos:
SELECT id, nome, cpf, telefone, ativo FROM moradores WHERE ativo = 1;

-- Moradores sem aceite LGPD pendente:
SELECT nome, cpf FROM moradores WHERE dt_aceite_lgpd IS NULL AND ativo = 1;

-- Fotos vencidas:
SELECT nome, dt_foto_validade FROM moradores
WHERE dt_foto_validade < CAST(GETDATE() AS DATE) AND ativo = 1;


-- 4.2 — MORADOR + RESIDENCIA (JOIN N:N) ------------------------------------

-- Visao completa: morador + sua unidade:
SELECT
    m.nome,
    r.numero_residencia,
    r.bloco,
    r.andar,
    r.tipo_moradia,        -- CAMPO DO ADEMILSON
    r.interfone,           -- CAMPO DO ADEMILSON
    r.observacao,          -- CAMPO DO ADEMILSON
    mr.tipo_morador,
    r.codigo_condominio
FROM moradores m
    JOIN morador_residencia mr ON m.id = mr.morador_id
    JOIN residencias r         ON mr.residencia_id = r.id
WHERE m.ativo = 1 AND mr.ativo = 1
ORDER BY r.bloco, r.numero_residencia;

-- Moradores com mais de uma unidade:
SELECT m.nome, COUNT(mr.residencia_id) AS total_unidades
FROM moradores m
    JOIN morador_residencia mr ON m.id = mr.morador_id
WHERE m.ativo = 1 AND mr.ativo = 1
GROUP BY m.id
HAVING COUNT(mr.residencia_id) > 1;

-- Proprietarios vs inquilinos por tipo de moradia:
SELECT r.tipo_moradia, mr.tipo_morador, COUNT(*) AS quantidade
FROM morador_residencia mr
    JOIN residencias r ON mr.residencia_id = r.id
WHERE mr.ativo = 1
GROUP BY r.tipo_moradia, mr.tipo_morador;


-- 4.3 — ACESSOS COM JOIN ---------------------------------------------------

-- Todos os acessos com nomes:
SELECT
    a.id AS registro,
    v.nome AS visitante,
    m.nome AS morador_visitado,
    a.motivo,
    a.tipo_acesso,
    a.dt_entrada_em,
    a.dt_saida_em,
    a.porteiro
FROM acessos a
    JOIN visitantes v ON a.visitante_id = v.id
    JOIN moradores  m ON a.morador_id   = m.id
ORDER BY a.dt_entrada_em DESC;

-- Quem esta DENTRO agora?
SELECT v.nome AS visitante, m.nome AS morador, a.motivo, a.dt_entrada_em
FROM acessos a
    JOIN visitantes v ON a.visitante_id = v.id
    JOIN moradores  m ON a.morador_id   = m.id
WHERE a.dt_saida_em IS NULL;


-- 4.4 — VEICULOS -----------------------------------------------------------

-- Todos os veiculos com nome do proprietario:
SELECT
    v.placa, v.modelo, v.cor,
    CASE
        WHEN v.morador_id     IS NOT NULL THEN 'Morador: ' + m.nome
        WHEN v.funcionario_id IS NOT NULL THEN 'Funcionario: ' + f.nome
        WHEN v.visitante_id   IS NOT NULL THEN 'Visitante: ' + vis.nome
        ELSE 'Sem proprietario'
    END AS proprietario
FROM veiculos v
    LEFT JOIN moradores    m   ON v.morador_id     = m.id
    LEFT JOIN funcionarios f   ON v.funcionario_id = f.id
    LEFT JOIN visitantes   vis ON v.visitante_id   = vis.id
WHERE v.ativo = 1;


-- 4.5 — RESUMO DO CONDOMINIO -----------------------------------------------
SELECT
    (SELECT COUNT(*) FROM moradores WHERE ativo = 1)                              AS moradores_ativos,
    (SELECT COUNT(*) FROM visitantes)                                              AS total_visitantes,
    (SELECT COUNT(*) FROM visitantes WHERE bloqueado = 1)                          AS visitantes_bloqueados,
    (SELECT COUNT(*) FROM acessos WHERE dt_saida_em IS NULL)                       AS dentro_agora,
    (SELECT COUNT(*) FROM acessos)                                                 AS total_acessos,
    (SELECT COUNT(*) FROM moradores WHERE dt_aceite_lgpd IS NULL AND ativo = 1)   AS lgpd_pendente;


-- ============================================================================
-- PARTE 5: EXERCICIOS PARA PRATICAR
-- ============================================================================

-- EXERCICIO 1: Insira um novo morador chamado 'Luiza Barbosa',
--   CPF '22233344455', telefone '83944556677'.
-- Sua resposta aqui:

-- RESPOSTA 1:
-- INSERT INTO moradores (nome, cpf, telefone, correlation_id)
-- VALUES ('Luiza Barbosa', '22233344455', '83944556677', '<hash-sha256>');


-- EXERCICIO 2: Adicione uma residencia para a Luiza (Apto 401, Bloco B).
-- Dica: primeiro INSERT em residencias, depois em morador_residencia.
-- Sua resposta aqui:

-- RESPOSTA 2:
-- INSERT INTO residencias (codigo_condominio, numero_residencia, bloco, andar, tipo_moradia, interfone, correlation_id)
-- VALUES ('COND-001', '401', 'B', 4, 'apartamento', '401', '<hash>');
-- INSERT INTO morador_residencia (morador_id, residencia_id, tipo_morador, correlation_id)
-- VALUES (11, 11, 'inquilino', '<hash>');


-- EXERCICIO 3: Registre a SAIDA do Roberto (acesso id=4, ainda dentro).
-- Dica: UPDATE acessos SET dt_saida_em = ... WHERE id = 4
-- Sua resposta aqui:

-- RESPOSTA 3:
-- UPDATE acessos SET dt_saida_em = '2026-04-09 16:00:00' WHERE id = 4;


-- EXERCICIO 4: Liste todos os moradores do Bloco A com seus interfones.
-- Dica: JOIN moradores + morador_residencia + residencias WHERE bloco='A'
-- Sua resposta aqui:

-- RESPOSTA 4:
-- SELECT m.nome, r.numero_residencia, r.interfone, mr.tipo_morador
-- FROM moradores m
--     JOIN morador_residencia mr ON m.id = mr.morador_id
--     JOIN residencias r ON mr.residencia_id = r.id
-- WHERE r.bloco = 'A' AND m.ativo = 1
-- ORDER BY r.numero_residencia;


-- EXERCICIO 5 (DESAFIO): Quantos moradores de cada tipo_moradia existem?
-- Dica: JOIN + GROUP BY tipo_moradia
-- Sua resposta aqui:

-- RESPOSTA 5:
-- SELECT r.tipo_moradia, COUNT(DISTINCT m.id) AS total_moradores
-- FROM moradores m
--     JOIN morador_residencia mr ON m.id = mr.morador_id
--     JOIN residencias r ON mr.residencia_id = r.id
-- WHERE m.ativo = 1 AND mr.ativo = 1
-- GROUP BY r.tipo_moradia;


-- EXERCICIO 6 (DESAFIO): Quem tem MAIS de uma unidade? (demo N:N)
-- Dica: GROUP BY m.id + HAVING COUNT > 1
-- Sua resposta aqui:

-- RESPOSTA 6:
-- SELECT m.nome, COUNT(mr.residencia_id) AS unidades
-- FROM moradores m
--     JOIN morador_residencia mr ON m.id = mr.morador_id
-- WHERE mr.tipo_morador = 'proprietario' AND mr.ativo = 1
-- GROUP BY m.id HAVING COUNT(mr.residencia_id) > 1;


-- EXERCICIO 7 (DESAFIO LGPD): Qual % de moradores ainda nao aceitou os termos?
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
-- FOREIGN KEY   — chave estrangeira: link entre tabelas (relacao entre dados)
-- VARBINARY(MAX)          — dados binarios (foto, PDF, biometria)
-- DATE          — apenas data: 'AAAA-MM-DD'
-- DATETIME2      — data e hora: 'AAAA-MM-DD HH:MM:SS'
-- BIT       — verdadeiro/falso, armazenado como 0 ou 1 no SQLite
-- INDEX         — estrutura de busca rapida (como indice de livro)
-- LEFT JOIN     — retorna todos da tabela esquerda, mesmo sem correspondencia
-- SHA-256       — funcao que transforma texto em hash de 64 hex chars
-- CORRELATION_ID — hash usado como ID global para sync entre bancos
-- LGPD          — Lei Geral de Protecao de Dados (Lei 13.709/2018)
-- SOFT DELETE   — desativar (ativo=0) em vez de deletar — preserva historico
-- JUNCTION TABLE — tabela intermediaria que resolve relacao N:N
-- IDENTITY(1,1)  — SQL Server: auto-incremento (equivalente ao AUTOINCREMENT)
-- NVARCHAR       — SQL Server: texto Unicode (suporta acentos nativamente)
-- GETDATE()      — SQL Server: data/hora atual (equivalente ao CURRENT_TIMESTAMP)
-- ============================================================================


-- ============================================================================
-- PARTE 6: GABARITO — RESPOSTAS EXECUTAVEIS (SQL SERVER)
-- ============================================================================
-- Ademilson, so olhe aqui DEPOIS de tentar sozinho!
-- Execute no SSMS (SQL Server Management Studio) ou via sqlcmd.
-- ============================================================================

-- ──────────────────────────────────────────────
-- RESPOSTA 1: Inserir novo morador
-- ──────────────────────────────────────────────
INSERT INTO moradores (nome, cpf, telefone, correlation_id)
VALUES (N'Luiza Barbosa', N'22233344455', N'83944556677',
        N'gabarito_resp1_luiza_barbosa_22233344455');

-- Conferir:
SELECT id, nome, cpf, telefone FROM moradores WHERE cpf = N'22233344455';
GO


-- ──────────────────────────────────────────────
-- RESPOSTA 2: Residencia + vinculo morador_residencia
-- ──────────────────────────────────────────────
INSERT INTO residencias (codigo_condominio, numero_residencia, bloco, andar, tipo_moradia, interfone, correlation_id)
VALUES (N'COND-001', N'401', N'B', 4, N'apartamento', N'401',
        N'gabarito_resp2_residencia_401_bloco_b');

-- Usa subquery para pegar os IDs dinamicamente (mais seguro que chutar numeros!)
DECLARE @morador_id INT = (SELECT id FROM moradores WHERE cpf = N'22233344455');
DECLARE @residencia_id INT = (SELECT id FROM residencias WHERE numero_residencia = N'401' AND bloco = N'B');

INSERT INTO morador_residencia (morador_id, residencia_id, tipo_morador, correlation_id)
VALUES (@morador_id, @residencia_id, N'inquilino',
        N'gabarito_resp2_vinculo_luiza_401b');

-- Conferir:
SELECT m.nome, r.numero_residencia, r.bloco, mr.tipo_morador
FROM moradores m
    JOIN morador_residencia mr ON m.id = mr.morador_id
    JOIN residencias r ON mr.residencia_id = r.id
WHERE m.cpf = N'22233344455';
GO


-- ──────────────────────────────────────────────
-- RESPOSTA 3: Registrar saida do Roberto
-- ──────────────────────────────────────────────
UPDATE acessos SET dt_saida_em = '2026-04-09 16:00:00' WHERE id = 4;

-- Conferir:
SELECT id, dt_entrada_em, dt_saida_em FROM acessos WHERE id = 4;
GO


-- ──────────────────────────────────────────────
-- RESPOSTA 4: Moradores do Bloco A com interfone
-- ──────────────────────────────────────────────
SELECT m.nome, r.numero_residencia, r.interfone, mr.tipo_morador
FROM moradores m
    JOIN morador_residencia mr ON m.id = mr.morador_id
    JOIN residencias r ON mr.residencia_id = r.id
WHERE r.bloco = N'A' AND m.ativo = 1
ORDER BY r.numero_residencia;
GO


-- ──────────────────────────────────────────────
-- RESPOSTA 5: Moradores por tipo_moradia
-- ──────────────────────────────────────────────
SELECT r.tipo_moradia, COUNT(DISTINCT m.id) AS total_moradores
FROM moradores m
    JOIN morador_residencia mr ON m.id = mr.morador_id
    JOIN residencias r ON mr.residencia_id = r.id
WHERE m.ativo = 1 AND mr.ativo = 1
GROUP BY r.tipo_moradia;
GO


-- ──────────────────────────────────────────────
-- RESPOSTA 6: Quem tem mais de uma unidade (N:N)
-- ──────────────────────────────────────────────
SELECT m.nome, COUNT(mr.residencia_id) AS unidades
FROM moradores m
    JOIN morador_residencia mr ON m.id = mr.morador_id
WHERE mr.tipo_morador = N'proprietario' AND mr.ativo = 1
GROUP BY m.id, m.nome
HAVING COUNT(mr.residencia_id) > 1;
GO


-- ──────────────────────────────────────────────
-- RESPOSTA 7: Percentual LGPD pendente
-- ──────────────────────────────────────────────
SELECT
    COUNT(*) AS total,
    SUM(CASE WHEN dt_aceite_lgpd IS NULL THEN 1 ELSE 0 END) AS sem_aceite,
    ROUND(
        CAST(SUM(CASE WHEN dt_aceite_lgpd IS NULL THEN 1.0 ELSE 0 END) AS FLOAT)
        / COUNT(*) * 100, 1
    ) AS pct_pendente
FROM moradores
WHERE ativo = 1;
GO

-- ============================================================================
-- FIM DO GABARITO
-- ============================================================================
