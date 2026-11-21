from controllers.autenticacao import User
import customtkinter as ctk

#Defininção do padrão de fundo
ctk.set_appearance_mode("Light") 
ctk.set_default_color_theme("blue")

class FrameLogin(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.validador = User()

        #Configuração do grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #Frame que será o formulário de login
        self.card_login = ctk.CTkFrame(
            self,
            border_width=1,
            fg_color="#FFFFFF",
            border_color="#E2E8F0",
            corner_radius=12
        )
        self.card_login.grid(row=0, column=0, padx=20, pady=20)
        
        self.card_login.grid_columnconfigure(0, weight=1)

        self.title = ctk.CTkLabel(
            self.card_login, 
            text="Clínica Bem-Estar - Login de Usuário", 
            font=("Segoe UI", 28, "bold"), 
            text_color="#144475"
        )
        self.title.grid(row=0, column=0, padx=40, pady=(35, 25))

        self.user_text = ctk.CTkLabel(
            self.card_login,
            text="Usuário",
            font=("Segoe UI", 15),
            text_color="#1E293B"
        )
        self.user_text.grid(row=1, column=0, padx=40, pady=(5, 2), sticky="w")
        
        self.entry_usuario = ctk.CTkEntry(
            self.card_login,
            placeholder_text="Digite seu nome de usuario...",
            width=350,
            height=40,
            border_width=1
        )
        self.entry_usuario.grid(row=2, column=0, padx=40, pady=2, sticky="ew")

        self.entry_text = ctk.CTkLabel(
            self.card_login,
            text="Senha",
            font=("Segoe UI", 15),
            text_color="#1E293B"
        )
        self.entry_text.grid(row=3, column=0, padx=40, pady=(20, 2), sticky="w")
        
        self.entry_senha = ctk.CTkEntry(
            self.card_login,
            placeholder_text="Digite sua senha...",
            show="*", 
            width=350,
            height=40,
            border_width=1
        )
        self.entry_senha.grid(row=4, column=0, padx=40, pady=2, sticky="ew")

        self.button_entrar = ctk.CTkButton(
            self.card_login,
            text="Entrar",
            command=self.click_save,
            width=350,
            height=45,
            font=("Arial", 14, "bold")
        )
        self.button_entrar.grid(row=5, column=0, padx=40, pady=(25, 35), sticky="ew")

        self.text_feedback = ctk.CTkLabel(
            self.card_login, 
            text="", 
            font=("Arial", 12), 
            wraplength=260 ) 
        self.text_feedback.grid(row=6, column=0, padx=20, pady=(5, 20))

    def click_save(self):
        usuario_digitado = self.entry_usuario.get().strip()
        senha_digitado = self.entry_senha.get().strip()

        sucesso, mensagem = self.validador.validar_credenciais(usuario_digitado, senha_digitado)

        if sucesso:
            self.text_feedback.configure(text=mensagem, text_color="#2FA572")
            self.entry_senha.delete(0, "end")
            self.controller.abrir_menu()

        else:
            self.text_feedback.configure(text=mensagem, text_color="#FF5555")
            if usuario_digitado and senha_digitado:
                self.entry_senha.delete(0, "end")

