import customtkinter as ctk
from controllers.autenticacao import User

class FrameAdmin(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#F1F5F9")
        self.controller = controller
        self.gerenciador_usuarios = User()

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._criar_header()
        self._criar_sidebar()
        self._criar_area_conteudo()
        self.atualizar_tabela()

    def _criar_header(self):
        header = ctk.CTkFrame(self, height=60, fg_color="#FFFFFF", corner_radius=0)
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        ctk.CTkFrame(header, height=1, fg_color="#E2E8F0").place(relx=0, rely=0.98, relwidth=1)

        text_logo = ctk.CTkLabel(
            header,
            text="🩺 Clínica Bem-Estar - Administração",
            font=("Segoe UI", 18, "bold"),
            text_color="#144475"
        )
        text_logo.grid(row=0, column=0, padx=25, pady=15, sticky="w")

        button_sair = ctk.CTkButton(
            header,
            text="Sair (Admin) ▾",
            fg_color="transparent",
            text_color="#1E293B",
            hover_color="#F1F5F9",
            font=("Segoe UI", 13),
            width=120,
            command=self._voltar_login
        )
        button_sair.grid(row=0, column=2, padx=25, pady=15, sticky="e")

    def _criar_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=160, fg_color="#FFFFFF", corner_radius=0)
        sidebar.grid(row=1, column=0, sticky="ns")
        sidebar.grid_propagate(False)

        ctk.CTkFrame(sidebar, width=1, fg_color="#E2E8F0").place(relx=0.99, rely=0, relheight=1)

        itens_menu = [
            ("👥\nGerenciar\nUsuários", True)
        ]

        for texto, ativo in itens_menu:
            button = ctk.CTkButton(
                sidebar,
                text=texto,
                height=75,
                corner_radius=0,
                fg_color="#E2E8F0" if ativo else "transparent",
                text_color="#144475" if ativo else "#64748B",
                hover_color="#F1F5F9",
                font=("Segoe UI", 12, "bold" if ativo else "normal")
            )
            button.pack(fill="x", pady=2)

    def _criar_area_conteudo(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=1, column=1, padx=25, pady=20, sticky="nsew")
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(2, weight=1)

        text_titulo = ctk.CTkLabel(
            container,
            text="Gerenciar Usuários",
            font=("Segoe UI", 24, "bold"),
            text_color="#0F172A"
        )
        text_titulo.grid(row=0, column=0, pady=(0, 15), sticky="w")

        card_cadastro = ctk.CTkFrame(
            container,
            fg_color="#FFFFFF",
            border_width=1,
            border_color="#E2E8F0",
            corner_radius=12
        )
        card_cadastro.grid(row=1, column=0, pady=(0, 20), sticky="ew")
        card_cadastro.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkLabel(
            card_cadastro,
            text="Cadastrar Novo Usuário",
            font=("Segoe UI", 16, "bold"),
            text_color="#1E293B"
        ).grid(row=0, column=0, columnspan=4, padx=20, pady=(15, 10), sticky="w")

        ctk.CTkLabel(card_cadastro, text="Nome (Login)", font=("Segoe UI", 12, "bold"), text_color="#334155").grid(row=1, column=0, padx=(20, 10), sticky="w")
        self.entry_nome = ctk.CTkEntry(card_cadastro, placeholder_text="Ex: Fernanda Costa", height=38)
        self.entry_nome.grid(row=2, column=0, padx=(20, 10), pady=(2, 10), sticky="ew")

        ctk.CTkLabel(card_cadastro, text="Senha", font=("Segoe UI", 12, "bold"), text_color="#334155").grid(row=1, column=1, padx=10, sticky="w")
        self.entry_senha = ctk.CTkEntry(card_cadastro, placeholder_text="Digite a senha...", show="*", height=38)
        self.entry_senha.grid(row=2, column=1, padx=10, pady=(2, 10), sticky="ew")

        ctk.CTkLabel(card_cadastro, text="Cargo", font=("Segoe UI", 12, "bold"), text_color="#334155").grid(row=1, column=2, padx=10, sticky="w")
        self.combo_cargo = ctk.CTkOptionMenu(
            card_cadastro,
            values=["Atendente", "Admin"],
            height=38,
            fg_color="#F8FAFC",
            button_color="#CBD5E1",
            button_hover_color="#94A3B8",
            text_color="#1E293B"
        )
        self.combo_cargo.grid(row=2, column=2, padx=10, pady=(2, 10), sticky="ew")

        button_cadastrar = ctk.CTkButton(
            card_cadastro,
            text="Cadastrar Usuário",
            fg_color="#1E40AF",
            hover_color="#1D4ED8",
            font=("Segoe UI", 13, "bold"),
            height=38,
            command=self._acao_cadastrar
        )
        button_cadastrar.grid(row=2, column=3, padx=(10, 20), pady=(2, 10), sticky="ew")

        self.text_feedback = ctk.CTkLabel(card_cadastro, text="", font=("Segoe UI", 12))
        self.text_feedback.grid(row=3, column=0, columnspan=4, padx=20, pady=(0, 12), sticky="w")

        card_tabela = ctk.CTkFrame(
            container,
            fg_color="#FFFFFF",
            border_width=1,
            border_color="#E2E8F0",
            corner_radius=12
        )
        card_tabela.grid(row=2, column=0, sticky="nsew")
        card_tabela.grid_columnconfigure(0, weight=1)
        card_tabela.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            card_tabela,
            text="Tabela de Usuários Ativos",
            font=("Segoe UI", 16, "bold"),
            text_color="#1E293B"
        ).grid(row=0, column=0, padx=20, pady=(15, 10), sticky="w")

        header_tabela = ctk.CTkFrame(card_tabela, fg_color="#F8FAFC", height=35, corner_radius=6)
        header_tabela.grid(row=1, column=0, padx=20, sticky="ew")
        header_tabela.grid_columnconfigure((0, 1, 2), weight=1)

        colunas = ["Nome", "Cargo", "Data de Cadastro", "Ações"]
        for i, col in enumerate(colunas):
            ctk.CTkLabel(
                header_tabela,
                text=col,
                font=("Segoe UI", 12, "bold"),
                text_color="#475569"
            ).grid(row=0, column=i, padx=15, pady=6, sticky="w" if i < 3 else "e")

        self.scroll_usuarios = ctk.CTkScrollableFrame(card_tabela, fg_color="transparent")
        self.scroll_usuarios.grid(row=2, column=0, padx=15, pady=(5, 15), sticky="nsew")
        self.scroll_usuarios.grid_columnconfigure((0, 1, 2), weight=1)

    def _acao_cadastrar(self):
        nome = self.entry_nome.get().strip()
        senha = self.entry_senha.get().strip()
        cargo = self.combo_cargo.get()

        sucesso, msg = self.gerenciador_usuarios.cadastrar_usuario(nome, senha, cargo)

        if sucesso:
            self.text_feedback.configure(text=msg, text_color="#16A34A")
            self.entry_nome.delete(0, "end")
            self.entry_senha.delete(0, "end")
            self.atualizar_tabela()
        else:
            self.text_feedback.configure(text=msg, text_color="#DC2626")

    def atualizar_tabela(self):
        for widget in self.scroll_usuarios.winfo_children():
            widget.destroy()

        usuarios = self.gerenciador_usuarios.carregar_usuarios()

        for idx, u in enumerate(usuarios, start=1):
            linha = ctk.CTkFrame(self.scroll_usuarios, fg_color="transparent")
            linha.pack(fill="x", pady=2)
            linha.grid_columnconfigure((0, 1, 2), weight=1)

            ctk.CTkLabel(linha, text=f"{idx}. {u['nome']}", font=("Segoe UI", 12), text_color="#1E293B").grid(row=0, column=0, padx=15, pady=6, sticky="w")
            ctk.CTkLabel(linha, text=u["cargo"], font=("Segoe UI", 12), text_color="#1E293B").grid(row=0, column=1, padx=15, pady=6, sticky="w")
            ctk.CTkLabel(linha, text=u["data_cadastro"], font=("Segoe UI", 12), text_color="#475569").grid(row=0, column=2, padx=15, pady=6, sticky="w")

            if u["nome"].lower() != "admin":
                button_del = ctk.CTkButton(
                    linha,
                    text="🗑️",
                    width=30,
                    height=28,
                    fg_color="transparent",
                    text_color="#DC2626",
                    hover_color="#FEE2E2",
                    command=lambda nome=u["nome"]: self._excluir_registro(nome)
                )
                button_del.grid(row=0, column=3, padx=15, sticky="e")
            else:
                ctk.CTkLabel(linha, text="Fixo", font=("Segoe UI", 11), text_color="#94A3B8").grid(row=0, column=3, padx=20, sticky="e")

            ctk.CTkFrame(self.scroll_usuarios, height=1, fg_color="#F1F5F9").pack(fill="x")

    def _excluir_registro(self, nome):
        self.gerenciador_usuarios.excluir_usuario(nome)
        self.atualizar_tabela()

    def _voltar_login(self):
        self.winfo_toplevel().destroy()