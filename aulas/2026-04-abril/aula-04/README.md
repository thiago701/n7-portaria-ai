# Aula 04 — API REST: O Garçom Digital do Nosso Sistema

**Data:** 23 de abril de 2026
**Duração:** 2 horas
**Objetivo:** Criar sua primeira API REST e entender como sistemas conversam pela internet

---

## A Analogia do Garçom Digital

Você já parou para pensar no que um garçom faz no restaurante?

Um **garçom:**
1. **Recebe seu pedido** (você pede um café)
2. **Leva o pedido para a cozinha**
3. **Aguarda a cozinha preparar**
4. **Traz a resposta** (seu café pronto)

Pois é! Uma **API REST** funciona exatamente assim!

### Como Funciona a Analogia:

- **Você** = Cliente (seu navegador ou celular)
- **Garçom** = API REST (nosso servidor Flask)
- **Cozinha** = Banco de dados e funções
- **Pedido** = Requisição HTTP (GET, POST, DELETE)
- **Comida pronta** = Resposta JSON (os dados)

Quando você acessa um site como o Google, seu navegador funciona como um cliente pedindo informações. O servidor (garçom digital) recebe, processa e devolve a resposta. É assim que a internet funciona!

---

## O que Vamos Aprender Hoje?

### Parte 1: Teoria (30 minutos)

1. **O que é um Servidor Web?**
   - Como computadores conversam pela internet
   - Porta, localhost, IP — entendendo os endereços
   - Por que temos servidores?

2. **HTTP: A Língua da Internet**
   - GET: Pedir informações (como pedir um café)
   - POST: Enviar informações (como fazer um pedido)
   - DELETE: Remover dados (como cancelar um prato)
   - PUT/PATCH: Atualizar dados

3. **O que é Flask?**
   - A biblioteca Python para criar servidores web
   - Rotas e como elas funcionam
   - Decoradores @app.route() - como endereços do servidor

4. **JSON: A Linguagem Universal da Web**
   - Por que JSON é importante
   - Estrutura de dados: chaves e valores
   - Como Python transforma dados em JSON e vice-versa

### Parte 2: Prática (1 hora e 30 minutos)

**Projeto: Sua Primeira API de Moradores**

Vamos criar um servidor que gerencia a lista de moradores do condomínio:

- Uma rota de boas-vindas (`/`)
- Listar todos os moradores (`GET /api/moradores`)
- Adicionar um novo morador (`POST /api/moradores`)
- Buscar um morador específico (`GET /api/moradores/<id>`)

Você poderá testar tudo usando:
- Seu navegador (para requisições GET)
- Ferramentas especiais como Postman (para POST, DELETE, etc.)

---

## Checklist de Aprendizado

Ao final dessa aula, você deve conseguir:

- [ ] Entender o que é um servidor web e como funciona
- [ ] Explicar o que é uma API REST usando a analogia do garçom
- [ ] Conhecer os métodos HTTP: GET, POST, DELETE
- [ ] Instalar Flask no seu computador
- [ ] Criar um servidor Flask funcionando em localhost
- [ ] Entender o que são rotas e como defini-las
- [ ] Usar @app.route() para criar endpoints
- [ ] Retornar dados em formato JSON
- [ ] Listar dados de um banco SQLite via API
- [ ] Adicionar dados via POST (enviando JSON)
- [ ] Buscar um item específico por ID
- [ ] Testar sua API com o navegador e ferramentas
- [ ] Fazer commit do seu trabalho no Git

---

## Estrutura da Aula

```
aula-04_2026-04-23/
├── README.md                      (este arquivo - teoria e conceitos)
├── material-complementar.md        (vídeos e artigos para aprender mais)
└── exercicio/
    ├── INSTRUCOES.md              (passo a passo do que fazer)
    └── app.py                     (seu arquivo de trabalho - incompleto!)
```

---

## Dicas para Aproveitar Melhor

1. **Comece com a teoria.** A analogia do garçom vai fazer muito sentido quando você escrever o código.

2. **Não se preocupe com portas e localhost.** Você vai ver que é mais simples do que parece.

3. **Use o arquivo de instruções.** O arquivo `exercicio/INSTRUCOES.md` guia você passo a passo até o final.

4. **Teste cada rota.** Depois de criar uma rota nova, teste ela no navegador ou em uma ferramenta antes de passar para a próxima.

5. **JSON é só texto.** JSON parece complicado, mas é apenas uma forma de organizar dados em texto — como um formulário preenchido.

6. **Erros são amigos.** Se der erro na API, a mensagem vai te ajudar a entender o que está errado.

---

## Próximos Passos

Após essa aula, você estará pronto para:
- Entender como qualquer aplicativo móvel se conecta a um servidor
- Criar endpoints mais complexos para seu sistema de portaria
- Trabalhar com segurança e validação de dados
- Publicar seu servidor na internet

---

**Vamos começar? Hora de criar nosso primeiro servidor web! 🚀**

Parabéns por chegar até aqui, Ademilson. Você está prestes a entender como toda a internet realmente funciona.
