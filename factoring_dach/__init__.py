"""
factoring_dach — DACH B2B Factoring-, Einkaufsfinanzierungs- & Working-Capital-Rechner 2026
"""

from .calculator import (
    FactoringInput,
    FactoringResult,
    calculate_factoring,
    get_country_legal_standard,
)

__all__ = [
    "FactoringInput",
    "FactoringResult",
    "calculate_factoring",
    "get_country_legal_standard",
]
__version__ = "1.0.0"
