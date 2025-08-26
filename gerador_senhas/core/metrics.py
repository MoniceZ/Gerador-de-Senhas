"""Cálculo de entropia e classificação de força."""
from __future__ import annotations

import math


def entropy_bits(length: int, charset_size: int) -> float:
    """Retorna a entropia em bits de uma senha aleatória.

    Parameters
    ----------
    length : int
        Comprimento da senha.
    charset_size : int
        Tamanho do conjunto de caracteres.

    Returns
    -------
    float
        Entropia em bits.
    """
    if length <= 0 or charset_size <= 1:
        return 0.0
    return length * math.log2(charset_size)


def strength_label_and_ratio(entropy: float) -> tuple[str, float]:
    """Classifica a força pela entropia.

    Faixas:
    < 40 fraca, 40-60 média, 60-80 forte, >80 excelente
    """
    if entropy < 40:
        return "Fraca", 0.25
    if entropy < 60:
        return "Média", 0.50
    if entropy < 80:
        return "Forte", 0.75
    return "Excelente", 1.00
