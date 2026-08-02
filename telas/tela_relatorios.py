from datetime import date, datetime
from tkinter import messagebox

import customtkinter as ctk

from banco_de_dados import (
    listar_metas,
    relatorio_anual,
    relatorio_diario,
    relatorio_mensal
)


FUNDO = ("#F5F7FB", "#111827")
BRANCO = ("#FFFFFF", "#1F2937")
BORDA = ("#E5E7EB", "#374151")
TEXTO = ("#111827", "#F9FAFB")
SECUNDARIO = ("#6B7280", "#9CA3AF")
AZUL = "#1F4FBF"
VERDE = "#16A34A"
VERMELHO = "#DC2626"


def _ativar_scroll_mouse(pagina, raiz):
    canvas = pagina._parent_canvas
    tag_scroll = f"RelatoriosScroll{id(pagina)}"

    def rolar(event):
        if getattr(event, "num", None) == 4:
            direcao = -3
        elif getattr(event, "num", None) == 5:
            direcao = 3
        else:
            direcao = -3 if event.delta > 0 else 3
        canvas.yview_scroll(direcao, "units")

    def vincular(widget):
        if not getattr(widget, "_scroll_mouse_configurado", False):
            widget.bindtags((tag_scroll,) + widget.bindtags())
            widget._scroll_mouse_configurado = True
        for filho in widget.winfo_children():
            vincular(filho)

    if not getattr(pagina, "_scroll_classe_configurada", False):
        canvas.bind_class(tag_scroll, "<MouseWheel>", rolar, add="+")
        canvas.bind_class(tag_scroll, "<Button-4>", rolar, add="+")
        canvas.bind_class(tag_scroll, "<Button-5>", rolar, add="+")
        pagina._scroll_classe_configurada = True
    vincular(raiz)
    vincular(canvas)


def _formatar(valor):
    valor = float(valor or 0)
    if valor.is_integer():
        return f"{int(valor):,}".replace(",", ".")
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _progresso(porcentagem):
    return max(0, min(float(porcentagem or 0) / 100, 1))


def _card_resumo(master, titulo, periodo, dados, coluna):
    card = ctk.CTkFrame(
        master=master,
        corner_radius=14,
        border_width=1,
        border_color=BORDA,
        fg_color=BRANCO
    )
    card.grid(row=0, column=coluna, sticky="nsew", padx=5, pady=5)
    card.grid_columnconfigure((0, 1), weight=1)

    ctk.CTkLabel(
        master=card,
        text=titulo,
        font=("Segoe UI", 16, "bold"),
        text_color=TEXTO,
        anchor="w"
    ).grid(row=0, column=0, sticky="ew", padx=(16, 5), pady=(15, 2))
    ctk.CTkLabel(
        master=card,
        text=periodo,
        font=("Segoe UI", 11),
        text_color=SECUNDARIO,
        anchor="e"
    ).grid(row=0, column=1, sticky="ew", padx=(5, 16), pady=(15, 2))

    ctk.CTkLabel(
        master=card,
        text=f"Meta\n{_formatar(dados['meta'])}",
        font=("Segoe UI", 13, "bold"),
        text_color=SECUNDARIO,
        justify="left",
        anchor="w"
    ).grid(row=1, column=0, sticky="ew", padx=(16, 5), pady=(10, 7))
    ctk.CTkLabel(
        master=card,
        text=f"Realizado\n{_formatar(dados['realizado'])}",
        font=("Segoe UI", 13, "bold"),
        text_color=AZUL,
        justify="left",
        anchor="w"
    ).grid(row=1, column=1, sticky="ew", padx=(5, 16), pady=(10, 7))

    barra = ctk.CTkProgressBar(
        master=card,
        height=10,
        corner_radius=5,
        fg_color="#E5E7EB",
        progress_color=VERDE if dados["bateu_meta"] else AZUL
    )
    barra.grid(row=2, column=0, columnspan=2, sticky="ew", padx=16, pady=(3, 5))
    barra.set(_progresso(dados["porcentagem"]))
    ctk.CTkLabel(
        master=card,
        text=f"{dados['porcentagem']:.1f}% atingido",
        font=("Segoe UI", 11, "bold"),
        text_color=VERDE if dados["bateu_meta"] else SECUNDARIO,
        anchor="w"
    ).grid(row=3, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 14))


def _grafico(master, periodos):
    card = ctk.CTkFrame(
        master=master,
        corner_radius=14,
        border_width=1,
        border_color=BORDA,
        fg_color=BRANCO
    )
    card.pack(fill="x", pady=6)

    ctk.CTkLabel(
        master=card,
        text="Comparativo Meta x Realizado",
        font=("Segoe UI", 18, "bold"),
        text_color=TEXTO,
        anchor="w"
    ).pack(fill="x", padx=20, pady=(17, 2))
    ctk.CTkLabel(
        master=card,
        text="Visão consolidada dos resultados diário, mensal e anual",
        font=("Segoe UI", 12),
        text_color=SECUNDARIO,
        anchor="w"
    ).pack(fill="x", padx=20, pady=(0, 12))

    comparativos = ctk.CTkFrame(master=card, fg_color="transparent")
    comparativos.pack(fill="x", padx=14, pady=(0, 16))
    comparativos.grid_columnconfigure((0, 1, 2), weight=1)

    for coluna, (nome, dados) in enumerate(periodos):
        atingiu = dados["bateu_meta"]
        periodo_card = ctk.CTkFrame(
            master=comparativos,
            corner_radius=12,
            border_width=1,
            border_color=BORDA,
        fg_color=("#F9FAFB", "#253044")
        )
        periodo_card.grid(row=0, column=coluna, sticky="nsew", padx=6)
        periodo_card.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(
            master=periodo_card,
            text=nome,
            font=("Segoe UI", 16, "bold"),
            text_color=TEXTO,
            anchor="w"
        ).grid(row=0, column=0, sticky="ew", padx=(15, 5), pady=(14, 10))

        ctk.CTkLabel(
            master=periodo_card,
            text=f"{dados['porcentagem']:.1f}%",
            width=72,
            height=27,
            corner_radius=9,
            fg_color="#DCFCE7" if atingiu else "#E8EEFC",
            text_color=VERDE if atingiu else AZUL,
            font=("Segoe UI", 12, "bold")
        ).grid(row=0, column=1, sticky="e", padx=(5, 15), pady=(14, 10))

        meta_box = ctk.CTkFrame(master=periodo_card, fg_color="transparent")
        meta_box.grid(row=1, column=0, sticky="ew", padx=(15, 7), pady=(2, 10))
        ctk.CTkLabel(
            master=meta_box,
            text="META",
            font=("Segoe UI", 10, "bold"),
            text_color=AZUL,
            anchor="w"
        ).pack(fill="x")
        ctk.CTkLabel(
            master=meta_box,
            text=_formatar(dados["meta"]),
            font=("Segoe UI", 20, "bold"),
            text_color=TEXTO,
            anchor="w"
        ).pack(fill="x", pady=(2, 0))

        realizado_box = ctk.CTkFrame(master=periodo_card, fg_color="transparent")
        realizado_box.grid(row=1, column=1, sticky="ew", padx=(7, 15), pady=(2, 10))
        ctk.CTkLabel(
            master=realizado_box,
            text="REALIZADO",
            font=("Segoe UI", 10, "bold"),
            text_color=VERDE,
            anchor="w"
        ).pack(fill="x")
        ctk.CTkLabel(
            master=realizado_box,
            text=_formatar(dados["realizado"]),
            font=("Segoe UI", 20, "bold"),
            text_color=TEXTO,
            anchor="w"
        ).pack(fill="x", pady=(2, 0))

        progresso = ctk.CTkProgressBar(
            master=periodo_card,
            height=9,
            corner_radius=5,
            fg_color="#E5E7EB",
            progress_color=VERDE if atingiu else AZUL
        )
        progresso.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=15,
            pady=(3, 7)
        )
        progresso.set(_progresso(dados["porcentagem"]))

        ctk.CTkLabel(
            master=periodo_card,
            text="Meta atingida" if atingiu else "Meta não atingida",
            font=("Segoe UI", 11, "bold"),
            text_color=VERDE if atingiu else VERMELHO,
            anchor="w"
        ).grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=15,
            pady=(0, 14)
        )


def _filtrar_metas(metas, periodo, data_filtro, mes, ano):
    if periodo == "Dia":
        return [meta for meta in metas if meta[2] == data_filtro]
    if periodo == "Mês":
        prefixo = f"{ano}-{mes}-"
        return [meta for meta in metas if meta[2].startswith(prefixo)]
    return [meta for meta in metas if meta[2].startswith(f"{ano}-")]


def _desempenho_funcionarios(master, metas, periodo):
    card = ctk.CTkFrame(
        master=master,
        corner_radius=14,
        border_width=1,
        border_color=BORDA,
        fg_color=BRANCO
    )
    card.pack(fill="x", pady=(6, 22))

    ctk.CTkLabel(
        master=card,
        text=f"Desempenho dos funcionários — {periodo}",
        font=("Segoe UI", 18, "bold"),
        text_color=TEXTO,
        anchor="w"
    ).pack(fill="x", padx=20, pady=(17, 2))
    ctk.CTkLabel(
        master=card,
        text="Meta, realizado e percentual individual no período selecionado",
        font=("Segoe UI", 12),
        text_color=SECUNDARIO,
        anchor="w"
    ).pack(fill="x", padx=20, pady=(0, 12))

    funcionarios = {}
    for _, nome, _, meta, realizado in metas:
        dados = funcionarios.setdefault(nome, {"meta": 0, "realizado": 0})
        dados["meta"] += float(meta or 0)
        dados["realizado"] += float(realizado or 0)

    if not funcionarios:
        ctk.CTkLabel(
            master=card,
            text="Não existem dados para o período selecionado.",
            font=("Segoe UI", 14, "bold"),
            text_color=SECUNDARIO,
            fg_color=("#F3F4F6", "#253044"),
            corner_radius=10,
            height=60
        ).pack(fill="x", padx=20, pady=(8, 22))
        return

    ordenados = sorted(
        funcionarios.items(),
        key=lambda item: item[1]["realizado"] / item[1]["meta"] if item[1]["meta"] else 0,
        reverse=True
    )
    for posicao, (nome, dados) in enumerate(ordenados, 1):
        percentual = dados["realizado"] / dados["meta"] * 100 if dados["meta"] else 0
        atingiu = dados["meta"] > 0 and dados["realizado"] >= dados["meta"]
        linha = ctk.CTkFrame(
            master=card,
            corner_radius=10,
            border_width=1,
            border_color=BORDA,
            fg_color=("#FAFAFB", "#253044")
        )
        linha.pack(fill="x", padx=20, pady=5)
        linha.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            master=linha,
            text=f"{posicao}.  {nome}",
            font=("Segoe UI", 13, "bold"),
            text_color=TEXTO,
            anchor="w"
        ).grid(row=0, column=0, sticky="ew", padx=14, pady=(10, 2))
        ctk.CTkLabel(
            master=linha,
            text="Atingida" if atingiu else "Não atingida",
            font=("Segoe UI", 11, "bold"),
            text_color=VERDE if atingiu else VERMELHO
        ).grid(row=0, column=1, padx=14, pady=(10, 2))
        ctk.CTkLabel(
            master=linha,
            text=f"Meta: {_formatar(dados['meta'])}   •   Realizado: {_formatar(dados['realizado'])}",
            font=("Segoe UI", 11),
            text_color=SECUNDARIO,
            anchor="w"
        ).grid(row=1, column=0, columnspan=2, sticky="ew", padx=14)

        barra = ctk.CTkProgressBar(
            master=linha,
            height=9,
            corner_radius=5,
            fg_color="#E5E7EB",
            progress_color=VERDE if atingiu else AZUL
        )
        barra.grid(row=2, column=0, sticky="ew", padx=(14, 8), pady=(7, 11))
        barra.set(_progresso(percentual))
        ctk.CTkLabel(
            master=linha,
            text=f"{percentual:.1f}%",
            width=65,
            font=("Segoe UI", 12, "bold"),
            text_color=VERDE if atingiu else AZUL
        ).grid(row=2, column=1, padx=(0, 14), pady=(7, 11))


def abrir_tela_relatorios(frame_principal):
    for widget in frame_principal.winfo_children():
        widget.destroy()

    hoje = date.today()
    pagina = ctk.CTkScrollableFrame(
        master=frame_principal,
        fg_color=FUNDO,
        corner_radius=0,
        scrollbar_button_color="#9CA3AF",
        scrollbar_button_hover_color="#6B7280"
    )
    pagina.pack(fill="both", expand=True)
    pagina.grid_columnconfigure(0, weight=1)

    cabecalho = ctk.CTkFrame(master=pagina, fg_color="transparent")
    cabecalho.grid(row=0, column=0, sticky="ew", padx=34, pady=(25, 13))
    ctk.CTkLabel(
        master=cabecalho,
        text="Relatórios",
        font=("Segoe UI", 30, "bold"),
        text_color=TEXTO,
        anchor="w"
    ).pack(fill="x")
    ctk.CTkLabel(
        master=cabecalho,
        text="Analise metas e resultados por diferentes períodos.",
        font=("Segoe UI", 14),
        text_color=SECUNDARIO,
        anchor="w"
    ).pack(fill="x", pady=(3, 0))

    filtros = ctk.CTkFrame(
        master=pagina,
        corner_radius=14,
        border_width=1,
        border_color=BORDA,
        fg_color=BRANCO
    )
    filtros.grid(row=1, column=0, sticky="ew", padx=34, pady=(0, 12))
    filtros.grid_columnconfigure((0, 1, 2, 3), weight=1)

    def campo_filtro(titulo, coluna):
        grupo = ctk.CTkFrame(master=filtros, fg_color="transparent")
        grupo.grid(row=0, column=coluna, sticky="ew", padx=8, pady=14)
        ctk.CTkLabel(
            master=grupo,
            text=titulo,
            font=("Segoe UI", 12, "bold"),
            text_color=TEXTO,
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        return grupo

    grupo_data = campo_filtro("Data", 0)
    entrada_data = ctk.CTkEntry(master=grupo_data, height=38)
    entrada_data.pack(fill="x")
    entrada_data.insert(0, hoje.strftime("%Y-%m-%d"))

    grupo_mes = campo_filtro("Mês", 1)
    combo_mes = ctk.CTkComboBox(
        master=grupo_mes,
        values=[f"{mes:02d}" for mes in range(1, 13)],
        state="readonly",
        height=38
    )
    combo_mes.pack(fill="x")
    combo_mes.set(hoje.strftime("%m"))

    grupo_ano = campo_filtro("Ano", 2)
    entrada_ano = ctk.CTkEntry(master=grupo_ano, height=38)
    entrada_ano.pack(fill="x")
    entrada_ano.insert(0, hoje.strftime("%Y"))

    grupo_periodo = campo_filtro("Desempenho por", 3)
    seletor_periodo = ctk.CTkSegmentedButton(
        master=grupo_periodo,
        values=["Dia", "Mês", "Ano"],
        height=38
    )
    seletor_periodo.pack(fill="x")
    seletor_periodo.set("Dia")

    botao_aplicar = ctk.CTkButton(
        master=filtros,
        text="Aplicar filtros",
        height=40,
        corner_radius=8,
        font=("Segoe UI", 13, "bold"),
        fg_color=AZUL
    )
    botao_aplicar.grid(row=1, column=0, columnspan=4, sticky="ew", padx=8, pady=(0, 14))

    resultados = ctk.CTkFrame(master=pagina, fg_color="transparent")
    resultados.grid(row=2, column=0, sticky="ew", padx=28)

    def atualizar_relatorio():
        data_filtro = entrada_data.get().strip()
        mes = combo_mes.get()
        ano = entrada_ano.get().strip()

        try:
            datetime.strptime(data_filtro, "%Y-%m-%d")
            if len(ano) != 4:
                raise ValueError
            int(ano)
        except ValueError:
            messagebox.showerror(
                "Filtros inválidos",
                "Informe a data como AAAA-MM-DD e o ano com quatro números."
            )
            return

        for widget in resultados.winfo_children():
            widget.destroy()

        diario = relatorio_diario(data_filtro)
        mensal = relatorio_mensal(mes, ano)
        anual = relatorio_anual(ano)
        metas = listar_metas()
        periodo = seletor_periodo.get()
        metas_filtradas = _filtrar_metas(metas, periodo, data_filtro, mes, ano)

        resumos = ctk.CTkFrame(master=resultados, fg_color="transparent")
        resumos.pack(fill="x", pady=(0, 6))
        resumos.grid_columnconfigure((0, 1, 2), weight=1)
        _card_resumo(resumos, "Resumo diário", data_filtro, diario, 0)
        _card_resumo(resumos, "Resumo mensal", f"{mes}/{ano}", mensal, 1)
        _card_resumo(resumos, "Resumo anual", ano, anual, 2)

        _grafico(
            resultados,
            (("Dia", diario), ("Mês", mensal), ("Ano", anual))
        )
        _desempenho_funcionarios(resultados, metas_filtradas, periodo)
        _ativar_scroll_mouse(pagina, pagina)

    botao_aplicar.configure(command=atualizar_relatorio)
    atualizar_relatorio()
