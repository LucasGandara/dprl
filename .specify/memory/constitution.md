<!--
SYNC IMPACT REPORT
==================
Version change: 0.0.0 → 1.0.0
Bump rationale: MAJOR - Initial constitution creation from template

Modified principles:
- [PRINCIPLE_1_NAME] → I. User-First API Design
- [PRINCIPLE_2_NAME] → II. Gymnasium Compatibility
- [PRINCIPLE_3_NAME] → III. Reproducibility
- [PRINCIPLE_4_NAME] → IV. Testing & Validation
- [PRINCIPLE_5_NAME] → V. Simplicity & YAGNI

Added sections:
- Core Principles (5 principles defined)
- Technology Stack
- Development Standards
- Governance

Removed sections:
- [SECTION_2_NAME] placeholder → replaced with Technology Stack
- [SECTION_3_NAME] placeholder → replaced with Development Standards

Templates requiring updates:
- ✅ plan-template.md - No changes needed (Constitution Check section already generic)
- ✅ spec-template.md - No changes needed (requirements structure compatible)
- ✅ tasks-template.md - No changes needed (task structure compatible)

Follow-up TODOs: None
-->

# DPRL Constitution

## Core Principles

### I. User-First API Design

All public interfaces (classes, functions, types) MUST prioritize ease of use for researchers and practitioners:

- Utilities, algorithms, and plotters MUST have clear, self-documenting APIs
- Default parameters MUST work for common use cases without configuration
- Error messages MUST be actionable and point to solutions
- Breaking changes to public APIs MUST be documented in release notes

**Rationale**: RL researchers should spend time on experiments, not debugging library internals.

### II. Gymnasium Compatibility

All environments and algorithms MUST follow Gymnasium standards:

- Custom environments MUST implement the `gymnasium.Env` interface (`reset()`, `step()`, `render()`)
- Algorithms MUST accept any Gymnasium-compatible environment
- Observation and action spaces MUST use Gymnasium's `Space` types
- Environment wrappers MUST be composable with standard Gymnasium wrappers

**Rationale**: Gymnasium is the de facto standard for RL environments; compatibility ensures interoperability.

### III. Reproducibility

All experiments MUST be reproducible:

- Random seeds MUST be configurable at all stochasticity points
- Model checkpoints MUST include all state needed for exact resumption
- Training configurations MUST be serializable (YAML/JSON)
- Results MUST be deterministic given the same seed and configuration

**Rationale**: Scientific validity requires reproducible results.

### IV. Testing & Validation

Code correctness MUST be verified through testing:

- New features MUST include unit tests for core logic
- Algorithm implementations SHOULD include sanity checks (e.g., CartPole convergence)
- Bug fixes MUST include regression tests
- Tests MUST run via `pytest` and pass in CI

**Rationale**: RL algorithms have subtle failure modes; tests catch regressions early.

### V. Simplicity & YAGNI

Prefer simple, focused implementations:

- Each module MUST have a single clear purpose
- Avoid premature abstraction; extract patterns only after 3+ concrete uses
- Prefer stdlib solutions over external dependencies when equivalent
- Features MUST be requested before implementation (no speculative features)

**Rationale**: Complexity compounds; simpler code is easier to understand, debug, and maintain.

## Technology Stack

**Required technologies for all DPRL development**:

| Component | Technology | Version |
|-----------|------------|---------|
| Language | Python | ≥3.13 |
| Package Manager | uv | latest |
| ML Framework | PyTorch | ≥2.0.0 |
| RL Environments | Gymnasium | ≥0.29.0 |
| CLI | Click | ≥8.0.0 |
| Visualization | Dash, Plotly | latest |
| Console Output | Rich | ≥14.0.0 |
| Testing | pytest | ≥7.0.0 |
| Linting | ruff, black, mypy | latest |

**Dependency policy**: External dependencies MUST provide significant value over stdlib alternatives. Prefer widely-used, well-maintained packages.

## Development Standards

**Code organization**:

- Source code in `src/dprl/`
- Tests in `tests/`
- Examples in `examples/`
- Experiment outputs in `runs/` (gitignored)

**Quality gates for PRs**:

- All tests pass (`uv run pytest tests/`)
- Linting passes (`uv run ruff check src/`)
- Type checking passes (`uv run mypy src/`)
- New public APIs documented

**Commit conventions**:

- Use conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`
- Reference issue numbers when applicable

## Governance

This constitution defines non-negotiable standards for DPRL development:

- Constitution supersedes conflicting practices in other documentation
- Amendments require explicit documentation and version increment
- All PRs MUST comply; violations require explicit justification in Complexity Tracking
- Use CLAUDE.md for runtime development guidance specific to AI-assisted development

**Amendment procedure**:

1. Propose change with rationale
2. Update constitution with version increment
3. Update dependent templates if needed
4. Document in SYNC IMPACT REPORT

**Version**: 1.0.0 | **Ratified**: 2026-01-26 | **Last Amended**: 2026-01-26
