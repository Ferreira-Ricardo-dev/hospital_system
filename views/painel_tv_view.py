import customtkinter as ctk

class JanelaPainelTV(ctk.CTkToplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.fila_ctrl = self.controller.fila_atendimento

        self.title("Painel de Chamada - Clínica Bem-Estar")
        self.geometry("850x550")
        self.configure(fg_color="#0F172A")

        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=2)
        self.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(self, fg_color="#1E293B", height=60, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew")
        ctk.CTkLabel(
            header,
            text="🩺 CLÍNICA BEM-ESTAR  |  PAINEL DE ATENDIMENTO",
            font=("Segoe UI", 18, "bold"),
            text_color="#F8FAFC"
        ).pack(pady=15)

        card_destaque = ctk.CTkFrame(self, fg_color="#1E3A8A", corner_radius=16)
        card_destaque.grid(row=1, column=0, padx=30, pady=(25, 15), sticky="nsew")
        card_destaque.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card_destaque,
            text="SENHA ATUAL",
            font=("Segoe UI", 18, "bold"),
            text_color="#93C5FD"
        ).pack(pady=(25, 5))

        self.label_senha_grande = ctk.CTkLabel(
            card_destaque,
            text="---",
            font=("Segoe UI", 72, "bold"),
            text_color="#FFFFFF"
        )
        self.label_senha_grande.pack(pady=5)

        self.label_paciente_destino = ctk.CTkLabel(
            card_destaque,
            text="Aguardando início dos atendimentos",
            font=("Segoe UI", 24, "bold"),
            text_color="#E0F2FE"
        )
        self.label_paciente_destino.pack(pady=(5, 25))

        card_historico = ctk.CTkFrame(self, fg_color="#1E293B", corner_radius=12)
        card_historico.grid(row=2, column=0, padx=30, pady=(0, 25), sticky="nsew")

        ctk.CTkLabel(
            card_historico,
            text="ÚLTIMAS SENHAS CHAMADAS",
            font=("Segoe UI", 13, "bold"),
            text_color="#94A3B8"
        ).pack(anchor="w", padx=20, pady=(12, 5))

        self.frame_lista_hist = ctk.CTkFrame(card_historico, fg_color="transparent")
        self.frame_lista_hist.pack(fill="both", expand=True, padx=20, pady=(0, 12))

        self.atualizar_painel()

    def atualizar_painel(self):
        ultimo = self.fila_ctrl.ultimo_chamado
        if ultimo:
            self.label_senha_grande.configure(text=ultimo["senha"])
            self.label_paciente_destino.configure(
                text=f"{ultimo['nome']}  ➔  {ultimo['consultorio']} ({ultimo['especialidade']})"
            )

        for widget in self.frame_lista_hist.winfo_children():
            widget.destroy()

        for item in self.fila_ctrl.historico_chamadas[1:4]:
            linha = ctk.CTkLabel(
                self.frame_lista_hist,
                text=f"{item['senha']}  •  {item['nome']}  —  {item['consultorio']} ({item['hora_chamada']})",
                font=("Segoe UI", 15),
                text_color="#CBD5E1"
            )
            linha.pack(anchor="w", pady=2)