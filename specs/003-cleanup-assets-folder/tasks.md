# Tasks: Cleanup Assets Folder After Metrics Visualization

**Input**: Design documents from `/specs/003-cleanup-assets-folder/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, quickstart.md ✅

**Tests**: Unit tests required per Constitution Principle IV (Testing & Validation).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/dprl/`, `tests/` at repository root
- Primary file: `src/dprl/utils/metrics_plotter.py`
- Test file: `tests/unit/test_metrics_plotter_cleanup.py`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare test infrastructure for the feature

- [x] T001 Create tests/unit/ directory if it doesn't exist
- [x] T002 Create empty tests/unit/__init__.py file

**Checkpoint**: Test directory structure ready ✅

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core cleanup infrastructure that both user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Add `_assets_created: bool = False` instance attribute to MetricsPlotter.__init__() in src/dprl/utils/metrics_plotter.py
- [x] T004 Add `_cleanup_registered: bool = False` instance attribute to MetricsPlotter.__init__() in src/dprl/utils/metrics_plotter.py
- [x] T005 Add imports for atexit, signal, shutil, and Rich Console/Panel at top of src/dprl/utils/metrics_plotter.py

**Checkpoint**: Foundation ready - user story implementation can now begin ✅

---

## Phase 3: User Story 1 - Automatic Cleanup on Session End (Priority: P1) 🎯 MVP

**Goal**: Automatically remove the assets folder when MetricsPlotter visualization session ends normally

**Independent Test**: Run a visualization session with video, close the dashboard (Ctrl+C), verify assets folder no longer exists

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T006 [P] [US1] Create test file tests/unit/test_metrics_plotter_cleanup.py with test fixtures (temp directory, mock frames)
- [x] T007 [P] [US1] Write test_cleanup_removes_assets_folder_on_normal_exit() in tests/unit/test_metrics_plotter_cleanup.py
- [x] T008 [P] [US1] Write test_cleanup_handles_missing_folder_gracefully() in tests/unit/test_metrics_plotter_cleanup.py
- [x] T009 [P] [US1] Write test_assets_created_flag_set_when_video_added() in tests/unit/test_metrics_plotter_cleanup.py

### Implementation for User Story 1

- [x] T010 [US1] Set `self._assets_created = True` in add_video_from_frames() when folder is created in src/dprl/utils/metrics_plotter.py
- [x] T011 [US1] Implement `_cleanup_assets()` method that uses shutil.rmtree() to delete assets folder in src/dprl/utils/metrics_plotter.py
- [x] T012 [US1] Add check for `self._assets_created` before cleanup in _cleanup_assets() in src/dprl/utils/metrics_plotter.py
- [x] T013 [US1] Handle FileNotFoundError in _cleanup_assets() (folder doesn't exist) in src/dprl/utils/metrics_plotter.py
- [x] T014 [US1] Implement `_register_cleanup()` method that registers atexit handler in src/dprl/utils/metrics_plotter.py
- [x] T015 [US1] Call `_register_cleanup()` from add_video_from_frames() when first video is added in src/dprl/utils/metrics_plotter.py
- [x] T016 [US1] Add SIGINT signal handler in _register_cleanup() for Ctrl+C handling in src/dprl/utils/metrics_plotter.py
- [x] T017 [US1] Add SIGTERM signal handler in _register_cleanup() for kill command handling in src/dprl/utils/metrics_plotter.py
- [x] T018 [US1] Make cleanup idempotent (safe to call multiple times) using _cleanup_registered flag in src/dprl/utils/metrics_plotter.py

**Checkpoint**: User Story 1 complete - assets folder is automatically cleaned up on normal session end ✅

---

## Phase 4: User Story 2 - Graceful Cleanup on Errors (Priority: P2)

**Goal**: Handle cleanup failures gracefully with clear user feedback showing the exact path and manual deletion instructions

**Independent Test**: Simulate a cleanup failure (locked file), verify error message shows path and instructions

### Tests for User Story 2

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T019 [P] [US2] Write test_cleanup_failure_shows_error_message() in tests/unit/test_metrics_plotter_cleanup.py
- [x] T020 [P] [US2] Write test_error_message_contains_path() in tests/unit/test_metrics_plotter_cleanup.py
- [x] T021 [P] [US2] Write test_cleanup_does_not_crash_on_permission_error() in tests/unit/test_metrics_plotter_cleanup.py

### Implementation for User Story 2

- [x] T022 [US2] Create Rich Console instance as module-level variable in src/dprl/utils/metrics_plotter.py
- [x] T023 [US2] Implement `_display_cleanup_error(path: str)` method using Rich Panel in src/dprl/utils/metrics_plotter.py
- [x] T024 [US2] Add try/except around shutil.rmtree() in _cleanup_assets() to catch PermissionError and OSError in src/dprl/utils/metrics_plotter.py
- [x] T025 [US2] Call _display_cleanup_error() when cleanup fails, passing the assets folder path in src/dprl/utils/metrics_plotter.py
- [x] T026 [US2] Ensure cleanup never raises exceptions (catches all errors, displays message, continues) in src/dprl/utils/metrics_plotter.py

**Checkpoint**: User Story 2 complete - cleanup failures show clear error messages with path and instructions ✅

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and documentation

- [x] T027 Run full test suite: `uv run pytest tests/unit/test_metrics_plotter_cleanup.py -v`
- [x] T028 Run linting: `uv run ruff check src/dprl/utils/metrics_plotter.py`
- [x] T029 Run type checking: `uv run mypy src/dprl/utils/metrics_plotter.py`
- [ ] T030 Validate quickstart.md example works end-to-end

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately ✅
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories ✅
- **User Story 1 (Phase 3)**: Depends on Foundational phase ✅
- **User Story 2 (Phase 4)**: Depends on User Story 1 (extends _cleanup_assets with error handling) ✅
- **Polish (Phase 5)**: Depends on all user stories being complete ✅

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories ✅
- **User Story 2 (P2)**: Depends on User Story 1 (adds error handling to existing cleanup method) ✅

### Within Each User Story

- Tests MUST be written and FAIL before implementation ✅
- Core cleanup logic before signal handlers ✅
- Basic functionality before error handling ✅
- Story complete before moving to next priority ✅

### Parallel Opportunities

- T006, T007, T008, T009 (US1 tests) can run in parallel ✅
- T019, T020, T021 (US2 tests) can run in parallel ✅
- Setup tasks (T001, T002) can run in parallel ✅

---

## Parallel Execution Examples

### User Story 1 Tests (can run in parallel)

```bash
# Launch all US1 tests together:
Task: T006 "Create test file with fixtures"
Task: T007 "Write test_cleanup_removes_assets_folder"
Task: T008 "Write test_cleanup_handles_missing_folder"
Task: T009 "Write test_assets_created_flag_set"
```

### User Story 2 Tests (can run in parallel)

```bash
# Launch all US2 tests together:
Task: T019 "Write test_cleanup_failure_shows_error_message"
Task: T020 "Write test_error_message_contains_path"
Task: T021 "Write test_cleanup_does_not_crash_on_permission_error"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T002) ✅
2. Complete Phase 2: Foundational (T003-T005) ✅
3. Complete Phase 3: User Story 1 (T006-T018) ✅
4. **STOP and VALIDATE**: Run `uv run pytest tests/unit/test_metrics_plotter_cleanup.py -v` ✅
5. Assets folder cleanup works on normal exit ✅

### Full Feature (Both User Stories)

1. Complete MVP above ✅
2. Complete Phase 4: User Story 2 (T019-T026) ✅
3. Complete Phase 5: Polish (T027-T030) ⏳ (T030 remaining)
4. **VALIDATE**: Run full test suite and linting ✅

---

## Notes

- All tasks modify a single file: `src/dprl/utils/metrics_plotter.py`
- Tests are in a separate file: `tests/unit/test_metrics_plotter_cleanup.py`
- US2 extends US1 (adds error handling to cleanup method)
- Rich is already a project dependency - no new installs needed
- Cleanup must be idempotent (safe to call multiple times)
- Signal handlers must preserve original handlers (call them after cleanup)
