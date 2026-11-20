import customtkinter as ctk

#Defininção do padrão de fundo
ctk.set_appearance_mode("Light") 
ctk.set_default_color_theme("blue")

class FrameLogin(ctk.CTkFrame):
    def __init__(self, master, width = 200, height = 200, corner_radius = None, border_width = None, bg_color = "transparent", fg_color = None, border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self.title = ctk.CTkLabel(
            self, 
            text="Autenticação de Usuário", 
            font=("Arial", 20, "bold")
            )
        self.title.grid(row=0, column=0, padx=10, pady=(25, 15), sticky="w")

        self.entry_usuario = ctk.CTkEntry(
            self,
            placeholder_text="Digite seu nome de usuario...",
            width=200,
            height=35
        )
        self.entry_usuario.grid(row=1, column=0, padx=5, pady=10)

        self.entry_senha = ctk.CTkEntry(
                    self,
                    placeholder_text="Digite sua senha...",
                    width=200,
                    height=35
                )
        self.entry_senha.grid(row=2, column=0, padx=5, pady=10)

        #Para uma futura função de controle
        self.button_entrar = ctk.CTkButton(
            self,
            text="Entrar",
            width=200,
            height=38,
            font=("Arial", 14, "bold")
        )
        self.button_entrar.grid(row=3, column=0, padx=5, pady=(5, 20), sticky="nsew")