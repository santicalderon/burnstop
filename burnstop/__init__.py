"""burnstop — pre-flight budget gate for AI agent runaways.

Born from the Nov 2025 $47K LangChain A2A loop, the April 2026 PocketOS DB wipe,
and a weekend $4.2K LangGraph burn. Same shape every time: no per-run budget
that lives outside the model's context. burnstop is that primitive.
"""
__version__ = "0.1.0"

from .proxy import Receipt, BudgetExceeded
from .pricing import estimate_cost, decompose_cache
from .integrations import install, uninstall

__all__ = [
    "Receipt", "BudgetExceeded",
    "estimate_cost", "decompose_cache",
    "install", "uninstall",
]
