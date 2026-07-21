import customtkinter as ctk

#criar a janela
janela = ctk.CTk()

# configurar a janela
janela.title("Sistema de Cadastro de Metas")

janela.geometry("900x600")

# criar o frame
frame_menu = ctk.CTkFrame(janela)

# posicionar o frame
frame_menu = ctk.CTkFrame(
    janela,
    width=250,
    height=800
)

frame_menu.place(x=0, y=0)

janela.mainloop()