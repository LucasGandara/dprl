# Implementation Plan: Cleanup Assets Folder After Metrics Visualization

**Branch**: `003-cleanup-assets-folder` | **Date**: 2026-01-26 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-cleanup-assets-folder/spec.md`

## Summary

Implement automatic cleanup of the `assets` folder created by `MetricsPlotter.add_video_from_frames()` when the Dash visualization session ends. The cleanup must handle edge cases gracefully (missing folder, files in use) and provide clear user feedback using Rich console output when cleanup fails, including the exact path and manual deletion instructions.

## Technical Context

**Language/Version**: Python 3.13 (per constitution)
**Primary Dependencies**: Dash 3.3.0, Rich 14.2.0, shutil (stdlib)
**Storage**: Local filesystem (assets folder in caller's directory)
**Testing**: pytest (per constitution)
**Target Platform**: Linux/macOS/Windows (cross-platform)
**Project Type**: Single project (Python library)
**Performance Goals**: Cleanup within 5 seconds for 1-10 video files
**Constraints**: Must not crash on cleanup failures; must provide actionable user feedback
**Scale/Scope**: Single folder with typically 1-10 MP4 files

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. User-First API Design | ✅ Pass | No API changes; cleanup is automatic. Error messages are actionable (show path, give instructions). |
| II. Gymnasium Compatibility | ✅ N/A | Feature does not involve environments or algorithms. |
| III. Reproducibility | ✅ N/A | Feature does not affect experiment reproducibility (cleanup happens post-visualization). |
| IV. Testing & Validation | ✅ Pass | Unit tests will be added for cleanup logic (per FR requirements). |
| V. Simplicity & YAGNI | ✅ Pass | Using stdlib `shutil.rmtree`; Rich already a dependency; no new abstractions. |

**Technology Stack Compliance**:
- ✅ Python ≥3.13
- ✅ Rich ≥14.0.0 (already in project)
- ✅ pytest for testing

**Development Standards Compliance**:
- ✅ Source code in `src/dprl/`
- ✅ Tests in `tests/`

## Project Structure

### Documentation (this feature)

```text
specs/003-cleanup-assets-folder/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
src/dprl/
└── utils/
    └── metrics_plotter.py    # Primary file to modify

tests/
└── unit/
    └── test_metrics_plotter_cleanup.py    # New test file
```

**Structure Decision**: Single project structure per constitution. Changes are localized to the existing `metrics_plotter.py` utility file with new unit tests in `tests/unit/`.

## Complexity Tracking

No constitution violations. Simple implementation using:
- `shutil.rmtree()` for recursive folder deletion (stdlib, per Principle V)
- `atexit` module for shutdown hook registration (stdlib)
- `signal` module for keyboard interrupt handling (stdlib)
- Rich `Console` for styled error messages (existing dependency)
