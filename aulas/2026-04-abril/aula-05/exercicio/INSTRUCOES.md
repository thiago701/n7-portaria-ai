# Instruções — Aula 05: Interface Gráfica com CustomTkinter

> **Tempo estimado:** 1 hora e 30 minutos
> **Arquivo principal:** `portaria_gui.py`

---

## Antes de Começar

Certifique-se de que:
- O Python está instalado e funcionando
- O banco de dados `portaria.db` existe (criado nas aulas anteriores)
- O ambiente virtual está ativado

---

## Passo 1 — Instalar o CustomTkinter

No terminal, com o ambiente virtual ativado:

```bash
pip install customtkinter
```

**Verifique a instalação:**
```bash
python -c "import customtkinter; print('CustomTkinter OK!')"
```

Se aparecer "CustomTkinter OK!", estamos prontos!

---

## Passo 2 — Copiar o Arquivo para a Pasta Correta

Copie o arquivo `portaria_gui.py` da pasta `exercicio` para `src/interface/gui/` do seu projeto.

Seu projeto deve parecer assim agora:
```
src/
├── interface/
│   ├── gui/
│   │   └── portaria_gui.py     ← Seu programa GUI!
│   └── app.py
├── core/
└── infra/
```

## Passo 3 — Entender a Estrutura do Arquivo

Abra o arquivo `src/interface/gui/portaria_gui.py`. Ele já tem a estrutura básica:

- **Importações** — As bibliotecas que usamos
- **Classe PortariaApp** — O "coração" da nossa interface
- **__init__** — Onde a janela é configurada
- **criar_formulario()** — Monta o formulário de cadastro
- **criar_lista()** — Monta a lista de moradores
- **cadastrar_morador()** — Salva no banco (VOCÊ VAI COMPLETAR!)
- **carregar_moradores()** — Lê do banco e mostra na lista (VOCÊ VAI COMPLETAR!)
- **limpar_campos()** — Limpa o formulário após cadastrar

---

## Passo 4 — Completar o TODO 1: Criar os Campos do Formulário

Dentro da função `criar_formulario()`, procure o `TODO 1`.

Você precisa criar campos para: **CPF, Apartamento, Bloco, Telefone e E-mail**.

O campo "Nome" já está feito como exemplo. Siga o mesmo padrão:

```python
# Exemplo (já feito): Campo Nome
self.label_nome = customtkinter.CTkLabel(self.frame_form, text="Nome Completo:")
self.label_nome.grid(row=1, column=0, padx=10, pady=5, sticky="w")
self.entry_nome = customtkinter.CTkEntry(self.frame_form, width=280, placeholder_text="Ex: João da Silva")
self.entry_nome.grid(row=1, column=1, padx=10, pady=5)
```

**Dica:** Cada campo novo usa a próxima `row`. CPF fica na row=2, Apartamento na row=3, e assim por diante.

---

## Passo 5 — Completar o TODO 2: Cadastrar Morador no Banco

Dentro da função `cadastrar_morador()`, procure o `TODO 2`.

Você precisa:
1. Ler o texto de cada campo usando `.get()`
2. Inserir no banco de dados com SQL
3. Chamar `carregar_moradores()` para atualizar a lista
4. Chamar `limpar_campos()` para limpar o formulário

**Lembre-se da Aula 03!** O INSERT é igual ao que fizemos no CRUD:
```python
cursor.execute("INSERT INTO moradores (nome, cpf, numero_residencia, ...) VALUES (?, ?, ?, ...)",
               (nome, cpf, numero_residencia, ...))
```

---

## Passo 6 — Completar o TODO 3: Carregar e Exibir Moradores

Dentro da função `carregar_moradores()`, procure o `TODO 3`.

Você precisa:
1. Conectar ao banco de dados
2. Fazer um SELECT de todos os moradores ativos
3. Para cada morador, criar um "card" na lista

**O padrão de card já está exemplificado nos comentários.** Siga o modelo!

---

## Passo 7 — Testar o Programa

Execute o programa:
```bash
python src/interface/gui/portaria_gui.py
```

**Teste na seguinte ordem:**
1. A janela abriu corretamente?
2. Todos os campos do formulário aparecem?
3. Cadastre um morador e clique "Cadastrar"
4. O morador apareceu na lista à direita?
5. Cadastre mais 2 moradores — todos aparecem?
6. Feche e abra novamente — os moradores ainda estão lá? (Banco de dados!)

---

## Passo 8 — Commit no Git

```bash
git add src/interface/gui/
git commit -m "feat: adiciona interface gráfica com CustomTkinter para moradores"
git push
```

---

## Dicas Importantes

**Se a janela não abrir:**
- Verifique se o CustomTkinter está instalado
- Verifique a versão do Python (`python --version`) — precisa ser 3.7+

**Se der erro no banco:**
- Verifique se o arquivo `portaria.db` existe em `src/infra/database/`
- Verifique se a tabela `moradores` foi criada (Aula 02)

**Se os moradores não aparecerem:**
- Verifique se o SELECT está correto
- Use `print(moradores)` para ver o que o banco retorna

---

## Checklist Final

- [ ] CustomTkinter instalado
- [ ] Janela abre sem erros
- [ ] Formulário tem todos os 6 campos
- [ ] Botão "Cadastrar" funciona e salva no banco
- [ ] Lista mostra os moradores cadastrados
- [ ] Dados persistem ao reabrir o programa
- [ ] Commit feito no Git

---

*Você acabou de construir um programa com interface gráfica. Isso é incrível!*
