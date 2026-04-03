-- Aula 02: Schema do Banco de Dados
-- Este arquivo descreve a estrutura da tabela de moradores

-- TODO: Complete a instrução CREATE TABLE abaixo
-- Você precisa adicionar as colunas que faltam entre os comentários TODO
-- Use TEXT para texto (nome, email, etc.) e INTEGER para números (id, apartamento, etc.)
-- Revise a teoria no README.md para lembrar da sintaxe!

CREATE TABLE moradores (
    -- Identificador único (PRIMARY KEY significa "chave única")
    -- TODO: Adicione a coluna 'id' como INTEGER PRIMARY KEY

    -- Nome completo do morador
    -- TODO: Adicione a coluna 'nome' como TEXT e NOT NULL (obrigatório)

    -- CPF do morador (sem formatação: apenas números)
    -- TODO: Adicione a coluna 'cpf' como TEXT UNIQUE (cada CPF é único)

    -- Número do apartamento
    -- TODO: Adicione a coluna 'apartamento' como INTEGER

    -- Bloco/prédio (A, B, C, etc.)
    -- TODO: Adicione a coluna 'bloco' como TEXT DEFAULT 'A'

    -- Telefone para contato
    -- TODO: Adicione a coluna 'telefone' como TEXT

    -- Email para contato
    -- TODO: Adicione a coluna 'email' como TEXT

    -- Flag indicando se o morador está ativo (1 = ativo, 0 = inativo)
    -- TODO: Adicione a coluna 'ativo' como INTEGER DEFAULT 1

    -- Data/hora de criação do registro
    -- TODO: Adicione a coluna 'criado_em' como TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- Explicação de cada tipo de dado:
-- INTEGER: números inteiros (id, apartamento, ativo)
-- TEXT: texto (nome, cpf, bloco, telefone, email)
-- TIMESTAMP: data e hora (criado_em)
-- PRIMARY KEY: garante que cada ID é único e não nulo
-- NOT NULL: garante que a coluna sempre tem um valor
-- UNIQUE: garante que não há valores duplicados
-- DEFAULT: valor padrão se nenhum for fornecido
