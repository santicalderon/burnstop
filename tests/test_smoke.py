"""Smoke test — gate fires when budget exhausted, decomp parses real Anthropic body."""
from burnstop import Receipt, BudgetExceeded
from burnstop.pricing import decompose_cache, estimate_cost
import pytest


def test_gate_fires_on_exceeded():
    r = Receipt(budget_envelope_usd=0.05, model="claude-3-5-sonnet")
    # First call: 4500 in + 2048 max out = ~$0.044 → ok
    r.check(input_tokens=4500, max_output=2048)
    r.record(actual_response_body={"usage": {"input_tokens": 4500, "output_tokens": 2000}})
    # Second call should be over the envelope
    with pytest.raises(BudgetExceeded):
        r.check(input_tokens=4500, max_output=2048)


def test_cache_decomposition_parses():
    body = {"usage": {
        "input_tokens": 100,
        "cache_creation_input_tokens": 500,
        "cache_read_input_tokens": 2000,
        "output_tokens": 800,
    }}
    d = decompose_cache({}, body)
    assert d["cache_creation"] == 500
    assert d["cache_read"] == 2000
    cost = estimate_cost("claude-3-5-sonnet",
                        input_tokens=100, cache_creation_tokens=500,
                        cache_read_tokens=2000, output_tokens_max=800)
    assert cost > 0
