"""Ponto de entrada do Gerador de Senhas."""
from gerador_senhas.app import PasswordGeneratorApp

if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()