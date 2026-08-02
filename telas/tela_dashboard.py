from datetime import date

import customtkinter as ctk

from banco_de_dados import listar_metas, relatorio_diario


FUNDO = ("#F5F7FB", "#111827")
BRANCO = ("#FFFFFF", "#1F2937")
BORDA = ("#E5E7EB", "#374151")
TEXTO = ("#111827", "#F9FAFB")
TEXTO_SECUNDARIO = ("#6B7280", "#9CA3AF")
AZUL = "#1F4FBF"
VERDE = "#16A34A"
VERMELHO = "#DC2626"


def _ativar_scroll_mouse(pagina, raiz):
    canvas = pagina._parent_canvas
    tag_scroll = f"DashboardScroll{id(pagina)}"

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

    canvas.bind_class(tag_scroll, "<MouseWheel>", rolar, add="+")
    canvas.bind_class(tag_scroll, "<Button-4>", rolar, add="+")
    canvas.bind_class(tag_scroll, "<Button-5>", rolar, add="+")
    vincular(raiz)
    vincular(canvas)


def _formatar_valor(valor):
    valor = float(valor or 0)
    if valor.is_integer():
        return f"{int(valor):,}".replace(",", ".")
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _criar_indicador(master, titulo, valor, descricao, cor, linha, coluna):
    card = ctk.CTkFrame(
        master=master,
        corner_radius=14,
        border_width=1,
        border_color=BORDA,
        fg_color=BRANCO
    )
    card.grid(row=linha, column=coluna, sticky="nsew", padx=6, pady=6)

    faixa = ctk.CTkFrame(master=card, width=6, corner_radius=3, fg_color=cor)
    faixa.pack(side="left", fill="y", padx=(0, 14), pady=15)

    conteudo = ctk.CTkFrame(master=card, fg_color="transparent")
    conteudo.pack(fill="both", expand=True, padx=(0, 14), pady=15)

    ctk.CTkLabel(
        master=conteudo,
        text=titulo,
        font=("Segoe UI", 13, "bold"),
        text_color=TEXTO_SECUNDARIO,
        anchor="w"
    ).pack(fill="x")
    ctk.CTkLabel(
        master=conteudo,
        text=valor,
        font=("Segoe UI", 24, "bold"),
        text_color=TEXTO,
        anchor="w"
    ).pack(fill="x", pady=(5, 1))
    ctk.CTkLabel(
        master=conteudo,
        text=descricao,
        font=("Segoe UI", 11),
        text_color=TEXTO_SECUNDARIO,
        anchor="w"
    ).pack(fill="x")


def _desempenho_do_dia(metas, data_atual):
    funcionarios = {}
    for _, nome, data_meta, meta, realizado in metas:
        if data_meta != data_atual:
            continue
        dados = funcionarios.setdefault(nome, {"meta": 0, "realizado": 0})
        dados["meta"] += float(meta or 0)
        dados["realizado"] += float(realizado or 0)

    atingiram = sum(
        1 for dados in funcionarios.values()
        if dados["meta"] > 0 and dados["realizado"] >= dados["meta"]
    )
    return atingiram, len(funcionarios) - atingiram


def abrir_tela_dashboard(frame_principal):
    for widget in frame_principal.winfo_children():
        widget.destroy()

    hoje = date.today()
    data_atual = hoje.strftime("%Y-%m-%d")
    dados = relatorio_diario(data_atual)
    atingiram, pendentes = _desempenho_do_dia(listar_metas(), data_atual)

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
    cabecalho.grid(row=0, column=0, sticky="ew", padx=34, pady=(26, 13))
    cabecalho.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        master=cabecalho,
        text="Dashboard",
        font=("Segoe UI", 30, "bold"),
        text_color=TEXTO,
        anchor="w"
    ).grid(row=0, column=0, sticky="ew")
    ctk.CTkLabel(
        master=cabecalho,
        text="Acompanhe rapidamente os resultados de hoje.",
        font=("Segoe UI", 14),
        text_color=TEXTO_SECUNDARIO,
        anchor="w"
    ).grid(row=1, column=0, sticky="ew", pady=(3, 0))
    ctk.CTkLabel(
        master=cabecalho,
        text=hoje.strftime("%d/%m/%Y"),
        font=("Segoe UI", 13, "bold"),
        text_color=AZUL,
        fg_color=("#E8EEFC", "#253B66"),
        corner_radius=10,
        width=108,
        height=32
    ).grid(row=0, column=1, rowspan=2, padx=(15, 0))

    indicadores = ctk.CTkFrame(master=pagina, fg_color="transparent")
    indicadores.grid(row=1, column=0, sticky="ew", padx=28)
    indicadores.grid_columnconfigure((0, 1), weight=1)

    bateu_meta = dados["bateu_meta"]
    cards = (
        ("Meta de hoje", _formatar_valor(dados["meta"]), "Total planejado", AZUL),
        ("Realizado hoje", _formatar_valor(dados["realizado"]), "Produção registrada", VERDE),
        ("Porcentagem atingida", f"{dados['porcentagem']:.1f}%", "Progresso diário", "#7C3AED"),
        (
            "Status da meta",
            "Atingida" if bateu_meta else "Não atingida",
            "Situação do resultado diário",
            VERDE if bateu_meta else VERMELHO
        ),
        ("Funcionários na meta", str(atingiram), "Atingiram a meta de hoje", VERDE),
        ("Funcionários pendentes", str(pendentes), "Ainda não atingiram a meta", "#F97316")
    )
    for indice, card in enumerate(cards):
        _criar_indicador(
            indicadores,
            *card,
            linha=indice // 2,
            coluna=indice % 2
        )

    resumo = ctk.CTkFrame(
        master=pagina,
        corner_radius=14,
        border_width=1,
        border_color=BORDA,
        fg_color=BRANCO
    )
    resumo.grid(row=2, column=0, sticky="ew", padx=34, pady=(12, 28))

    ctk.CTkLabel(
        master=resumo,
        text="Resumo do dia",
        font=("Segoe UI", 18, "bold"),
        text_color=TEXTO,
        anchor="w"
    ).pack(fill="x", padx=20, pady=(18, 3))
    ctk.CTkLabel(
        master=resumo,
        text=(
            f"{_formatar_valor(dados['realizado'])} realizados de "
            f"{_formatar_valor(dados['meta'])} planejados"
        ),
        font=("Segoe UI", 13),
        text_color=TEXTO_SECUNDARIO,
        anchor="w"
    ).pack(fill="x", padx=20, pady=(0, 12))

    barra = ctk.CTkProgressBar(
        master=resumo,
        height=14,
        corner_radius=7,
        fg_color=("#E5E7EB", "#374151"),
        progress_color=VERDE if bateu_meta else AZUL
    )
    barra.pack(fill="x", padx=20, pady=(0, 7))
    barra.set(max(0, min(dados["porcentagem"] / 100, 1)))
    ctk.CTkLabel(
        master=resumo,
        text=f"{dados['porcentagem']:.1f}% da meta atingida",
        font=("Segoe UI", 12, "bold"),
        text_color=VERDE if bateu_meta else TEXTO_SECUNDARIO,
        anchor="w"
    ).pack(fill="x", padx=20, pady=(0, 18))

    _ativar_scroll_mouse(pagina, pagina)
