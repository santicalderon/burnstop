# Changelog

## [0.1.0] — 2026-06-07

### Added
- `Receipt` class with budget envelope, wall-clock ceiling, and token ceiling
- `install()` monkey-patch for the Anthropic SDK
- CLI: `burnstop demo`, `burnstop status`
- `cache_creation` vs `cache_read` decomposition via `decompose_cache()` and `estimate_cost()`
- Pricing model for claude-3-5-sonnet, claude-3-5-haiku, claude-3-opus, claude-opus-4
- pytest suite (gate fires + cache decomposition)
- GitHub Actions CI on Python 3.10/3.11/3.12

### Documentation
- README with four documented runaway incidents
- AGENT_CARD.md
- LICENSE (MIT)
