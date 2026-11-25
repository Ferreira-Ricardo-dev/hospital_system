import customtkinter as ctk

class FrameAtendente(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#F1F5F9")
        self.controller = controller
        self.fila_ctrl = self.controller.fila_atendimento

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._criar_header()
        self._criar_corpo()
        self.atualizar_lista_fila()

    def _criar_header(self):
        header = ctk.CTkFrame(self, height=60, fg_color="#FFFFFF", corner_radius=0)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        ctk.CTkFrame(header, height=1, fg_color="#E2E8F0").place(relx=0, rely=0.98, relwidth=1)

        nome_atendente = self.controller.usuario_atual.get("nome", "Atendente") if self.controller.usuario_atual else "Atendente"

        ctk.CTkLabel(
            header,
            text="🩺 Clínica Bem-Estar - Recepção & Triagem",
            font=("Segoe UI", 18, "bold"),
            text_color="#144475"
        ).grid(row=0, column=0, padx=25, pady=15, sticky="w")

        button_tv = ctk.CTkButton(
            header,
            text="📺 Abrir Painel de Exposição",
            fg_color="#0F766E",
            hover_color="#115E59",
            font=("Segoe UI", 12, "bold"),
            height=34,
            command=self.controller.abrir_painel_tv
        )
        button_tv.grid(row=0, column=1, padx=15, pady=15, sticky="e")

        button_sair = ctk.CTkButton(
            header,
            text=f"Sair ({nome_atendente}) ▾",
            fg_color="transparent",
            text_color="#1E293B",
            hover_color="#F1F5F9",
            font=("Segoe UI", 13),
            command=self.controller.exibir_login
        )
        button_sair.grid(row=0, column=2, padx=(0, 25), pady=15, sticky="e")

    def _criar_corpo(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=1, column=0, padx=25, pady=20, sticky="nsew")
        container.grid_columnconfigure(0, weight=2)
        container.grid_columnconfigure(1, weight=3)
        container.grid_rowconfigure(0, weight=1)

        card_registro = ctk.CTkFrame(container, fg_color="#FFFFFF", border_width=1, border_color="#E2E8F0", corner_radius=12)
        card_registro.grid(row=0, column=0, padx=(0, 12), sticky="nsew")
        card_registro.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card_registro,
            text="Novo Atendimento (Triagem)",
            font=("Segoe UI", 18, "bold"),
            text_color="#0F172A"
        ).grid(row=0, column=0, padx=25, pady=(20, 15), sticky="w")

        ctk.CTkLabel(card_registro, text="Nome do Paciente", font=("Segoe UI", 12, "bold"), text_color="#334155").grid(row=1, column=0, padx=25, sticky="w")
        self.entry_paciente = ctk.CTkEntry(card_registro, placeholder_text="Digite o nome completo...", height=38)
        self.entry_paciente.grid(row=2, column=0, padx=25, pady=(2, 12), sticky="ew")

        ctk.CTkLabel(card_registro, text="Idade", font=("Segoe UI", 12, "bold"), text_color="#334155").grid(row=3, column=0, padx=25, sticky="w")
        self.entry_idade = ctk.CTkEntry(card_registro, placeholder_text="Ex: 34", height=38)
        self.entry_idade.grid(row=4, column=0, padx=25, pady=(2, 12), sticky="ew")
        self.entry_idade.bind("<KeyRelease>", self._verificar_idade_preferencial)

        ctk.CTkLabel(card_registro, text="Especialidade / Fila", font=("Segoe UI", 12, "bold"), text_color="#334155").grid(row=5, column=0, padx=25, sticky="w")
        self.combo_especialidade = ctk.CTkOptionMenu(
            card_registro,
            values=list(self.fila_ctrl.filas.keys()),
            height=38,
            fg_color="#F8FAFC",
            button_color="#CBD5E1",
            button_hover_color="#94A3B8",
            text_color="#1E293B",
            command=self._ao_trocar_especialidade
        )
        self.combo_especialidade.grid(row=6, column=0, padx=25, pady=(2, 12), sticky="ew")

        ctk.CTkLabel(card_registro, text="Classificação de Prioridade", font=("Segoe UI", 12, "bold"), text_color="#334155").grid(row=7, column=0, padx=25, sticky="w")
        self.combo_prioridade = ctk.CTkOptionMenu(
            card_registro,
            values=list(self.fila_ctrl.PRIORIDADES.keys()),
            height=38,
            fg_color="#F8FAFC",
            button_color="#CBD5E1",
            button_hover_color="#94A3B8",
            text_color="#1E293B"
        )
        self.combo_prioridade.set("Normal")
        self.combo_prioridade.grid(row=8, column=0, padx=25, pady=(2, 20), sticky="ew")

        button_gerar = ctk.CTkButton(
            card_registro,
            text="+ Gerar Senha e Inserir na Fila",
            fg_color="#1E40AF",
            hover_color="#1D4ED8",
            font=("Segoe UI", 14, "bold"),
            height=44,
            command=self._acao_adicionar_paciente
        )
        button_gerar.grid(row=9, column=0, padx=25, pady=(5, 10), sticky="ew")

        self.label_feedback = ctk.CTkLabel(card_registro, text="", font=("Segoe UI", 12), wraplength=300)
        self.label_feedback.grid(row=10, column=0, padx=25, pady=(5, 15))

        card_fila = ctk.CTkFrame(container, fg_color="#FFFFFF", border_width=1, border_color="#E2E8F0", corner_radius=12)
        card_fila.grid(row=0, column=1, padx=(12, 0), sticky="nsew")
        card_fila.grid_columnconfigure(0, weight=1)
        card_fila.grid_rowconfigure(3, weight=1)

        topo_fila = ctk.CTkFrame(card_fila, fg_color="transparent")
        topo_fila.grid(row=0, column=0, padx=25, pady=(20, 10), sticky="ew")
        topo_fila.grid_columnconfigure(0, weight=1)

        self.label_titulo_fila = ctk.CTkLabel(
            topo_fila,
            text="Fila de Espera: Clínico Geral",
            font=("Segoe UI", 18, "bold"),
            text_color="#0F172A"
        )
        self.label_titulo_fila.grid(row=0, column=0, sticky="w")

        self.combo_consultorio = ctk.CTkOptionMenu(
            topo_fila,
            values=["Consultório 01", "Consultório 02", "Consultório 03", "Sala de Triagem"],
            width=150,
            height=32,
            fg_color="#F8FAFC",
            button_color="#CBD5E1",
            text_color="#1E293B"
        )
        self.combo_consultorio.grid(row=0, column=1, sticky="e")

        banner_atual = ctk.CTkFrame(card_fila, fg_color="#EFF6FF", border_width=1, border_color="#BFDBFE", corner_radius=8)
        banner_atual.grid(row=1, column=0, padx=25, pady=(5, 15), sticky="ew")
        banner_atual.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(banner_atual, text="ÚLTIMA SENHA CHAMADA", font=("Segoe UI", 10, "bold"), text_color="#1D4ED8").grid(row=0, column=0, padx=15, pady=(8, 0), sticky="w")
        self.label_chamado_atual = ctk.CTkLabel(
            banner_atual,
            text="Nenhum paciente chamado ainda",
            font=("Segoe UI", 16, "bold"),
            text_color="#1E3A8A"
        )
        self.label_chamado_atual.grid(row=1, column=0, padx=15, pady=(2, 10), sticky="w")

        button_chamar = ctk.CTkButton(
            card_fila,
            text="📢 Chamar Próximo da Fila",
            fg_color="#16A34A",
            hover_color="#15803D",
            font=("Segoe UI", 15, "bold"),
            height=46,
            command=self._acao_chamar_proximo
        )
        button_chamar.grid(row=2, column=0, padx=25, pady=(0, 15), sticky="ew")

        self.scroll_fila = ctk.CTkScrollableFrame(card_fila, fg_color="#F8FAFC", corner_radius=8)
        self.scroll_fila.grid(row=3, column=0, padx=25, pady=(0, 20), sticky="nsew")
        self.scroll_fila.grid_columnconfigure(1, weight=1)

    def _verificar_idade_preferencial(self, event=None):
        """Seleciona automaticamente Preferencial se a idade for >= 60 e não estiver em Emergência."""
        texto_idade = self.entry_idade.get().strip()
        if texto_idade.isdigit():
            idade = int(texto_idade)
            if idade >= 60 and self.combo_prioridade.get() == "Normal":
                self.combo_prioridade.set("Preferencial (Idade / Gestante / PCD)")
            elif idade < 60 and self.combo_prioridade.get() == "Preferencial (Idade / Gestante / PCD)":
                self.combo_prioridade.set("Normal")

    def _ao_trocar_especialidade(self, escolha):
        self.label_titulo_fila.configure(text=f"Fila de Espera: {escolha}")
        self.atualizar_lista_fila()

    def _acao_adicionar_paciente(self):
        nome = self.entry_paciente.get().strip()
        idade_str = self.entry_idade.get().strip()
        especialidade = self.combo_especialidade.get()
        prioridade = self.combo_prioridade.get()

        if not idade_str.isdigit():
            self.label_feedback.configure(text="Informe uma idade válida (apenas números).", text_color="#DC2626")
            return

        sucesso, msg, _ = self.fila_ctrl.adicionar_paciente(nome, int(idade_str), prioridade, especialidade)

        if sucesso:
            self.label_feedback.configure(text=msg, text_color="#16A34A")
            self.entry_paciente.delete(0, "end")
            self.entry_idade.delete(0, "end")
            self.combo_prioridade.set("Normal")
            self.atualizar_lista_fila()
            if self.controller.janela_tv is not None and self.controller.janela_tv.winfo_exists():
                self.controller.janela_tv.atualizar_painel()
        else:
            self.label_feedback.configure(text=msg, text_color="#DC2626")

    def _acao_chamar_proximo(self):
        especialidade = self.combo_especialidade.get()
        consultorio = self.combo_consultorio.get()

        paciente = self.fila_ctrl.chamar_proximo(especialidade, consultorio)
        if paciente:
            self.label_chamado_atual.configure(
                text=f"{paciente['senha']} — {paciente['nome']} ({paciente['consultorio']})"
            )
            self.atualizar_lista_fila()
            if self.controller.janela_tv is not None and self.controller.janela_tv.winfo_exists():
                self.controller.janela_tv.atualizar_painel()
        else:
            self.label_feedback.configure(text=f"Não há pacientes aguardando em {especialidade}.", text_color="#D97706")

    def atualizar_lista_fila(self):
        for widget in self.scroll_fila.winfo_children():
            widget.destroy()

        especialidade = self.combo_especialidade.get()
        pacientes = self.fila_ctrl.listar_fila_ordenada(especialidade)

        if not pacientes:
            ctk.CTkLabel(
                self.scroll_fila,
                text="Nenhum paciente aguardando nesta fila.",
                font=("Segoe UI", 13),
                text_color="#64748B"
            ).pack(pady=40)
            return

        cores_badge = {
            1: ("#FEE2E2", "#DC2626", "EMERGÊNCIA"),
            2: ("#FEF3C7", "#D97706", "PREFERENCIAL"),
            3: ("#E0F2FE", "#0284C7", "NORMAL")
        }

        for pos, p in enumerate(pacientes, start=1):
            bg_badge, fg_badge, texto_badge = cores_badge[p["peso"]]

            item = ctk.CTkFrame(self.scroll_fila, fg_color="#FFFFFF", border_width=1, border_color="#E2E8F0", corner_radius=8)
            item.pack(fill="x", padx=5, pady=4)
            item.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(
                item,
                text=f"#{pos}  {p['senha']}",
                font=("Segoe UI", 13, "bold"),
                text_color="#144475",
                width=95
            ).grid(row=0, column=0, padx=12, pady=10, sticky="w")

            ctk.CTkLabel(
                item,
                text=f"{p['nome']} ({p['idade']} anos)  •  Chegada: {p['hora_chegada']}",
                font=("Segoe UI", 12),
                text_color="#1E293B"
            ).grid(row=0, column=1, padx=5, pady=10, sticky="w")

            ctk.CTkLabel(
                item, text=f"Espera estimada: {(pos - 1) * 30} min",
                font=("Segoe UI", 11), text_color="#64748B"
            ).grid(row=1, column=1, padx=5, pady=(0, 8), sticky="w")

            badge = ctk.CTkLabel(
                item,
                text=texto_badge,
                font=("Segoe UI", 10, "bold"),
                fg_color=bg_badge,
                text_color=fg_badge,
                corner_radius=6,
                width=95,
                height=24
            )
            badge.grid(row=0, column=2, padx=12, pady=10, sticky="e")
