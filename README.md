# burnstop

> **Stop AI agents from burning your money.** Pre-flight budget gate. Hard-stop before token-1. ~$0.001 per check.

I built this after my own autonomous platform hit runaway LLM costs — loops that looked like progress but were burning through budget with zero output. The model causing the loop is the same one you'd ask to self-throttle. That doesn't work. burnstop is the primitive that lives *outside* the model's context.

[![test](https://github.com/santicalderon/burnstop/actions/workflows/test.yml/badge.svg)](https://github.com/santicalderon/burnstop/actions/workflows/test.yml)
[![MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

```bash
# Via GitHub (available now):
pip install git+https://github.com/santicalderon/burnstop

# Via PyPI (coming soon):
# pip install burnstop
```

```python
import burnstop
burnstop.install(budget_envelope_usd=5.00, model="claude-3-5-sonnet")

# your existing code, unchanged:
from anthropic import Anthropic
client = Anthropic()
client.messages.create(...)   # burnstop intercepts, raises BudgetExceeded if over envelope
```

That's the entire integration. Drop-in. No refactor.

---

## Why this exists — four real incidents

| Date | Stack | Loss | Source |
|---|---|---|---|
| Jul 2025 | Replit AI | prod DB + 1,206 records | [Fortune](https://fortune.com/2025/07/23/ai-coding-tool-replit-wiped-database-called-it-a-catastrophic-failure/) |
| Nov 2025 | LangChain + A2A (11-day loop) | **$47,000** | [Medium](https://medium.com/@theabhishek.040/our-47-000-ai-agent-production-lesson-the-reality-of-a2a-and-mcp-60c2c000d904) |
| 2026 | LangGraph weekend autonomous refactor | $4,200 | [DEV.to](https://dev.to/sapph1re/how-to-stop-ai-agent-cost-blowups-before-they-happen-1ehp) |
| Apr 2026 | Cursor + Claude | PocketOS DB wiped in 9s, 30h outage | [OECD.AI](https://oecd.ai/en/incidents/2026-04-27-6153) |

**Same shape every time:** no per-run budget that lives *outside* the model's context. The model that loops is the same one you would ask to self-throttle. burnstop is the primitive that fixes it.

## What burnstop does

Before each tool call:
1. Estimates the projected $ cost (cache_creation + cache_read + output decomposition the response headers don't expose — see [anthropic-cookbook#46829](https://github.com/anthropics/anthropic-cookbook/issues/46829))
2. Returns `OK` if within envelope, raises `BudgetExceeded` if not
3. After the call lands, records actual cost and updates running total

```
$ burnstop demo --budget 0.30
[burnstop] OK call=1 proj=$0.0442 left=$0.3000
[burnstop] CALL#1 actual=$0.0435 cache_read=0% cumul=$0.0435
[burnstop] OK call=2 proj=$0.0442 left=$0.2565
...
[burnstop] 402 BUDGET_EXCEEDED: would_spend=$0.0442 envelope_left=$0.0390
```


## Framework adapters

burnstop ships as a core library + drop-in adapters for every major agent framework:

| Adapter | Install | Framework |
|---|---|---|
| [burnstop-langchain](https://github.com/santicalderon/burnstop-langchain) | `pip install burnstop-langchain` | LangChain callbacks |
| [burnstop-langgraph](https://github.com/santicalderon/burnstop-langgraph) | `pip install burnstop-langgraph` | LangGraph nodes |
| [burnstop-autogen](https://github.com/santicalderon/burnstop-autogen) | `pip install burnstop-autogen` | AutoGen agents |
| [burnstop-crewai](https://github.com/santicalderon/burnstop-crewai) | `pip install burnstop-crewai` | CrewAI crews |

Each adapter wraps the same `Receipt` primitive — one budget envelope, same `BudgetExceeded` exception, works across frameworks.

## Manual usage (without monkey-patch)

```python
from burnstop import Receipt, BudgetExceeded

r = Receipt(budget_envelope_usd=5.00, model="claude-3-5-sonnet")
try:
    r.check(input_tokens=4500, max_output=2048)
    # ... your call lands ...
    r.record(actual_response_body=response)
except BudgetExceeded as e:
    # graceful stop, don't retry
    log.warning(f"agent stopped at envelope: {e}")
```

## Maintainer

- DID: `did:web:mcp.mi-kernel2026.xyz`
- Agent Card: https://mcp.mi-kernel2026.xyz/.well-known/agent-card.json
- Issues / PRs welcome; responses within 24h on weekdays

See [AGENT_CARD.md](./AGENT_CARD.md) for the substrate this is built on.

## Ecosystem

- [burnstop-langchain](https://github.com/santicalderon/burnstop-langchain) — LangChain callback adapter
- [burnstop-langgraph](https://github.com/santicalderon/burnstop-langgraph) — LangGraph node wrapper + shared middleware
- [burnstop-crewai](https://github.com/santicalderon/burnstop-crewai) — per-agent / per-crew budget gate

## License

MIT — see [LICENSE](./LICENSE).

---

## Built on kernel

burnstop is part of the [kernel](https://github.com/santicalderon/kernel) autonomous AI Business substrate.

- 🌐 **kernel** → [kernel.mi-kernel2026.xyz](https://kernel.mi-kernel2026.xyz/)
- 📋 **AI Business Audit** $499 → [/audit/](https://kernel.mi-kernel2026.xyz/audit/)
- 🔁 **InvoiceChaser** $14.50/mo → [/invoicechaser/](https://kernel.mi-kernel2026.xyz/invoicechaser/)
- 📰 **Reviews + newsletter** → [/reviews/](https://kernel.mi-kernel2026.xyz/reviews/)
