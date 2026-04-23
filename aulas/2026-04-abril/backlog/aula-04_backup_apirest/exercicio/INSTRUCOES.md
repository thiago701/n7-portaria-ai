# Exercício Aula 04 - Sua Primeira API REST com Flask

**Objetivo:** Criar um servidor web que funciona como uma API para gerenciar moradores.

**Tempo estimado:** 1 hora e 30 minutos

**Materiais necessários:**
- Terminal
- Git instalado
- Python 3.11+ instalado
- Editor de texto ou IDE
- Seu ambiente virtual (venv) da Aula 01

---

## Passo 1: Instalar Flask

Seu projeto já tem Flask no requirements.txt, mas vamos garantir que está instalado.

### No terminal (dentro de n7-portaria-ai):

```bash
# Ative o ambiente virtual
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# Instale Flask
pip install flask
```

**Como saber se funcionou?**

```bash
python -c "import flask; print(flask.__version__)"
```

Deve mostrar uma versão (exemplo: 2.3.0).

---

## Passo 2: Copiar o Arquivo app.py

Este é seu arquivo de trabalho com TODOs para completar.

### Faça isto:

1. Abra a pasta `exercicio` desta aula
2. Copie o arquivo `app.py`
3. Cole na pasta `src/interface/` do seu projeto

**Seu projeto deve parecer assim agora:**
```
n7-portaria-ai/
├── src/
│   ├── core/
│   │   ├── models/
│   │   └── usercase/
│   ├── infra/
│   │   └── database/
│   └── interface/
│       └── app.py                ← Seu servidor Flask!
├── aulas/
│   └── 2026-04-abril/
│       └── aula-04_2026-04-23/
├── venv/
└── requirements.txt
```

---

## Passo 3: Examinar o Arquivo app.py

Abra o arquivo `src/interface/app.py` no seu editor.

**O que você verá:**

```python
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# ... código aqui
```

O arquivo já tem:
- ✅ Imports corretos
- ✅ Criação da app Flask
- ✅ Função para conectar ao banco (conectar_banco)
- ✅ Rota de boas-vindas (/)
- ❌ TODOs para você completar

---

## Passo 4: Executar o Servidor Flask

Vamos ligar o servidor e ver se funciona!

### No terminal (com venv ativo):

```bash
python src/interface/app.py
```

**Esperado:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

Parabéns! Seu servidor está funcionando!

---

## Passo 5: Testar a Rota de Boas-vindas

Seu servidor está rodando. Agora vamos testá-lo.

### Abra o navegador:

Digite na barra de endereço:
```
http://localhost:5000/
```

**Esperado:** Uma mensagem de boas-vindas em JSON

```json
{
  "mensagem": "Bem-vindo ao Sistema de Portaria!",
  "versao": "1.0.0"
}
```

Se viu isto, ótimo! A rota básica funciona.

---

## Passo 6: Completar o TODO 1 - GET /api/moradores

Esta rota deve **listar todos os moradores** do banco de dados.

### Encontre o comentário TODO 1:

```python
# TODO 1: Implementar GET /api/moradores - Listar todos os moradores
@app.route('/api/moradores', methods=['GET'])
def listar_moradores():
    # Escreva seu código aqui
    pass
```

### O que seu código deve fazer:

1. Conectar ao banco de dados com `conectar_banco()`
2. Executar um SELECT para trazer todos os moradores
3. Guardar o resultado em uma lista
4. Retornar essa lista como JSON usando `jsonify()`

### Dica de código:

```python
@app.route('/api/moradores', methods=['GET'])
def listar_moradores():
    conn = conectar_banco()
    cursor = conn.cursor()

    # Execute um SELECT * para trazer todos
    cursor.execute("SELECT * FROM moradores")
    # Guarde os resultados
    moradores = cursor.fetchall()
    conn.close()

    # Retorne como JSON
    return jsonify(moradores)
```

**Teste no navegador:**
```
http://localhost:5000/api/moradores
```

Deve mostrar uma lista em JSON (pode estar vazia se não tem dados ainda).

---

## Passo 7: Completar o TODO 2 - POST /api/moradores

Esta rota deve **adicionar um novo morador** ao banco de dados.

### Encontre o comentário TODO 2:

```python
# TODO 2: Implementar POST /api/moradores - Adicionar novo morador
@app.route('/api/moradores', methods=['POST'])
def adicionar_morador():
    # Escreva seu código aqui
    pass
```

### O que seu código deve fazer:

1. Pegar os dados JSON que chegaram com `request.get_json()`
2. Extrair nome, cpf, numero_residencia e email
3. Conectar ao banco e fazer um INSERT
4. Fazer commit() para salvar
5. Retornar uma mensagem de sucesso

### Dica de código:

```python
@app.route('/api/moradores', methods=['POST'])
def adicionar_morador():
    # Pega os dados JSON que foram enviados
    dados = request.get_json()

    # Extrai os campos
    nome = dados.get('nome')
    cpf = dados.get('cpf')
    numero_residencia = dados.get('numero_residencia')
    email = dados.get('email')

    conn = conectar_banco()
    cursor = conn.cursor()

    # Insere um novo morador
    cursor.execute("""
        INSERT INTO moradores (nome, cpf, numero_residencia, email)
        VALUES (?, ?, ?, ?)
    """, (nome, cpf, numero_residencia, email))

    conn.commit()
    conn.close()

    # Retorna mensagem de sucesso
    return jsonify({'mensagem': 'Morador adicionado com sucesso!'})
```

### Teste (não é pelo navegador):

Para testar POST, você vai usar uma ferramenta como:
- **Postman** (visual, fácil)
- **curl** no terminal (mais técnico)

**Usando curl:**
```bash
curl -X POST http://localhost:5000/api/moradores \
  -H "Content-Type: application/json" \
  -d '{"nome":"João Silva","cpf":"123.456.789-00","numero_residencia":"101","email":"joao@email.com"}'
```

---

## Passo 8: Completar o TODO 3 - GET /api/moradores/<id>

Esta rota deve **buscar um morador específico pelo ID**.

### Encontre o comentário TODO 3:

```python
# TODO 3: Implementar GET /api/moradores/<id> - Buscar um morador específico
@app.route('/api/moradores/<int:id>', methods=['GET'])
def obter_morador(id):
    # Escreva seu código aqui
    pass
```

### O que seu código deve fazer:

1. Receber o ID da URL
2. Conectar ao banco e fazer SELECT WHERE id = ?
3. Se encontrou, retornar o morador
4. Se não encontrou, retornar erro 404

### Dica de código:

```python
@app.route('/api/moradores/<int:id>', methods=['GET'])
def obter_morador(id):
    conn = conectar_banco()
    cursor = conn.cursor()

    # Busca por ID
    cursor.execute("SELECT * FROM moradores WHERE id = ?", (id,))
    morador = cursor.fetchone()
    conn.close()

    # Se não encontrou
    if morador is None:
        return jsonify({'erro': 'Morador não encontrado'}), 404

    # Se encontrou, retorna
    return jsonify(morador)
```

### Teste no navegador:

```
http://localhost:5000/api/moradores/1
```

(Substitua 1 pelo ID de um morador que existe)

---

## Passo 9: Testar Sua API Completamente

Agora que todo o código está pronto, vamos testar tudo!

### 1. Reinicie o servidor

Se o servidor está rodando, pressione **CTRL+C** e depois rode novamente:

```bash
python src/app.py
```

### 2. Teste as rotas em ordem:

**a) Boas-vindas:**
```
http://localhost:5000/
```

**b) Listar moradores (vazio no início):**
```
http://localhost:5000/api/moradores
```

**c) Adicionar um novo morador (usando curl ou Postman)**

**d) Listar novamente (deve aparecer o novo morador)**

**e) Buscar por ID:**
```
http://localhost:5000/api/moradores/1
```

---

## Passo 10: Entender a Resposta JSON

Quando você acessa `/api/moradores`, recebe algo assim:

```json
[
  [1, "João Silva", "123.456.789-00", "101", "joao@email.com"],
  [2, "Maria Santos", "987.654.321-00", "202", "maria@email.com"]
]
```

Isto é uma **lista de listas**. Cada lista interna é um morador: `[id, nome, cpf, numero_residencia, email]`

**Por que assim?** Porque assim foi estruturado no banco de dados na Aula 03.

---

## Passo 11: Parar o Servidor

Quando terminar os testes, pare o servidor no terminal:

```bash
CTRL+C
```

---

## Passo 12: Fazer o Commit no Git

Vamos salvar seu trabalho no Git!

### No terminal:

```bash
# Ver o status
git status

# Adicionar os arquivos modificados
git add src/interface/app.py

# Fazer o commit
git commit -m "Aula 04: Implementar API REST com rotas GET e POST"

# Ver o histórico
git log
```

---

## Checklist - Você Completou?

Verifique se fez tudo:

- [ ] Instalei Flask com `pip install flask`
- [ ] Copiei `app.py` para a pasta `src/interface/`
- [ ] Rodei o servidor com `python src/interface/app.py`
- [ ] Testei a rota de boas-vindas no navegador
- [ ] Implementei o TODO 1 - GET /api/moradores
- [ ] Implementei o TODO 2 - POST /api/moradores
- [ ] Implementei o TODO 3 - GET /api/moradores/<id>
- [ ] Testei todas as rotas
- [ ] Fiz commit no Git

---

## Se Algo Deu Errado...

**Erro: "No module named 'flask'"**
- Certifique-se de que o venv está ativo
- Rode: `pip install flask`

**Erro ao conectar no banco**
- Verifique se o banco `portaria.db` existe na pasta onde você rodou o servidor
- Se não existe, rode o código de CRUD da Aula 03 primeiro

**Rota não funciona**
- Verifique a indentação (Python é sensível a espaços)
- Procure pelo TODO no arquivo
- Certifique-se de fazer commit (salvar) antes de recarregar

**Servidor não inicia**
- Verifique se há outro servidor rodando na porta 5000
- Ou mude a porta no if __name__ do final do arquivo

---

## Parabéns!

Você acabou de:
✅ Criar um servidor web Flask funcionando
✅ Entender como uma API REST funciona
✅ Implementar rotas com GET e POST
✅ Trabalhar com JSON
✅ Fazer operações no banco via servidor

**Você está oficialmente criando sistemas web reais!** 🎉

---

**Dúvidas?** Revisit o README.md ou o material complementar!
