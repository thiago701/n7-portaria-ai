"""
Aula 03: CRUD Completo de Moradores
===================================

Projeto: Sistema de Gerenciamento de Moradores da Portaria
Objetivo: Implementar as 4 operações mágicas (CRUD) em Python

Este arquivo é um exercício - algumas funções estão incompletas
com TODOs. Sua tarefa é completar essas funções!

Adelilson, você está no caminho certo! Python é uma linguagem
muito lógica, e CRUD é a base de tudo. Vamos lá!
"""

import sqlite3
from datetime import datetime

# ============================================================================
# CONEXÃO COM O BANCO DE DADOS
# ============================================================================

# Conectamos ao banco de dados. Se não existir, ele cria automaticamente.
conexao = sqlite3.connect('moradores.db')
cursor = conexao.cursor()

# Criamos a tabela se ela não existir (idempotente - roda sem problema mesmo
# se a tabela já existe)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS moradores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT UNIQUE NOT NULL,
        numero_residencia TEXT NOT NULL,
        bloco TEXT DEFAULT 'A',
        telefone TEXT,
        email TEXT,
        tipo_morador TEXT DEFAULT 'proprietario'
            CHECK(tipo_morador IN ('proprietario', 'inquilino')),
        foto_url TEXT,
        dt_foto_validade TEXT,
        biometria_hash TEXT,
        dt_biometria_validade TEXT,
        ativo INTEGER DEFAULT 1,
        dt_criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
        dt_atualizado_em TEXT DEFAULT CURRENT_TIMESTAMP
    )
""")
conexao.commit()

# ============================================================================
# FUNÇÕES AUXILIARES (já prontas - você pode usar!)
# ============================================================================

def limpar_tela():
    """Limpa a tela do terminal para deixar mais organizado."""
    import os
    os.system('clear' if os.name == 'posix' else 'cls')


def formatar_cpf(cpf):
    """Formata CPF para exibição bonita: 12345678901 -> 123.456.789-01"""
    try:
        if len(cpf) == 11:
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    except:
        pass
    return cpf


def buscar_morador_por_cpf(cpf):
    """
    Busca um morador no banco pelo CPF.
    Retorna os dados (tupla) se encontrar, ou None se não encontrar.

    Isso é útil para validar se um CPF já existe antes de cadastrar!
    """
    try:
        cursor.execute("SELECT * FROM moradores WHERE cpf = ?", (cpf,))
        resultado = cursor.fetchone()
        return resultado
    except Exception as erro:
        print(f"Erro ao buscar CPF: {erro}")
        return None


def obter_data_hora_atual():
    """Retorna a data e hora atual formatada."""
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


# ============================================================================
# OPERAÇÕES CRUD - COMPLETE ESTAS FUNÇÕES!
# ============================================================================

def cadastrar_morador():
    """
    CREATE: Adiciona um novo morador ao banco de dados.

    Tarefa: Complete esta função seguindo os TODOs abaixo.

    O que você precisa fazer:
    1. Pedir os dados do morador ao usuário
    2. Validar se o CPF já existe (usar buscar_morador_por_cpf)
    3. Se existir, mostrar erro e retornar
    4. Se não existir, inserir no banco com INSERT
    5. Usar try/except para tratar erros
    6. Mostrar mensagem de sucesso ou erro
    """
    print("\n" + "="*60)
    print("CADASTRAR NOVO MORADOR")
    print("="*60)

    try:
        # TODO 1: Peça o nome ao usuário
        nome = input("Nome do morador: ").strip()

        # TODO 2: Peça o CPF (sem pontos)
        cpf = input("CPF (somente números): ").strip()

        # TODO 3: Peça o numero_residencia
        numero_residencia = input("Apartamento (ex: 101, 202): ").strip()

        # TODO 4: Peça o email
        email = input("Email: ").strip()

        # Validação: CPF não pode estar vazio
        if not cpf or len(cpf) != 11:
            print("Erro: CPF deve ter 11 dígitos!")
            return

        # Validação: Nome não pode estar vazio
        if not nome:
            print("Erro: Nome não pode estar vazio!")
            return

        # TODO 5: Valide se o CPF já existe usando buscar_morador_por_cpf()
        morador_existente = buscar_morador_por_cpf(cpf)
        if morador_existente is not None:
            print(f"Erro: Já existe um morador com o CPF {formatar_cpf(cpf)}")
            print(f"       Nome: {morador_existente[1]}")
            return

        # TODO 6: Insira o novo morador no banco de dados
        # Use: cursor.execute("INSERT INTO moradores (...) VALUES (...)", (...))
        data_atual = obter_data_hora_atual()
        cursor.execute(
            """INSERT INTO moradores
               (nome, cpf, numero_residencia, email, data_cadastro, data_atualizacao)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (nome, cpf, numero_residencia, email, data_atual, data_atual)
        )

        # Salva as mudanças no banco (IMPORTANTE!)
        conexao.commit()

        print("\nSucesso! Morador cadastrado com sucesso!")
        print(f"Nome: {nome}")
        print(f"CPF: {formatar_cpf(cpf)}")
        print(f"Apartamento: {numero_residencia}")

    except sqlite3.IntegrityError as erro:
        print(f"Erro de integridade: CPF pode estar duplicado!")
        print(f"Detalhes: {erro}")
    except Exception as erro:
        print(f"Erro ao cadastrar morador: {erro}")


def listar_moradores():
    """
    READ: Lista todos os moradores cadastrados e ativos.

    Tarefa: Complete esta função.

    O que você precisa fazer:
    1. Executar SELECT para trazer todos os moradores ATIVOS
    2. Usar fetchall() para pegar todos os resultados
    3. Se não houver resultados, mostre "Nenhum morador"
    4. Se houver, mostre em formato tabela legal
    5. Use try/except para erros
    """
    print("\n" + "="*60)
    print("LISTA DE MORADORES")
    print("="*60)

    try:
        # TODO 1: Execute SELECT para trazer moradores onde ativo = 1
        cursor.execute(
            "SELECT id, nome, cpf, numero_residencia, email FROM moradores WHERE ativo = 1 ORDER BY nome"
        )

        # TODO 2: Busque todos os resultados
        moradores = cursor.fetchall()

        # TODO 3: Se não houver resultados, mostre mensagem
        if not moradores:
            print("\nNenhum morador cadastrado ainda.")
            return

        # TODO 4: Mostre os dados em forma de tabela
        print(f"\nTotal de moradores: {len(moradores)}\n")
        print(f"{'ID':<4} {'Nome':<25} {'CPF':<14} {'Apto':<6} {'Email':<25}")
        print("-" * 80)

        for morador in moradores:
            id_m, nome, cpf, numero_residencia, email = morador
            cpf_formatado = formatar_cpf(cpf)
            email_display = email if email else "Sem email"
            print(f"{id_m:<4} {nome:<25} {cpf_formatado:<14} {numero_residencia:<6} {email_display:<25}")

    except Exception as erro:
        print(f"Erro ao listar moradores: {erro}")


def buscar_morador():
    """
    READ específico: Procura um morador pelo nome.

    Tarefa: Complete esta função.

    O que você precisa fazer:
    1. Peça um nome ao usuário
    2. Use SELECT com LIKE para busca parcial
    3. Se encontrar, mostre os dados
    4. Se não encontrar, mostre "Não encontrado"
    5. Use try/except
    """
    print("\n" + "="*60)
    print("BUSCAR MORADOR")
    print("="*60)

    try:
        # TODO 1: Peça o nome ao usuário
        nome_busca = input("\nDigite parte do nome do morador: ").strip()

        if not nome_busca:
            print("Erro: Digite um nome para buscar!")
            return

        # TODO 2: Execute SELECT com LIKE para busca parcial
        # Dica: Use % antes e depois do nome para buscar em qualquer posição
        cursor.execute(
            "SELECT id, nome, cpf, numero_residencia, email, ativo FROM moradores WHERE nome LIKE ? AND ativo = 1",
            (f"%{nome_busca}%",)
        )

        # TODO 3: Busque todos os resultados
        resultados = cursor.fetchall()

        # TODO 4: Se não encontrou, mostre mensagem
        if not resultados:
            print(f"\nNenhum morador encontrado com o nome '{nome_busca}'")
            return

        # Mostre os resultados encontrados
        print(f"\nEncontrado(s) {len(resultados)} morador(es):\n")

        for morador in resultados:
            id_m, nome, cpf, numero_residencia, email, ativo = morador
            status = "Ativo" if ativo == 1 else "Inativo"
            print(f"ID: {id_m}")
            print(f"Nome: {nome}")
            print(f"CPF: {formatar_cpf(cpf)}")
            print(f"Apartamento: {numero_residencia}")
            print(f"Email: {email if email else 'Sem email'}")
            print(f"Status: {status}")
            print("-" * 40)

    except Exception as erro:
        print(f"Erro ao buscar morador: {erro}")


def atualizar_morador():
    """
    UPDATE: Atualiza os dados de um morador existente.

    IMPORTANTE: Esta função está PRONTA como exemplo!
    Estude ela para entender como fazer UPDATE.
    """
    print("\n" + "="*60)
    print("ATUALIZAR MORADOR")
    print("="*60)

    try:
        # Primeiro, pedimos o ID do morador que quer atualizar
        id_morador = input("\nID do morador a atualizar: ").strip()

        try:
            id_morador = int(id_morador)
        except ValueError:
            print("Erro: ID deve ser um número!")
            return

        # Verificamos se o morador existe
        cursor.execute("SELECT * FROM moradores WHERE id = ?", (id_morador,))
        morador = cursor.fetchone()

        if not morador:
            print("Morador não encontrado!")
            return

        # Mostramos os dados atuais
        print(f"\nDados atuais:")
        print(f"Nome: {morador[1]}")
        print(f"CPF: {formatar_cpf(morador[2])}")
        print(f"Apartamento: {morador[3]}")
        print(f"Email: {morador[4]}")

        # Pedimos os novos dados
        print("\nDigite os novos dados (deixe em branco para manter o atual):")
        novo_nome = input("Novo nome: ").strip() or morador[1]
        novo_email = input("Novo email: ").strip() or morador[4]
        novo_apartamento = input("Novo numero_residencia: ").strip() or morador[3]

        # Atualizamos no banco
        data_atual = obter_data_hora_atual()
        cursor.execute(
            """UPDATE moradores
               SET nome = ?, email = ?, numero_residencia = ?, data_atualizacao = ?
               WHERE id = ?""",
            (novo_nome, novo_email, novo_apartamento, data_atual, id_morador)
        )

        conexao.commit()

        print("\nSucesso! Morador atualizado com sucesso!")

    except Exception as erro:
        print(f"Erro ao atualizar morador: {erro}")


def desativar_morador():
    """
    DELETE (macio): Marca um morador como inativo.

    Tarefa: Complete esta função.

    IMPORTANTE: Não deletamos de verdade! Apenas marcamos como inativo.
    Isso é mais seguro e permite recuperar dados depois.

    O que você precisa fazer:
    1. Peça o ID do morador
    2. Valide se é um número
    3. Execute UPDATE para marcar como inativo (ativo = 0)
    4. Use try/except
    5. Mostre mensagem de sucesso ou erro
    """
    print("\n" + "="*60)
    print("DESATIVAR MORADOR")
    print("="*60)

    try:
        # TODO 1: Peça o ID do morador
        id_morador = input("\nID do morador a desativar: ").strip()

        # TODO 2: Valide se é um número inteiro
        try:
            id_morador = int(id_morador)
        except ValueError:
            print("Erro: ID deve ser um número!")
            return

        # Verificamos se o morador existe
        cursor.execute("SELECT * FROM moradores WHERE id = ?", (id_morador,))
        morador = cursor.fetchone()

        if not morador:
            print("Morador não encontrado!")
            return

        # Confirmação antes de desativar
        print(f"\nVocê tem certeza que quer desativar o morador {morador[1]}?")
        confirmacao = input("Digite 's' para sim ou 'n' para não: ").strip().lower()

        if confirmacao != 's':
            print("Operação cancelada!")
            return

        # TODO 3: Execute UPDATE para marcar como inativo
        # Use: cursor.execute("UPDATE moradores SET ativo = 0 WHERE id = ?", ...)
        data_atual = obter_data_hora_atual()
        cursor.execute(
            "UPDATE moradores SET ativo = 0, data_atualizacao = ? WHERE id = ?",
            (data_atual, id_morador)
        )

        # Salva as mudanças
        conexao.commit()

        # TODO 4: Mostre mensagem de sucesso
        print(f"\nSucesso! Morador {morador[1]} foi desativado.")
        print("(Os dados foram preservados e podem ser reativados se necessário)")

    except Exception as erro:
        print(f"Erro ao desativar morador: {erro}")


# ============================================================================
# FUNÇÃO MENU - JÁ PRONTA!
# ============================================================================

def menu():
    """
    Mostra o menu de opções e retorna a escolha do usuário.

    Esta função já está completa - você só precisa implementar as funções
    CRUD que ela chama!
    """
    print("\n" + "="*60)
    print("SISTEMA DE GERENCIAMENTO DE MORADORES - PORTARIA")
    print("="*60)
    print("\nO que você gostaria de fazer?")
    print("\n1. Cadastrar novo morador")
    print("2. Listar todos os moradores")
    print("3. Buscar morador pelo nome")
    print("4. Atualizar dados de um morador")
    print("5. Desativar um morador")
    print("0. Sair do sistema")
    print("-"*60)

    opcao = input("\nDigite sua escolha (0-5): ").strip()

    return opcao


# ============================================================================
# LOOP PRINCIPAL
# ============================================================================

def main():
    """
    Loop principal do programa.

    Mostra o menu e executa a operação escolhida pelo usuário.
    """
    print("\nBem-vindo, Ademilson!")
    print("Você está aprendendo programação no melhor estilo:")
    print("Praticando com código de VERDADE!\n")

    while True:
        opcao = menu()

        if opcao == "1":
            cadastrar_morador()
        elif opcao == "2":
            listar_moradores()
        elif opcao == "3":
            buscar_morador()
        elif opcao == "4":
            atualizar_morador()
        elif opcao == "5":
            desativar_morador()
        elif opcao == "0":
            print("\n" + "="*60)
            print("Obrigado por usar o sistema!")
            print("Até a próxima aula! Você está indo muito bem!")
            print("="*60 + "\n")

            # Fecha a conexão com o banco de forma segura
            conexao.close()
            break
        else:
            print("\nOpção inválida! Digite uma opção entre 0 e 5.")

        # Pequena pausa para o usuário ver a mensagem
        input("\nPressione ENTER para continuar...")


# ============================================================================
# PONTO DE ENTRADA DO PROGRAMA
# ============================================================================

if __name__ == "__main__":
    # Se este arquivo for executado como programa principal, inicia o main()
    main()

