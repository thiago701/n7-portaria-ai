-- Aula 02: Schema do Banco de Dados
-- Este arquivo descreve a estrutura da tabela de moradores
-- Atualizado com os campos do documento de requisitos (foto, biometria, tipo)

-- TODO: Complete a instrução CREATE TABLE abaixo
-- Você precisa adicionar as colunas que faltam entre os comentários TODO
-- Use TEXT para texto (nome, email, etc.) e INTEGER para números (id, ativo, etc.)
-- Revise a teoria no README.md para lembrar da sintaxe!

CREATE TABLE moradores (
    -- Identificador único (PRIMARY KEY significa "chave única")
    -- TODO: Adicione a coluna 'id' como INTEGER PRIMARY KEY

    -- Nome completo do morador
    -- TODO: Adicione a coluna 'nome' como TEXT e NOT NULL (obrigatório)

    -- CPF do morador (sem formatação: apenas números — exatamente 11 dígitos)
    -- TODO: Adicione a coluna 'cpf' como TEXT UNIQUE NOT NULL
    --       com CHECK(length(cpf) = 11) para garantir 11 dígitos

    -- Número do numero_residencia
    -- TODO: Adicione a coluna 'numero_residencia' como TEXT NOT NULL

    -- Bloco/prédio (A, B, C, etc.)
    -- TODO: Adicione a coluna 'bloco' como TEXT DEFAULT 'A'

    -- Telefone para contato
    -- TODO: Adicione a coluna 'telefone' como TEXT

    -- Email para contato (opcional, mas se informado precisa ter '@' e '.')
    -- TODO: Adicione a coluna 'email' como TEXT
    --       com CHECK(email LIKE '%@%.%') para validação básica de formato

    -- Tipo do morador: proprietário ou inquilino
    -- TODO: Adicione a coluna 'tipo_morador' como TEXT DEFAULT 'proprietario'
    --       com CHECK(tipo_morador IN ('proprietario', 'inquilino'))

    -- Foto do morador (caminho do arquivo)
    -- TODO: Adicione a coluna 'foto_url' como TEXT

    -- Validade da foto (renovar a cada 2 anos)
    -- TODO: Adicione a coluna 'dt_foto_validade' como TEXT

    -- Biometria digital (hash criptográfico, NUNCA a imagem real)
    -- TODO: Adicione a coluna 'biometria_hash' como TEXT

    -- Validade da biometria (renovar a cada 2 anos)
    -- TODO: Adicione a coluna 'dt_biometria_validade' como TEXT

    -- Flag indicando se o morador está ativo (1 = ativo, 0 = inativo)
    -- TODO: Adicione a coluna 'ativo' como BOOLEAN DEFAULT 1
    --       com CHECK(ativo IN (0, 1)) para garantir valor booleano
    --       (SQLite armazena BOOLEAN como INTEGER internamente, mas BOOLEAN
    --        deixa o schema mais legível para quem vai trabalhar no projeto)

    -- Data/hora de criação do registro
    -- TODO: Adicione a coluna 'dt_criado_em' como TEXT DEFAULT CURRENT_TIMESTAMP

    -- Data/hora da última atualização
    -- TODO: Adicione a coluna 'dt_atualizado_em' como TEXT DEFAULT CURRENT_TIMESTAMP

);

-- Explicação de cada tipo de dado:
-- INTEGER: números inteiros (id, ativo)
-- TEXT: texto (nome, cpf, bloco, telefone, email, tipo_morador, foto_url, etc.)
-- DATE: data no formato 'AAAA-MM-DD' (ex: '2028-04-09')
-- DATETIME: data e hora no formato 'AAAA-MM-DD HH:MM:SS'
-- PRIMARY KEY: garante que cada ID é único e não nulo
-- AUTOINCREMENT: o banco gera o número sozinho (1, 2, 3...)
-- NOT NULL: garante que a coluna sempre tem um valor
-- UNIQUE: garante que não há valores duplicados
-- DEFAULT: valor padrão se nenhum for fornecido
-- CHECK: regra de validação — o banco RECUSA dados inválidos
--   Exemplos de CHECK:
--   CHECK(length(cpf) = 11)        → CPF deve ter exatamente 11 dígitos
--   CHECK(email LIKE '%@%.%')      → email deve ter '@' e '.'
--   CHECK(ativo IN (0, 1))         → só aceita 0 ou 1 (valor booleano)
--   CHECK(tipo IN ('a', 'b', 'c')) → só aceita valores da lista
