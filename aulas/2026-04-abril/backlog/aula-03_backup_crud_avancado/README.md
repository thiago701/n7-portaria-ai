# Aula 03 — CRUD Avançado: Visitantes, JOINs e Organização do Código

**Data:** 16 de abril de 2026
**Duração:** 2 horas
**Pré-requisito:** Aula 02 concluída (CRUD de moradores funcionando)

---

## Recapitulação: O que Você Já Construiu

Até agora, seu progresso é impressionante:

**Tarefa antecipada (antes da Aula 02):**
- Criou o banco `portaria.db` com 3 tabelas: moradores, visitantes e acessos
- Praticou SQL: CREATE TABLE, INSERT, SELECT, UPDATE, JOIN, GROUP BY
- Resolveu 10 exercícios SQL

**Aula 02:**
- Conectou o banco de dados ao Python com sqlite3
- Implementou CRUD completo de moradores (cadastrar, listar, buscar, atualizar, desativar)
- Criou menu interativo de texto
- Aprendeu try/except para tratar erros
- Validou CPF duplicado antes de cadastrar

**Hoje vamos expandir esse sistema!**

---

## O que Vamos Aprender Hoje

### Parte 1: Teoria (30 minutos)

#### 1.1 CRUD de Visitantes — Reutilizando o Padrão

Você já sabe fazer CRUD de moradores. A boa notícia: o CRUD de visitantes segue **exatamente o mesmo padrão!**

| Operação | Moradores (você já fez!) | Visitantes (hoje!) |
|----------|--------------------------|---------------------|
| CREATE | `INSERT INTO moradores ...` | `INSERT INTO visitantes ...` |
| READ | `SELECT * FROM moradores` | `SELECT * FROM visitantes` |
| UPDATE | `UPDATE moradores SET ...` | `UPDATE visitantes SET ...` |
| DELETE | `UPDATE moradores SET ativo = 0` | `UPDATE visitantes SET bloqueado = 1` |

A única diferença é que visitantes não têm "ativo" — eles têm "bloqueado". Bloquear um visitante é como desativar um morador.

#### 1.2 JOINs no Python — Cruzando Tabelas

Na tarefa antecipada você praticou JOINs no SQL puro. Hoje vamos executar essas mesmas consultas pelo Python!

```python
# Listar todos os acessos com nomes (visitante + morador)
cursor.execute("""
    SELECT v.nome AS visitante, m.nome AS morador, m.numero_residencia, a.motivo, a.dt_entrada_em
    FROM acessos a
        JOIN visitantes v ON a.visitante_id = v.id
        JOIN moradores  m ON a.morador_id   = m.id
    ORDER BY a.dt_entrada_em DESC
""")
```

É o mesmo SQL! O Python só executa e mostra bonito na tela.

#### 1.3 Organizando o Código — Funções Bem Separadas

Até agora, nosso código está todo em um arquivo só. Isso funciona, mas começa a ficar grande. Vamos aprender a organizar melhor:

```
moradores_crud.py          ← Aula 02 (tudo junto, funcionou!)

sistema_portaria.py        ← Aula 03 (organizado!)
├── Funções de conexão     ← Conectar/desconectar banco
├── Funções de moradores   ← CRUD moradores (você já fez)
├── Funções de visitantes  ← CRUD visitantes (NOVO!)
├── Funções de acessos     ← Registrar entrada/saída (NOVO!)
├── Funções de relatórios  ← Resumo do condomínio (NOVO!)
└── Menu principal         ← Menu expandido
```

**Princípio:** Cada grupo de funções cuida de UMA responsabilidade. Isso facilita encontrar e corrigir problemas.

#### 1.4 Registrando Acessos — Entrada e Saída de Visitantes

A tabela `acessos` é onde registramos quem entrou e quem saiu. O fluxo real é:

1. Visitante chega na portaria
2. Porteiro verifica se não está bloqueado
3. Porteiro registra entrada (INSERT em acessos)
4. Visitante sai
5. Porteiro registra saída (UPDATE em acessos — preenche `dt_saida_em`)

Vamos implementar esse fluxo em Python!

---

### Parte 2: Prática (1h30)

**Projeto: Expandir o Sistema de Portaria**

Vamos evoluir o `moradores_crud.py` para um sistema mais completo:

1. **CRUD de Visitantes** — Cadastrar, listar, buscar e bloquear visitantes
2. **Registro de Acessos** — Registrar entrada e saída
3. **Consultas com JOIN** — Ver quem está dentro do condomínio, histórico de visitas
4. **Relatório do Condomínio** — Resumo com estatísticas (total de moradores, visitantes, acessos)

---

## Checklist de Aprendizado

Ao final desta aula, você conseguirá:

- [ ] Implementar CRUD de visitantes reutilizando o padrão da Aula 02
- [ ] Executar consultas JOIN pelo Python
- [ ] Registrar entrada e saída de visitantes no sistema
- [ ] Verificar se um visitante está bloqueado antes de autorizar entrada
- [ ] Gerar um relatório/resumo do condomínio
- [ ] Organizar funções por responsabilidade
- [ ] Entender o fluxo completo: visitante chega → porteiro consulta → autoriza → registra
- [ ] Fazer commit do seu trabalho no Git

---

## Estrutura da Aula

```
aula-03/
├── README.md                       ← Este arquivo (teoria e conceitos)
├── material-complementar.md        ← Vídeos e artigos extras
└── exercicio/
    ├── INSTRUCOES.md               ← Passo a passo detalhado
    └── sistema_portaria.py         ← Seu arquivo de trabalho
```

---

## Dicas para Aproveitar Melhor

1. **Reutilize o que já sabe.** CRUD de visitantes é muito parecido com moradores — copie e adapte!
2. **Teste cada função isoladamente.** Não espere terminar tudo para testar.
3. **Lembre dos exercícios SQL.** As consultas JOIN que você praticou na tarefa antecipada são as mesmas que vai usar aqui.
4. **Se travar, olhe o código da Aula 02.** Ele é seu melhor modelo.

---

## Próximos Passos

Após essa aula, você terá um sistema funcional com:
- Gerenciamento completo de moradores e visitantes
- Controle de entrada e saída
- Relatórios do condomínio

Na **Aula 04**, vamos transformar isso em uma **API REST com Flask** — o primeiro passo para que o sistema funcione na web!

Vamos lá? Mãos à obra!
