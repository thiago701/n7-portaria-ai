# Exercício Aula 01 - Montando Seu Primeiro Projeto

**Objetivo:** Criar a estrutura completa do seu primeiro projeto e fazer seu primeiro commit no Git.

**Tempo estimado:** 1 hora e 30 minutos

**Materiais necessários:**
- Terminal (CMD no Windows, Terminal no Mac/Linux)
- Git instalado
- Python 3.11+ instalado
- Editor de texto (VSCode, PyCharm, ou similar)

---

## Passo 1: Criar a Estrutura de Pastas do Projeto

Vamos criar as pastas que o projeto precisa. Pense em cada pasta como um "cômodo" da casa do seu projeto.

### No seu terminal, faça isto:

```bash
# Crie a pasta principal do projeto
mkdir n7-portaria-ai
cd n7-portaria-ai

# Crie as subpastas principais
mkdir src
mkdir tests
mkdir docs
mkdir aulas
```

**O que você criou:**
- `src/` - Onde o código principal do seu sistema vai ficar
- `tests/` - Onde os testes automáticos vão ficar
- `docs/` - Documentação do projeto
- `aulas/` - Materiais das aulas

**Seu projeto deve parecer assim agora:**
```
n7-portaria-ai/
├── src/
├── tests/
├── docs/
└── aulas/
```

---

## Passo 2: Criar o Arquivo requirements.txt

Este arquivo é como uma "lista de compras" das bibliotecas que seu projeto usa.

### Faça isto:

```bash
# No terminal, dentro da pasta n7-portaria-ai, crie o arquivo:
echo "Flask==2.3.0" > requirements.txt
```

Ou manualmente:
1. Abra seu editor de texto
2. Crie um arquivo chamado `requirements.txt`
3. Escreva isto dentro:

```
Flask==2.3.0
```

4. Salve na pasta raiz de `n7-portaria-ai/`

**Por que Flask?**
Flask é uma biblioteca para criar aplicações web. Vamos usá-la em aulas futuras para criar a interface do nosso sistema de portaria.

---

## Passo 3: Criar e Ativar o Ambiente Virtual

O ambiente virtual é como criar um "cantinho só seu" para as bibliotecas do seu projeto.

### Windows:

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
venv\Scripts\activate
```

### Mac/Linux:

```bash
# Criar o ambiente virtual
python3 -m venv venv

# Ativar o ambiente virtual
source venv/bin/activate
```

**Como saber se funcionou?**

Veja o terminal. Se ativar bem, você verá algo assim:
```
(venv) C:\Users\seu-nome\n7-portaria-ai>
```

Aquele `(venv)` no começo significa "parabéns, o ambiente está ativo!"

### Instalar as Dependências

Agora que o ambiente está ativo, instale o Flask:

```bash
pip install -r requirements.txt
```

**O que aconteceu:** pip baixou a biblioteca Flask de acordo com o que está listado em requirements.txt e instalou no seu ambiente virtual.

---

## Passo 4: Copiar o Arquivo hello_portaria.py

Este é o seu primeiro script Python!

### Faça isto:

1. Abra a pasta `exercicio` neste repositório
2. Copie o arquivo `hello_portaria.py`
3. Cole dentro da pasta `src/` do seu projeto

**Seu projeto deve parecer assim agora:**
```
n7-portaria-ai/
├── src/
│   └── hello_portaria.py  ← Seu arquivo Python
├── tests/
├── docs/
├── aulas/
├── venv/
├── requirements.txt
```

---

## Passo 5: Completar os TODOs do Script

Abra o arquivo `hello_portaria.py` no seu editor.

Você verá comentários com **TODO** que indicam lugares onde você precisa escrever código.

### TODOs a Completar:

1. **TODO 1:** Na função `obter_nome_portaria()` - Pergunte ao usuário o nome da portaria
2. **TODO 2:** Na função `obter_nome_portaria()` - Retorne o nome digitado
3. **TODO 3:** Na função `main()` - Chame a função `obter_nome_portaria()` e guarde o resultado em uma variável
4. **TODO 4:** Na função `main()` - Chame a função `exibir_mensagem_boas_vindas()` com o nome da portaria

**Dica:** Observe o código já escrito. Procure por comentários em português que explicam o que fazer.

**Não sabe como fazer?** Volte ao README.md e procure no material complementar ou pergunte!

---

## Passo 6: Executar Seu Script

Vamos ver seu código funcionando!

### No terminal (com o ambiente virtual ativo):

```bash
python src/hello_portaria.py
```

**Esperado:** O script deve perguntar o nome da portaria, você digita, e recebe uma mensagem formatada.

**Exemplo:**
```
Bem-vindo ao Sistema de Portaria Inteligente!
Digite o nome da sua portaria: Portaria Central
=========================================
Olá Portaria Central!
Você está usando o Sistema de Portaria v1.0.0
Vamos gerenciar seu condominio com inteligência!
=========================================
```

**Se der erro:** Não é problema! Erros são normais.
- Leia a mensagem de erro com calma
- Procure pela linha do erro
- Verifique se o código está igual aos TODOs preenchidos
- Se ainda não conseguir, volte para o passo anterior

---

## Passo 7: Inicializar o Git

Git é para controlar as versões do seu código.

### Faça isto no terminal:

```bash
# Dentro de n7-portaria-ai, inicialize o Git
git init

# Configure seu nome e email (de uma vez por todas)
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
```

---

## Passo 8: Criar o Arquivo .gitignore

Este arquivo diz ao Git quais pastas não controlar (como a pasta `venv` que é muita grande).

### Faça isto:

1. Na raiz de `n7-portaria-ai/`, crie um arquivo chamado `.gitignore`
2. Escreva isto dentro:

```
venv/
__pycache__/
*.pyc
.env
.DS_Store
```

**O que isto faz:** Git vai ignorar a pasta venv (que é pesada) e outros arquivos temporários.

---

## Passo 9: Seu Primeiro Commit

Agora vamos "tirar uma foto" do estado atual do seu projeto no Git.

### Faça isto no terminal:

```bash
# Ver o status do Git (arquivos que mudaram)
git status

# Adicionar todos os arquivos para o commit
git add .

# Criar o commit com uma mensagem
git commit -m "Aula 01: Estrutura inicial do projeto e primeiro script Python"

# Ver o histórico de commits
git log
```

**O que você verá:**

Após `git status`, verá algo assim:
```
On branch master
Changes not staged for commit:
  new file:   requirements.txt
  new file:   src/hello_portaria.py
  new file:   .gitignore
```

Após `git commit`, verá:
```
[master (root-commit) abc1234] Aula 01: Estrutura inicial...
 3 files changed, 45 insertions(+)
 create mode 100644 requirements.txt
 create mode 100644 src/hello_portaria.py
 create mode 100644 .gitignore
```

---

## Passo 10 (Opcional): Enviar para o GitHub

Se você tiver uma conta no GitHub:

1. Crie um repositório chamado `n7-portaria-ai`
2. No terminal, adicione o repositório remoto:

```bash
# Troque seu-usuario e seu-repositorio pelos seus dados
git remote add origin https://github.com/seu-usuario/n7-portaria-ai.git

# Envie seu código para GitHub
git push -u origin master
```

---

## Checklist - Você Completou?

Verifique se fez tudo:

- [ ] Criei a pasta `n7-portaria-ai` com subpastas
- [ ] Criei o arquivo `requirements.txt` com Flask
- [ ] Criei um ambiente virtual com `python -m venv venv`
- [ ] Ativei o ambiente virtual (vi o `(venv)` no terminal)
- [ ] Instalei o Flask com `pip install -r requirements.txt`
- [ ] Copiei `hello_portaria.py` para `src/`
- [ ] Completei todos os TODOs no script Python
- [ ] Executei o script e funcionou!
- [ ] Criei `.gitignore`
- [ ] Fiz `git init` e meu primeiro `git commit`
- [ ] (Opcional) Enviei para GitHub

---

## Se Algo Deu Errado...

**Erro ao ativar ambiente virtual?**
- Certifique-se de estar na pasta correta
- Use exatamente o comando para seu sistema operacional

**Erro ao instalar Flask?**
- Verifique se o ambiente virtual está ativo (procure por `(venv)` no terminal)
- Tente novamente: `pip install Flask`

**Python não encontrado?**
- Certifique-se que Python está instalado
- No terminal, digite: `python --version`

**Script não executa?**
- Verifique se preencheu todos os TODOs
- Verifique a indentação (espaços em branco no Python são importantes!)
- Procure pela linha exata do erro na mensagem

---

## Parabéns!

Você acabou de:
✅ Criar uma estrutura profissional de projeto
✅ Configurar um ambiente virtual Python
✅ Escrever seu primeiro script Python
✅ Fazer seu primeiro commit no Git

Você está no caminho certo! Descanse um pouco, e na próxima aula vamos aprender muito mais.

---

**Dúvidas?** Anotaremos e resolvemos juntos!
