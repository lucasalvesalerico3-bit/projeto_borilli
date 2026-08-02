import customtkinter as ctk
from datetime import date
from tkinter import messagebox

from banco_de_dados import (
    apontar_realizado,
    atualizar_metas,
    cadastrar_metas,
    excluir_metas,
    listar_funcionarios,
    listar_metas
)


def abrir_tela_metas(frame_principal):

    # Limpa qualquer tela que já esteja aberta
    for widget in frame_principal.winfo_children():
        widget.destroy()

    # Busca os funcionários cadastrados
    funcionarios = listar_funcionarios()

    # Monta as opções que aparecerão no ComboBox
    opcoes_funcionarios = []

    for funcionario in funcionarios:
        funcionario_id = funcionario[0]
        nome = funcionario[1]

        opcao = f"{funcionario_id} - {nome}"
        opcoes_funcionarios.append(opcao)

    # Caso ainda não exista nenhum funcionário cadastrado
    if not opcoes_funcionarios:
        opcoes_funcionarios = ["Nenhum funcionário cadastrado"]

    # CABEÇALHO DA TELA
    titulo = ctk.CTkLabel(
        master=frame_principal,
        text="Metas Diárias",
        font=("Segoe UI", 30, "bold"),
        text_color=("#111827", "#F9FAFB")
    )

    titulo.pack(
        anchor="w",
        padx=40,
        pady=(30, 0)
    )

    descricao = ctk.CTkLabel(
        master=frame_principal,
        text="Cadastre e acompanhe as metas diárias dos funcionários.",
        font=("Segoe UI", 14),
        text_color=("#6B7280", "#9CA3AF")
    )

    descricao.pack(
        anchor="w",
        padx=40,
        pady=(5, 20)
    )

    # CARD PRINCIPAL DO FORMULÁRIO
    card_formulario = ctk.CTkFrame(
        master=frame_principal,
        corner_radius=14,
        border_width=1,
        border_color=("#D1D5DB", "#374151"),
        fg_color=("#FFFFFF", "#1F2937")
    )

    card_formulario.pack(
        fill="x",
        padx=40,
        pady=(0, 12)
    )

    # Faz as duas colunas crescerem igualmente
    card_formulario.grid_columnconfigure(0, weight=1)
    card_formulario.grid_columnconfigure(1, weight=1)

    titulo_card = ctk.CTkLabel(
        master=card_formulario,
        text="Informações da Meta",
        font=("Segoe UI", 20, "bold"),
        text_color=("#111827", "#F9FAFB")
    )

    titulo_card.grid(
        row=0,
        column=0,
        columnspan=2,
        sticky="w",
        padx=25,
        pady=(20, 5)
    )

    descricao_card = ctk.CTkLabel(
        master=card_formulario,
        text="Informe o funcionário, a data e os valores da produção.",
        font=("Segoe UI", 13),
        text_color=("#6B7280", "#9CA3AF")
    )

    descricao_card.grid(
        row=1,
        column=0,
        columnspan=2,
        sticky="w",
        padx=25,
        pady=(0, 20)
    )

    # COLUNA ESQUERDA
    coluna_esquerda = ctk.CTkFrame(
        master=card_formulario,
        fg_color="transparent"
    )

    coluna_esquerda.grid(
        row=2,
        column=0,
        sticky="nsew",
        padx=(25, 15),
        pady=(0, 20)
    )

    label_funcionario = ctk.CTkLabel(
        master=coluna_esquerda,
        text="Funcionário",
        font=("Segoe UI", 14, "bold"),
        text_color=("#374151", "#D1D5DB")
    )

    label_funcionario.pack(
        anchor="w",
        pady=(0, 6)
    )

    combo_funcionarios = ctk.CTkComboBox(
        master=coluna_esquerda,
        values=opcoes_funcionarios,
        height=42,
        corner_radius=8,
        state="readonly"
    )

    combo_funcionarios.pack(
        fill="x",
        pady=(0, 18)
    )

    combo_funcionarios.set(opcoes_funcionarios[0])

    label_data = ctk.CTkLabel(
        master=coluna_esquerda,
        text="Data",
        font=("Segoe UI", 14, "bold"),
        text_color=("#374151", "#D1D5DB")
    )

    label_data.pack(
        anchor="w",
        pady=(0, 6)
    )

    campo_data = ctk.CTkEntry(
        master=coluna_esquerda,
        height=42,
        corner_radius=8
    )

    campo_data.pack(
        fill="x",
        pady=(0, 18)
    )

    campo_data.insert(
        0,
        date.today().strftime("%Y-%m-%d")
    )

    label_meta = ctk.CTkLabel(
        master=coluna_esquerda,
        text="Meta do dia",
        font=("Segoe UI", 14, "bold"),
        text_color=("#374151", "#D1D5DB")
    )

    label_meta.pack(
        anchor="w",
        pady=(0, 6)
    )

    campo_meta = ctk.CTkEntry(
        master=coluna_esquerda,
        placeholder_text="Digite a meta diária",
        height=42,
        corner_radius=8
    )

    campo_meta.pack(
        fill="x"
    )


    # COLUNA DIREITA
    coluna_direita = ctk.CTkFrame(
        master=card_formulario,
        fg_color="transparent"
    )

    coluna_direita.grid(
        row=2,
        column=1,
        sticky="nsew",
        padx=(15, 25),
        pady=(0, 20)
    )

    label_realizado = ctk.CTkLabel(
        master=coluna_direita,
        text="Quantidade realizada",
        font=("Segoe UI", 14, "bold"),
        text_color=("#374151", "#D1D5DB")
    )

    label_realizado.pack(
        anchor="w",
        pady=(0, 6)
    )

    campo_realizado = ctk.CTkEntry(
        master=coluna_direita,
        placeholder_text="Digite o valor realizado",
        height=42,
        corner_radius=8
    )

    campo_realizado.pack(
        fill="x",
        pady=(0, 20)
    )

    meta_em_edicao = {"id": None}

    def limpar_formulario():
        meta_em_edicao["id"] = None
        campo_meta.delete(0, "end")
        campo_realizado.delete(0, "end")
        botao_salvar.configure(text="Cadastrar Meta")

    def carregar_meta_para_edicao(meta_id, funcionario, data_meta, valor_meta, realizado):
        opcao_funcionario = next(
            (
                opcao for opcao in opcoes_funcionarios
                if opcao.split(" - ", 1)[-1] == funcionario
            ),
            None
        )

        if opcao_funcionario:
            combo_funcionarios.set(opcao_funcionario)

        campo_data.delete(0, "end")
        campo_data.insert(0, data_meta)
        campo_meta.delete(0, "end")
        campo_meta.insert(0, f"{valor_meta:g}")
        campo_realizado.delete(0, "end")
        campo_realizado.insert(0, f"{realizado:g}")
        meta_em_edicao["id"] = meta_id
        botao_salvar.configure(text="Salvar Alterações")
        campo_meta.focus_set()

    def excluir_meta(meta_id):
        confirmar = messagebox.askyesno(
            "Excluir meta",
            "Deseja realmente excluir esta meta?"
        )

        if not confirmar:
            return

        try:
            excluir_metas(meta_id)
        except Exception as erro:
            messagebox.showerror(
                "Erro ao excluir",
                f"Não foi possível excluir a meta: {erro}"
            )
            return

        if meta_em_edicao["id"] == meta_id:
            limpar_formulario()

        atualizar_listagem()
        messagebox.showinfo("Sucesso", "Meta excluída com sucesso!")

    def salvar_meta():
        funcionario_selecionado = combo_funcionarios.get()
        data_informada = campo_data.get().strip()
        meta_informada = campo_meta.get().strip()
        realizado_informado = campo_realizado.get().strip()

        if not funcionarios:
            messagebox.showwarning(
                "Funcionário não cadastrado",
                "Cadastre um funcionário antes de cadastrar uma meta."
            )
            return

        try:
            funcionario_id = int(funcionario_selecionado.split(" - ", 1)[0])
            date.fromisoformat(data_informada)
            valor_meta = float(meta_informada.replace(",", "."))
            valor_realizado = (
                float(realizado_informado.replace(",", "."))
                if realizado_informado else 0
            )

            if valor_meta <= 0 or valor_realizado < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Dados inválidos",
                "Informe uma data válida, uma meta maior que zero e um realizado não negativo."
            )
            return

        try:
            if meta_em_edicao["id"] is None:
                meta_id = cadastrar_metas(funcionario_id, data_informada, valor_meta)
                mensagem_sucesso = "Meta cadastrada com sucesso!"
            else:
                meta_id = meta_em_edicao["id"]
                atualizar_metas(meta_id, funcionario_id, data_informada, valor_meta)
                mensagem_sucesso = "Meta atualizada com sucesso!"

            apontar_realizado(meta_id, valor_realizado)
        except Exception as erro:
            messagebox.showerror(
                "Erro ao salvar",
                f"Não foi possível salvar a meta: {erro}"
            )
            return

        limpar_formulario()
        atualizar_listagem()
        messagebox.showinfo("Sucesso", mensagem_sucesso)

    # BOTÃO SALVAR
    botao_salvar = ctk.CTkButton(
        master=card_formulario,
        text="Cadastrar Meta",
        height=45,
        corner_radius=8,
        font=("Segoe UI", 15, "bold"),
        command=salvar_meta
    )

    botao_salvar.grid(
        row=3,
        column=0,
        columnspan=2,
        sticky="ew",
        padx=25,
        pady=(0, 25)
    )

    # ÁREA DAS METAS CADASTRADAS
    card_listagem = ctk.CTkFrame(
        master=frame_principal,
        height=380,
        corner_radius=14,
        border_width=1,
        border_color=("#D1D5DB", "#374151"),
        fg_color=("#FFFFFF", "#1F2937")
    )

    card_listagem.pack(
        fill="both",
        expand=True,
        padx=40,
        pady=(0, 30)
    )
    card_listagem.pack_propagate(False)

    cabecalho_listagem = ctk.CTkFrame(
        master=card_listagem,
        fg_color="transparent"
    )
    cabecalho_listagem.pack(fill="x", padx=25, pady=(18, 10))

    titulo_listagem = ctk.CTkLabel(
        master=cabecalho_listagem,
        text="Metas cadastradas",
        font=("Segoe UI", 20, "bold"),
        text_color=("#111827", "#F9FAFB")
    )
    titulo_listagem.pack(side="left")

    total_metas = ctk.CTkLabel(
        master=cabecalho_listagem,
        text="0 registros",
        font=("Segoe UI", 13, "bold"),
        text_color="#1F4FBF",
        fg_color=("#E8EEFC", "#253B66"),
        corner_radius=10,
        width=100,
        height=28
    )
    total_metas.pack(side="right")

    frame_metas = ctk.CTkScrollableFrame(
        master=card_listagem,
        fg_color=("#F3F4F6", "#111827"),
        corner_radius=10,
        scrollbar_button_color="#9CA3AF",
        scrollbar_button_hover_color="#6B7280"
    )

    frame_metas.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=(0, 18)
    )

    def rolar_metas(event):
        if getattr(event, "num", None) == 4:
            direcao = -1
        elif getattr(event, "num", None) == 5:
            direcao = 1
        else:
            direcao = -1 if event.delta > 0 else 1

        frame_metas._parent_canvas.yview_scroll(direcao, "units")

    def ativar_scroll_mouse(widget):
        widget.bind("<MouseWheel>", rolar_metas, add="+")
        widget.bind("<Button-4>", rolar_metas, add="+")
        widget.bind("<Button-5>", rolar_metas, add="+")

    ativar_scroll_mouse(frame_metas)
    ativar_scroll_mouse(frame_metas._parent_canvas)

    def atualizar_listagem():
        for widget in frame_metas.winfo_children():
            widget.destroy()

        metas = listar_metas()
        quantidade = len(metas)
        total_metas.configure(
            text=f"{quantidade} registro{'s' if quantidade != 1 else ''}"
        )

        if not metas:
            mensagem_vazia = ctk.CTkLabel(
                master=frame_metas,
                text="Nenhuma meta cadastrada.",
                font=("Segoe UI", 14),
                text_color=("#6B7280", "#9CA3AF")
            )
            mensagem_vazia.pack(pady=30)
            ativar_scroll_mouse(mensagem_vazia)
            return

        for indice, (meta_id, funcionario, data_meta, valor_meta, realizado) in enumerate(metas):
            linha_meta = ctk.CTkFrame(
                master=frame_metas,
                corner_radius=10,
                border_width=1,
                border_color=("#E5E7EB", "#374151"),
                fg_color=("#FFFFFF", "#253044")
            )
            linha_meta.pack(fill="x", pady=5, padx=2)
            linha_meta.grid_columnconfigure(0, weight=1)
            ativar_scroll_mouse(linha_meta)

            nome_funcionario = ctk.CTkLabel(
                master=linha_meta,
                text=f"#{meta_id}  {funcionario}",
                font=("Segoe UI", 14, "bold"),
                text_color=("#111827", "#F9FAFB"),
                anchor="w"
            )
            nome_funcionario.grid(row=0, column=0, sticky="ew", padx=14, pady=(10, 3))

            data_da_meta = ctk.CTkLabel(
                master=linha_meta,
                text=data_meta,
                font=("Segoe UI", 13),
                text_color=("#6B7280", "#9CA3AF")
            )
            data_da_meta.grid(row=0, column=1, padx=14, pady=(10, 3))

            valores_meta = ctk.CTkLabel(
                master=linha_meta,
                text=f"Meta:  {valor_meta:g}     •     Realizado:  {realizado:g}",
                font=("Segoe UI", 13, "bold"),
                text_color="#1F4FBF",
                anchor="w"
            )
            valores_meta.grid(
                row=1,
                column=0,
                sticky="ew",
                padx=14,
                pady=(3, 10)
            )

            acoes_meta = ctk.CTkFrame(
                master=linha_meta,
                fg_color="transparent"
            )
            acoes_meta.grid(row=1, column=1, padx=12, pady=(3, 10))

            botao_editar = ctk.CTkButton(
                master=acoes_meta,
                text="Editar",
                width=72,
                height=30,
                corner_radius=7,
                fg_color="#1F4FBF",
                hover_color="#173B8F",
                command=lambda dados=(
                    meta_id,
                    funcionario,
                    data_meta,
                    valor_meta,
                    realizado
                ): carregar_meta_para_edicao(*dados)
            )
            botao_editar.pack(side="left", padx=(0, 6))

            botao_excluir = ctk.CTkButton(
                master=acoes_meta,
                text="Excluir",
                width=72,
                height=30,
                corner_radius=7,
                fg_color="#DC2626",
                hover_color="#B91C1C",
                command=lambda id_meta=meta_id: excluir_meta(id_meta)
            )
            botao_excluir.pack(side="left")

            ativar_scroll_mouse(nome_funcionario)
            ativar_scroll_mouse(data_da_meta)
            ativar_scroll_mouse(valores_meta)
            ativar_scroll_mouse(acoes_meta)
            ativar_scroll_mouse(botao_editar)
            ativar_scroll_mouse(botao_excluir)

    atualizar_listagem()
