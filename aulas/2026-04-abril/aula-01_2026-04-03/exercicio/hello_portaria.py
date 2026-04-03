#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sistema de Portaria Inteligente - Primeiro Script
=================================================

Este é o seu primeiro script Python!
Ele vai demonstrar conceitos básicos como:
- Variáveis e strings
- Funções
- Entrada de dados do usuário (input)
- Saída de dados (print)

Seu trabalho: Complete os TODOs marcados abaixo!
Boa sorte!
"""

# ============================================
# CONFIGURAÇÕES DO SISTEMA
# ============================================

# A versão do nosso sistema
VERSAO_SISTEMA = "1.0.0"

# Caracteres para criar linhas bonitas
LINHA_SEPARADORA = "========================================="


# ============================================
# FUNÇÕES DO SISTEMA
# ============================================

def obter_nome_portaria():
    """
    Esta função pede ao usuário o nome da portaria.

    Ela não recebe nenhum parâmetro de entrada.
    Ela retorna uma string com o nome digitado pelo usuário.

    Exemplo:
        >>> obter_nome_portaria()
        Digite o nome da sua portaria: Portaria Central
        "Portaria Central"
    """

    # Exibe uma mensagem amigável para o usuário
    print("\nDigite o nome da sua portaria: ", end="")

    # TODO 1: Use input() para ler o que o usuário digita
    # A função input() para e espera o usuário digitar algo e pressionar Enter
    # Guarde o resultado em uma variável chamada 'nome'
    # Dica: nome = input(...)

    # TODO 2: Retorne o nome que foi digitado
    # Use a palavra-chave 'return' para devolver o valor
    # Dica: return ...


def exibir_versao_sistema():
    """
    Esta função mostra qual versão do sistema está sendo usada.

    Ela não recebe parâmetros.
    Ela não retorna nada (apenas imprime na tela).
    """
    print(f"Você está usando o Sistema de Portaria v{VERSAO_SISTEMA}")


def exibir_mensagem_boas_vindas(nome_portaria):
    """
    Esta função exibe uma mensagem bonita de boas-vindas.

    Ela recebe um parâmetro:
    - nome_portaria: o nome da portaria (uma string)

    Ela imprime uma mensagem formatada com o nome.

    Exemplo:
        >>> exibir_mensagem_boas_vindas("Portaria Central")
        Olá Portaria Central!
        Você está usando o Sistema de Portaria v1.0.0
        Vamos gerenciar seu condominio com inteligência!
    """

    # Exibe a linha separadora (fica bonito!)
    print(LINHA_SEPARADORA)

    # Exibe a mensagem de boas-vindas com o nome da portaria
    # Note o f-string: f"..." permite colocar variáveis dentro de strings com {variável}
    print(f"Olá {nome_portaria}!")

    # Mostra a versão
    exibir_versao_sistema()

    # Mensagem de motivação
    print("Vamos gerenciar seu condominio com inteligência!")

    # Exibe a linha separadora novamente
    print(LINHA_SEPARADORA)


def main():
    """
    Esta é a função principal do programa.
    Ela coordena todas as outras funções.

    Ordem das coisas:
    1. Mostrar boas-vindas iniciais
    2. Pedir o nome da portaria
    3. Mostrar mensagem de boas-vindas personalizada
    """

    # Mensagem inicial (esta parte já está completa para você ver como funciona)
    print("\nBem-vindo ao Sistema de Portaria Inteligente!")

    # TODO 3: Chame a função obter_nome_portaria() e guarde o resultado
    # em uma variável chamada 'nome'
    # Dica: nome = obter_nome_portaria()

    # TODO 4: Chame a função exibir_mensagem_boas_vindas() passando o nome
    # como parâmetro
    # Dica: exibir_mensagem_boas_vindas(...)


# ============================================
# PONTO DE ENTRADA DO PROGRAMA
# ============================================

# Em Python, 'if __name__ == "__main__":' significa:
# "Execute isto apenas se este arquivo foi rodado diretamente
# (não se foi importado como biblioteca em outro arquivo)"
if __name__ == "__main__":
    # Chama a função principal
    main()

    # Mensagem final amigável
    print("\nAté a próxima! 👋\n")
