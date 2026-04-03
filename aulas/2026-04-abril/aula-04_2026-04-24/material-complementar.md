# Material Complementar - Aula 04

Aqui estão recursos extras para você aprender mais sobre APIs REST e Flask.

---

## Vídeos Recomendados

### 1. **O Que é Uma API REST?** (Conceitual)
- **Título sugerido:** "API REST explicada para iniciantes"
- **Duração:** ~15 minutos
- **Por quê assistir:** Vai reforçar a analogia do garçom. Procure vídeos que usem analogias cotidianas.
- **Plataformas:** YouTube, Udemy
- **Dica:** Procure vídeos em português que mencionem "analogia da API"

### 2. **Flask Beginner Tutorial** (Prático)
- **Título sugerido:** "Python Flask Tutorial para Iniciantes"
- **Duração:** ~30-45 minutos
- **Por quê assistir:** Ver alguém criando uma aplicação Flask do zero ajuda a entender melhor.
- **Plataformas:** YouTube, Real Python
- **Dica:** Prefira vídeos de 2024-2025, pois o Flask evolui

### 3. **HTTP Methods Explained** (Teoria)
- **Título sugerido:** "HTTP GET, POST, PUT, DELETE explicados"
- **Duração:** ~10-15 minutos
- **Por quê assistir:** Entender a diferença entre os métodos HTTP é fundamental.
- **Plataformas:** YouTube, Codecademy
- **Dica:** Procure vídeos que usem exemplos visuais (diagramas de requisição/resposta)

---

## Artigos e Documentação

### 1. **O que é uma API REST?** (Leitura Geral)
- **Fonte:** MDN Web Docs ou freeCodeCamp
- **Por quê ler:** Explicações escritas muitas vezes são mais claras que vídeos.
- **Resumo:** Um artigo bem estruturado vai cobrir:
  - O que é API
  - O que é REST (Representational State Transfer)
  - Como APIs REST funcionam
  - Exemplos do mundo real

### 2. **Flask Official Documentation** (Referência)
- **Fonte:** https://flask.palletsprojects.com/
- **Por quê ler:** A documentação oficial é sempre a mais confiável.
- **Seções importantes:**
  - Quick Start (começo rápido)
  - Routing (como definir rotas)
  - Request Object (como pegar dados da requisição)

### 3. **Understanding HTTP Status Codes** (Técnico)
- **Fonte:** MDN Web Docs
- **Por quê ler:** Status codes (200, 404, 500) são essenciais para APIs.
- **Resumo:**
  - 200 = OK (sucesso)
  - 404 = Not Found (não encontrado)
  - 500 = Server Error (erro no servidor)
  - 201 = Created (criado com sucesso)

### 4. **JSON: A Lightweight Data Format** (Conceitual)
- **Fonte:** json.org ou tutoriais da W3Schools
- **Por quê ler:** Entender JSON é fundamental em APIs modernas.
- **Conceitos:**
  - Estrutura de chaves e valores
  - Tipos de dados em JSON (string, number, boolean, array, object)
  - Como JSON é usado em APIs

---

## Ferramentas para Testar APIs

### 1. **Postman** (Recomendado para Iniciantes)
- **O que é:** Uma ferramenta visual para testar APIs
- **Por quê usar:** Você clica em botões ao invés de digitar comandos
- **Como usar:**
  1. Baixe em https://www.postman.com/downloads/
  2. Crie uma nova requisição
  3. Selecione GET ou POST
  4. Digite a URL: http://localhost:5000/api/moradores
  5. Clique em Send
  6. Veja a resposta em JSON

### 2. **curl** (Mais Técnico)
- **O que é:** Ferramenta de linha de comando para testar APIs
- **Por quê usar:** Não precisa baixar nada, vem no terminal
- **Exemplo básico:**
  ```bash
  # GET (listar)
  curl http://localhost:5000/api/moradores

  # POST (adicionar)
  curl -X POST http://localhost:5000/api/moradores \
    -H "Content-Type: application/json" \
    -d '{"nome":"João","cpf":"123.456.789-00","apartamento":"101","email":"joao@email.com"}'
  ```

### 3. **Navegador Web**
- **O que é:** Sim, seu navegador é uma ferramenta de teste!
- **Por quê usar:** Simples e direto para testar GET
- **Exemplo:**
  1. Abra seu navegador
  2. Digite: http://localhost:5000/
  3. Digite: http://localhost:5000/api/moradores
  4. Veja a resposta formatada

### 4. **Insomnia** (Alternativa ao Postman)
- **O que é:** Similar ao Postman, mas mais leve
- **Por quê usar:** Se Postman for pesado para seu computador
- **Site:** https://insomnia.rest/

---

## Conceitos Importantes Resumidos

### O Ciclo de Uma Requisição HTTP

```
Seu Navegador        →  Servidor Flask        →  Seu Navegador
    (Cliente)              (Garçom)                  (Cliente)

1. Você digita URL      2. Servidor processa    3. Recebe resposta
2. Envia requisição     3. Busca dados          4. Mostra na tela
3. Aguarda resposta     4. Retorna JSON
```

### Métodos HTTP - Resumo

| Método | O Que Faz | Analogia |
|--------|-----------|----------|
| **GET** | Buscar dados | Pedir um café |
| **POST** | Criar dados | Fazer um novo pedido |
| **PUT** | Atualizar dados inteiros | Trocar o pedido por outro |
| **PATCH** | Atualizar dados parciais | Adicionar açúcar a um café já pronto |
| **DELETE** | Remover dados | Cancelar um pedido |

### JSON - Estrutura Básica

```json
{
  "nome": "João Silva",
  "cpf": "123.456.789-00",
  "apartamento": 101,
  "ativo": true
}
```

**Partes:**
- `{}` = Objeto (como um registro)
- `"chave": valor` = Pares chave-valor
- `"string"` = Texto (entre aspas)
- `123` = Número (sem aspas)
- `true/false` = Booleano (verdadeiro/falso)

---

## Dicas e Truques

### 1. **Reconhecer Erros Comuns**

**Erro: 404 Not Found**
- Significado: A rota não existe ou foi digitada errado
- Solução: Verifique a URL se está correta

**Erro: 500 Internal Server Error**
- Significado: Algo deu errado no servidor
- Solução: Verifique o terminal onde rodou o servidor para ver a mensagem de erro

**Erro: Connection Refused**
- Significado: O servidor não está rodando
- Solução: Execute `python src/app.py` novamente

### 2. **Estrutura do app.py**

Seu arquivo Flask segue este padrão:

```python
from flask import Flask
app = Flask(__name__)

@app.route('/rota', methods=['GET', 'POST'])
def funcao_rota():
    return jsonify({'dados': 'aqui'})

if __name__ == '__main__':
    app.run()
```

### 3. **JSON e Python**

- Python tem **dicionários** → JSON tem **objetos**
- Python tem **listas** → JSON tem **arrays**
- `jsonify()` do Flask converte Python em JSON automaticamente

```python
# Python
dados = {'nome': 'João', 'idade': 30}

# JSON (resultado de jsonify)
{"nome": "João", "idade": 30}
```

---

## Próximas Aulas - O Que Vem

Após dominar esta aula, você estará pronto para:

- **Aula 05:** Segurança - Validar dados antes de salvar
- **Aula 06:** Tratamento de erros melhorado
- **Aula 07:** Autenticação - Proteger suas rotas
- **Aula 08:** Deploy - Publicar seu servidor na internet

---

## Sites Úteis

- **Flask Documentation:** https://flask.palletsprojects.com/
- **Real Python Flask Tutorial:** https://realpython.com/flask-by-example/
- **REST API Best Practices:** https://restfulapi.net/
- **HTTP Status Codes:** https://httpwg.org/specs/rfc7231.html#status.codes
- **JSON Tutorial:** https://www.w3schools.com/js/js_json.asp
- **Python Documentation:** https://docs.python.org/3/

---

## Resumo Rápido

✅ **Uma API REST é como um garçom:** recebe seu pedido (requisição) e traz a resposta (dados em JSON)

✅ **GET busca dados, POST cria dados**

✅ **JSON é a lingua universal da web**

✅ **Flask é uma ferramenta para criar servidores em Python**

✅ **localhost:5000 é seu servidor local (só você acessa)**

✅ **Postman é uma ferramenta visual para testar APIs**

---

**Bom aprendizado! Se tiver dúvidas, revisit o README.md ou as instruções do exercício.** 📚
