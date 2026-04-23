# Material Complementar — Aula 03

Aqui estão recursos extras para você aprofundar seu aprendizado sobre CRUD, funções e tratamento de erros em Python.

---

## Vídeos Recomendados

### 1. Python Functions (Funções em Python)

Se você quer revisar como as funções funcionam em Python, este vídeo é excelente:

**YouTube:** "Python Functions - Tutorial for Beginners"
- **Criador:** Corey Schafer
- **Duração:** ~18 minutos
- **Link:** https://www.youtube.com/watch?v=9Os0o12WeWs

**Por que assistir:** Você já viu isso na aula anterior, mas revisar nunca dói! Funções são a base de tudo que você vai fazer.

---

### 2. CRUD Concept Explained

Um vídeo que explica CRUD de forma visual e clara:

**YouTube:** "CRUD Operations Explained"
- **Criador:** Web Dev Simplified
- **Duração:** ~7 minutos
- **Link:** https://www.youtube.com/watch?v=7-Iy4qp4a1c

**Por que assistir:** Ver CRUD de forma visual ajuda a fixar melhor o conceito.

---

## Artigos Úteis

### 3. Try and Except in Python (Tratamento de Erros)

Entender try/except bem é importantíssimo:

**Real Python:** "Python Exceptions: An Introduction"
- **Link:** https://realpython.com/python-exceptions/
- **Tempo de leitura:** ~15 minutos

**Resumo:** Explica como funcionam exceções e como usar try/except para proteger seu código.

---

### 4. SQLite3 em Python

Se quiser entender melhor como conectar e usar bancos de dados:

**Real Python:** "Python sqlite3 Tutorial"
- **Link:** https://realpython.com/python-sqlite-tutorial/
- **Tempo de leitura:** ~20 minutos

**Resumo:** Guia completo sobre como usar o módulo sqlite3, que é exatamente o que você está usando!

---

## Dicas Rápidas

### Sobre Funções

Lembre-se:
- Uma função é um bloco de código reutilizável
- Você define com `def`, chama com `funcao()`
- Pode ter parâmetros: `def funcao(parametro):`
- Pode retornar algo: `return resultado`

---

### Sobre CRUD

As 4 operações que TODO programador precisa saber:

```
CREATE  = Adicionar novo registro (INSERT)
READ    = Consultar registros (SELECT)
UPDATE  = Modificar registro existente (UPDATE)
DELETE  = Remover registro (DELETE ou UPDATE para marcar inativo)
```

---

### Sobre Try/Except

Proteja seu código de erros:

```python
try:
    # Código que pode dar erro
    resultado = 10 / 0
except Exception as erro:
    # O que fazer se der erro
    print(f"Oops! Erro: {erro}")
```

Isso evita que seu programa "quebra" (crash) quando algo dá errado.

---

## Desafio Extra (Opcional)

Se você terminou o exercício rapidinho e quer praticar mais:

### Adicione essas features ao seu programa:

1. **Listar apenas inativos:** Crie uma função `listar_inativos()` que mostra apenas os moradores desativados.

2. **Reativar morador:** Crie uma função `reativar_morador()` que muda um inativo de volta para ativo.

3. **Contar moradores:** Adicione uma função `contar_moradores()` que mostra o total de ativos e inativos.

4. **Deletar de verdade:** Adicione uma função `deletar_morador_permanente()` com confirmação dupla.

5. **Relatório por numero_residencia:** Crie uma função que lista todos os moradores de um numero_residencia específico.

6. **Salvar em arquivo:** Implemente uma função que exporta a lista de moradores para um arquivo .txt ou .csv.

---

## Próximas Aulas

Agora que você domina CRUD, você estará pronto para:

- **Aula 04 (23/04)**: API REST com Flask — O garçom digital do sistema
- **Aula 05 (30/04)**: Interface Gráfica com CustomTkinter — Dando rosto ao sistema
- **Fase 2 (Maio)**: Visitantes, SQL JOINs e Login do Porteiro

---

## Perguntas Frequentes

### "Preciso memorizar todos os comandos SQL?"

**Resposta:** Não! Você pode sempre consultar. O importante é entender o conceito. Conforme usa mais, vai memorizar naturalmente.

### "Por que não deletamos os dados direto?"

**Resposta:** Segurança! Deletes são irreversíveis. Marcando como inativo (soft delete), você:
- Recupera dados se precisar
- Mantém histórico
- É mais profissional

### "Meu programa travou! O que faço?"

**Resposta:** Isso é normal! Tente:
1. Adicione mais try/except
2. Imprima mensagens de debug: `print("Chegou aqui!")`
3. Teste cada função isoladamente
4. Pergunte!

---

## Recursos Técnicos

Se você quiser aprofundar (não obrigatório):

- **Python Official Docs:** https://docs.python.org/3/
- **SQLite Official:** https://www.sqlite.org/index.html
- **Real Python (site):** https://realpython.com/
- **W3Schools SQL Tutorial:** https://www.w3schools.com/sql/

---

## Resumo

Parabéns por chegar até aqui! Você aprendeu:

✓ CRUD - as 4 operações mágicas
✓ Funções em Python
✓ Como conectar a um banco de dados SQLite
✓ Tratamento de erros com try/except
✓ Menu de texto funcional

Isso é sério! Você já está programando como um profissional. Não é pouco não!

Continue assim e logo você estará construindo aplicações incríveis! 🚀

