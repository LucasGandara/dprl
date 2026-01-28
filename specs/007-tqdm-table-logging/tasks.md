# Tasks: TQDM and Table Logging for Training

**Input**: Design documents from `specs/007-tqdm-table-logging/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Unit tests requested in plan.md (Phase 4: Testing).

**Organization**: Tasks grouped by user story for independent implementation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Add tqdm dependency and prepare project structure

- [X] T001 Add `tqdm>=4.66.0` to dependencies in pyproject.toml
- [X] T002 Run `uv sync` to install tqdm dependency

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create TrainingLogger class that all user stories depend on

**CRITICAL**: No user story work can begin until this phase is complete

- [X] T003 Create TrainingLogger class skeleton in
  src/dprl/utils/training_logger.py with __init__, update, close methods
- [X] T004 Implement __enter__ and __exit__ for context manager support in
  src/dprl/utils/training_logger.py
- [X] T005 Export TrainingLogger from src/dprl/utils/__init__.py

**Checkpoint**: Foundation ready - user story implementation can begin

---

## Phase 3: User Story 1 - TQDM Progress Bar (Priority: P1) MVP

**Goal**: Display TQDM progress bar by default with epoch, loss, max reward

**Independent Test**: Run `vpg_cartpole.py` and observe progress bar updates

### Tests for User Story 1

- [X] T006 [P] [US1] Create test file tests/unit/test_training_logger.py
  with test_init_with_progress_bar_enabled
- [X] T007 [P] [US1] Add test_init_with_progress_bar_disabled in
  tests/unit/test_training_logger.py
- [X] T008 [P] [US1] Add test_update_sets_postfix in
  tests/unit/test_training_logger.py

### Implementation for User Story 1

- [X] T009 [US1] Implement tqdm.rich progress bar creation in TrainingLogger
  __init__ method in src/dprl/utils/training_logger.py
- [X] T010 [US1] Implement update method to set_postfix with loss and reward
  in src/dprl/utils/training_logger.py
- [X] T011 [US1] Implement close method to properly close progress bar in
  src/dprl/utils/training_logger.py
- [X] T012 [US1] Add max_reward tracking to TrainingLogger in
  src/dprl/utils/training_logger.py
- [X] T013 [US1] Add progress_bar field to VPGConfig (default=True) in
  src/dprl/algorithms/vpg/config.py
- [X] T014 [US1] Add --progress-bar/--no-progress-bar CLI option to
  examples/vpg_cartpole.py
- [X] T015 [US1] Replace print() with TrainingLogger in training loop in
  examples/vpg_cartpole.py
- [X] T016 [P] [US1] Add --progress-bar/--no-progress-bar CLI option to
  examples/vpg_flappy_bird.py
- [X] T017 [P] [US1] Replace print() with TrainingLogger in
  examples/vpg_flappy_bird.py

**Checkpoint**: Progress bar works with default settings and can be disabled

---

## Phase 4: User Story 2 - Table Logging (Priority: P2)

**Goal**: Display Rich table with detailed metrics every N epochs

**Independent Test**: Run training with `--table-log-freq 10` and verify tables

### Tests for User Story 2

- [X] T018 [P] [US2] Add test_table_logging_at_interval in
  tests/unit/test_training_logger.py
- [X] T019 [P] [US2] Add test_table_logging_disabled_when_freq_zero in
  tests/unit/test_training_logger.py

### Implementation for User Story 2

- [X] T020 [US2] Add Rich Console and Table imports to
  src/dprl/utils/training_logger.py
- [X] T021 [US2] Add table_log_freq parameter to TrainingLogger __init__ in
  src/dprl/utils/training_logger.py
- [X] T022 [US2] Implement _log_table private method with Rich Table in
  src/dprl/utils/training_logger.py
- [X] T023 [US2] Add table logging trigger in update method when
  epoch % table_log_freq == 0 in src/dprl/utils/training_logger.py
- [X] T024 [US2] Add table_log_freq field to VPGConfig (default=0) in
  src/dprl/algorithms/vpg/config.py
- [X] T025 [US2] Add --table-log-freq CLI option to examples/vpg_cartpole.py
- [X] T026 [US2] Pass table_log_freq to TrainingLogger in
  examples/vpg_cartpole.py
- [X] T027 [P] [US2] Add --table-log-freq CLI option to
  examples/vpg_flappy_bird.py
- [X] T028 [P] [US2] Pass table_log_freq to TrainingLogger in
  examples/vpg_flappy_bird.py

**Checkpoint**: Tables appear at configured intervals with all metrics

---

## Phase 5: User Story 3 - Configuration Integration (Priority: P3)

**Goal**: All logging options configurable via YAML and CLI with override

**Independent Test**: Create config file, verify settings applied, CLI overrides

### Tests for User Story 3

- [X] T029 [P] [US3] Add test_config_fields_in_vpg_config in
  tests/unit/test_training_logger.py

### Implementation for User Story 3

- [X] T030 [US3] Verify generate_template includes progress_bar and
  table_log_freq fields in src/dprl/algorithms/vpg/config.py
- [X] T031 [US3] Update vpg_cartpole.py to read logging options from config
  and pass to TrainingLogger in examples/vpg_cartpole.py
- [X] T032 [US3] Update vpg_flappy_bird.py to read logging options from config
  and pass to TrainingLogger in examples/vpg_flappy_bird.py

**Checkpoint**: Config file and CLI both work, CLI overrides config values

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Ensure code quality and completeness

- [X] T033 [P] Add test_context_manager_closes_properly in
  tests/unit/test_training_logger.py
- [X] T034 Run all tests with `uv run pytest tests/unit/test_training_logger.py`
- [X] T035 Run linting with `uv run ruff check src/dprl/utils/training_logger.py`
- [X] T036 [P] Run type checking with `uv run mypy src/dprl/utils/`
- [X] T037 Verify all lines are < 80 characters in new/modified files
- [X] T038 Run quickstart.md validation by executing example commands

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - Stories can proceed sequentially: P1 -> P2 -> P3
  - P2 builds on P1 (adds table logging to existing logger)
  - P3 builds on P1+P2 (config integration)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - MVP deliverable
- **User Story 2 (P2)**: Builds on US1 TrainingLogger (adds table method)
- **User Story 3 (P3)**: Builds on US1+US2 (verifies config integration)

### Within Each User Story

- Tests written first (should fail initially)
- Core implementation (TrainingLogger changes)
- Config changes (VPGConfig fields)
- CLI integration (examples/*.py)

### Parallel Opportunities

Within Phase 3 (US1):
- T006, T007, T008 (tests) can run in parallel
- T016, T017 (flappy_bird changes) parallel to T014, T015 (cartpole)

Within Phase 4 (US2):
- T018, T019 (tests) can run in parallel
- T027, T028 (flappy_bird) parallel to T25, T26 (cartpole)

Within Phase 6 (Polish):
- T033, T035, T036 can run in parallel

---

## Parallel Example: User Story 1 Tests

```bash
# Launch all tests for User Story 1 together:
Task: "Create test file tests/unit/test_training_logger.py"
Task: "Add test_init_with_progress_bar_disabled"
Task: "Add test_update_sets_postfix"

# After TrainingLogger core is done, update both scripts in parallel:
Task: "Add --progress-bar/--no-progress-bar to vpg_cartpole.py"
Task: "Add --progress-bar/--no-progress-bar to vpg_flappy_bird.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (add tqdm dependency)
2. Complete Phase 2: Foundational (create TrainingLogger skeleton)
3. Complete Phase 3: User Story 1 (progress bar works!)
4. **STOP and VALIDATE**: Run `vpg_cartpole.py --epochs 20`
5. Progress bar should show with loss and max reward

### Incremental Delivery

1. Setup + Foundational -> TrainingLogger exists
2. Add User Story 1 -> Test progress bar -> MVP ready!
3. Add User Story 2 -> Test table logging -> Enhanced logging
4. Add User Story 3 -> Test config file -> Full feature complete
5. Each story adds value without breaking previous stories

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- US2 and US3 build on US1, so sequential execution recommended
- Verify tests fail before implementing
- Commit after each task or logical group
- Line length must be < 80 characters in all new code
- Use tqdm.rich (not plain tqdm) for Rich integration
