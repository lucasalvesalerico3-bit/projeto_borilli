import customtkinter as ctk
from PIL import Image
from telas.tela_funcionarios import abrir_tela_funcionarios
from telas.tela_metas import abrir_tela_metas

ctk.set_appearance_mode("light")

# criar a janela
janela = ctk.CTk()

# configurar a janela
janela.title("Sistema de Cadastro de Metas")
janela.geometry("900x600")


# criar a side bar
frame_menu = ctk.CTkFrame(
    janela,
    width=300
)
frame_menu.place(x=0, y=0, relheight=1)

# criar frame princiapl
frame_principal = ctk.CTkFrame(
    master=janela,
    fg_color="#f5f5f5",
    corner_radius=0
)

frame_principal.place(
    x=200,
    y=0,
    relwidth=1,
    relheight=1
)

# criando titulo do menu
titulo_menu = ctk.CTkLabel(
    frame_menu,
    text="Sistema de Cadastro de Metas",
    font=("Segoe UI", 18, "bold"),
)
titulo_menu.place(x=15, y=15)

# logo da empresa
logo = ctk.CTkImage(
    light_image=Image.open("imagens/logo.png"),
    dark_image=Image.open("imagens/logo.png"),
    size=(190, 90)
)

label_logo = ctk.CTkLabel(
    frame_menu,
    image=logo,
    text=""
)
label_logo.place(x=40, y=40)

# icones dos botoes
icone_funcionarios = ctk.CTkImage(
    light_image=Image.open("imagens/funcionarios.png"),
    dark_image=Image.open("imagens/funcionarios.png"),
    size=(24, 24)
)

icone_metas = ctk.CTkImage(
    light_image=Image.open("imagens/meta.png"),
    dark_image=Image.open("imagens/meta.png"),
    size=(24, 24)
)

icone_dashboard = ctk.CTkImage(
    light_image=Image.open("imagens/grafico.png"),
    dark_image=Image.open("imagens/grafico.png"),
    size=(24, 24)
)

icone_relatorios = ctk.CTkImage(
    light_image=Image.open("imagens/relatorios.png"),
    dark_image=Image.open("imagens/relatorios.png"),
    size=(24, 24)
)

icone_configuracoes = ctk.CTkImage(
    light_image=Image.open("imagens/configuracoes.png"),
    dark_image=Image.open("imagens/configuracoes.png"),
    size=(24, 24)
)

icone_sair = ctk.CTkImage(
    light_image=Image.open("imagens/exit-door.png"),
    dark_image=Image.open("imagens/exit-door.png"),
    size=(24, 24)
)

estilo_botao_menu = {
    "width": 240,
    "height": 50,
    "corner_radius": 8,
    "fg_color": "#1f4fbf",
    "hover_color": "#2b5fd1",
    "font": ("Segoe UI", 18),
    "compound": "left",
    "anchor": "w",
}

# criando os botoes
botao_funcionarios = ctk.CTkButton(
    master=frame_menu,
    text=" Funcionários",
    image=icone_funcionarios,
    **estilo_botao_menu,
    command=lambda: abrir_tela_funcionarios(frame_principal)
)
botao_funcionarios.place(x=15, y=155)

botao_metas = ctk.CTkButton(
    frame_menu,
    text="  Metas",
    image=icone_metas,
    **estilo_botao_menu,
    command=lambda: abrir_tela_metas(frame_principal)
)
botao_metas.place(x=15, y=220)

botao_dashboard = ctk.CTkButton(
    frame_menu,
    text="  Dashboard",
    image=icone_dashboard,
    **estilo_botao_menu
)
botao_dashboard.place(x=15, y=285)

botao_relatorios = ctk.CTkButton(
    frame_menu,
    text="  Relatórios",
    image=icone_relatorios,
    **estilo_botao_menu
)
botao_relatorios.place(x=15, y=350)

botao_configuracoes = ctk.CTkButton(
    frame_menu,
    text="  Configurações",
    image=icone_configuracoes,
    **estilo_botao_menu
)
botao_configuracoes.place(x=15, y=415)

botao_sair = ctk.CTkButton(
    frame_menu,
    text="  Sair",
    image=icone_sair,
    **estilo_botao_menu
)
botao_sair.place(x=15, rely=1, y=-70, anchor="sw")

janela.mainloop()
