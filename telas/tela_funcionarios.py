import customtkinter as ctk

def abrir_tela_funcionarios(frame_principal):
    for widget in frame_principal.winfo_children():
        widget.destroy()

    titulo = ctk.CTkLabel(
        master=frame_principal,
        text="Funcionários",
        font=("Arial", 28, "bold")
    )

    titulo.pack(pady=30)