import customtkinter as ctk
from views.login_view import FrameLogin
from views.admin_view import FrameAdmin

ctk.set_appearance_mode("Light") #Defininção do padrão de fundo
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.title("Teste para Janela v1.0")
        self.geometry("900x700")
        self.minsize(width=900, height=550)
        self.resizable(width=True, height=True)

        #Configurando linhas e colunas
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.painel_login = FrameLogin(parent=self, controller=self)
        self.painel_login.grid(row=0, column=0, sticky="nsew")

    def abrir_menu(self):
        self.painel_login.grid_forget()

        self.painel_admin = FrameAdmin(parent=self, controller=self)
        self.painel_admin.grid(row=0, column=0, sticky="nsew")


if __name__ == "__main__":
    app = App()
    app.mainloop()