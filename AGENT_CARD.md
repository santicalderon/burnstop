# Agent Card — burnstop

This package is signed by the Samurai substrate.

- **DID:** `did:web:mcp.mi-kernel2026.xyz`
- **Agent Card endpoint:** https://mcp.mi-kernel2026.xyz/.well-known/agent-card.json
- **Public services exposed via x402:** `cache.get`, `causal.recall`, `consensus.check`
- **Maintainer pings:** open an issue OR comment on the package.
- **Disclosed incidents this package is calibrated against:**
  - LangChain A2A $47K loop (Nov 2025)
  - PocketOS Cursor+Claude DB wipe (Apr 2026)
  - LangGraph weekend $4.2K refactor (2026)
  - Replit AI `DROP DATABASE` (Jul 2025)

## How burnstop fits in agentic infrastructure

burnstop is the *pre-flight gate*. It does NOT replace:
- token telemetry (Helicone / Langfuse / Langsmith)
- runtime guardrails (Lakera / Robust Intelligence)
- post-hoc evals (Braintrust / Anthropic console)

It is the missing primitive that lives between the budget envelope and the model: a hard-stop the model cannot bypass because it runs in *your* process, not the model's context.
