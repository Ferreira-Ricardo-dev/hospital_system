import customtkinter as ctk

#Defininção do padrão de fundo
ctk.set_appearance_mode("Light") 
ctk.set_default_color_theme("blue")

class FrameAdmin(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.controller = controller

        self.configure(
            border_width=1,
            fg_color="#FFFFFF",
            border_color="#E2E8F0",
            corner_radius=12
            )