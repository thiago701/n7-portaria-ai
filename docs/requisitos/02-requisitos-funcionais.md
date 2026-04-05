# n7-portaria-ai — Requisitos Funcionais

> **Versão:** 1.0 | **Data:** 03/04/2026
> **Classificação:** RF = Requisito Funcional | Prioridade: P1 (essencial), P2 (importante), P3 (desejável)

---

## Módulo 1 — Cadastro de Moradores

| ID | Requisito | Prioridade | Aula |
|----|-----------|------------|------|
| RF-001 | O sistema deve permitir cadastrar um morador com: nome completo, CPF, numero_residencia, bloco, telefone, e-mail, tipo de morador (proprietário/inquilino), foto (renovada a cada 2 anos) e biometria digital (renovada a cada 2 anos) | P1 | 03 |
| RF-002 | O sistema deve listar todos os moradores cadastrados com paginação | P1 | 03 |
| RF-003 | O sistema deve permitir buscar morador por nome ou numero_residencia | P1 | 04 |
| RF-004 | O sistema deve permitir editar dados de um morador | P1 | 04 |
| RF-005 | O sistema deve permitir desativar (soft delete) um morador | P2 | 04 |
| RF-006 | O sistema deve validar CPF antes de salvar | P2 | 05 |
| RF-007 | O sistema deve impedir cadastro duplicado (mesmo CPF) | P1 | 03 |

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

## Regras de Negócio

| ID | Regra | Módulo |
|----|-------|--------|
| RN-001 | Todo visitante deve estar vinculado a pelo menos um morador | Mod. 2 |
| RN-002 | Um morador desativado não pode receber visitantes | Mod. 1, 2 |
| RN-003 | O registro de saída não pode ser anterior ao de entrada | Mod. 3 |
| RN-004 | Visitantes na lista de bloqueio geram alerta mas não são impedidos automaticamente (decisão humana) | Mod. 3 |
| RN-005 | O sistema deve manter histórico de todos os acessos por no mínimo 12 meses | Mod. 3 |
| RN-006 | Apenas administradores podem gerenciar a lista de bloqueio | Mod. 3 |
| RN-007 | O porteiro é o operador padrão do sistema; moradores têm acesso limitado | Geral |

---

## Mapeamento Módulo × Aulas (Primeiras 5 Aulas - Fase 1)

| Aula | Data | Módulo | Requisitos Cobertos |
|------|------|--------|---------------------|
| 01 | 03/04 | — | Setup do projeto, ambiente, estrutura de pastas |
| 02 | 09/04 | Mod. 1 (base + expansão) | Banco de dados, schema completo (moradores, visitantes, acessos), RF-001 e estrutura para Mod. 2-3 |
| 03 | 16/04 | Mod. 1 | CRUD moradores completo (RF-001, RF-002, RF-007) |
| 04 | 23/04 | Mod. 1 | API REST + busca e edição (RF-003, RF-004, RF-005) |
| 05 | 30/04 | Mod. 1 | Interface gráfica desktop + validações (RF-006, CustomTkinter) |

---

*Cada requisito será detalhado em histórias de usuário no momento da aula correspondente.*
