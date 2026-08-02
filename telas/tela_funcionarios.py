import customtkinter as ctk

from banco_de_dados import (
    atualizar_funcionario,
    cadastrar_funcionario,
    excluir_funcionario,
    listar_funcionarios
)


def abrir_tela_funcionarios(frame_principal):

    def solicitar_id(titulo_dialogo):
        resposta = ctk.CTkInputDialog(
            text="Digite o ID do funcionário:",
            title=titulo_dialogo
        ).get_input()

        if resposta is None:
            return None

        try:
            return int(resposta)
        except ValueError:
            return None

    def cadastrar():
        nome = ctk.CTkInputDialog(
            text="Digite o nome do funcionário:",
            title="Cadastrar funcionário"
        ).get_input()
        if not nome:
            return

        cargo = ctk.CTkInputDialog(
            text="Digite o cargo do funcionário:",
            title="Cadastrar funcionário"
        ).get_input()
        if cargo is None:
            return

        cadastrar_funcionario(nome, cargo)
        abrir_tela_funcionarios(frame_principal)

    def atualizar():
        funcionario_id = solicitar_id("Atualizar funcionário")
        if funcionario_id is None:
            return

        nome = ctk.CTkInputDialog(
            text="Digite o novo nome:",
            title="Atualizar funcionário"
        ).get_input()
        if not nome:
            return

        cargo = ctk.CTkInputDialog(
            text="Digite o novo cargo:",
            title="Atualizar funcionário"
        ).get_input()
        if cargo is None:
            return

        atualizar_funcionario(nome, cargo, funcionario_id)
        abrir_tela_funcionarios(frame_principal)

    def excluir():
        funcionario_id = solicitar_id("Excluir funcionário")
        if funcionario_id is None:
            return

        excluir_funcionario(funcionario_id)
        abrir_tela_funcionarios(frame_principal)

    # Limpa a tela anterior
    for widget in frame_principal.winfo_children():
        widget.destroy()

    # Título
    titulo = ctk.CTkLabel(
        master=frame_principal,
        text="Funcionários",
        font=("Arial", 28, "bold")
    )

    titulo.pack(pady=30)

    frame_botoes = ctk.CTkFrame(
        master=frame_principal,
        fg_color="transparent"
    )
    frame_botoes.pack(fill="x", padx=30, pady=10)

    for coluna in range(3):
        frame_botoes.grid_columnconfigure(coluna, weight=1)

    estilo_botao = {
        "width": 170,
        "height": 50,
        "corner_radius": 8,
        "fg_color": "#1f4fbf",
        "hover_color": "#2b5fd1",
        "font": ("Segoe UI", 16),
    }

    botao_excluir = ctk.CTkButton(
        master=frame_botoes,
        text="Excluir Funcionário",
        command=excluir,
        **estilo_botao
    )
    botao_excluir.grid(row=0, column=0, sticky="w")

    botao_atualizar = ctk.CTkButton(
        master=frame_botoes,
        text="Atualizar Funcionário",
        command=atualizar,
        **estilo_botao
    )
    botao_atualizar.grid(row=0, column=1)

    botao_cadastrar = ctk.CTkButton(
        master=frame_botoes,
        text="Cadastrar Funcionários",
        command=cadastrar,
        **estilo_botao
    )
    botao_cadastrar.grid(row=0, column=2, sticky="e")

    # Busca os funcionários no banco
    funcionarios = listar_funcionarios()

    # Exibe todos os funcionários
    for funcionario in funcionarios:
        funcionario_id = funcionario[0]
        nome = funcionario[1]
        cargo = funcionario[2]

        card_funcionario = ctk.CTkFrame(
            master=frame_principal,
            height=75,
            corner_radius=10,
            fg_color="#ffffff",
            border_width=1,
            border_color="#d1d5db"
        )

        card_funcionario.pack(
            fill="x",
            padx=30,
            pady=8
        )

        nome_funcionario = ctk.CTkLabel(
            master=card_funcionario,
            text=nome,
            font=("Segoe UI", 17, "bold"),
            text_color="#1f2937"
        )

        nome_funcionario.place(x=20, y=12)

        cargo_funcionario = ctk.CTkLabel(
            master=card_funcionario,
            text=cargo,
            font=("Segoe UI", 14),
            text_color="#6b7280"
        )

        cargo_funcionario.place(x=20, y=42)

        id_funcionario = ctk.CTkLabel(
            master=card_funcionario,
            text=f"ID: {funcionario_id}",
            font=("Segoe UI", 13),
            text_color="#6b7280"
        )

        id_funcionario.place(relx=0.97, y=25, anchor="e")
