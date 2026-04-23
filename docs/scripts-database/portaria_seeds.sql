-- ============================================================================
-- PORTARIA INTELIGENTE — SEEDS (v1.1)
-- ============================================================================
-- Pré-requisito: schema criado (portaria_schema.sql)
-- Rodar: psql -d portaria -f portaria_seeds.sql
-- ============================================================================

BEGIN;

-- PARTE 3: SEEDS
-- ============================================================================

-- 3.0 — Precisa existir condomínio antes das residências (por conta da nova FK)
INSERT INTO assinatura_condominio
    (codigo_condominio, nome_condominio, endereco, numero_contrato,
     dt_vigencia_inicio, status, correlation_id)
VALUES
    ('COND-001', 'Residencial Exemplo', 'Rua das Palmeiras, 100',
     'CT-2024-0001', '2024-01-01', 'ativo',
     'cc0000000000000000000000000000000000000000000000000000000000cc01');

-- 3.1 — Moradores (todos ativos exigem dt_aceite_lgpd preenchido — CHECK)
INSERT INTO moradores (nome, cpf, telefone, email, ativo, dt_aceite_lgpd, foto, dt_foto_validade, biometria, dt_biometria_validade, correlation_id) VALUES
    ('Joao Carlos da Silva',    '11122233344','83999001122','joao.silva@email.com',      TRUE,'2026-04-09 10:00:00', NULL,'2028-04-09', NULL,'2028-04-09','72104cb9e6cf2f1ac722a5513d1145b32a94fdc216e2ff09c991f88e5e343e8a'),
    ('Maria Aparecida Santos',  '55566677788','83988112233','maria.santos@email.com',    TRUE,'2026-04-09 10:00:00', NULL,'2028-04-09', NULL, NULL,         'acec16f37ddd60d6ab79d892a5e2b6d8c5fed2e7c7d23a28eebc9fc84205f8bb'),
    ('Pedro Henrique Oliveira', '99988877766','83977223344','pedro.oliveira@email.com',  TRUE,'2026-04-09 10:00:00', NULL, NULL,         NULL, NULL,         '16b60edc33103400e13f71c96d9b69d2c70c1592938e42586e68f2dc1eddba49'),
    ('Ana Paula Ferreira',      '44433322211','83966334455','ana.ferreira@email.com',    TRUE,'2026-04-09 10:00:00', NULL,'2028-04-09', NULL,'2028-04-09','33d18f4959453b7f40ec89b81f289fcfbe9853c0b6ff55723696994f24470690'),
    ('Carlos Eduardo Lima',     '77788899900','83955445566', NULL,                       TRUE,'2026-04-09 10:00:00', NULL, NULL,         NULL, NULL,         'c65ef5d5e73cb4f14ccac8d2e158f28b7a12370964116e8229929095b91fbc37'),
    ('Lucia Fernandes Gomes',   '12312312300','83922001133','lucia.gomes@email.com',     TRUE,'2026-04-09 10:00:00', NULL, NULL,         NULL,'2028-04-09','d34026bfb80b7750340269732c5f9df2311bd0f2e4345512d377e68c64d3b3ad'),
    ('Rafael Souza Mendes',     '45645645600','83911009988', NULL,                       TRUE,'2026-04-09 10:00:00', NULL, NULL,         NULL, NULL,         'a7171fb127844865bf7ea8807e3ddcf7592ed5a0c9a3d36759d5469ce5358be0'),
    ('Dona Teresa Albuquerque', '78978978700','83900112233','teresa.albuquerque@email.com',TRUE,'2026-04-09 10:00:00',NULL,'2028-04-09', NULL,'2028-04-09','302d4921ec2a44f2638ae243de0d9bf18953658719d3fe6d74d3dc30df923f6b'),
    ('Bruno Martins Costa',     '14725836900','83988776655','bruno.martins@email.com',   TRUE,'2026-04-09 10:00:00', NULL,'2025-03-15', NULL, NULL,         '0bc2e0e60c01f6c0f042f1ffced27dfdaa9a37a100d3bd942b03832d45e1594e'),
    -- Sergio está INATIVO — pela regra, não precisa de dt_aceite_lgpd
    ('Sergio Ramos Pereira',    '96385274100','83977665544','sergio.ramos@email.com',    FALSE, NULL,                 NULL, NULL,         NULL, NULL,         '9607837e767aaf6dd26683a4f4a4729c9828d6646157c9d0cd513218aef2d64a');

-- 3.2 — Residencias
INSERT INTO residencias (codigo_condominio, numero_residencia, bloco, quadra, andar, tipo_moradia, interfone, observacao, correlation_id) VALUES
    ('COND-001','101','A',   NULL, 1,'apartamento','101', NULL,                  '1ccd150e2b552bc7bb71a6bec19ff9110ce1a8a76cf0a1a81db6eaad16685b08'),
    ('COND-001','202','A',   NULL, 2,'apartamento','202', NULL,                  'f7e5a6c9f4e8156d0de4d6fdbe5a73d776ef5dfa76b62258fbc8d2a86f2782bc'),
    ('COND-001','303','B',   NULL, 3,'apartamento','303', NULL,                  '2f9251ab6a5c4338f485b4ac1e01e4ae7a811454b54ab5d999519c0f10ca24ab'),
    ('COND-001','104','A',   NULL, 1,'apartamento','104', NULL,                  'f132abc2f047e8f15468d8f9dbcce0973edfa50544aa4555addb37e79a6e5a1a'),
    ('COND-001','501','C',   NULL, 5,'apartamento','501', NULL,                  '826ae84e9c67b31c5a1bd069ea68bf5089dec85286e0b63253bd1ed3a48fee92'),
    ('COND-001','102','A',   NULL, 1,'apartamento','102', NULL,                  '1d362ac2452307e641e0e1aaa50783160346042b7af3ca948905e71d3f4dead5'),
    ('COND-001','08', NULL,  '03', NULL,'casa',      NULL,'Lote 08 da Quadra 03','3cb2c94dddc8eca081e06b962525ffdb72bb8f30582dcc64b077f48b8ff8997d'),
    ('COND-001','14', NULL,  '07', NULL,'casa',      NULL,'Lote 14 da Quadra 07','639310841f7f3c153c7f2d2d7733e5b83af825c8ee2fc440468132d1e5649f08'),
    ('COND-001','301',NULL,  NULL, 3,'apartamento','301','Predinho sem bloco',   '99814f834cc117b151dcc7d9c0cf5de717730bcc93c7b3782f82793e94e098f6'),
    ('COND-001','402','B',   NULL, 4,'apartamento','402', NULL,                  '921dfc608b24288ec61a9459b0090030708a5725f116a2d9b679121316b77b7e');

-- 3.3 — Vínculos morador x residência
INSERT INTO morador_residencia (morador_id, residencia_id, tipo_morador, dt_inicio, correlation_id) VALUES
    (1, 1, 'proprietario', '2024-01-10', 'e2fa727090a47afdcad043747f94d378b6e5865fed0291e72e417a7cddd63076'),
    (2, 2, 'inquilino',    '2025-06-01', 'd89c2b30b2ebd21654705b470d34ee61a829fbaf34ab464e21e5f61e0bbbff65'),
    (3, 3, 'proprietario', '2020-03-01', '2f78470e823125ec48c0efa7c236e06343889f11ed0d0c17b3ab42039fc6d6e3'),
    (4, 4, 'proprietario', '2023-03-15', '55bb9b3615a4ff69272decbaf4789c5ee904d6c6d502c98282dea2196dd3eb90');
    -- [ATENÇÃO] A linha que estava truncada no arquivo original ia aqui.
    -- Complete com o hash correto quando disponível. Exemplo:
    -- (4, 1, 'proprietario', '2023-03-15', '<HASH_SHA256_AQUI>');

COMMIT;
