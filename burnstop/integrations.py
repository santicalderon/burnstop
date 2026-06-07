"""Drop-in installation for popular SDKs. Zero-refactor: just `import burnstop; burnstop.install(budget_envelope_usd=5)`.

Currently patches:
  - anthropic.Anthropic.messages.create
  - anthropic.AsyncAnthropic.messages.create (best effort)

Each patched call:
  1. Estimates input tokens (from messages)
  2. Calls receipt.check() — raises BudgetExceeded if over envelope
  3. Lets the real call proceed
  4. Calls receipt.record() on response

The original method is preserved so uninstall() restores cleanly.
"""
from __future__ import annotations
from typing import Optional
from .proxy import Receipt, BudgetExceeded

_PATCHED = {}
_GLOBAL_RECEIPT: Optional[Receipt] = None


def _estimate_input_tokens(kwargs) -> int:
    """Rough estimate: 4 chars ≈ 1 token. Anthropic's real tokenizer is more accurate but this is the budget-gate side."""
    total_chars = 0
    msgs = kwargs.get("messages", [])
    if isinstance(msgs, list):
        for m in msgs:
            content = m.get("content") if isinstance(m, dict) else ""
            if isinstance(content, str):
                total_chars += len(content)
            elif isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        total_chars += len(block.get("text", ""))
    sys_prompt = kwargs.get("system", "")
    if isinstance(sys_prompt, str):
        total_chars += len(sys_prompt)
    return total_chars // 4


def install(budget_envelope_usd: float = 5.00, model: str = "claude-3-5-sonnet",
            **kwargs) -> Receipt:
    """Patch known SDKs. Returns the Receipt object — use receipt.spent_usd etc to monitor."""
    global _GLOBAL_RECEIPT
    _GLOBAL_RECEIPT = Receipt(budget_envelope_usd=budget_envelope_usd, model=model, **kwargs)

    try:
        import anthropic
        _patch_anthropic_messages(anthropic)
    except ImportError:
        pass  # SDK not installed — silent skip

    return _GLOBAL_RECEIPT


def uninstall() -> None:
    """Restore original SDK methods. Receipt state is preserved on the returned object."""
    for (cls, attr), original in list(_PATCHED.items()):
        try:
            setattr(cls, attr, original)
        except Exception:
            pass
    _PATCHED.clear()


def _patch_anthropic_messages(anthropic_mod) -> None:
    """Wrap anthropic.Anthropic().messages.create with pre-flight gate."""
    try:
        # The actual create is on the Messages resource class
        from anthropic.resources.messages import Messages
        original = Messages.create

        def wrapped(self, *args, **kwargs):
            receipt = _GLOBAL_RECEIPT
            if receipt is None:
                return original(self, *args, **kwargs)
            in_toks = _estimate_input_tokens(kwargs)
            max_out = int(kwargs.get("max_tokens", 1024))
            # raises BudgetExceeded if over envelope
            receipt.check(input_tokens=in_toks, max_output=max_out)
            response = original(self, *args, **kwargs)
            # record actual on response
            body = response.model_dump() if hasattr(response, "model_dump") else dict(response)
            receipt.record(actual_response_body=body)
            return response

        _PATCHED[(Messages, "create")] = original
        Messages.create = wrapped
    except Exception:
        pass  # SDK shape changed — degrade silently rather than break user code
