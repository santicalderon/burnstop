# Comparison

How burnstop fits alongside other agentic-infrastructure tools. Honest take, not marketing.

| Tool | Layer | Fires | License | Best at |
|---|---|---|---|---|
| **burnstop** | pre-call | BEFORE token-1 | MIT | Hard-stop $-envelope outside model context |
| [Helicone](https://github.com/Helicone/helicone) | post-call telemetry | AFTER call lands | Apache-2.0 | Per-call observability + dashboards |
| [Langfuse](https://github.com/langfuse/langfuse) | trace + eval | AFTER | MIT | Multi-step trace storage, eval framework |
| [Langsmith](https://docs.langchain.com/langsmith/) | trace + eval | AFTER | proprietary | Eval bank + dataset management |
| [Lakera Guard](https://www.lakera.ai/) | content guard | DURING (per-prompt) | proprietary | Prompt-injection / PII detection |
| [Protect AI](https://protectai.com/) | model + supply-chain | scan | proprietary | Model vulnerability scanning |
| [Braintrust](https://www.braintrust.dev/) | eval + experiment | AFTER + offline | proprietary | Comparing model variants on golden datasets |
| LangChain `max_iterations` | loop counter | DURING | MIT | Stop runaway turn count |
| LangChain `max_execution_time` | wall-clock | DURING | MIT | Stop runaway wall time |
| `agentic-receipts` (this org) | post-action attestation | AFTER, signed | MIT | SOC2/ISO42001 audit trail |

## What's unique about burnstop

- **Fires before token-1.** Most tools fire after the call lands (telemetry/eval). burnstop's hard-stop runs in your process so the model cannot bypass it.
- **Exposes cache_creation vs cache_read.** Anthropic response headers don't surface this separately — see [anthropic-sdk-python#1547](https://github.com/anthropics/anthropic-sdk-python/issues/1547). burnstop computes the decomposition explicitly.
- **Same pricing primitive across SDK + LangChain + LangGraph + CrewAI + AutoGen.** Adapter packages share one `Receipt` class.
- **Stdlib-only core.** No `cryptography`, no `numpy`, no platform shims.

## What burnstop does NOT do

- Not a telemetry replacement. Use Helicone/Langfuse/Langsmith for post-call analysis.
- Not a content moderator. Use Lakera/ProtectAI for prompt-injection / PII.
- Not an eval framework. Use Braintrust/Langsmith for offline eval.

## When to NOT use burnstop

- If you're not running anything more expensive than chat (no agents, no tools, no auto-loops), the gate adds 1 line of code for ~0 marginal value. We use it ourselves; we don't think every chat app needs it.
- If you've already wrapped the SDK with your own cost-projection layer that hard-stops, burnstop duplicates that.
