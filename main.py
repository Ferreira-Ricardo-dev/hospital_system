import customtkinter as ctk
from login_view import FrameLogin

ctk.set_appearance_mode("Light") #Defininção do padrão de fundo
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.title("Teste para Janela de Login v1.0")
        self.geometry("900x550")
        self.minsize(width=900, height=550)
        self.resizable(width=True, height=True)

        #Configuração das Colunas
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        #Configuração das Linhas
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.painel_login = FrameLogin(master=self)
        self.painel_login.grid(row=1, column=2, padx=30, pady=30, sticky="nsew")

if __name__ == "__main__":
    app = App()
    app.mainloop()