"""Sidebar com parâmetros do gerador."""
from __future__ import annotations

import tkinter as tk
import customtkinter as ctk
from typing import Callable


class Sidebar(ctk.CTkFrame):
    """Painel lateral com controles."""

    def __init__(self, parent: ctk.CTk | ctk.CTkFrame) -> None:
        super().__init__(parent, width=280)
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)

        # Vars
        self.len_var = tk.IntVar(value=16)
        self.lower_var = tk.BooleanVar(value=True)
        self.upper_var = tk.BooleanVar(value=True)
        self.digit_var = tk.BooleanVar(value=True)
        self.symbol_var = tk.BooleanVar(value=True)
        self.require_each_class_var = tk.BooleanVar(value=True)
        self.no_ambig_var = tk.BooleanVar(value=True)
        self.batch_var = tk.IntVar(value=1)

        # Widgets
        title = ctk.CTkLabel(self, text="Parâmetros",
                             font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 4))

        self._len_lbl = ctk.CTkLabel(self, text="Comprimento: 16")
        self._len_lbl.grid(row=1, column=0, sticky="ew", padx=12, pady=(6, 0))
        len_slider = ctk.CTkSlider(
            self, from_=4, to=128, number_of_steps=124,
            command=self._on_len_change
        )
        len_slider.set(self.len_var.get())
        len_slider.grid(row=2, column=0, sticky="ew", padx=12, pady=6)

        ctk.CTkCheckBox(self, text="a-z",
                        variable=self.lower_var).grid(row=3, column=0, sticky="w", padx=12, pady=(8, 0))
        ctk.CTkCheckBox(self, text="A-Z",
                        variable=self.upper_var).grid(row=4, column=0, sticky="w", padx=12, pady=2)
        ctk.CTkCheckBox(self, text="0-9",
                        variable=self.digit_var).grid(row=5, column=0, sticky="w", padx=12, pady=2)
        ctk.CTkCheckBox(self, text="Símbolos (!@#$...)",
                        variable=self.symbol_var).grid(row=6, column=0, sticky="w", padx=12, pady=2)

        ctk.CTkCheckBox(self, text="Exigir 1 de cada classe",
                        variable=self.require_each_class_var).grid(row=7, column=0, sticky="w", padx=12, pady=(10, 0))
        ctk.CTkCheckBox(self, text="Evitar caracteres ambíguos",
                        variable=self.no_ambig_var).grid(row=8, column=0, sticky="w", padx=12, pady=(2, 0))

        excl_lbl = ctk.CTkLabel(self, text="Excluir caracteres específicos:")
        excl_lbl.grid(row=9, column=0, sticky="w", padx=12, pady=(12, 2))
        self.excluir_entry = ctk.CTkEntry(self, placeholder_text=r"Ex.: {}[]()/\'\"`~,.;:")
        self.excluir_entry.grid(row=10, column=0, sticky="ew", padx=12, pady=(0, 8))

        self._batch_lbl = ctk.CTkLabel(self, text="Gerar em lote: 1 senha")
        self._batch_lbl.grid(row=11, column=0, sticky="ew", padx=12, pady=(10, 0))
        batch_slider = ctk.CTkSlider(
            self, from_=1, to=50, number_of_steps=49,
            command=self._on_batch_change
        )
        batch_slider.set(self.batch_var.get())
        batch_slider.grid(row=12, column=0, sticky="ew", padx=12, pady=6)

        tema_lbl = ctk.CTkLabel(self, text="Tema da interface:")
        tema_lbl.grid(row=13, column=0, sticky="w", padx=12, pady=(10, 0))
        self.tema_option = ctk.CTkOptionMenu(
            self, values=["System", "Dark", "Light"]
        )
        self.tema_option.set("System")
        self.tema_option.grid(row=14, column=0, sticky="ew", padx=12, pady=(0, 12))

        # Callbacks externos
        self._generate_cb: Callable[[], None] | None = None
        self._theme_cb: Callable[[str], None] | None = None

    # Exposição de callbacks
    def bind_generate(self, callback: Callable[[], None]) -> None:
        self._generate_cb = callback

    def bind_theme_change(self, callback: Callable[[str], None]) -> None:
        self._theme_cb = callback
        self.tema_option.configure(command=callback)

    # Acesso aos valores
    def get_options(self) -> dict:
        return {
            "length": self.len_var.get(),
            "use_lower": self.lower_var.get(),
            "use_upper": self.upper_var.get(),
            "use_digits": self.digit_var.get(),
            "use_symbols": self.symbol_var.get(),
            "require_each": self.require_each_class_var.get(),
            "avoid_ambiguous": self.no_ambig_var.get(),
            "exclude_custom": self.excluir_entry.get().strip(),
            "batch": self.batch_var.get(),
        }

    # Eventos internos
    def _on_len_change(self, value: float) -> None:
        val = int(float(value))
        self.len_var.set(val)
        self._len_lbl.configure(text=f"Comprimento: {val}")

    def _on_batch_change(self, value: float) -> None:
        val = int(float(value))
        self.batch_var.set(val)
        suffix = "senhas" if val > 1 else "senha"
        self._batch_lbl.configure(text=f"Gerar em lote: {val} {suffix}")
