# Exercício Aula 01 — Arquitetura do Projeto Python

**Objetivo:** Configurar um projeto Python profissional com estrutura em camadas, clean code e boas práticas de engenharia de software.

**Tempo estimado:** 1 hora e 30 minutos

**Pré-requisitos:**
- Python 3.11+ instalado
- Git instalado
- VS Code (ou editor de sua preferência)
- Noções básicas de Python (variáveis, funções, classes)

---

## Visão Geral da Arquitetura

Neste exercício, o arquivo `hello_portaria.py` simula a estrutura que nosso projeto terá quando separado em arquivos. Cada seção do código representa uma **camada**:

```
┌─────────────────────────────────┐
│  INTERFACE  (print/input)       │  ← Camada mais externa
├─────────────────────────────────┤
│  SERVIÇO    (PortariaService)   │  ← Lógica de negócio
├─────────────────────────────────┤
│  MODELO     (Morador, Visitante)│  ← Estrutura dos dados
├─────────────────────────────────┤
│  CONFIG     (constantes)        │  ← Configuração centralizada
└─────────────────────────────────┘
```

**Regra de ouro:** cada camada só conhece a de baixo. A Interface chama o Serviço, o Serviço usa Modelos, e ninguém depende da Interface.

---

## Passo 1: Criar a Estrutura de Pastas

No terminal, crie a estrutura profissional do projeto:

```bash
mkdir n7-portaria-ai
cd n7-portaria-ai

# Estrutura em camadas
mkdir -p app/models app/services app/routes
mkdir -p database tests docs aulas

# Arquivos de inicialização de pacote Python
touch app/__init__.py
touch app/models/__init__.py
touch app/services/__init__.py
touch app/routes/__init__.py
```

**Por que `__init__.py`?**
Esse arquivo transforma uma pasta em um **pacote Python**. Sem ele, o Python não consegue importar módulos de dentro da pasta. Pode ser vazio por enquanto — o importante é que exista.

**Seu projeto deve ficar assim:**
```
n7-portaria-ai/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   └── __init__.py
│   ├── services/
│   │   └── __init__.py
│   └── routes/
│       └── __init__.py
├── database/
├── tests/
├── docs/
└── aulas/
```

---

## Passo 2: Configurar o Projeto Python

### 2.1 Criar o ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

Você deve ver `(venv)` no início do terminal.

### 2.2 Criar requirements.txt

Crie o arquivo `requirements.txt` na raiz:

```
Flask==3.1.0
customtkinter==5.2.2
```

Instale:
```bash
pip install -r requirements.txt
```

### 2.3 Criar .gitignore

Crie `.gitignore` na raiz:

```
# Python
venv/
__pycache__/
*.pyc
*.pyo
.env

# IDE
.vscode/
.idea/

# Sistema
.DS_Store
Thumbs.db

# Banco de dados local
*.db
```

### 2.4 Criar config.py (opcional, desafio bônus)

Na raiz, crie `config.py`:

```python
"""Configuração centralizada do projeto."""

APP_NAME = "n7-portaria-ai"
APP_VERSION = "0.1.0"
DATABASE_NAME = "portaria.db"
MAX_MORADORES = 500
DEBUG_MODE = True
```

Este é o conceito que você vai praticar no **TODO 1** do exercício.

---

## Passo 3: Copiar e Abrir o Exercício

1. Copie o arquivo `hello_portaria.py` para a pasta `app/` do seu projeto
2. Abra no VS Code

---

## Passo 4: Completar os TODOs

O exercício tem **7 TODOs** organizados por camada. Cada um ensina um conceito de arquitetura:

### Camada de Configuração
| TODO | Conceito | O que fazer |
|------|----------|-------------|
| **1** | Constantes centralizadas | Definir DATABASE_NAME, MAX_MORADORES, DEBUG_MODE |

### Camada de Modelo
| TODO | Conceito | O que fazer |
|------|----------|-------------|
| **2** | Encapsulamento | Criar método `endereco_completo()` na classe Morador |
| **3** | Domain Modeling | Criar a classe Visitante com @dataclass |

### Camada de Serviço
| TODO | Conceito | O que fazer |
|------|----------|-------------|
| **4** | Lógica no Service | Criar método `listar_moradores()` com filtro por bloco |

### Camada de Interface
| TODO | Conceito | O que fazer |
|------|----------|-------------|
| **5** | Separação de responsabilidades | Criar função de cadastro interativo |
| **6** | Usar o service, não manipular dados | Chamar listar_moradores() e exibir resultado |
| **7** | Orquestração na main() | Integrar tudo no fluxo principal |

---

## Passo 5: Executar e Testar

```bash
python app/hello_portaria.py
```

**Saída esperada (após completar todos os TODOs):**

```
==================================================
  n7-portaria-ai v0.1.0
  Sistema de Portaria Inteligente para Condomínios
==================================================

📋 Cadastrando moradores de exemplo...
   → Maria Silva: Apto 101 - Bloco A
   → João Santos: Apto 202 - Bloco B
   → Ana Oliveira: Apto 303

Moradores do Bloco A: 1
Total de moradores: 3

👤 Cadastre um novo morador:
Nome do morador: Pedro Lima
Apartamento: 404
Bloco (Enter para pular): A
✅ Morador cadastrado: Apto 404 - Bloco A

📊 Resumo do Sistema:
   Moradores cadastrados: 4
   Banco de dados: portaria.db
   Modo debug: Ativado

==================================================
  Ademilson, cada camada do código tem seu lugar.
  Assim como cada pessoa no condomínio. 🏢
==================================================
```

---

## Passo 6: Git — Primeiro Commit Profissional

```bash
git init

git config user.name "Seu Nome"
git config user.email "seu.email@exemplo.com"

# Verifique o status (o .gitignore deve excluir venv/)
git status

# Adicione os arquivos
git add .

# Commit com mensagem no padrão profissional
git commit -m "feat: estrutura inicial do projeto com arquitetura em camadas"

# Verifique o histórico
git log --oneline
```

**Padrão de commit:**
- `feat:` = nova funcionalidade
- `fix:` = correção de bug
- `docs:` = documentação
- `refactor:` = reestruturação sem mudar comportamento

---

## Passo 7 (Bônus): Desafio Extra

Se terminou tudo e quer ir além:

1. **Adicione validação no modelo Visitante:** documento deve ter exatamente 11 dígitos (CPF) ou entre 5-15 caracteres (RG). Use `__post_init__` do dataclass.

2. **Crie um método `registrar_visita` no PortariaService** que recebe um Visitante e um Morador e imprime: "Visitante {nome} visitando {morador} em {endereco_completo}"

3. **Separe em arquivos reais:** mova cada camada para seu arquivo dentro de `app/`:
   - `app/models/morador.py`
   - `app/models/visitante.py`
   - `app/services/portaria_service.py`

---

## Checklist de Aprendizado

Ao final desta aula, você deve entender:

- [ ] Por que separamos código em camadas (Model / Service / Interface)
- [ ] O que é `@dataclass` e por que evita código repetitivo
- [ ] O que é `Optional[str]` (type hints)
- [ ] Para que serve `__init__.py` em pastas Python
- [ ] O que é injeção de dependência (receber service como parâmetro)
- [ ] Diferença entre constantes (`UPPER_CASE`) e variáveis (`snake_case`)
- [ ] Por que a interface não deve manipular dados diretamente
- [ ] Como fazer um commit profissional com mensagem descritiva

---

## Se Algo Deu Errado...

**Erro `NameError: name 'DATABASE_NAME' is not defined`**
→ Você esqueceu de completar o TODO 1. Defina as constantes.

**Erro `AttributeError: 'Morador' object has no attribute 'endereco_completo'`**
→ Você esqueceu de completar o TODO 2. Crie o método na classe.

**Erro de indentação**
→ Em Python, indentação importa! Use 4 espaços (nunca tab). No VS Code, configure: "editor.tabSize": 4.

**`@dataclass` não funciona**
→ Certifique-se de ter `from dataclasses import dataclass` no topo do arquivo.

---

## Parabéns!

Você aprendeu a pensar como um **arquiteto de software**:

✅ Configuração centralizada (não espalhe valores mágicos)
✅ Modelos isolados (representam dados, nada mais)
✅ Serviços com lógica de negócio (validação, filtros, regras)
✅ Interface separada (print/input podem mudar sem quebrar o resto)

Na **Aula 02**, vamos conectar essa estrutura ao **SQLite** — o banco de dados do nosso sistema. Os modelos que você criou aqui serão as tabelas do banco!

---

**Dúvidas?** Anote e resolveremos juntos na próxima sessão.
