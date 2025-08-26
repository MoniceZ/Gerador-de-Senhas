"""Aplicação principal do Gerador de Senhas."""
from __future__ import annotations

import tkinter as tk
import customtkinter as ctk

from gerador_senhas.ui.sidebar import Sidebar
from gerador_senhas.ui.main_panel import MainPanel


class PasswordGeneratorApp(ctk.CTk):
    """Janela principal."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Gerador de Senhas • CustomTkinter")
        self.geometry("900x540")
        ctk.set_appearance_mode("System")  # "Dark", "Light", "System"
        ctk.set_default_color_theme("blue")

        # Estado compartilhado simples
        self.history: list[str] = []

        # Layout base
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Construção das áreas
        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=0, column=0, sticky="nsw", padx=12, pady=12)

        self.main = MainPanel(self)
        self.main.grid(row=0, column=1, sticky="nsew", padx=(0, 12), pady=12)

        # Ligações entre UI
        self.sidebar.bind_generate(self.main.handle_generate)
        self.sidebar.bind_theme_change(self._set_theme)

    def _set_theme(self, choice: str) -> None:
        """Alterna o tema de aparência."""
        ctk.set_appearance_mode(choice)

    # Utilidades de clipboard para uso pela MainPanel
    def copy_to_clipboard(self, value: str) -> None:
        """Copia valor para o clipboard."""
        self.clipboard_clear()
        self.clipboard_append(value)
        self.update()  # garante persistência no X11
