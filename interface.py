import customtkinter as ctk
from PIL import Image, ImageTk

#criar a janela
janela = ctk.CTk()

# configurar a janela
janela.title("Sistema de Cadastro de Metas")

janela.geometry("900x600")

# criar a side bar
frame_menu = ctk.CTkFrame(janela)

# posicionar o frame
frame_menu = ctk.CTkFrame(
    janela,
    width=270,
    height=800
)

frame_menu.place(x=0, y=0)

# criandoo titulo do menu
titulo_menu = ctk.CTkLabel(
    frame_menu,
    text="Sistema de Cadastro de Metas",
    font=("Segoe UI", 18, "bold"),
)
titulo_menu.place(x=15, y=15)

# criando os botoes
botao_funcionarios = ctk.CTkButton(
    frame_menu,
    text = "Funcionários",
    width = 220,
    height = 40
)
botao_funcionarios.place(x=20, y=80)

botao_metas = ctk.CTkButton(
    frame_menu,
    text = "Metas",
    width = 220,
    height = 40
)
botao_metas.place(x=20, y=140)

botao_dashboard = ctk.CTkButton(
    frame_menu,
    text = "Dashboard",
    width = 220,
    height = 40
)
botao_dashboard.place(x=20, y=200)

botao_relatorios = ctk.CTkButton(
    frame_menu,
    text = "Relatórios",
    width = 220,
    height = 40
)
botao_relatorios.place(x=20, y=260)

logo = ctk.CTkImage(
    light_image=Image.open("imagens/borilli3.png"),
    dark_image=Image.open("imagens/borilli3.png"),
    size=(80, 80)
)

label_logo = ctk.CTkLabel(
    frame_menu,
    image=logo,
    text=""
)
label_logo.place(x=110, y=60)

janela.mainloop()