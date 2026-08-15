from datetime import datetime
import json
from pathlib import Path
import shutil
from tkinter import filedialog, messagebox

import customtkinter as ctk


def abrir_tela_configuracoes(frame_principal):
    for widget in frame_principal.winfo_children():
        widget.destroy()

    fundo = ("#F5F7FB", "#111827")
    branco = ("#FFFFFF", "#1F2937")
    borda = ("#E5E7EB", "#374151")
    texto = ("#111827", "#F9FAFB")
    secundario = ("#6B7280", "#9CA3AF")
    azul = "#1F4FBF"
    azul_hover = "#173B8F"
    caminho_banco = Path(__file__).resolve().parent.parent / "metas.db"
    caminho_configuracoes = caminho_banco.with_name("configuracoes.json")
    configuracoes = {
        "tema": "☀ Claro",
        "confirmar_exclusao": True,
        "abrir_maximizado": False,
        "atualizar_listas": True,
        "mensagens_sucesso": True
    }

    try:
        with open(caminho_configuracoes, "r", encoding="utf-8") as arquivo:
            dados_salvos = json.load(arquivo)
            if isinstance(dados_salvos, dict):
                configuracoes.update(dados_salvos)
    except (OSError, json.JSONDecodeError):
        pass

    def gravar_configuracoes():
        temporario = caminho_configuracoes.with_suffix(".tmp")
        try:
            with open(temporario, "w", encoding="utf-8") as arquivo:
                json.dump(configuracoes, arquivo, ensure_ascii=False, indent=2)
            temporario.replace(caminho_configuracoes)
        except OSError as erro:
            messagebox.showerror(
                "Erro ao salvar",
                f"Não foi possível salvar as configurações: {erro}"
            )
            return False
        return True

    def alterar_tema(tema):
        modos = {
            "☀ Claro": "light",
            "🌙 Escuro": "dark",
            "💻 Seguir o sistema": "system"
        }
        ctk.set_appearance_mode(modos.get(tema, "light"))
        configuracoes["tema"] = tema
        gravar_configuracoes()

    def banco_valido(caminho):
        try:
            with open(caminho, "rb") as arquivo:
                return arquivo.read(16) == b"SQLite format 3\x00"
        except OSError:
            return False

    def copiar_banco(destino, titulo_sucesso):
        try:
            shutil.copy2(caminho_banco, destino)
        except OSError as erro:
            messagebox.showerror(
                "Erro na operação",
                f"Não foi possível copiar o banco de dados: {erro}"
            )
            return
        messagebox.showinfo("Operação concluída", titulo_sucesso)

    def criar_backup():
        nome_padrao = f"backup_metas_{datetime.now():%Y%m%d_%H%M%S}.db"
        destino = filedialog.asksaveasfilename(
            title="Salvar backup do banco",
            initialfile=nome_padrao,
            defaultextension=".db",
            filetypes=[("Banco SQLite", "*.db"), ("Todos os arquivos", "*.*")]
        )
        if destino:
            copiar_banco(destino, "Backup criado com sucesso!")

    def substituir_banco(titulo, mensagem_confirmacao, mensagem_sucesso):
        origem = filedialog.askopenfilename(
            title=titulo,
            filetypes=[("Banco SQLite", "*.db"), ("Todos os arquivos", "*.*")]
        )
        if not origem:
            return

        origem = Path(origem).resolve()
        if origem == caminho_banco.resolve():
            messagebox.showwarning(
                "Arquivo já utilizado",
                "Selecione um arquivo diferente do banco atualmente utilizado."
            )
            return
        if not banco_valido(origem):
            messagebox.showerror(
                "Arquivo inválido",
                "O arquivo selecionado não é um banco SQLite válido."
            )
            return
        if not messagebox.askyesno("Confirmar operação", mensagem_confirmacao):
            return

        temporario = caminho_banco.with_name("metas_importacao_temporaria.db")
        try:
            shutil.copy2(origem, temporario)
            temporario.replace(caminho_banco)
        except OSError as erro:
            if temporario.exists():
                temporario.unlink()
            messagebox.showerror(
                "Erro na operação",
                f"Não foi possível substituir o banco de dados: {erro}"
            )
            return
        messagebox.showinfo("Operação concluída", mensagem_sucesso)

    def restaurar_backup():
        substituir_banco(
            "Selecionar backup",
            "A restauração substituirá os dados atuais. Deseja continuar?",
            "Backup restaurado com sucesso!"
        )

    pagina = ctk.CTkScrollableFrame(
        master=frame_principal,
        fg_color=fundo,
        corner_radius=0,
        scrollbar_button_color="#9CA3AF",
        scrollbar_button_hover_color="#6B7280"
    )
    pagina.pack(fill="both", expand=True)
    pagina.grid_columnconfigure(0, weight=1)

    # Cabeçalho
    cabecalho = ctk.CTkFrame(master=pagina, fg_color="transparent")
    cabecalho.grid(row=0, column=0, sticky="ew", padx=34, pady=(26, 14))

    ctk.CTkLabel(
        master=cabecalho,
        text="Configurações",
        font=("Segoe UI", 30, "bold"),
        text_color=texto,
        anchor="w"
    ).pack(fill="x")
    ctk.CTkLabel(
        master=cabecalho,
        text="Personalize o comportamento do sistema e gerencie suas preferências.",
        font=("Segoe UI", 14),
        text_color=secundario,
        anchor="w"
    ).pack(fill="x", pady=(3, 0))

    conteudo = ctk.CTkFrame(master=pagina, fg_color="transparent")
    conteudo.grid(row=1, column=0, sticky="ew", padx=28)
    conteudo.grid_columnconfigure((0, 1), weight=1, uniform="configuracoes")

    # Aparência
    card_aparencia = ctk.CTkFrame(
        master=conteudo,
        corner_radius=14,
        border_width=1,
        border_color=borda,
        fg_color=branco
    )
    card_aparencia.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)

    ctk.CTkLabel(
        master=card_aparencia,
        text="Aparência",
        font=("Segoe UI", 18, "bold"),
        text_color=texto,
        anchor="w"
    ).pack(fill="x", padx=20, pady=(18, 3))
    ctk.CTkLabel(
        master=card_aparencia,
        text="Escolha como o sistema deve ser exibido.",
        font=("Segoe UI", 12),
        text_color=secundario,
        anchor="w"
    ).pack(fill="x", padx=20, pady=(0, 18))
    ctk.CTkLabel(
        master=card_aparencia,
        text="Tema",
        font=("Segoe UI", 13, "bold"),
        text_color=texto,
        anchor="w"
    ).pack(fill="x", padx=20, pady=(0, 6))

    menu_tema = ctk.CTkOptionMenu(
        master=card_aparencia,
        values=["☀ Claro", "🌙 Escuro", "💻 Seguir o sistema"],
        height=42,
        corner_radius=8,
        fg_color=azul,
        button_color=azul_hover,
        button_hover_color="#123272",
        command=alterar_tema
    )
    menu_tema.pack(fill="x", padx=20, pady=(0, 20))
    menu_tema.set(configuracoes["tema"])

    # Preferências
    card_preferencias = ctk.CTkFrame(
        master=conteudo,
        corner_radius=14,
        border_width=1,
        border_color=borda,
        fg_color=branco
    )
    card_preferencias.grid(row=0, column=1, sticky="nsew", padx=6, pady=6)

    ctk.CTkLabel(
        master=card_preferencias,
        text="Preferências",
        font=("Segoe UI", 18, "bold"),
        text_color=texto,
        anchor="w"
    ).pack(fill="x", padx=20, pady=(18, 3))
    ctk.CTkLabel(
        master=card_preferencias,
        text="Defina comportamentos padrão da aplicação.",
        font=("Segoe UI", 12),
        text_color=secundario,
        anchor="w"
    ).pack(fill="x", padx=20, pady=(0, 12))

    preferencias = (
        ("confirmar_exclusao", "Confirmar antes de excluir registros"),
        ("abrir_maximizado", "Abrir sistema maximizado"),
        ("atualizar_listas", "Atualizar listas automaticamente após cadastros"),
        ("mensagens_sucesso", "Exibir mensagens de sucesso")
    )
    switches_preferencias = {}
    for chave, rotulo in preferencias:
        opcao = ctk.CTkSwitch(
            master=card_preferencias,
            text=rotulo,
            font=("Segoe UI", 12),
            text_color=texto,
            progress_color=azul,
            button_hover_color=azul_hover
        )
        opcao.pack(fill="x", padx=20, pady=6)
        switches_preferencias[chave] = opcao
        if configuracoes.get(chave, False):
            opcao.select()

    # Banco de dados
    card_banco = ctk.CTkFrame(
        master=conteudo,
        corner_radius=14,
        border_width=1,
        border_color=borda,
        fg_color=branco
    )
    card_banco.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=6, pady=6)
    card_banco.grid_columnconfigure((0, 1), weight=1)

    ctk.CTkLabel(
        master=card_banco,
        text="Banco de Dados",
        font=("Segoe UI", 18, "bold"),
        text_color=texto,
        anchor="w"
    ).grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(18, 3))
    ctk.CTkLabel(
        master=card_banco,
        text="Ferramentas para gerenciamento dos dados.",
        font=("Segoe UI", 12),
        text_color=secundario,
        anchor="w"
    ).grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 12))

    banco_atual = ctk.CTkFrame(
        master=card_banco,
        corner_radius=9,
        fg_color=("#E8EEFC", "#253B66")
    )
    banco_atual.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 14))
    ctk.CTkLabel(
        master=banco_atual,
        text="Banco utilizado",
        font=("Segoe UI", 11),
        text_color=secundario,
        anchor="w"
    ).pack(fill="x", padx=12, pady=(9, 0))
    ctk.CTkLabel(
        master=banco_atual,
        text="metas.db",
        font=("Segoe UI", 14, "bold"),
        text_color=azul,
        anchor="w"
    ).pack(fill="x", padx=12, pady=(1, 9))

    botoes_banco = (
        ("Criar Backup", criar_backup, 0, 0),
        ("Restaurar Backup", restaurar_backup, 0, 1)
    )
    for rotulo, comando, linha, coluna in botoes_banco:
        ctk.CTkButton(
            master=card_banco,
            text=rotulo,
            height=38,
            corner_radius=8,
            fg_color=azul,
            hover_color=azul_hover,
            command=comando
        ).grid(
            row=linha + 3,
            column=coluna,
            sticky="ew",
            padx=(20 if coluna == 0 else 6, 6 if coluna == 0 else 20),
            pady=6
        )

    # Sobre
    card_sobre = ctk.CTkFrame(
        master=conteudo,
        corner_radius=14,
        border_width=1,
        border_color=borda,
        fg_color=branco
    )
    card_sobre.grid(row=2, column=0, columnspan=2, sticky="ew", padx=6, pady=6)
    card_sobre.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        master=card_sobre,
        text="Sobre",
        font=("Segoe UI", 18, "bold"),
        text_color=texto,
        anchor="w"
    ).grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 3))
    ctk.CTkLabel(
        master=card_sobre,
        text="Sistema de Cadastro de Metas",
        font=("Segoe UI", 16, "bold"),
        text_color=azul,
        anchor="w"
    ).grid(row=1, column=0, sticky="ew", padx=20, pady=(8, 3))
    ctk.CTkLabel(
        master=card_sobre,
        text="Versão 1.0   •   Python + CustomTkinter   •   SQLite   •   GitHub",
        font=("Segoe UI", 12),
        text_color=secundario,
        anchor="w"
    ).grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 8))
    ctk.CTkLabel(
        master=card_sobre,
        text="Projeto desenvolvido por Lucas Alérico Alves para gerenciamento de metas de produção.",
        font=("Segoe UI", 12),
        text_color=texto,
        anchor="w"
    ).grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 18))

    # Rodapé
    def salvar_preferencias():
        configuracoes["tema"] = menu_tema.get()
        for chave, switch in switches_preferencias.items():
            configuracoes[chave] = bool(switch.get())

        if gravar_configuracoes():
            messagebox.showinfo(
                "Configurações salvas",
                "As configurações foram salvas com sucesso!"
            )

    ctk.CTkButton(
        master=pagina,
        text="Salvar Configurações",
        height=48,
        corner_radius=9,
        font=("Segoe UI", 15, "bold"),
        fg_color=azul,
        hover_color=azul_hover,
        command=salvar_preferencias
    ).grid(row=2, column=0, sticky="ew", padx=34, pady=(12, 28))

    # Permite rolar mesmo com o ponteiro sobre os controles.
    canvas = pagina._parent_canvas
    tag_scroll = f"ConfiguracoesScroll{id(pagina)}"

    def rolar(event):
        if getattr(event, "num", None) == 4:
            direcao = -3
        elif getattr(event, "num", None) == 5:
            direcao = 3
        else:
            direcao = -3 if event.delta > 0 else 3
        canvas.yview_scroll(direcao, "units")

    def vincular_scroll(widget):
        widget.bindtags((tag_scroll,) + widget.bindtags())
        for filho in widget.winfo_children():
            vincular_scroll(filho)

    canvas.bind_class(tag_scroll, "<MouseWheel>", rolar, add="+")
    canvas.bind_class(tag_scroll, "<Button-4>", rolar, add="+")
    canvas.bind_class(tag_scroll, "<Button-5>", rolar, add="+")
    vincular_scroll(pagina)
    vincular_scroll(canvas)
