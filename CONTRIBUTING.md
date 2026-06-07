# Contributing to burnstop

Thanks for considering a contribution. The project is small on purpose — most PRs are welcome.

## Quick start

```bash
git clone https://github.com/santicalderon/burnstop.git
cd burnstop
pip install -e .
pytest
```

## What we accept happily

- New SDK adapters (OpenAI / Google / Cohere / Mistral)
- New framework adapters (Haystack / Semantic Kernel)
- Real bug reports with reproductions
- Pricing model updates when providers change rates
- Tests on platforms we don't cover

## What we'd discuss first

- Hosted dashboard / SaaS UI — open an issue first
- Adding mandatory dependencies — stdlib-only is a deliberate choice for the core
- Major API changes — semver matters once a user lands

## How we review

- Tests must pass
- Public API changes need a CHANGELOG entry
- PRs that close an issue should reference it (`Closes #N`)
- Maintainer response: within 48h on weekdays (we are an indie, please be patient on weekends)

## Code of conduct

Be kind. We are all here because someone burned through a budget once. See [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).
