# Aula 05 — Interface Gráfica: Dando Rosto ao Nosso Sistema

> **Data:** 30 de Abril de 2026 (Quarta-feira)
> **Duração:** 2 horas | **Módulo:** Moradores (Fase 1 - Finalização)
> **Projeto:** n7-portaria-ai | Neural Tech

---

## Objetivos da Aula

Ao final desta aula, o Ademilson será capaz de:
1. Entender o que é uma interface gráfica (GUI) e por que usamos
2. Conhecer o CustomTkinter e criar janelas com Python
3. Criar campos de formulário, botões e tabelas visuais
4. Conectar a interface gráfica ao banco de dados de moradores
5. Celebrar a conclusão da Fase 1 com um programa completo e visual!

---

## Agenda

### Teoria (30 minutos) — "A Vitrine da Nossa Loja"

**Analogia do dia:** Até agora, nosso sistema era como uma loja sem vitrine — funcionava por dentro, mas ninguém via. Hoje vamos criar a **vitrine**: uma janela bonita no computador onde o porteiro vai trabalhar.

**Conceitos:**
- **GUI (Graphical User Interface)** — Interface gráfica do usuário. São as janelas, botões e campos que vemos no computador.
- **Desktop vs Web** — Dois caminhos para criar interfaces. Hoje vamos pelo desktop (mais direto e visual). Web virá em módulos futuros!
- **CustomTkinter** — Uma biblioteca Python que cria interfaces modernas e bonitas com poucas linhas de código.
- **Widgets** — Os "tijolos" da interface: janelas, labels, campos de texto, botões, tabelas.

**Widgets que vamos usar:**
- `CTkLabel` — Texto na tela (como uma etiqueta)
- `CTkEntry` — Campo para digitar texto
- `CTkButton` — Botão clicável
- `CTkFrame` — Uma "caixa" que agrupa outros widgets
- `CTkScrollableFrame` — Uma caixa com rolagem para listas grandes
- `CTkOptionMenu` — Menu de opções (dropdown)

**Por que CustomTkinter e não Tkinter puro?**
- Aparência moderna (parece um programa profissional)
- Tema claro e escuro automáticos
- Mesma lógica do Tkinter, mas mais bonito
- Perfeito para aprender GUI sem complicação

### Prática (1 hora e 30 minutos) — Mão na Massa!

1. Instalar CustomTkinter (`pip install customtkinter`)
2. Criar a janela principal do sistema
3. Criar o formulário de cadastro de moradores
4. Criar a lista visual de moradores (com scroll)
5. Conectar tudo ao banco de dados SQLite
6. Testar o programa completo
7. Commit e celebração da Fase 1!

---

## Materiais da Aula

| Arquivo | Descrição |
|---------|-----------|
| `slides/apresentacao-aula05.pptx` | Apresentação de teoria (30 min) |
| `exercicio/INSTRUCOES.md` | Guia passo a passo do exercício |
| `exercicio/portaria_gui.py` | Aplicação GUI (com TODOs para completar) |
| `material-complementar.md` | Vídeos e leituras opcionais |

---

## Checklist de Aprendizado

Ao final da aula, verifique se consegue:

- [ ] Explicar o que é uma GUI e por que é importante
- [ ] Criar uma janela com CustomTkinter
- [ ] Adicionar labels, campos de texto e botões
- [ ] Organizar widgets em frames
- [ ] Conectar um botão a uma função Python
- [ ] Ler dados de campos de texto
- [ ] Exibir dados do banco em uma lista visual
- [ ] Fazer commit no Git

---

## Celebração — Fase 1 Completa!

Parabéns, Ademilson! Em 5 semanas você construiu:

```
Aula 01 → Setup do projeto e ambiente Python
Aula 02 → Banco de dados com SQLite
Aula 03 → CRUD completo de moradores
Aula 04 → API REST com Flask
Aula 05 → Interface gráfica desktop ← VOCÊ ESTÁ AQUI!
```

**Resultado:** Um programa de computador completo, com janela visual, que cadastra e lista moradores, salvando tudo no banco de dados. Isso é programação de verdade!

**Próximos passos (Maio):** Vamos adicionar visitantes ao sistema, aprender SQL JOINs e criar o login do porteiro!

---

*Cada linha de código que você escreveu é uma conquista. Continue assim!*
