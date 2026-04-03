# Material Complementar — Aula 02

Aqui você encontra recursos adicionais para entender melhor bancos de dados e SQL.

**Tempo sugerido**: 20 a 30 minutos (opcional, mas recomendado!)

---

## 1. Vídeos Introdutórios

### "SQL para Iniciantes" — Curso em Vídeo
**Instrutor**: Gustavo Guanabara

Link: [Curso em Vídeo — SQL](https://www.cursoemvideo.com/)

**Por que assistir**:
- Gustavo é conhecido por ensinar de forma clara e didática
- Ele começa do zero, exatamente como você
- Os vídeos são curtos (5-15 minutos) e objetivos

**Recomendação**: Assista os primeiros 3 vídeos (CREATE TABLE, INSERT, SELECT)

---

## 2. Artigos e Tutoriais

### "O que é SQLite?" — TecMundo
Link: [TecMundo — SQLite](https://www.tecmundo.com.br/)

**Por que ler**:
- Explica de forma simples o que é SQLite
- Mostra exemplos reais de apps que usam SQLite
- Ajuda a entender por que SQLite é bom para nosso projeto

**Tempo**: 5-10 minutos

### "Começando com SQL" — W3Schools
Link: [W3Schools — SQL Tutorial](https://www.w3schools.com/sql/)

**Por que visitar**:
- Website com tutoriais interativos
- Você lê um pouco e logo testa praticando
- Tem exercícios para fazer

**Recomendação**: Faça os exercícios de CREATE TABLE, INSERT e SELECT

---

## 3. Ferramentas Interativas

### SQLite Online
**Link**: [sqliteonline.com](https://sqliteonline.com/)

**Como usar**:
1. Acesse o site
2. Clique em "New Database" (criar novo banco)
3. Na caixa SQL, digite seus comandos CREATE TABLE, INSERT, SELECT
4. Execute clicando em "Run"
5. Veja os resultados aparecer!

**Por que é legal**:
- Não precisa instalar nada
- Você vê o resultado instantaneamente
- Ótimo para experimentar e cometer erros sem medo
- Pode salvar seus experimentos

**Sugestão**: Tente recriar a tabela de moradores nessa ferramenta antes de fazer o exercício!

---

## 4. Dicas Práticas

### Dica 1: Nomes de Tabelas e Colunas
- Use **minúsculas** (seguindo a convenção)
- Use **underline** para separar palavras: `data_criacao`, `numero_apartamento`
- Seja **descritivo**: `morador_nome` é melhor que `m_n`

### Dica 2: Tipos de Dados
Alguns tipos que você verá frequentemente:

| Tipo | O que é | Exemplo |
|------|---------|---------|
| INTEGER | Números inteiros | 102, 1, 999 |
| REAL | Números com decimais | 3.14, 99.99 |
| TEXT | Texto (qualquer tamanho) | "Ademilson Silva", "abc123" |
| BLOB | Dados binários (imagens, etc) | (não usaremos agora) |
| TIMESTAMP | Data e hora | 2026-04-10 14:30:00 |

### Dica 3: Estruturando um bom CREATE TABLE
```sql
CREATE TABLE minha_tabela (
    -- Sempre comece com ID como chave única
    id INTEGER PRIMARY KEY,

    -- Depois colunas obrigatórias (NOT NULL)
    nome TEXT NOT NULL,
    email TEXT NOT NULL,

    -- Depois colunas opcionais com valores padrão
    ativo INTEGER DEFAULT 1,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Dica 4: Ordem Importa em INSERT
Quando você faz um INSERT, a ordem dos valores deve corresponder à ordem das colunas:

```sql
-- Se você disse:
INSERT INTO moradores (nome, cpf, apartamento) VALUES (?, ?, ?)

-- Deve fornecer valores NESSA ordem:
('Ademilson Silva', '123.456.789-00', 102)
```

---

## 5. Referência Rápida de SQL

### CREATE TABLE
```sql
CREATE TABLE tabela (
    id INTEGER PRIMARY KEY,
    coluna1 TEXT NOT NULL,
    coluna2 INTEGER DEFAULT 0
);
```

### INSERT
```sql
INSERT INTO tabela (coluna1, coluna2) VALUES ('valor1', 123);
```

### SELECT
```sql
-- Todas as colunas
SELECT * FROM tabela;

-- Colunas específicas
SELECT id, nome FROM tabela;

-- Com filtro
SELECT * FROM tabela WHERE id = 1;
```

### UPDATE
```sql
UPDATE tabela SET coluna1 = 'novo valor' WHERE id = 1;
```

### DELETE
```sql
DELETE FROM tabela WHERE id = 1;
```

---

## 6. Exercícios Bônus

Se você quer praticar mais, aqui estão alguns desafios:

### Desafio 1: Criar mais tabelas
Depois que terminar a tabela de moradores, tente criar:
- Tabela `visitantes` (visitantes que vêm ao condomínio)
- Tabela `encomendas` (encomendas recebidas na portaria)

### Desafio 2: Adicionar mais dados
Modifique `criar_banco.py` para inserir 10 moradores (em vez de 3).

### Desafio 3: Consultas mais complexas
Tente adicionar ao `criar_banco.py` um comando que:
- Liste apenas moradores do bloco A
- Liste moradores com apartamento acima de 200

**Dica**: Use `WHERE` no SELECT!

```python
sql = "SELECT * FROM moradores WHERE bloco = 'A'"
```

---

## 7. Troubleshooting Comum

### "Syntax error"
Provavelmente há um erro no SQL. Revise:
- Faltou ponto-e-vírgula (;) no final?
- Faltou aspas em texto?
- Tipo de dado escrito errado?

**Solução**: Compare com o README.md e com a referência rápida acima.

### "Table already exists"
A tabela já foi criada uma vez. Você pode:
- Deletar o arquivo `portaria.db` e executar o script novamente
- Ou modificar o script para usar `CREATE TABLE IF NOT EXISTS`

### "No such column"
Você está tentando inserir/consultar uma coluna que não existe.

**Solução**: Verifique se o nome da coluna está correto (maiúsculas/minúsculas importam!).

---

## 8. Próximos Passos

Depois que dominar esta aula, você aprenderá:
- **Aula 3**: Consultas avançadas com WHERE, ORDER BY, etc.
- **Aula 4**: Relacionamentos entre tabelas (FOREIGN KEY)
- **Aula 5**: Interface gráfica para gerenciar o banco

Você está no caminho certo!

---

## Dúvidas?

Se ficar preso em algo:
1. Releia a seção relevante do README.md
2. Procure no SQLite Online por exemplos similares
3. Compare com o código nos arquivos `schema.sql` e `criar_banco.py`

Não desista! Programadores experientes também consultam documentação todos os dias.

---

**Boa sorte com seus estudos!** 🎓
