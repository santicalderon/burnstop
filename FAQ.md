# FAQ

## Why is this not just `max_iterations`?

`max_iterations` caps loop turn count. burnstop caps **USD spent**. A single iteration can cost $50; 100 cheap iterations can cost less than one expensive one. The two compose — use both as defense-in-depth.

## How is this different from Helicone / Langfuse / Langsmith?

| Tool | What it does | When it fires |
|---|---|---|
| Helicone / Langfuse / Langsmith | telemetry, evaluation, observability | AFTER the call |
| burnstop | pre-flight budget gate | BEFORE the call |

burnstop is the *first* primitive in the call path; the others are the *last*. They are complementary, not competitive.

## What about `temperature=0` agents that should be deterministic?

Still applicable — even deterministic agents hit cache layers, retry on transient errors, and trigger sub-calls. The four documented runaway incidents all involved code that "should have terminated."

## Why HMAC and not Ed25519 for `agentic-receipts`?

HMAC keeps the package stdlib-only (zero deps). Ed25519 is on the roadmap as an optional `[crypto]` extra. The signing surface is intentionally narrow so swapping is one function.

## Can I use this with non-Anthropic SDKs?

Yes — the `Receipt` class is provider-agnostic. The `install()` monkey-patch currently wraps `anthropic.resources.messages.Messages.create`; PRs welcome for OpenAI / Google / Cohere SDK adapters. The framework-specific adapters ([langchain](https://github.com/santicalderon/burnstop-langchain), [langgraph](https://github.com/santicalderon/burnstop-langgraph), [crewai](https://github.com/santicalderon/burnstop-crewai), [autogen](https://github.com/santicalderon/burnstop-autogen)) work with whatever provider those frameworks call.

## What's on the roadmap?

See [ROADMAP.md](./ROADMAP.md).

## Where's the pricing for the hosted version?

We don't have a hosted version yet. The OSS package is free. The "90 days of Pro free for a 15-min call" mentioned in [issue #1](https://github.com/santicalderon/burnstop/issues/1) is a research-sprint promise that will get a real pricing page once we have 10+ paying customers (per the axiom we are testing).

## I had a runaway. How do I claim the 90 days?

Comment on [issue #1](https://github.com/santicalderon/burnstop/issues/1) with the incident shape (anonymized fine). First 20 replies. No automated funnel — every reply gets a personal review.
