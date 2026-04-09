# n7-portaria-ai — Requisitos Funcionais

> **Versao:** 2.0 | **Data:** 09/04/2026
> **Classificacao:** RF = Requisito Funcional | Prioridade: P1 (essencial), P2 (importante), P3 (desejavel)
> **Changelog v2.0:** Novos RFs para N:N moradores/residencias, 2FA, LGPD, correlation_id, config_acesso, assinatura_condominio

---

## Módulo 1 — Cadastro de Moradores

| ID | Requisito | Prioridade | Aula |
|----|-----------|------------|------|
| RF-001 | O sistema deve permitir cadastrar um morador com: nome completo, CPF (11 digitos), telefone, e-mail, foto (BLOB, renovada a cada 2 anos) e biometria digital (BLOB, renovada a cada 2 anos). Dados de residencia sao vinculados via morador_residencia (N:N). | P1 | 03 |
| RF-002 | O sistema deve listar todos os moradores cadastrados com JOIN em residencias (via morador_residencia) | P1 | 03 |
| RF-003 | O sistema deve permitir buscar morador por nome, CPF ou numero_residencia (via JOIN) | P1 | 04 |
| RF-004 | O sistema deve permitir editar dados pessoais de um morador (telefone, email). Dados de residencia sao editados separadamente. | P1 | 04 |
| RF-005 | O sistema deve permitir desativar (soft delete) um morador (ativo=0, dados preservados) | P2 | 04 |
| RF-006 | O sistema deve validar CPF (11 digitos) e email (formato basico) antes de salvar | P2 | 05 |
| RF-007 | O sistema deve impedir cadastro duplicado (CPF UNIQUE no banco) | P1 | 03 |

---

## Módulo 2 — Registro de Visitantes

| ID | Requisito | Prioridade | Aula |
|----|-----------|------------|------|
| RF-008 | O sistema deve permitir registrar um visitante com: nome, documento (RG/CPF), motivo da visita e morador visitado | P1 | 06 |
| RF-009 | O sistema deve registrar data e hora de entrada automaticamente | P1 | 06 |
| RF-010 | O sistema deve permitir registrar a hora de saída do visitante | P1 | 07 |
| RF-011 | O sistema deve listar visitantes presentes no momento (sem saída registrada) | P1 | 07 |
| RF-012 | O sistema deve exibir histórico de visitas por morador | P2 | 08 |
| RF-013 | O sistema deve exibir histórico de visitas por período | P2 | 08 |
| RF-014 | O sistema deve alertar se visitante está na lista de bloqueio | P2 | 10 |

---

## Módulo 3 — Controle de Acesso

| ID | Requisito | Prioridade | Aula |
|----|-----------|------------|------|
| RF-015 | O sistema deve gerar um log de cada entrada/saída com timestamp | P1 | 07 |
| RF-016 | O sistema deve permitir que morador autorize acesso antecipado | P2 | 09 |
| RF-017 | O sistema deve respeitar regras de horário de acesso (ex: visitantes até 22h) | P3 | 10 |
| RF-018 | O sistema deve manter lista de bloqueio de visitantes | P2 | 10 |
| RF-019 | O sistema deve registrar qual porteiro realizou cada operação | P2 | 09 |

---

## Módulo 4 — Notificações

| ID | Requisito | Prioridade | Aula |
|----|-----------|------------|------|
| RF-020 | O sistema deve notificar o morador quando um visitante solicitar acesso | P1 | 11 |
| RF-021 | O sistema deve permitir que o morador autorize ou recuse pelo sistema | P2 | 12 |
| RF-022 | O sistema deve enviar resumo diário de movimentação ao síndico | P3 | 14 |
| RF-023 | O sistema deve alertar quando houver tentativa de acesso fora do horário | P3 | 14 |

---

## Módulo 5 — Assistente IA

| ID | Requisito | Prioridade | Aula |
|----|-----------|------------|------|
| RF-024 | O sistema deve oferecer um chatbot para o porteiro consultar informações | P1 | 13 |
| RF-025 | A IA deve responder perguntas como "Quem mora no apto 301?" | P1 | 13 |
| RF-026 | A IA deve sugerir informações relevantes (ex: "Este visitante esteve aqui 3x esta semana") | P2 | 15 |
| RF-027 | A IA deve gerar relatórios sob demanda por comando de texto | P3 | 16 |
| RF-028 | A IA deve funcionar offline com respostas básicas (cache de dados) | P3 | 18 |

---

## Módulo 6 — Dashboard e Relatórios

| ID | Requisito | Prioridade | Aula |
|----|-----------|------------|------|
| RF-029 | O sistema deve exibir painel com métricas do dia (entradas, saídas, total visitantes) | P1 | 15 |
| RF-030 | O sistema deve exibir gráfico de movimentação por hora do dia | P2 | 16 |
| RF-031 | O sistema deve exibir gráfico de movimentação semanal/mensal | P2 | 16 |
| RF-032 | O sistema deve permitir exportar relatórios em PDF | P3 | 17 |
| RF-033 | O sistema deve permitir exportar relatórios em CSV | P3 | 17 |

---

## Módulo 7 — Gestão de Funcionários e Veículos *(v3.0 — contribuição do aluno)*

| ID | Requisito | Prioridade | Aula |
|----|-----------|------------|------|
| RF-034 | O sistema deve permitir cadastrar funcionários com: nome, CPF, cargo, setor e login/senha (hash) | P2 | 09 |
| RF-035 | O sistema deve diferenciar perfis: porteiro, zelador, administrador | P2 | 09 |
| RF-036 | O sistema deve permitir cadastrar veículos vinculados a moradores, funcionários ou visitantes | P2 | 10 |
| RF-037 | O sistema deve registrar qual funcionário efetuou cada registro de acesso | P2 | 07 |
| RF-038 | O sistema deve registrar o veículo utilizado no acesso (quando aplicável) | P3 | 10 |

---

## Modulo 8 — Residencias e Vinculo N:N *(novo — v8.0, 09/04/2026)*

| ID | Requisito | Prioridade | Aula |
|----|-----------|------------|------|
| RF-039 | O sistema deve permitir cadastrar residencias com: codigo_condominio, numero, bloco, quadra, andar, tipo_moradia, interfone, observacao | P1 | 02 |
| RF-040 | O sistema deve suportar relacao N:N entre moradores e residencias (um morador pode ter varias unidades, uma unidade pode ter varios moradores) | P1 | 02 |
| RF-041 | O sistema deve registrar tipo_morador (proprietario/inquilino) no vinculo morador_residencia, nao no morador | P1 | 02 |
| RF-042 | O sistema deve permitir historico de vinculos (dt_inicio, dt_fim) para rastrear mudancas | P2 | 08 |

---

## Modulo 9 — Seguranca e Autenticacao 2FA *(novo — v8.0, 09/04/2026)*

| ID | Requisito | Prioridade | Aula |
|----|-----------|------------|------|
| RF-043 | Todo registro de acesso deve ter pelo menos 1 fator de autenticacao (auth_senha, auth_digital ou auth_facial) | P1 | 10 |
| RF-044 | O sistema deve permitir configurar politica de seguranca individual por morador (1 ou 2 fatores requeridos) | P2 | 10 |
| RF-045 | O sistema deve permitir ativar/desativar tipos de autenticacao por morador (senha, digital, facial) | P2 | 10 |
| RF-046 | Moradores sem config_acesso_morador usam o padrao do condominio (1 fator, qualquer tipo) | P2 | 10 |

---

## Modulo 10 — LGPD e Conformidade *(novo — v8.0, 09/04/2026)*

| ID | Requisito | Prioridade | Aula |
|----|-----------|------------|------|
| RF-047 | O sistema deve armazenar os termos LGPD aceitos pelo morador como BLOB (PDF original) | P2 | 09 |
| RF-048 | O sistema deve registrar data/hora do aceite LGPD (dt_aceite_lgpd). NULL = pendente. | P2 | 09 |
| RF-049 | O sistema deve permitir consultar moradores com aceite LGPD pendente | P2 | 09 |
| RF-050 | O sistema deve usar correlation_id (SHA-256) em todas as tabelas para sincronizacao entre bancos | P2 | 02 |

---

## Modulo 11 — Assinatura do Condominio *(novo — v8.0, 09/04/2026)*

| ID | Requisito | Prioridade | Aula |
|----|-----------|------------|------|
| RF-051 | O sistema deve registrar a assinatura/contrato do condominio com o servico n7-portaria-ai | P2 | — |
| RF-052 | Cada condominio pode ter no maximo 1 assinatura ativa (UNIQUE codigo_condominio) | P1 | — |
| RF-053 | O sistema deve armazenar o PDF do contrato assinado como BLOB | P3 | — |
| RF-054 | O sistema deve rastrear status da assinatura (ativo, pendente, vencido, cancelado) | P2 | — |

---

## Regras de Negocio

| ID | Regra | Modulo |
|----|-------|--------|
| RN-001 | Todo visitante deve estar vinculado a pelo menos um morador | Mod. 2 |
| RN-002 | Um morador desativado nao pode receber visitantes | Mod. 1, 2 |
| RN-003 | O registro de saida nao pode ser anterior ao de entrada | Mod. 3 |
| RN-004 | Visitantes na lista de bloqueio geram alerta mas nao sao impedidos automaticamente (decisao humana) | Mod. 3 |
| RN-005 | O sistema deve manter historico de todos os acessos por no minimo 12 meses | Mod. 3 |
| RN-006 | Apenas administradores podem gerenciar a lista de bloqueio | Mod. 3 |
| RN-007 | O porteiro e o operador padrao do sistema; moradores tem acesso limitado | Geral |
| RN-008 | Um morador pode ser proprietario de uma unidade e inquilino de outra simultaneamente | Mod. 8 |
| RN-009 | Nenhum acesso pode ser registrado sem pelo menos 1 fator de autenticacao | Mod. 9 |
| RN-010 | Dados biometricos (foto, digital) tem validade de 2 anos e devem ser renovados | Mod. 1 |
| RN-011 | Senhas de funcionarios NUNCA sao armazenadas em texto puro — apenas SHA-256 | Mod. 7 |
| RN-012 | Registros de acesso NUNCA sao deletados — apenas consultas e insercoes | Mod. 3 |

---

## Mapeamento Modulo x Aulas (Fase 1 — Abril 2026)

| Aula | Data | Modulo | Requisitos Cobertos | Status |
|------|------|--------|---------------------|--------|
| 01 | 03/04 | — | Setup do projeto, ambiente, estrutura de pastas | CONCLUIDA |
| 02 | 09/04 | Mod. 1, 8, 10 | Banco completo (9 tabelas), DBeaver+SQLite, dominio Python (morador.py), RF-001 parcial, RF-039 a RF-042, RF-050 | CONCLUIDA |
| 03 | 16/04 | Mod. 1 | CRUD moradores completo (RF-001, RF-002, RF-007) | PENDENTE |
| 04 | 23/04 | Mod. 1 | API REST + busca e edicao (RF-003, RF-004, RF-005) | PENDENTE |
| 05 | 30/04 | Mod. 1 | Interface grafica desktop + validacoes (RF-006, CustomTkinter) | PENDENTE |

---

*Cada requisito sera detalhado em historias de usuario no momento da aula correspondente.*
