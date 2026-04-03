#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
n7-portaria-ai — Aula 01: Arquitetura do Projeto
=================================================

Nesta aula, você não vai apenas "rodar um print".
Você vai CONFIGURAR um projeto Python profissional.

Conceitos que vamos praticar:
- Estrutura de pacotes Python (__init__.py)
- Configuração centralizada (config.py)
- Separação de camadas (models / services / app)
- Type hints e docstrings (clean code)
- Constantes vs variáveis
- Entry point profissional (__main__.py)

Seu trabalho: Complete os TODOs marcados abaixo!
Cada TODO ensina um conceito de arquitetura.
"""

import os
import sys
from dataclasses import dataclass
from typing import Optional


# ============================================
# CAMADA 1: CONFIGURAÇÃO (config.py na vida real)
# ============================================

# Em projetos reais, configurações ficam centralizadas.
# Nunca espalhe "strings mágicas" pelo código!

APP_NAME: str = "n7-portaria-ai"
APP_VERSION: str = "0.1.0"
APP_DESCRIPTION: str = "Sistema de Portaria Inteligente para Condomínios"

# TODO 1 — CONSTANTES DE CONFIGURAÇÃO
# Defina estas constantes seguindo o padrão UPPER_SNAKE_CASE:
#
# DATABASE_NAME  → deve valer "portaria.db"
# MAX_MORADORES  → deve valer 500
# DEBUG_MODE     → deve valer True
#
# Por que isso importa?
# Constantes centralizadas permitem mudar o comportamento
# do sistema inteiro alterando UMA única linha.
# Exemplo: trocar "portaria.db" por "portaria_prod.db"
#
# Escreva as 3 linhas abaixo:




# ============================================
# CAMADA 2: MODELO (models/ na vida real)
# ============================================

# Modelos representam os DADOS do sistema.
# Usamos @dataclass para criar classes limpas, sem boilerplate.
# Cada modelo é um "molde" para um tipo de dado.

@dataclass
class Morador:
    """
    Representa um morador do condomínio.

    Em arquitetura limpa, o Model NÃO sabe sobre banco de dados,
    NÃO sabe sobre interface, NÃO sabe sobre nada além dos dados.
    Ele é o "coração" isolado do sistema.

    Attributes:
        nome: Nome completo do morador
        apartamento: Número do apartamento (ex: "101", "302A")
        bloco: Bloco do condomínio (opcional)
    """
    nome: str
    apartamento: str
    bloco: Optional[str] = None

    # TODO 2 — MÉTODO DO MODELO
    # Crie um método chamado 'endereco_completo' que retorna
    # uma string formatada com o endereço do morador.
    #
    # Se o morador tem bloco: "Apto 101 - Bloco A"
    # Se NÃO tem bloco:      "Apto 101"
    #
    # Conceito: Encapsulamento — a lógica de formatar o endereço
    # pertence ao MODELO, não ao código que usa o modelo.
    #
    # Dica: use f-string e um if/else
    #
    # def endereco_completo(self) -> str:
    #     ...




# TODO 3 — CRIAR UM SEGUNDO MODELO
# Crie a classe Visitante usando @dataclass, seguindo o mesmo padrão:
#
# Campos obrigatórios:
#   - nome: str
#   - documento: str  (CPF ou RG)
#   - motivo: str     (motivo da visita)
#
# Campos opcionais:
#   - telefone: Optional[str] = None
#
# Conceito: Cada entidade do negócio vira um modelo separado.
# Isso é a base do Domain-Driven Design (DDD) simplificado.
#
# @dataclass
# class Visitante:
#     ...




# ============================================
# CAMADA 3: SERVIÇO (services/ na vida real)
# ============================================

# Serviços contêm a LÓGICA DE NEGÓCIO.
# Eles orquestram modelos, validam dados, aplicam regras.
# O serviço NÃO sabe sobre interface (print/input).

class PortariaService:
    """
    Serviço principal da portaria.

    Responsabilidades:
    - Gerenciar lista de moradores
    - Registrar visitantes
    - Aplicar regras de negócio

    Em arquitetura limpa, o Service é a camada que SABE
    como o negócio funciona. A interface apenas chama o service.
    """

    def __init__(self):
        """Inicializa o serviço com listas vazias."""
        self._moradores: list[Morador] = []
        self._visitantes: list = []  # Será list[Visitante] após TODO 3

    def cadastrar_morador(self, nome: str, apartamento: str, bloco: Optional[str] = None) -> Morador:
        """
        Cadastra um novo morador no sistema.

        Args:
            nome: Nome completo
            apartamento: Número do apartamento
            bloco: Bloco (opcional)

        Returns:
            O morador cadastrado

        Raises:
            ValueError: Se nome estiver vazio ou apartamento duplicado
        """
        # Validação: nome não pode ser vazio
        if not nome.strip():
            raise ValueError("Nome do morador não pode ser vazio")

        # Validação: apartamento não pode ser duplicado no mesmo bloco
        for m in self._moradores:
            if m.apartamento == apartamento and m.bloco == bloco:
                raise ValueError(f"Já existe morador no Apto {apartamento}" +
                                 (f" Bloco {bloco}" if bloco else ""))

        # Cria e armazena o morador
        morador = Morador(nome=nome, apartamento=apartamento, bloco=bloco)
        self._moradores.append(morador)
        return morador

    # TODO 4 — MÉTODO DE LISTAGEM COM FILTRO
    # Crie um método chamado 'listar_moradores' que:
    #
    # - Recebe um parâmetro opcional 'bloco: Optional[str] = None'
    # - Se bloco for None, retorna TODOS os moradores (self._moradores)
    # - Se bloco foi informado, retorna apenas os moradores daquele bloco
    # - Retorna uma list[Morador]
    #
    # Conceito: Filtros ficam no SERVICE, nunca na interface.
    # A interface só chama: service.listar_moradores(bloco="A")
    #
    # Dica: use list comprehension
    #   [m for m in self._moradores if m.bloco == bloco]
    #
    # def listar_moradores(self, bloco: Optional[str] = None) -> list[Morador]:
    #     ...



    @property
    def total_moradores(self) -> int:
        """Retorna o total de moradores cadastrados."""
        return len(self._moradores)


# ============================================
# CAMADA 4: INTERFACE / APP (a "casca" do sistema)
# ============================================

# A interface é a camada mais EXTERNA.
# Ela faz print/input e chama o Service.
# Se amanhã trocarmos print por GUI ou Web, só esta camada muda.

def exibir_cabecalho() -> None:
    """Exibe o cabeçalho do sistema no terminal."""
    largura = 50
    print("=" * largura)
    print(f"  {APP_NAME} v{APP_VERSION}")
    print(f"  {APP_DESCRIPTION}")
    print("=" * largura)


def exibir_resumo(service: PortariaService) -> None:
    """
    Exibe um resumo do estado atual do sistema.

    Note que recebemos o service como parâmetro.
    Isso é INJEÇÃO DE DEPENDÊNCIA simplificada:
    a função não cria o service, ela RECEBE pronto.
    """
    print(f"\n📊 Resumo do Sistema:")
    print(f"   Moradores cadastrados: {service.total_moradores}")
    print(f"   Banco de dados: {DATABASE_NAME}")
    print(f"   Modo debug: {'Ativado' if DEBUG_MODE else 'Desativado'}")


# TODO 5 — FUNÇÃO DA INTERFACE: CADASTRO INTERATIVO
# Crie uma função chamada 'cadastrar_morador_interativo' que:
#
# - Recebe o service (service: PortariaService) como parâmetro
# - Pede ao usuário: nome (input), apartamento (input), bloco (input, pode ser vazio)
# - Chama service.cadastrar_morador(...) com os dados
# - Se der erro (ValueError), imprime a mensagem de erro
# - Se der certo, imprime "Morador cadastrado: {morador.endereco_completo()}"
#
# Conceito: A interface NUNCA manipula dados diretamente.
# Ela pede input → chama o service → mostra o resultado.
#
# Estrutura:
# def cadastrar_morador_interativo(service: PortariaService) -> None:
#     nome = input("Nome do morador: ")
#     apartamento = input("Apartamento: ")
#     bloco = input("Bloco (Enter para pular): ").strip() or None
#     try:
#         morador = service.cadastrar_morador(...)
#         print(f"✅ Morador cadastrado: {morador.endereco_completo()}")
#     except ValueError as e:
#         print(f"❌ Erro: {e}")




def main() -> None:
    """
    Função principal — orquestra o fluxo do programa.

    Arquitetura do fluxo:
    1. Exibe cabeçalho (interface)
    2. Cria o service (lógica de negócio)
    3. Cadastra dados de exemplo (service)
    4. Interage com usuário (interface → service)
    5. Exibe resumo (interface ← service)
    """
    # 1. Interface: cabeçalho
    exibir_cabecalho()

    # 2. Cria a instância do serviço (aqui nasce a "engine" do sistema)
    service = PortariaService()

    # 3. Cadastra moradores de exemplo para demonstração
    print("\n📋 Cadastrando moradores de exemplo...")
    try:
        m1 = service.cadastrar_morador("Maria Silva", "101", "A")
        m2 = service.cadastrar_morador("João Santos", "202", "B")
        m3 = service.cadastrar_morador("Ana Oliveira", "303")  # Sem bloco

        print(f"   → {m1.nome}: {m1.endereco_completo()}")
        print(f"   → {m2.nome}: {m2.endereco_completo()}")
        print(f"   → {m3.nome}: {m3.endereco_completo()}")
    except ValueError as e:
        print(f"   ⚠️ Erro no cadastro de exemplo: {e}")

    # TODO 6 — TESTAR O FILTRO POR BLOCO
    # Use o método listar_moradores() que você criou no TODO 4.
    #
    # a) Liste todos os moradores do Bloco A:
    #    moradores_a = service.listar_moradores(bloco="A")
    #    print(f"\nMoradores do Bloco A: {len(moradores_a)}")
    #
    # b) Liste TODOS os moradores (sem filtro):
    #    todos = service.listar_moradores()
    #    print(f"Total de moradores: {len(todos)}")
    #
    # Conceito: O service faz o filtro. A interface só exibe.



    # TODO 7 — CHAMAR A FUNÇÃO DE CADASTRO INTERATIVO
    # Chame a função que você criou no TODO 5:
    #
    # print("\n👤 Cadastre um novo morador:")
    # cadastrar_morador_interativo(service)
    #
    # Conceito: A main() é o "maestro" — ela não toca instrumento,
    # ela coordena quem toca.



    # 5. Exibe resumo final
    exibir_resumo(service)

    # Mensagem de encerramento
    print(f"\n{'=' * 50}")
    print("  Ademilson, cada camada do código tem seu lugar.")
    print("  Assim como cada pessoa no condomínio. 🏢")
    print(f"{'=' * 50}\n")


# ============================================
# ENTRY POINT PROFISSIONAL
# ============================================

# Em projetos reais, este bloco fica em __main__.py
# Por enquanto, usamos aqui. Na Aula 02 vamos separar!

if __name__ == "__main__":
    main()
