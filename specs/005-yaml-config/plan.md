# Implementation Plan: YAML Config Integration with Experiments

**Branch**: `005-yaml-config` | **Date**: 2026-01-27 | **Spec**: spec.md
**Input**: User clarification - "Config implemented but not used in experiment"

## Summary

The YAML configuration system (loading, validation, template generation) is fully
implemented and functional. The `--config` option works via Click's `default_map`
mechanism. However, the configuration values are not being **saved alongside
experiment results** for reproducibility. This plan addresses saving the active
configuration with each experiment run.

## Technical Context

**Language/Version**: Python ≥3.13
**Primary Dependencies**: Click ≥8.0.0, PyYAML ≥6.0, Pydantic, PyTorch
**Storage**: Local filesystem (`runs/` directory)
**Testing**: pytest
**Target Platform**: Linux/macOS (CLI tool)
**Project Type**: Single project (src/dprl layout)
**Performance Goals**: N/A (config serialization is not performance-critical)
**Constraints**: Must maintain backward compatibility with existing saved experiments
**Scale/Scope**: Single algorithm (VPG) initially, extensible to other algorithms

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. User-First API Design | ✅ PASS | Config saving is transparent to user |
| II. Gymnasium Compatibility | ✅ N/A | No environment changes |
| III. Reproducibility | ✅ PASS | **This feature directly supports this principle** |
| IV. Testing & Validation | ✅ PASS | Will add unit tests for config saving |
| V. Simplicity & YAGNI | ✅ PASS | Minimal change to existing code |

**Gate Result**: PASS - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/005-yaml-config/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (via /speckit.tasks)
```

### Source Code (repository root)

```text
src/dprl/
├── algorithms/
│   └── vpg/
│       ├── __init__.py
│       └── config.py          # VPGConfig (exists)
└── utils/
    ├── __init__.py
    ├── config.py              # BaseConfig (exists)
    └── experiment_logger.py   # save_experiment_details (modify)

examples/
└── vpg_cartpole.py            # (modify to pass config)

tests/
└── unit/
    ├── test_base_config.py    # (exists)
    └── test_vpg_config.py     # (exists)
```

**Structure Decision**: Single project layout. Modifications to existing files only.

## Complexity Tracking

> No violations - implementation is minimal and follows existing patterns.

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| Config storage format | YAML | Human-readable, matches input format |
| Storage location | Same folder as experiment | Co-located for easy reference |
| Backward compatibility | Optional config field | Existing experiments without config still load |

---

## Post-Design Constitution Re-Check

*Re-evaluated after Phase 1 design completion.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. User-First API Design | ✅ PASS | Optional param maintains simple API; config saving is automatic |
| II. Gymnasium Compatibility | ✅ N/A | No environment interface changes |
| III. Reproducibility | ✅ PASS | Config saved as YAML (Constitution: "serializable YAML/JSON") |
| IV. Testing & Validation | ✅ PASS | Tests defined in data-model.md for to_yaml(), load_config |
| V. Simplicity & YAGNI | ✅ PASS | Minimal additions: 1 method, 1 function, 1 optional param |

**Final Gate Result**: PASS - Ready for task generation

## Implementation Summary

**Files to Modify**:
1. `src/dprl/utils/config.py` - Add `to_yaml()` method to BaseConfig
2. `src/dprl/utils/experiment_logger.py` - Add `config` param and save logic
3. `src/dprl/utils/__init__.py` - Export `load_config_from_experiment`
4. `examples/vpg_cartpole.py` - Construct and pass VPGConfig to save
5. `examples/vpg_flappy_bird.py` - Same pattern

**Files to Create**:
- None (all modifications to existing files)

**Tests to Add**:
1. `test_base_config.py` - Test `to_yaml()` method
2. `test_experiment_logger.py` - Test config saving and loading
