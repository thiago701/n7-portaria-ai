# Aula 03 — CRUD: As 4 Operações Mágicas do Programador

**Data:** 17 de abril de 2026
**Duração:** 2 horas
**Objetivo:** Dominar as 4 operações fundamentais de qualquer sistema de dados

---

## A Magia do CRUD

Você já parou para pensar em como seu celular guarda nomes na agenda de contatos? Pois é... tudo funciona com 4 operações simples que todo programador do mundo usa!

### A Analogia do Seu Celular

Imagine sua agenda de contatos telefônicos:

- **C** de **Create** (Criar/Cadastrar): Quando você adiciona um novo número na sua agenda
- **R** de **Read** (Ler/Consultar): Quando você abre a agenda e procura por um contato
- **U** de **Update** (Atualizar): Quando você muda o número de telefone de um amigo
- **D** de **Delete** (Deletar/Remover): Quando você apaga um contato que não precisa mais

Pois é! Essas 4 operações — **CRUD** — são exatamente o que todo programa faz com dados. Banco de dados, aplicativos, sites... todos usam CRUD!

---

## O que Vamos Aprender Hoje?

### Parte 1: Teoria (30 minutos)

1. **O que é CRUD?**
   - As 4 operações mágicas que todo dado precisa
   - Por que CRUD é importante

2. **Funções em Python** (revisão)
   - Recapitulando def, parâmetros e retorno
   - Organizando código com funções

3. **Trabalhando com SQLite3**
   - Conectando ao banco de dados
   - Executando comandos SQL a partir do Python
   - Confirmando mudanças com commit()

4. **Tratamento de Erros Básico**
   - O bloco try/except
   - Como proteger seu código de falhas
   - Mensagens de erro úteis para o usuário

### Parte 2: Prática (1 hora e 30 minutos)

**Projeto: Sistema CRUD Completo de Moradores**

Vamos construir um sistema completo onde você pode:
- Cadastrar novos moradores com nome, CPF, apartamento e email
- Listar todos os moradores cadastrados
- Buscar um morador pelo nome
- Atualizar os dados de um morador
- Desativar um morador (sem deletar, apenas marcar como inativo)

Tudo será feito através de um **menu de texto** amigável, exatamente como você faria em um sistema profissional!

---

## Checklist de Aprendizado

Ao final dessa aula, você deve conseguir:

- [ ] Entender o conceito de CRUD e suas 4 operações
- [ ] Usar try/except para tratar erros em Python
- [ ] Conectar e consultar um banco de dados SQLite a partir do Python
- [ ] Escrever uma função para cadastrar dados (CREATE)
- [ ] Escrever uma função para listar dados (READ)
- [ ] Escrever uma função para buscar dados (READ específico)
- [ ] Escrever uma função para atualizar dados (UPDATE)
- [ ] Escrever uma função para desativar dados (DELETE macio)
- [ ] Criar um menu de texto que coordena todas essas operações
- [ ] Validar dados antes de salvar (por exemplo, evitar CPF duplicado)
- [ ] Fazer commit do seu trabalho no Git

---

## Estrutura da Aula

```
aula-03_2026-04-17/
├── README.md                      (este arquivo - teoria e conceitos)
├── material-complementar.md        (vídeos e artigos para aprender mais)
└── exercicio/
    ├── INSTRUCOES.md              (passo a passo do que fazer)
    └── moradores_crud.py          (seu arquivo de trabalho - incompleto!)
```

---

## Dicas para Aproveitar Melhor

1. **Leia a teoria com calma.** Não é muita coisa, e compreender o conceito é mais importante que correr.

2. **Não se apresse com o código.** A prática é feita para você aprender. Se errar, ótimo! Erros são aulas.

3. **Use o arquivo de instruções.** O arquivo `exercicio/INSTRUCOES.md` guia você passo a passo.

4. **Teste cada função.** Após implementar uma operação CRUD, teste ela sozinha antes de passar para a próxima.

5. **Pergunte!** Se tiver dúvida, melhor perguntar do que ficar perdido.

---

## Próximos Passos

Após essa aula, você estará pronto para:
- Entender como qualquer aplicativo guarda e recupera dados
- Começar a trabalhar com dados reais em Python
- Perceber que CRUD aparece em TUDO na programação

Vamos lá? Mãos à obra! 🚀

