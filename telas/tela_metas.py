import customtkinter as ctk

from banco_de_dados import (
    listar_funcionarios,
    cadastrar_metas
)


def abrir_tela_metas(frame_principal):
    for widget in frame_principal.winfo_children():
        widget.destroy()

    titulo = ctk.CTkLabel(
        master=frame_principal,
        text="Metas Diárias",
        font=("Segoe UI", 28, "bold")
    )

    titulo.pack(
        padx=30,
        pady=(30, 20)
    )