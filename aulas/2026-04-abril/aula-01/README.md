# Aula 01 — Montando Nosso Canteiro de Obras Digital

**Data:** 03 de Abril de 2026
**Duração:** 2 horas
**Instrutor:** Thiago (n7 Tech)
**Aluno:** Ademilson
**Projeto:** n7-portaria-ai — Sistema de Portaria Inteligente

---

## Objetivos da Aula

Nesta aula inaugural, vamos configurar o projeto como profissionais fazem. Como o Ademilson já tem noções de Python, pulamos o "Hello World" e vamos direto ao que importa: **como organizar software de verdade**.

Ao final desta aula, você será capaz de:

✅ Estruturar um projeto Python em camadas (Config → Model → Service → Interface)
✅ Entender por que separação de responsabilidades importa
✅ Usar `@dataclass` para criar modelos limpos
✅ Centralizar configurações em constantes
✅ Criar um serviço com validação e filtros
✅ Configurar venv, requirements.txt e .gitignore
✅ Fazer commits profissionais com mensagens descritivas

---

## Agenda da Aula

### Parte Teórica (30 minutos)

1. **O Projeto n7-portaria-ai** (5 min)
   - O que vamos construir ao longo de 25 aulas
   - Os 6 módulos: Moradores, Visitantes, Acesso, Notificações, IA, Dashboard

2. **Analogia: Software = Construir uma Casa** (5 min)
   - Fundação → Python | Paredes → Código | Fiação → Banco | Pintura → Interface

3. **Arquitetura em Camadas** (10 min)
   - Config: configurações centralizadas
   - Model: @dataclass, type hints, encapsulamento
   - Service: lógica de negócio, validação, filtros
   - Interface: a "casca" que pode mudar (terminal → GUI → web)
   - Regra: cada camada só conhece a de baixo

4. **Ferramentas e Ambiente** (5 min)
   - VS Code, Python, venv, Git
   - `__init__.py`: o que transforma pasta em pacote

5. **Clean Code na Prática** (5 min)
   - Constantes UPPER_SNAKE_CASE vs variáveis snake_case
   - Docstrings: documentar para o "eu do futuro"
   - Type hints: dizer ao Python (e a nós) o tipo dos dados

---

### Parte Prática (1 hora e 30 minutos)

1. **Criar a Estrutura do Projeto** (15 min)
   - Pastas: src/core/models, src/core/usercase, src/infra/database, src/interface/gui
   - Arquivos `__init__.py` em cada pacote
   - requirements.txt + .gitignore

2. **Configurar o Ambiente Virtual** (10 min)
   - Criar e ativar venv
   - Instalar dependências

3. **Exercício: hello_portaria.py — 7 TODOs** (45 min)
   - TODO 1: Constantes de configuração
   - TODO 2: Método no modelo (encapsulamento)
   - TODO 3: Criar modelo Visitante (@dataclass)
   - TODO 4: Filtro por bloco no serviço
   - TODO 5: Função de cadastro interativo (interface)
   - TODO 6: Usar o serviço para listar moradores
   - TODO 7: Orquestrar tudo na main()

4. **Git: Primeiro Commit** (20 min)
   - `git init` → `git add .` → `git commit -m "feat: ..."`
   - Padrão de mensagem: feat, fix, docs, refactor
   - Push para GitHub

---

## Conceitos Arquiteturais Abordados

### Separação em Camadas
```
Interface (gui/api)  ←  Core (usecases → models)  ←  Infra (database)
```
Cada camada tem uma responsabilidade única. Se trocarmos terminal por GUI ou API, só a Interface muda. As usecases e modelos no Core orquestram a lógica. A Infra cuida do acesso aos dados.

### @dataclass
Substitui classes com `__init__` repetitivo. Em vez de:
```python
class Morador:
    def __init__(self, nome, apto):
        self.nome = nome
        self.apto = apto
```
Escrevemos:
```python
@dataclass
class Morador:
    nome: str
    apto: str
```

### Injeção de Dependência (simplificada)
Funções recebem o service como parâmetro em vez de criá-lo internamente. Isso facilita testes e troca de implementação.

### Type Hints
`def cadastrar(nome: str) -> Morador` — deixa claro o que entra e o que sai da função.

---

## Checklist de Aprendizado

- [ ] Sei explicar por que separamos código em camadas
- [ ] Entendo o que @dataclass faz e por que é útil
- [ ] Sei a diferença entre Model, Service e Interface
- [ ] Entendo para que serve `__init__.py`
- [ ] Sei fazer um commit com mensagem profissional
- [ ] Configurei venv e instalei dependências
- [ ] Completei todos os 7 TODOs do exercício

---

## Recursos Utilizados

- **Linguagem:** Python 3.12+
- **Conceitos:** Dataclasses, Type Hints, Separação de Camadas
- **Ferramentas:** venv, pip, Git, VS Code
- **Bibliotecas:** (instaladas, usadas a partir da Aula 04+): Flask, CustomTkinter

---

## Próximos Passos

- **Aula 02 (09/04):** Banco de Dados com SQLite — os modelos que criamos aqui viram tabelas!
- **Aula 03 (16/04):** CRUD Completo — cadastrar, listar, editar e excluir moradores
- **Aula 04 (23/04):** API REST com Flask — o serviço vira endpoints HTTP

---

**Vamos começar!**

Ademilson, você já sabe Python. Agora vai aprender a **pensar como arquiteto de software**. Cada decisão que tomamos hoje vai facilitar nossa vida nas próximas 24 aulas.
