import customtkinter as ctk
from views.login_view import FrameLogin
from views.admin_view import FrameAdmin

ctk.set_appearance_mode("Light") #Defininção do padrão de fundo
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.title("Clínica Bem-Estar - Sistema de Atendimento")
        self.geometry("1050x700")
        self.minsize(width=950, height=600)
        self.resizable(width=True, height=True)

        #Configurando linhas e colunas
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.usuario_atual = None
        self.frame_atual = None
        self.janela_tv = None

        self.exibir_login()

    def _trocar_tela(self, novo_frame):
        if self.frame_atual is not None:
            self.frame_atual.destroy()

        self.frame_atual = novo_frame
        self.frame_atual.grid(row=0, column=0, sticky="nsew")

    def exibir_login(self):
        """Carrega ou retorna para a tela de autenticação."""
        self.usuario_atual = None
        self.title("Clínica Bem-Estar - Login")
        self._trocar_tela(FrameLogin(parent=self, controller=self))

    def abrir_menu(self, usuario_logado: dict):
        """Roteia o usuário para a interface correta com base no cargo."""
        self.usuario_atual = usuario_logado
        cargo = usuario_logado.get("cargo")
        nome = usuario_logado.get("nome")

        if cargo == "Admin":
            self.title(f"Clínica Bem-Estar - Administração ({nome})")
            self._trocar_tela(FrameAdmin(parent=self, controller=self))

        elif cargo == "Atendente":
            self.title(f"Clínica Bem-Estar - Recepção & Chamada ({nome})")
            self._exibir_placeholder_atendente(nome)

    def abrir_painel_tv(self):
        """Abre a tela pública de exibição de senhas em uma janela separada (CTkToplevel)."""
        if self.janela_tv is None or not self.janela_tv.winfo_exists():
            pass
        else:
            self.janela_tv.focus()

    def _exibir_placeholder_atendente(self, nome: str):
        """Tela temporária para testar o roteamento do cargo Atendente."""
        frame_temp = ctk.CTkFrame(self, fg_color="#F1F5F9")
        ctk.CTkLabel(
            frame_temp,
            text=f"Área do Atendente - Bem-vindo(a), {nome}!",
            font=("Segoe UI", 22, "bold"),
            text_color="#144475"
        ).pack(pady=(200, 20))

        ctk.CTkButton(
            frame_temp,
            text="Voltar ao Login",
            command=self.exibir_login
        ).pack()

        self._trocar_tela(frame_temp)

if __name__ == "__main__":
    app = App()
    app.mainloop()