-- ============================================================================
-- PROJETO PORTARIA INTELIGENTE — BANCO DE DADOS (v1.1 - REVISADO)
-- ============================================================================
-- Aluno: Ademilson
-- Revisão: Thiago (2026-04-23)
-- Target: PostgreSQL 16+
--
-- Principais mudanças vs v1.0:
--  [S1] SERIAL -> GENERATED ALWAYS AS IDENTITY (padrão SQL, PG 10+)
--  [S2] FKs ganham políticas ON DELETE/UPDATE explícitas
--  [S3] Removido 'porteiro TEXT' redundante em acessos (usar funcionario_id)
--  [S4] FK residencias.codigo_condominio -> assinatura_condominio (DEFERRABLE)
--  [S5] Trigger fn_touch_updated_at para dt_atualizado_em
--  [S6] CHECK de email com regex POSIX
--  [S7] Migração dentro de transação BEGIN/COMMIT
--  [S8] UPDATEs redundantes de fixtures consolidados nos próprios INSERTs
--  [S9] Seeds de moradores ativos agora exigem dt_aceite_lgpd coerente
-- ============================================================================

BEGIN;

-- ============================================================================
-- LIMPEZA (ordem reversa das dependências)
-- ============================================================================
DROP TABLE IF EXISTS acessos CASCADE;
DROP TABLE IF EXISTS morador_residencia CASCADE;
DROP TABLE IF EXISTS config_acesso_morador CASCADE;
DROP TABLE IF EXISTS veiculos CASCADE;
DROP TABLE IF EXISTS assinatura_condominio CASCADE;
DROP TABLE IF EXISTS visitantes CASCADE;
DROP TABLE IF EXISTS funcionarios CASCADE;
DROP TABLE IF EXISTS residencias CASCADE;
DROP TABLE IF EXISTS moradores CASCADE;
DROP FUNCTION IF EXISTS fn_touch_updated_at() CASCADE;

-- ============================================================================
-- TRIGGER FUNCTION — atualiza dt_atualizado_em em qualquer UPDATE
-- ============================================================================
CREATE OR REPLACE FUNCTION fn_touch_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.dt_atualizado_em := CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- PARTE 1: TABELAS
-- ============================================================================

CREATE TABLE moradores (
    id                    INTEGER   GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome                  TEXT      NOT NULL,
    cpf                   TEXT      UNIQUE NOT NULL CHECK (length(cpf) = 11),
    telefone              TEXT,
    email                 TEXT      CHECK (email ~ '^[^@\s]+@[^@\s]+\.[^@\s]+$'),
    dt_nascimento         DATE,
    foto                  BYTEA,
    dt_foto_validade      DATE,
    biometria             BYTEA,
    dt_biometria_validade DATE,
    termos_lgpd           BYTEA,
    dt_aceite_lgpd        TIMESTAMP,
    ativo                 BOOLEAN   NOT NULL DEFAULT TRUE,
    correlation_id        TEXT      UNIQUE NOT NULL,
    dt_criado_em          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dt_atualizado_em      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- Regra LGPD: morador ativo exige aceite registrado
    CONSTRAINT chk_moradores_lgpd_ativo
        CHECK (NOT ativo OR dt_aceite_lgpd IS NOT NULL)
);

CREATE TABLE assinatura_condominio (
    id                    INTEGER   GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    codigo_condominio     TEXT      UNIQUE NOT NULL,
    nome_condominio       TEXT      NOT NULL,
    endereco              TEXT,
    responsavel_id        INTEGER,
    numero_contrato       TEXT      UNIQUE NOT NULL,
    contrato              BYTEA,
    dt_ativacao           DATE,
    dt_vigencia_inicio    DATE      NOT NULL,
    dt_vigencia_fim       DATE      CHECK (dt_vigencia_fim IS NULL OR dt_vigencia_fim >= dt_vigencia_inicio),
    status                TEXT      NOT NULL DEFAULT 'ativo'
                                    CHECK (status IN ('ativo','pendente','vencido','cancelado')),
    observacoes           TEXT,
    correlation_id        TEXT      UNIQUE NOT NULL,
    dt_criado_em          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dt_atualizado_em      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_assinatura_responsavel
        FOREIGN KEY (responsavel_id) REFERENCES moradores(id)
        ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE residencias (
    id                    INTEGER   GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    codigo_condominio     TEXT      NOT NULL,
    numero_residencia     TEXT      NOT NULL,
    bloco                 TEXT,
    quadra                TEXT,
    andar                 INTEGER,
    tipo_moradia          TEXT      NOT NULL DEFAULT 'apartamento'
                                    CHECK (tipo_moradia IN ('apartamento','casa','comercial','outro')),
    interfone             TEXT,
    observacao            TEXT,
    ativo                 BOOLEAN   NOT NULL DEFAULT TRUE,
    correlation_id        TEXT      UNIQUE NOT NULL,
    dt_criado_em          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dt_atualizado_em      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_residencias_condominio
        FOREIGN KEY (codigo_condominio)
        REFERENCES assinatura_condominio(codigo_condominio)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE morador_residencia (
    id                    INTEGER   GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    morador_id            INTEGER   NOT NULL,
    residencia_id         INTEGER   NOT NULL,
    tipo_morador          TEXT      NOT NULL DEFAULT 'proprietario'
                                    CHECK (tipo_morador IN ('proprietario','inquilino')),
    dt_inicio             DATE      NOT NULL DEFAULT CURRENT_DATE,
    dt_fim                DATE      CHECK (dt_fim IS NULL OR dt_fim >= dt_inicio),
    ativo                 BOOLEAN   NOT NULL DEFAULT TRUE,
    correlation_id        TEXT      UNIQUE NOT NULL,
    dt_criado_em          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_mr_morador
        FOREIGN KEY (morador_id) REFERENCES moradores(id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_mr_residencia
        FOREIGN KEY (residencia_id) REFERENCES residencias(id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    UNIQUE (morador_id, residencia_id, dt_inicio)
);

CREATE TABLE visitantes (
    id                    INTEGER   GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome                  TEXT      NOT NULL,
    documento             TEXT      NOT NULL,
    tipo_documento        TEXT      NOT NULL DEFAULT 'RG'
                                    CHECK (tipo_documento IN ('RG','CNH','PASSAPORTE','OUTRO')),
    telefone              TEXT,
    foto                  BYTEA,
    bloqueado             BOOLEAN   NOT NULL DEFAULT FALSE,
    motivo_bloqueio       TEXT,
    dt_validade_inicio    DATE,
    dt_validade_fim       DATE      CHECK (dt_validade_fim IS NULL OR dt_validade_fim >= dt_validade_inicio),
    correlation_id        TEXT      UNIQUE NOT NULL,
    dt_criado_em          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- Bloqueio exige motivo
    CONSTRAINT chk_visitantes_bloqueio_motivo
        CHECK (NOT bloqueado OR motivo_bloqueio IS NOT NULL)
);

CREATE TABLE funcionarios (
    id                    INTEGER   GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome                  TEXT      NOT NULL,
    cpf                   TEXT      UNIQUE NOT NULL CHECK (length(cpf) = 11),
    cargo                 TEXT      NOT NULL DEFAULT 'porteiro'
                                    CHECK (cargo IN ('porteiro','zelador','administrador','outro')),
    setor                 TEXT,
    login                 TEXT      UNIQUE NOT NULL,
    senha_hash            TEXT      NOT NULL CHECK (length(senha_hash) = 64),
    ativo                 BOOLEAN   NOT NULL DEFAULT TRUE,
    correlation_id        TEXT      UNIQUE NOT NULL,
    dt_criado_em          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE veiculos (
    id                    INTEGER   GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    placa                 TEXT      UNIQUE NOT NULL CHECK (length(placa) >= 7),
    modelo                TEXT,
    cor                   TEXT,
    morador_id            INTEGER,
    funcionario_id        INTEGER,
    visitante_id          INTEGER,
    ativo                 BOOLEAN   NOT NULL DEFAULT TRUE,
    correlation_id        TEXT      UNIQUE NOT NULL,
    dt_criado_em          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- Veículo pertence a UM dos três (ou a nenhum, no caso de cadastro avulso)
    CONSTRAINT chk_veiculos_owner_exclusivo CHECK (
        (CASE WHEN morador_id     IS NOT NULL THEN 1 ELSE 0 END) +
        (CASE WHEN funcionario_id IS NOT NULL THEN 1 ELSE 0 END) +
        (CASE WHEN visitante_id   IS NOT NULL THEN 1 ELSE 0 END) <= 1
    ),
    CONSTRAINT fk_veiculos_morador
        FOREIGN KEY (morador_id)     REFERENCES moradores(id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_veiculos_funcionario
        FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_veiculos_visitante
        FOREIGN KEY (visitante_id)   REFERENCES visitantes(id)
        ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE acessos (
    id                    INTEGER   GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    visitante_id          INTEGER   NOT NULL,
    morador_id            INTEGER,
    funcionario_id        INTEGER,   -- Porteiro que autorizou (substitui 'porteiro TEXT')
    veiculo_id            INTEGER,
    tipo_acesso           TEXT      NOT NULL DEFAULT 'pedestre'
                                    CHECK (tipo_acesso IN ('pedestre','garagem')),
    auth_senha            BOOLEAN   NOT NULL DEFAULT FALSE,
    auth_digital          BOOLEAN   NOT NULL DEFAULT FALSE,
    auth_facial           BOOLEAN   NOT NULL DEFAULT FALSE,
    motivo                TEXT      NOT NULL,
    dt_entrada_em         TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dt_saida_em           TIMESTAMP CHECK (dt_saida_em IS NULL OR dt_saida_em >= dt_entrada_em),
    observacoes           TEXT,
    correlation_id        TEXT      UNIQUE NOT NULL,
    CHECK (auth_senha OR auth_digital OR auth_facial),
    -- Acesso é trilha de auditoria: JAMAIS cascatear DELETE; usar RESTRICT
    CONSTRAINT fk_acessos_visitante
        FOREIGN KEY (visitante_id)   REFERENCES visitantes(id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_acessos_morador
        FOREIGN KEY (morador_id)     REFERENCES moradores(id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_acessos_funcionario
        FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_acessos_veiculo
        FOREIGN KEY (veiculo_id)     REFERENCES veiculos(id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE config_acesso_morador (
    id                    INTEGER   GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    morador_id            INTEGER   UNIQUE NOT NULL,
    fatores_requeridos    INTEGER   NOT NULL DEFAULT 1 CHECK (fatores_requeridos IN (1,2)),
    permite_senha         BOOLEAN   NOT NULL DEFAULT TRUE,
    permite_digital       BOOLEAN   NOT NULL DEFAULT TRUE,
    permite_facial        BOOLEAN   NOT NULL DEFAULT FALSE,
    correlation_id        TEXT      UNIQUE NOT NULL,
    dt_criado_em          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dt_atualizado_em      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (permite_senha OR permite_digital OR permite_facial),
    CONSTRAINT fk_cam_morador
        FOREIGN KEY (morador_id) REFERENCES moradores(id)
        ON UPDATE CASCADE ON DELETE CASCADE  -- config é "parte de" morador
);

-- ============================================================================
-- TRIGGERS dt_atualizado_em
-- ============================================================================
CREATE TRIGGER trg_moradores_updated             BEFORE UPDATE ON moradores
    FOR EACH ROW EXECUTE FUNCTION fn_touch_updated_at();
CREATE TRIGGER trg_residencias_updated           BEFORE UPDATE ON residencias
    FOR EACH ROW EXECUTE FUNCTION fn_touch_updated_at();
CREATE TRIGGER trg_assinatura_updated            BEFORE UPDATE ON assinatura_condominio
    FOR EACH ROW EXECUTE FUNCTION fn_touch_updated_at();
CREATE TRIGGER trg_config_acesso_morador_updated BEFORE UPDATE ON config_acesso_morador
    FOR EACH ROW EXECUTE FUNCTION fn_touch_updated_at();

-- ============================================================================
-- PARTE 2: ÍNDICES
-- ============================================================================
CREATE INDEX idx_moradores_nome          ON moradores(nome);
CREATE INDEX idx_moradores_ativo         ON moradores(ativo);
CREATE INDEX idx_residencias_cond        ON residencias(codigo_condominio);
CREATE INDEX idx_residencias_num         ON residencias(numero_residencia);
CREATE INDEX idx_residencias_tipo        ON residencias(tipo_moradia);
CREATE INDEX idx_mr_morador              ON morador_residencia(morador_id);
CREATE INDEX idx_mr_residencia           ON morador_residencia(residencia_id);
CREATE INDEX idx_mr_ativo                ON morador_residencia(ativo);
CREATE INDEX idx_visitantes_documento    ON visitantes(documento);
CREATE INDEX idx_visitantes_bloqueado    ON visitantes(bloqueado);
CREATE INDEX idx_funcionarios_cargo      ON funcionarios(cargo);
CREATE INDEX idx_veiculos_morador        ON veiculos(morador_id);
CREATE INDEX idx_acessos_entrada         ON acessos(dt_entrada_em);
CREATE INDEX idx_acessos_visitante       ON acessos(visitante_id);
CREATE INDEX idx_acessos_morador         ON acessos(morador_id);
CREATE INDEX idx_acessos_funcionario     ON acessos(funcionario_id);
CREATE INDEX idx_acessos_veiculo         ON acessos(veiculo_id);
CREATE INDEX idx_assinatura_status       ON assinatura_condominio(status);
CREATE INDEX idx_assinatura_vig_fim      ON assinatura_condominio(dt_vigencia_fim);

-- ============================================================================
COMMIT;
