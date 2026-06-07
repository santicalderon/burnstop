# Roadmap

Honest. What's done, what's planned, what's parked.

## v0.1.0 (current — released 2026-06-07)
- [x] `Receipt` class with budget envelope + token + wall-clock ceilings
- [x] `install()` monkey-patch for `anthropic.Anthropic.messages.create`
- [x] CLI: `burnstop demo --budget X` + `burnstop status`
- [x] `cache_creation` / `cache_read` decomposition
- [x] Framework adapters: [langchain](https://github.com/santicalderon/burnstop-langchain), [langgraph](https://github.com/santicalderon/burnstop-langgraph), [crewai](https://github.com/santicalderon/burnstop-crewai), [autogen](https://github.com/santicalderon/burnstop-autogen)

## v0.2.0 (planned — next 30 days)
- [ ] PyPI publication via GitHub Actions OIDC trusted publishing
- [ ] OpenAI SDK adapter (`openai.OpenAI.chat.completions.create`)
- [ ] Google Gemini SDK adapter
- [ ] Cohere SDK adapter
- [ ] Async `install()` for `AsyncAnthropic`

## v0.3.0 (planned — next 90 days)
- [ ] OpenTelemetry exporter (receipt → OTLP)
- [ ] Webhook + Slack alerts on `BudgetExceeded`
- [ ] FastAPI middleware variant for proxy deployments
- [ ] Per-call "soft stop" mode (warns instead of raises)

## Parked / icebox
- Hosted SaaS dashboard — wait until 10+ paying users explicitly ask for it
- Auto-tuning envelopes from historical usage — premature without a corpus
- Multi-language ports (TS / Go / Rust) — Python first; community PRs welcome

## How priorities are decided
- Real incident shapes from [issue #1](https://github.com/santicalderon/burnstop/issues/1) replies move items up.
- Stars and forks on a specific adapter move that adapter's roadmap up.
