"""Pre-flight budget gate. Hard-stop before token-1 if envelope exceeded.

The model that loops is the same one you would ask to self-throttle. The
budget must live outside its context. This module is that primitive.

Usage:
    from receipt_wrapper import Receipt, BudgetExceeded

    receipt = Receipt(budget_envelope_usd=5.00, model="claude-3-5-sonnet")

    # before each agent tool call:
    receipt.check(input_tokens=4500, max_output=2048)
    # raises BudgetExceeded if projected cost would push over envelope

    # after the call lands:
    receipt.record(actual_response_body=resp_dict)
    # prints one-line pre-flight receipt to stderr + appends to ledger
"""
from __future__ import annotations
import json, os, sys, time, hashlib
from dataclasses import dataclass, field
from typing import Optional, Any
from .pricing import estimate_cost, decompose_cache


class BudgetExceeded(Exception):
    """Raised when a pending request would push spend past the envelope."""
    def __init__(self, reason: str, would_spend: float, envelope_left: float, ceiling: str):
        self.would_spend = would_spend
        self.envelope_left = envelope_left
        self.ceiling = ceiling
        super().__init__(reason)


@dataclass
class Receipt:
    budget_envelope_usd: float = 5.00
    model: str = "claude-3-5-sonnet"
    wall_clock_ceiling_s: Optional[float] = None
    token_ceiling: Optional[int] = None
    project: str = ""
    started_at: float = field(default_factory=time.time)
    spent_usd: float = 0.0
    tokens_spent: int = 0
    calls: int = 0
    ledger_path: str = field(default_factory=lambda: os.environ.get(
        "RECEIPT_LEDGER", os.path.expanduser("~/.receipt_wrapper_ledger.jsonl")))

    def _now_s(self) -> float:
        return time.time() - self.started_at

    def check(self, *, input_tokens: int = 0, max_output: int = 0,
              cache_creation: int = 0, cache_read: int = 0) -> dict:
        """Pre-flight gate. Returns receipt dict or raises BudgetExceeded."""
        projected = estimate_cost(
            self.model,
            input_tokens=input_tokens,
            cache_creation_tokens=cache_creation,
            cache_read_tokens=cache_read,
            output_tokens_max=max_output,
        )
        envelope_left = self.budget_envelope_usd - self.spent_usd
        if projected > envelope_left:
            reason = (f"BUDGET_EXCEEDED: would_spend=${projected:.4f} "
                      f"envelope_left=${envelope_left:.4f}")
            print(f"[burnstop] 402 {reason}", file=sys.stderr)
            raise BudgetExceeded(reason, projected, envelope_left, "budget_envelope_usd")
        if self.wall_clock_ceiling_s and self._now_s() > self.wall_clock_ceiling_s:
            reason = f"WALL_CLOCK_EXCEEDED: elapsed={self._now_s():.1f}s ceiling={self.wall_clock_ceiling_s}s"
            print(f"[burnstop] 402 {reason}", file=sys.stderr)
            raise BudgetExceeded(reason, projected, envelope_left, "wall_clock_ceiling_s")
        if self.token_ceiling and (self.tokens_spent + input_tokens + max_output) > self.token_ceiling:
            reason = f"TOKEN_CEILING_EXCEEDED: total={self.tokens_spent+input_tokens+max_output} ceiling={self.token_ceiling}"
            print(f"[burnstop] 402 {reason}", file=sys.stderr)
            raise BudgetExceeded(reason, projected, envelope_left, "token_ceiling")
        # All checks pass — emit pre-flight receipt
        rec = {
            "ts": time.time(),
            "call": self.calls + 1,
            "model": self.model,
            "projected_usd": round(projected, 5),
            "envelope_left_usd": round(envelope_left, 5),
            "tokens": {"input": input_tokens, "max_output": max_output,
                       "cache_creation": cache_creation, "cache_read": cache_read},
            "elapsed_s": round(self._now_s(), 2),
            "ok": True,
        }
        print(f"[burnstop] OK call={rec['call']} proj=${projected:.4f} "
              f"left=${envelope_left:.4f}", file=sys.stderr)
        return rec

    def record(self, *, actual_response_body: dict, headers: Optional[dict] = None) -> dict:
        """After the actual call lands, record true cost + decomposition."""
        decomp = decompose_cache(headers or {}, actual_response_body)
        actual = estimate_cost(
            self.model,
            input_tokens=decomp["input"],
            cache_creation_tokens=decomp["cache_creation"],
            cache_read_tokens=decomp["cache_read"],
            output_tokens_max=decomp["output"],
        )
        self.spent_usd += actual
        self.tokens_spent += sum(decomp.values())
        self.calls += 1
        rec = {
            "ts": time.time(),
            "call": self.calls,
            "model": self.model,
            "actual_usd": round(actual, 5),
            "spent_total_usd": round(self.spent_usd, 5),
            "envelope_left_usd": round(self.budget_envelope_usd - self.spent_usd, 5),
            "decomposition": decomp,
            "project": self.project,
        }
        try:
            with open(self.ledger_path, "a") as f:
                f.write(json.dumps(rec) + "\n")
        except Exception as e:
            print(f"[burnstop] warn: could not write ledger: {e}", file=sys.stderr)
        cache_pct = (decomp["cache_read"] / max(1, decomp["input"] + decomp["cache_read"])) * 100
        print(f"[burnstop] CALL#{self.calls} actual=${actual:.4f} "
              f"cache_read={cache_pct:.0f}% cumul=${self.spent_usd:.4f}",
              file=sys.stderr)
        return rec


def intercept(model: str, budget_envelope_usd: float = 5.00, **kw) -> Receipt:
    """Convenience: one-liner construction for drop-in use."""
    return Receipt(budget_envelope_usd=budget_envelope_usd, model=model, **kw)
