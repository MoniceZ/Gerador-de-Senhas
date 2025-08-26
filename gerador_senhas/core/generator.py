"""Construção de charset e geração de senhas."""
from __future__ import annotations

import secrets
import string
from typing import Iterable

from .constants import AMBIGUOUS, SAFE_SYMBOLS


def build_charset(
    use_lower: bool,
    use_upper: bool,
    use_digits: bool,
    use_symbols: bool,
    avoid_ambiguous: bool,
    exclude_custom: str | None,
) -> str:
    """Monta o charset final conforme as opções."""
    charset = ""
    if use_lower:
        charset += string.ascii_lowercase
    if use_upper:
        charset += string.ascii_uppercase
    if use_digits:
        charset += string.digits
    if use_symbols:
        charset += SAFE_SYMBOLS

    if avoid_ambiguous:
        charset = "".join(ch for ch in charset if ch not in AMBIGUOUS)

    if exclude_custom:
        excluir_set = set(exclude_custom)
        charset = "".join(ch for ch in charset if ch not in excluir_set)

    # Remove duplicatas e ordena para estabilidade
    return "".join(sorted(set(charset)))


def _mandatory_samples(
    require_each_class: bool,
    use_lower: bool,
    use_upper: bool,
    use_digits: bool,
    use_symbols: bool,
) -> list[str]:
    """Seleciona 1 de cada classe marcada, se exigido."""
    if not require_each_class:
        return []

    samples: list[str] = []
    if use_lower:
        samples.append(secrets.choice(string.ascii_lowercase))
    if use_upper:
        samples.append(secrets.choice(string.ascii_uppercase))
    if use_digits:
        samples.append(secrets.choice(string.digits))
    if use_symbols:
        samples.append(secrets.choice(SAFE_SYMBOLS))
    return samples


def _shuffle_in_place(items: list[str]) -> None:
    """Embaralha lista in-place via Fisher–Yates com secrets."""
    for i in range(len(items) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        items[i], items[j] = items[j], items[i]


def generate_password(
    length: int,
    charset: str,
    require_each_class: bool = False,
    use_lower: bool = False,
    use_upper: bool = False,
    use_digits: bool = False,
    use_symbols: bool = False,
) -> str:
    """Gera uma senha aleatória segura.

    Levanta ValueError para parâmetros inválidos.
    """
    if not charset:
        raise ValueError("Nenhum conjunto de caracteres selecionado.")
    if length <= 0:
        raise ValueError("Comprimento inválido.")

    mandatory = _mandatory_samples(
        require_each_class, use_lower, use_upper, use_digits, use_symbols
    )
    if len(mandatory) > length:
        raise ValueError(
            "O comprimento é menor que a quantidade de classes exigidas."
        )

    remaining = length - len(mandatory)
    body = [secrets.choice(charset) for _ in range(remaining)]
    password_chars = mandatory + body
    _shuffle_in_place(password_chars)
    return "".join(password_chars)
