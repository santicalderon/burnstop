# Security Policy

## Supported versions

| Version | Supported |
|---|---|
| 0.1.x | ✅ |
| < 0.1 | ❌ |

## Reporting a vulnerability

Open a private security advisory at https://github.com/santicalderon/burnstop/security/advisories/new — or email the address in [AGENT_CARD.md](./AGENT_CARD.md).

Please **do not open a public issue** for security reports.

We aim to acknowledge within 48h on weekdays.

## Scope

- Bypass of the pre-flight gate (e.g., a request that should have been blocked got through)
- Cost-estimation errors that lead to incorrect envelope decisions
- Information leakage in the ledger or stderr receipts
- Anything in the monkey-patch logic that could break user code in unexpected ways

## Out of scope

- Issues in upstream Anthropic SDK behavior (file with Anthropic)
- Issues in framework adapters specific to LangChain/LangGraph/CrewAI/AutoGen (file in respective repos)
- General OSS supply-chain concerns without a concrete vector (we keep dependencies minimal for this reason)
