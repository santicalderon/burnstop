"""Token cost estimation + cache_creation vs cache_read decomposition.

Public Anthropic pricing as of 2026-06 (verify before relying on this for billing):
  claude-3-5-sonnet:  input $3 / cache_creation $3.75 / cache_read $0.30 / output $15  per 1M tokens
  claude-3-5-haiku:   input $0.80 / cache_creation $1 / cache_read $0.08 / output $4   per 1M
  claude-3-opus:      input $15 / cache_creation $18.75 / cache_read $1.50 / output $75 per 1M
  claude-opus-4:      input $15 / cache_creation $18.75 / cache_read $1.50 / output $75 per 1M

The decomposition is the GH#46829/#53262 friction point: response headers don't
expose cache_creation vs cache_read separately, so engineers can't diagnose
silent cache miss cost spikes. This module exposes it.
"""
from __future__ import annotations
from typing import Optional

PRICING_PER_M = {
    "claude-3-5-sonnet": {"input": 3.0,  "cache_create": 3.75,  "cache_read": 0.30, "output": 15.0},
    "claude-3-5-haiku":  {"input": 0.80, "cache_create": 1.0,   "cache_read": 0.08, "output": 4.0},
    "claude-3-opus":     {"input": 15.0, "cache_create": 18.75, "cache_read": 1.50, "output": 75.0},
    "claude-opus-4":     {"input": 15.0, "cache_create": 18.75, "cache_read": 1.50, "output": 75.0},
    "claude-sonnet-4":   {"input": 3.0,  "cache_create": 3.75,  "cache_read": 0.30, "output": 15.0},
}

def _resolve(model: str) -> dict:
    for k, v in PRICING_PER_M.items():
        if k in model.lower():
            return v
    return PRICING_PER_M["claude-3-5-sonnet"]

def estimate_cost(
    model: str,
    *,
    input_tokens: int = 0,
    cache_creation_tokens: int = 0,
    cache_read_tokens: int = 0,
    output_tokens_max: int = 0,
) -> float:
    """Projected $ cost for this request. Uses max output tokens for upper-bound."""
    p = _resolve(model)
    return (
        input_tokens          * p["input"]        / 1_000_000
      + cache_creation_tokens * p["cache_create"] / 1_000_000
      + cache_read_tokens     * p["cache_read"]   / 1_000_000
      + output_tokens_max     * p["output"]       / 1_000_000
    )

def decompose_cache(headers: dict, body: dict) -> dict:
    """Extract cache_creation vs cache_read from Anthropic-style request/response.

    Anthropic returns usage with cache_creation_input_tokens / cache_read_input_tokens
    in the response body (when prompt caching is enabled). This pulls them.
    """
    usage = (body.get("usage") or {}) if isinstance(body, dict) else {}
    return {
        "input": int(usage.get("input_tokens", 0)),
        "cache_creation": int(usage.get("cache_creation_input_tokens", 0)),
        "cache_read": int(usage.get("cache_read_input_tokens", 0)),
        "output": int(usage.get("output_tokens", 0)),
    }
