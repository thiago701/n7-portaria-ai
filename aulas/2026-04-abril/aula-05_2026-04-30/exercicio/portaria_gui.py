"""
=============================================================
  n7-portaria-ai — Interface Gráfica da Portaria
  Aula 05: Dando Rosto ao Nosso Sistema
=============================================================

  Ademilson, este é o nosso programa com INTERFACE GRÁFICA!
  Até agora usamos o terminal (tela preta). Hoje vamos
  criar uma JANELA bonita com campos e botões.

  Você vai completar 3 TODOs para fazer tudo funcionar.
  Boa sorte! Você consegue! 💪

=============================================================
"""

# ---- IMPORTAÇÕES ----
# customtkinter = biblioteca para criar janelas bonitas
# sqlite3 = biblioteca para acessar o banco de dados
# tkinter.messagebox = para mostrar mensagens de alerta

import customtkinter
import sqlite3
from tkinter import messagebox

# ---- CONFIGURAÇÃO VISUAL ----
# Aparência moderna com tema escuro (pode trocar para "Light" ou "System")
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Caminho do banco de dados (mesmo das aulas anteriores)
BANCO_DE_DADOS = "portaria.db"


class PortariaApp(customtkinter.CTk):
    """
    Classe principal da nossa aplicação de portaria.

    Uma 'classe' é como um molde (receita de bolo).
    Cada vez que executamos o programa, criamos um 'bolo'
    a partir dessa receita.
    """

    def __init__(self):
        """
        Método especial que roda quando o programa inicia.
        Aqui configuramos a janela e montamos a interface.
        """
        super().__init__()

        # ---- Configurações da Janela ----
        self.title("🏢 n7-portaria-ai — Sistema de Portaria Inteligente")
        self.geometry("950x600")
        self.minsize(800, 500)

        # ---- Título Principal ----
        self.label_titulo = customtkinter.CTkLabel(
            self,
            text="Sistema de Portaria — Moradores",
            font=customtkinter.CTkFont(size=24, weight="bold")
        )
        self.label_titulo.pack(pady=15)

        # ---- Área Principal (dividida em duas partes) ----
        self.frame_principal = customtkinter.CTkFrame(self)
        self.frame_principal.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Lado esquerdo = Formulário de cadastro
        # Lado direito = Lista de moradores

        self.frame_principal.grid_columnconfigure(0, weight=1)
        self.frame_principal.grid_columnconfigure(1, weight=1)
        self.frame_principal.grid_rowconfigure(0, weight=1)

        # Monta as duas partes da interface
        self.criar_formulario()
        self.criar_lista()

        # Garante que a tabela existe no banco
        self.inicializar_banco()

        # Carrega os moradores que já existem no banco
        self.carregar_moradores()

    def inicializar_banco(self):
        """
        Cria a tabela moradores se ela não existir.
        Assim o programa funciona mesmo sem ter rodado as aulas anteriores.
        """
        conexao = sqlite3.connect(BANCO_DE_DADOS)
        cursor = conexao.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS moradores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                apartamento TEXT NOT NULL,
                bloco TEXT,
                telefone TEXT,
                email TEXT,
                ativo BOOLEAN DEFAULT 1,
                criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conexao.commit()
        conexao.close()

    # ================================================================
    #  FORMULÁRIO DE CADASTRO (lado esquerdo)
    # ================================================================

    def criar_formulario(self):
        """
        Cria o formulário com campos para cadastrar um morador.
        """
        # Frame (caixa) do formulário
        self.frame_form = customtkinter.CTkFrame(self.frame_principal)
        self.frame_form.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Título do formulário
        label_form_titulo = customtkinter.CTkLabel(
            self.frame_form,
            text="📋 Cadastrar Morador",
            font=customtkinter.CTkFont(size=18, weight="bold")
        )
        label_form_titulo.grid(row=0, column=0, columnspan=2, padx=10, pady=(15, 10))

        # --- Campo: Nome Completo (EXEMPLO - já está pronto!) ---
        self.label_nome = customtkinter.CTkLabel(
            self.frame_form, text="Nome Completo:"
        )
        self.label_nome.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.entry_nome = customtkinter.CTkEntry(
            self.frame_form,
            width=280,
            placeholder_text="Ex: João da Silva"
        )
        self.entry_nome.grid(row=1, column=1, padx=10, pady=5)

        # ===========================================================
        #  TODO 1: CRIE OS CAMPOS QUE FALTAM!
        # ===========================================================
        #
        #  Siga o mesmo padrão do campo "Nome" acima.
        #  Cada campo precisa de:
        #    1. Um CTkLabel (a etiqueta com o nome do campo)
        #    2. Um CTkEntry (o campo onde se digita)
        #
        #  Campos que faltam:
        #    - CPF           (row=2)  → self.entry_cpf
        #    - Apartamento   (row=3)  → self.entry_apartamento
        #    - Bloco         (row=4)  → self.entry_bloco
        #    - Telefone      (row=5)  → self.entry_telefone
        #    - E-mail        (row=6)  → self.entry_email
        #
        #  Dica: copie o bloco do "Nome" e mude o texto e a row!
        #
        #  Exemplo para CPF:
        #  self.label_cpf = customtkinter.CTkLabel(
        #      self.frame_form, text="CPF:"
        #  )
        #  self.label_cpf.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        #
        #  self.entry_cpf = customtkinter.CTkEntry(
        #      self.frame_form, width=280,
        #      placeholder_text="Ex: 123.456.789-00"
        #  )
        #  self.entry_cpf.grid(row=2, column=1, padx=10, pady=5)
        #
        #  AGORA É COM VOCÊ! Crie os campos abaixo:
        # ===========================================================



        # --- Botão de Cadastrar ---
        self.btn_cadastrar = customtkinter.CTkButton(
            self.frame_form,
            text="✅ Cadastrar Morador",
            font=customtkinter.CTkFont(size=14, weight="bold"),
            height=40,
            command=self.cadastrar_morador  # Função que roda ao clicar
        )
        self.btn_cadastrar.grid(
            row=7, column=0, columnspan=2, padx=10, pady=20
        )

        # --- Botão de Limpar ---
        self.btn_limpar = customtkinter.CTkButton(
            self.frame_form,
            text="🧹 Limpar Campos",
            fg_color="gray",
            hover_color="darkgray",
            command=self.limpar_campos
        )
        self.btn_limpar.grid(
            row=8, column=0, columnspan=2, padx=10, pady=(0, 15)
        )

    # ================================================================
    #  LISTA DE MORADORES (lado direito)
    # ================================================================

    def criar_lista(self):
        """
        Cria a área onde os moradores cadastrados são exibidos.
        """
        # Frame da lista
        self.frame_lista = customtkinter.CTkFrame(self.frame_principal)
        self.frame_lista.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Título da lista
        label_lista_titulo = customtkinter.CTkLabel(
            self.frame_lista,
            text="👥 Moradores Cadastrados",
            font=customtkinter.CTkFont(size=18, weight="bold")
        )
        label_lista_titulo.pack(padx=10, pady=(15, 10))

        # Área rolável (scroll) para quando tiver muitos moradores
        self.scroll_lista = customtkinter.CTkScrollableFrame(
            self.frame_lista,
            label_text=""
        )
        self.scroll_lista.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    # ================================================================
    #  FUNÇÕES DE AÇÃO
    # ================================================================

    def cadastrar_morador(self):
        """
        Função que roda quando o botão 'Cadastrar' é clicado.
        Lê os campos, valida e salva no banco de dados.
        """

        # Primeiro, lê o nome (exemplo)
        nome = self.entry_nome.get().strip()

        # Validação simples: nome não pode estar vazio
        if not nome:
            messagebox.showwarning(
                "Campo obrigatório",
                "Por favor, preencha o nome do morador."
            )
            return

        # ===========================================================
        #  TODO 2: COMPLETE O CADASTRO NO BANCO DE DADOS!
        # ===========================================================
        #
        #  Passos:
        #
        #  1) Leia os outros campos (como fizemos com o nome acima):
        #     cpf = self.entry_cpf.get().strip()
        #     apartamento = self.entry_apartamento.get().strip()
        #     bloco = self.entry_bloco.get().strip()
        #     telefone = self.entry_telefone.get().strip()
        #     email = self.entry_email.get().strip()
        #
        #  2) Valide: CPF e Apartamento não podem estar vazios
        #     (use o mesmo padrão do nome acima com messagebox)
        #
        #  3) Conecte ao banco e insira o morador:
        #     conexao = sqlite3.connect(BANCO_DE_DADOS)
        #     cursor = conexao.cursor()
        #     cursor.execute(
        #         "INSERT INTO moradores (nome, cpf, apartamento, bloco, telefone, email) "
        #         "VALUES (?, ?, ?, ?, ?, ?)",
        #         (nome, cpf, apartamento, bloco, telefone, email)
        #     )
        #     conexao.commit()
        #     conexao.close()
        #
        #  4) Mostre mensagem de sucesso:
        #     messagebox.showinfo("Sucesso", f"Morador {nome} cadastrado!")
        #
        #  5) Atualize a lista e limpe os campos:
        #     self.carregar_moradores()
        #     self.limpar_campos()
        #
        #  DICA: Use try/except para tratar erro de CPF duplicado:
        #     try:
        #         ... (código do banco aqui) ...
        #     except sqlite3.IntegrityError:
        #         messagebox.showerror("Erro", "CPF já cadastrado!")
        #
        #  AGORA É COM VOCÊ! Escreva o código abaixo:
        # ===========================================================



    def carregar_moradores(self):
        """
        Carrega todos os moradores do banco e exibe na lista.
        Esta função é chamada ao iniciar e após cada cadastro.
        """

        # Limpa a lista atual (remove cards antigos)
        for widget in self.scroll_lista.winfo_children():
            widget.destroy()

        # ===========================================================
        #  TODO 3: CARREGUE OS MORADORES DO BANCO E EXIBA NA LISTA!
        # ===========================================================
        #
        #  Passos:
        #
        #  1) Conecte ao banco e busque os moradores ativos:
        #     conexao = sqlite3.connect(BANCO_DE_DADOS)
        #     cursor = conexao.cursor()
        #     cursor.execute(
        #         "SELECT nome, cpf, apartamento, bloco, telefone "
        #         "FROM moradores WHERE ativo = 1 ORDER BY nome"
        #     )
        #     moradores = cursor.fetchall()
        #     conexao.close()
        #
        #  2) Para cada morador, crie um "card" visual:
        #     for morador in moradores:
        #         nome, cpf, apto, bloco, tel = morador
        #
        #         # Cria um frame (cartão) para este morador
        #         card = customtkinter.CTkFrame(self.scroll_lista)
        #         card.pack(fill="x", padx=5, pady=3)
        #
        #         # Nome do morador (em negrito)
        #         label_nome = customtkinter.CTkLabel(
        #             card,
        #             text=f"👤 {nome}",
        #             font=customtkinter.CTkFont(weight="bold")
        #         )
        #         label_nome.pack(anchor="w", padx=10, pady=(5, 0))
        #
        #         # Detalhes (apto, bloco, telefone)
        #         detalhes = f"Apto: {apto} | Bloco: {bloco} | Tel: {tel}"
        #         label_detalhe = customtkinter.CTkLabel(
        #             card, text=detalhes,
        #             text_color="gray"
        #         )
        #         label_detalhe.pack(anchor="w", padx=10, pady=(0, 5))
        #
        #  3) Se não houver moradores, mostre uma mensagem:
        #     if not moradores:
        #         label_vazio = customtkinter.CTkLabel(
        #             self.scroll_lista,
        #             text="Nenhum morador cadastrado ainda.\nUse o formulário ao lado!",
        #             text_color="gray"
        #         )
        #         label_vazio.pack(pady=50)
        #
        #  AGORA É COM VOCÊ! Escreva o código abaixo:
        # ===========================================================



    def limpar_campos(self):
        """
        Limpa todos os campos do formulário após cadastrar.
        """
        self.entry_nome.delete(0, "end")

        # Quando você criar os outros campos no TODO 1,
        # adicione aqui a limpeza deles também:
        # self.entry_cpf.delete(0, "end")
        # self.entry_apartamento.delete(0, "end")
        # self.entry_bloco.delete(0, "end")
        # self.entry_telefone.delete(0, "end")
        # self.entry_email.delete(0, "end")

        # Coloca o cursor de volta no campo nome
        self.entry_nome.focus()


# ================================================================
#  PONTO DE ENTRADA — Onde o programa começa!
# ================================================================

if __name__ == "__main__":
    print("=" * 50)
    print("  🏢 n7-portaria-ai — Interface Gráfica")
    print("  Iniciando o sistema de portaria...")
    print("=" * 50)

    # Cria a aplicação e abre a janela
    app = PortariaApp()
    app.mainloop()

    print("\nSistema encerrado. Até a próxima! 👋")
