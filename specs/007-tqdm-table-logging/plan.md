# Implementation Plan: TQDM and Table Logging for Training

**Branch**: `007-tqdm-table-logging` | **Date**: 2026-01-28 | **Spec**: spec.md
**Input**: Feature specification from `specs/007-tqdm-table-logging/spec.md`

## Summary

Add TQDM progress bars and Rich table logging to training scripts. Progress
bars are enabled by default, showing epoch progress with loss and max reward.
Users can optionally enable periodic table logging every N epochs for detailed
metrics. All logging options are configurable via CLI arguments or YAML config.

## Technical Context

**Language/Version**: Python ≥3.13
**Primary Dependencies**: tqdm ≥4.66.0, Rich ≥14.0.0 (existing), Click ≥8.0.0
**Storage**: N/A
**Testing**: pytest ≥7.0.0
**Target Platform**: Linux/macOS/Windows (terminal)
**Project Type**: Single Python package
**Performance Goals**: Minimal overhead (<1ms per epoch for logging)
**Constraints**: Line length <80 chars, no unnecessary dependencies
**Scale/Scope**: 2 training scripts, 1 new utility module

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. User-First API | PASS | Default progress bar requires no config |
| II. Gymnasium Compatibility | N/A | Logging feature, not env/algo |
| III. Reproducibility | PASS | Logging doesn't affect training |
| IV. Testing & Validation | PASS | Unit tests planned for logger |
| V. Simplicity & YAGNI | PASS | Minimal scope, requested feature |

**Technology Stack Compliance**:
- Python ≥3.13: PASS
- Rich ≥14.0.0: PASS (already in project)
- tqdm: NEW dependency required (see Complexity Tracking)
- Click ≥8.0.0: PASS (already in project)

## Project Structure

### Documentation (this feature)

```text
specs/007-tqdm-table-logging/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   ├── training_logger.py
│   └── config_extension.py
└── tasks.md             # Phase 2 output (created by /speckit.tasks)
```

### Source Code (repository root)

```text
src/dprl/
├── algorithms/
│   └── vpg/
│       └── config.py          # MODIFY: Add logging fields
├── utils/
│   ├── __init__.py            # MODIFY: Export TrainingLogger
│   └── training_logger.py     # NEW: TrainingLogger class

examples/
├── vpg_cartpole.py            # MODIFY: Use TrainingLogger
└── vpg_flappy_bird.py         # MODIFY: Use TrainingLogger

tests/
└── unit/
    └── test_training_logger.py  # NEW: Unit tests
```

**Structure Decision**: Single project structure (existing). New utility module
`training_logger.py` follows the pattern of `experiment_logger.py`.

## Implementation Phases

### Phase 1: Core Logger Module

**Files**:
- `src/dprl/utils/training_logger.py` (NEW)
- `src/dprl/utils/__init__.py` (MODIFY)

**Tasks**:
1. Create `TrainingLogger` class with `__init__`, `update`, `close`
2. Implement tqdm.rich progress bar wrapper
3. Implement Rich Table logging method
4. Add context manager support (`__enter__`, `__exit__`)
5. Export from `__init__.py`

### Phase 2: Configuration Extension

**Files**:
- `src/dprl/algorithms/vpg/config.py` (MODIFY)

**Tasks**:
1. Add `progress_bar` field (default=True)
2. Add `table_log_freq` field (default=0)
3. Verify `generate_template` includes new fields

### Phase 3: Training Script Integration

**Files**:
- `examples/vpg_cartpole.py` (MODIFY)
- `examples/vpg_flappy_bird.py` (MODIFY)

**Tasks**:
1. Add CLI options for `--progress-bar/--no-progress-bar`
2. Add CLI option for `--table-log-freq`
3. Replace `print()` statements with TrainingLogger
4. Add context manager usage pattern

### Phase 4: Testing

**Files**:
- `tests/unit/test_training_logger.py` (NEW)

**Tasks**:
1. Test TrainingLogger initialization
2. Test progress bar enable/disable
3. Test table logging at correct intervals
4. Test context manager behavior

### Phase 5: Dependency Update

**Files**:
- `pyproject.toml` (MODIFY)

**Tasks**:
1. Add `tqdm>=4.66.0` to dependencies
2. Run `uv sync` to update lock file

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected |
|-----------|------------|------------------------------|
| New dependency (tqdm) | Industry-standard progress bars with Rich integration | Custom Rich Progress requires more code and reinvents tqdm; plain print statements don't show progress bars |

## Dependencies

```
Phase 5 (deps) → Phase 1 (logger) → Phase 2 (config) → Phase 3 (scripts)
                                                            ↓
                                                    Phase 4 (tests)
```

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| tqdm/Rich conflict | Use tqdm.rich for native integration |
| Non-TTY environments | tqdm auto-disables; no special handling |
| Breaking existing scripts | Additive changes only, defaults match old behavior |

## Acceptance Criteria

1. Running `vpg_cartpole.py` shows TQDM progress bar by default
2. `--no-progress-bar` disables progress bar
3. `--table-log-freq 10` logs table every 10 epochs
4. YAML config supports all logging options
5. `--generate-config` includes logging options
6. All tests pass
7. Lines comply with 80-char limit
