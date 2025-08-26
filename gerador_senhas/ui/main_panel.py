"""Painel principal: campo de senha, força e histórico."""
from __future__ import annotations

import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox

import customtkinter as ctk

from gerador_senhas.core import (
    build_charset,
    entropy_bits,
    generate_password,
    strength_label_and_ratio,
)


class MainPanel(ctk.CTkFrame):
    """Área principal com geração, medidor e histórico."""

    def __init__(self, parent: ctk.CTk | ctk.CTkFrame) -> None:
        super().__init__(parent)
        self.parent = parent  # PasswordGeneratorApp
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        header = ctk.CTkLabel(
            self,
            text="Gerador de Senhas",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        header.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))

        # Campo de senha + botões
        entry_frame = ctk.CTkFrame(self)
        entry_frame.grid(row=1, column=0, sticky="ew", padx=12, pady=6)
        entry_frame.grid_columnconfigure(0, weight=1)
        entry_frame.grid_columnconfigure(1, weight=0)
        entry_frame.grid_columnconfigure(2, weight=0)

        self.password_var = tk.StringVar()
        self.password_entry = ctk.CTkEntry(
            entry_frame, textvariable=self.password_var, show="*", height=38
        )
        self.password_entry.grid(row=0, column=0, sticky="ew", padx=(8, 6), pady=8)

        self._show_var = tk.BooleanVar(value=False)
        show_btn = ctk.CTkSwitch(
            entry_frame, text="Mostrar", variable=self._show_var,
            command=self._toggle_show
        )
        show_btn.grid(row=0, column=1, padx=6, pady=8)

        copy_btn = ctk.CTkButton(entry_frame, text="Copiar", command=self._copy)
        copy_btn.grid(row=0, column=2, padx=(6, 8), pady=8)

        # Barra de força
        meter_frame = ctk.CTkFrame(self)
        meter_frame.grid(row=2, column=0, sticky="ew", padx=12, pady=6)
        meter_frame.grid_columnconfigure(0, weight=1)

        self.entropy_label = ctk.CTkLabel(
            meter_frame, text="Entropia: 0.0 bits • Força: —"
        )
        self.entropy_label.grid(row=0, column=0, sticky="w", padx=8, pady=(8, 2))
        self.meter = ctk.CTkProgressBar(meter_frame)
        self.meter.set(0.0)
        self.meter.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))

        # Histórico
        history_frame = ctk.CTkFrame(self)
        history_frame.grid(row=3, column=0, sticky="nsew", padx=12, pady=6)
        history_frame.grid_columnconfigure(0, weight=1)
        history_frame.grid_rowconfigure(1, weight=1)

        hist_lbl = ctk.CTkLabel(history_frame, text="Histórico (sessão atual)")
        hist_lbl.grid(row=0, column=0, sticky="w", padx=8, pady=(8, 4))

        self.hist_list = tk.Listbox(
            history_frame, height=8, exportselection=False
        )
        self.hist_list.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))

        hist_btns = ctk.CTkFrame(history_frame)
        hist_btns.grid(row=2, column=0, sticky="ew", padx=8, pady=(0, 8))
        hist_btns.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkButton(
            hist_btns, text="Copiar selecionada", command=self._copy_from_history
        ).grid(row=0, column=0, padx=4, pady=4, sticky="ew")
        ctk.CTkButton(
            hist_btns, text="Salvar histórico", command=self._save_history
        ).grid(row=0, column=1, padx=4, pady=4, sticky="ew")
        ctk.CTkButton(
            hist_btns, text="Limpar histórico", command=self._clear_history
        ).grid(row=0, column=2, padx=4, pady=4, sticky="ew")
        ctk.CTkButton(
            hist_btns, text="Gerar", command=self.handle_generate
        ).grid(row=0, column=3, padx=4, pady=4, sticky="ew")

        # Rodapé
        footer = ctk.CTkLabel(
            self,
            text="Dica: aumente o comprimento para elevar a entropia; 16+ é um bom ponto de partida.",
        )
        footer.grid(row=4, column=0, sticky="w", padx=12, pady=(4, 12))

    # Ligações externas
    def handle_generate(self) -> None:
        """Gera senha(s) com base nas opções do Sidebar."""
        options = self.master.sidebar.get_options()  # type: ignore[attr-defined]
        length = options["length"]
        use_lower = options["use_lower"]
        use_upper = options["use_upper"]
        use_digits = options["use_digits"]
        use_symbols = options["use_symbols"]
        require_each = options["require_each"]
        avoid_ambiguous = options["avoid_ambiguous"]
        exclude_custom = options["exclude_custom"]
        batch = options["batch"]

        if not any([use_lower, use_upper, use_digits, use_symbols]):
            messagebox.showwarning(
                "Atenção", "Selecione pelo menos um conjunto de caracteres."
            )
            return

        charset = build_charset(
            use_lower, use_upper, use_digits, use_symbols,
            avoid_ambiguous, exclude_custom
        )
        if len(charset) < 2:
            messagebox.showwarning(
                "Atenção", "Charset resultante muito pequeno. Ajuste as opções."
            )
            return

        generated: list[str] = []
        try:
            for _ in range(batch):
                pwd = generate_password(
                    length=length,
                    charset=charset,
                    require_each_class=require_each,
                    use_lower=use_lower,
                    use_upper=use_upper,
                    use_digits=use_digits,
                    use_symbols=use_symbols,
                )
                generated.append(pwd)
        except Exception as exc:
            messagebox.showerror("Erro", f"Falha ao gerar: {exc}")
            return

        # Atualiza campo principal com a primeira
        self.password_var.set(generated[0] if generated else "")

        # Entropia e força
        ent = entropy_bits(length, len(charset))
        label, ratio = strength_label_and_ratio(ent)
        self.entropy_label.configure(text=f"Entropia: {ent:.1f} bits • Força: {label}")
        self.meter.set(ratio)

        # Histórico
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for pwd in generated:
            line = f"{timestamp}  |  {pwd}"
            self.master.history.append(line)  # type: ignore[attr-defined]
            self.hist_list.insert(tk.END, line)

        if batch > 1:
            messagebox.showinfo(
                "Geradas", f"{batch} senhas geradas e adicionadas ao histórico."
            )

    # Ações locais
    def _toggle_show(self) -> None:
        self.password_entry.configure(show="" if self._show_var.get() else "*")

    def _copy(self) -> None:
        val = self.password_var.get()
        if not val:
            messagebox.showinfo("Copiar", "Nenhuma senha para copiar.")
            return
        try:
            self.master.copy_to_clipboard(val)  # type: ignore[attr-defined]
            messagebox.showinfo("Copiar", "Senha copiada para a área de transferência.")
        except Exception as exc:
            messagebox.showerror("Erro", f"Falha ao copiar: {exc}")

    def _copy_from_history(self) -> None:
        sel = self.hist_list.curselection()
        if not sel:
            messagebox.showinfo("Copiar", "Selecione uma senha no histórico.")
            return
        val = self.hist_list.get(sel[0]).split("  |  ")[-1]
        try:
            self.master.copy_to_clipboard(val)  # type: ignore[attr-defined]
            messagebox.showinfo("Copiar", "Senha copiada da lista.")
        except Exception as exc:
            messagebox.showerror("Erro", f"Falha ao copiar: {exc}")

    def _save_history(self) -> None:
        if not self.master.history:  # type: ignore[attr-defined]
            messagebox.showinfo("Salvar", "Histórico vazio.")
            return
        fname = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Texto", "*.txt"), ("Todos", "*.*")],
        )
        if not fname:
            return
        try:
            with open(fname, "w", encoding="utf-8") as f:
                f.write("\n".join(self.master.history))  # type: ignore[attr-defined]
            messagebox.showinfo("Salvar", "Histórico salvo.")
        except Exception as exc:
            messagebox.showerror("Erro", f"Falha ao salvar: {exc}")

    def _clear_history(self) -> None:
        self.master.history.clear()  # type: ignore[attr-defined]
        self.hist_list.delete(0, tk.END)
