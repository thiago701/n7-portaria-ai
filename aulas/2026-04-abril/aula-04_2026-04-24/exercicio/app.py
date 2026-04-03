"""
AULA 04 - API REST COM FLASK: Primeira Rota com Flask

Objetivo: Criar um servidor web que funciona como garçom digital,
recebendo pedidos (requisições) e devolvendo respostas (JSON).

Este arquivo demonstra como criar uma API REST simples para gerenciar
moradores do condomínio usando Flask e SQLite.

Instruções: Procure pelos comentários TODO para saber onde escrever seu código.
"""

from flask import Flask, request, jsonify
import sqlite3
import os

# Criar a aplicação Flask
# Flask é uma "máquina de garçom" que ouve por requisições HTTP
app = Flask(__name__)

# ============================================================================
# FUNÇÃO AUXILIAR: Conectar ao Banco de Dados
# ============================================================================

def conectar_banco():
    """
    Conecta ao banco de dados SQLite do projeto.

    O banco 'portaria.db' deve estar na mesma pasta onde você roda este script.
    Se não existir, você pode criar rodando primeiro o exercício da Aula 03 (CRUD).

    Retorna: conexão com o banco de dados
    """
    # Definir caminho do banco de dados
    # Este código pega o diretório onde app.py está e procura pelo banco lá
    caminho_app = os.path.dirname(os.path.abspath(__file__))
    caminho_banco = os.path.join(caminho_app, '..', '..', '..', 'portaria.db')

    conn = sqlite3.connect(caminho_banco)
    conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    return conn


# ============================================================================
# ROTA 1: Boas-vindas
# ============================================================================

@app.route('/', methods=['GET'])
def boas_vindas():
    """
    Rota de boas-vindas simples.

    Quando alguém acessa http://localhost:5000/
    o servidor responde com uma mensagem JSON.

    GET significa: "Me mostre algo" (ler dados)
    JSON é um formato de dados que computadores entendem bem.
    """
    resposta = {
        'mensagem': 'Bem-vindo ao Sistema de Portaria!',
        'versao': '1.0.0',
        'descricao': 'API para gerenciar moradores do condomínio'
    }
    return jsonify(resposta)


# ============================================================================
# ROTA 2: Listar Todos os Moradores (GET)
# ============================================================================

# TODO 1: Implementar GET /api/moradores - Listar todos os moradores
#
# INSTRUÇÃO:
# Este endpoint deve retornar uma lista de todos os moradores cadastrados.
#
# Siga os passos:
# 1. Conecte ao banco com conectar_banco()
# 2. Execute um SELECT * para trazer todos os moradores
# 3. Use fetchall() para pegar a lista completa
# 4. Feche a conexão com conn.close()
# 5. Retorne os dados com jsonify()
#
# Exemplo de teste:
#   http://localhost:5000/api/moradores
#
# Esperado:
#   Uma lista em JSON com todos os moradores
#   Se vazio: []

@app.route('/api/moradores', methods=['GET'])
def listar_moradores():
    """
    Lista todos os moradores do condomínio.

    Método HTTP: GET
    Usa-se GET quando quer SÓ BUSCAR dados (sem criar ou modificar).

    Retorna: JSON com lista de todos os moradores
    """
    try:
        # Escreva seu código aqui
        # Dica: use conectar_banco(), cursor.execute(), fetchall(), jsonify()
        pass

    except Exception as e:
        return jsonify({'erro': f'Erro ao listar moradores: {str(e)}'}), 500


# ============================================================================
# ROTA 3: Adicionar um Novo Morador (POST)
# ============================================================================

# TODO 2: Implementar POST /api/moradores - Adicionar novo morador
#
# INSTRUÇÃO:
# Este endpoint deve receber dados JSON (nome, cpf, apartamento, email)
# e inserir um novo morador no banco de dados.
#
# Siga os passos:
# 1. Use request.get_json() para pegar os dados enviados
# 2. Extraia: nome, cpf, apartamento, email
# 3. Conecte ao banco
# 4. Execute um INSERT com esses valores
# 5. Faça commit() para salvar
# 6. Feche a conexão
# 7. Retorne uma mensagem de sucesso em JSON
#
# Exemplo de teste (usando curl):
#   curl -X POST http://localhost:5000/api/moradores \
#     -H "Content-Type: application/json" \
#     -d '{"nome":"João Silva","cpf":"123.456.789-00","apartamento":"101","email":"joao@email.com"}'
#
# Esperado:
#   {"mensagem": "Morador adicionado com sucesso!"}

@app.route('/api/moradores', methods=['POST'])
def adicionar_morador():
    """
    Adiciona um novo morador ao banco de dados.

    Método HTTP: POST
    Usa-se POST quando quer CRIAR ou MODIFICAR dados (enviar algo novo).

    Espera receber JSON no formato:
    {
        "nome": "Nome do Morador",
        "cpf": "123.456.789-00",
        "apartamento": "101",
        "email": "morador@email.com"
    }

    Retorna: JSON com mensagem de sucesso ou erro
    """
    try:
        # Escreva seu código aqui
        # Dica: use request.get_json(), conectar_banco(),
        #       cursor.execute() com INSERT, commit(), jsonify()
        pass

    except Exception as e:
        return jsonify({'erro': f'Erro ao adicionar morador: {str(e)}'}), 500


# ============================================================================
# ROTA 4: Obter um Morador Específico (GET com ID)
# ============================================================================

# TODO 3: Implementar GET /api/moradores/<id> - Buscar um morador específico
#
# INSTRUÇÃO:
# Este endpoint deve buscar um morador pelo ID e retornar seus dados.
#
# Siga os passos:
# 1. Use <int:id> para receber o ID da URL
# 2. Conecte ao banco
# 3. Execute SELECT * WHERE id = ? para encontrar o morador
# 4. Use fetchone() para pegar UMA linha apenas
# 5. Se não encontrou (None), retorne erro 404
# 6. Se encontrou, retorne os dados com jsonify()
# 7. Feche a conexão
#
# Exemplo de teste:
#   http://localhost:5000/api/moradores/1
#   http://localhost:5000/api/moradores/2
#
# Esperado:
#   Se encontrou: {"id": 1, "nome": "João Silva", ...}
#   Se não encontrou: {"erro": "Morador não encontrado"} com código 404

@app.route('/api/moradores/<int:id>', methods=['GET'])
def obter_morador(id):
    """
    Obtém os dados de um morador específico pelo ID.

    Método HTTP: GET
    A URL contém o ID do morador que queremos buscar.

    Parâmetro de URL: id (número inteiro)

    Retorna: JSON com dados do morador ou mensagem de erro
    """
    try:
        # Escreva seu código aqui
        # Dica: use conectar_banco(), cursor.execute() com WHERE,
        #       fetchone(), jsonify()
        #
        # NÃO ESQUEÇA: Se não encontrou, retorne 404 assim:
        #   return jsonify({'erro': 'Morador não encontrado'}), 404
        pass

    except Exception as e:
        return jsonify({'erro': f'Erro ao obter morador: {str(e)}'}), 500


# ============================================================================
# EXECUTAR O SERVIDOR (Main)
# ============================================================================

if __name__ == '__main__':
    """
    Este bloco executa quando você roda:
        python src/app.py

    debug=True significa que o servidor vai reiniciar automaticamente
    quando você modifica o arquivo (muito útil durante desenvolvimento).

    host='127.0.0.1' significa que só você no seu computador pode acessar.
    port=5000 é a "porta" do servidor (como um número de telefone para o servidor).

    Para acessar: http://localhost:5000/
    """
    print("\n" + "="*60)
    print("SISTEMA DE PORTARIA - API REST")
    print("="*60)
    print("Servidor iniciando em: http://127.0.0.1:5000")
    print("Para parar o servidor, pressione CTRL+C")
    print("\nRotas disponíveis:")
    print("  GET  http://localhost:5000/                 → Boas-vindas")
    print("  GET  http://localhost:5000/api/moradores    → Listar todos")
    print("  POST http://localhost:5000/api/moradores    → Adicionar novo")
    print("  GET  http://localhost:5000/api/moradores/<id> → Buscar por ID")
    print("="*60 + "\n")

    # Inicia o servidor Flask
    app.run(host='127.0.0.1', port=5000, debug=True)
