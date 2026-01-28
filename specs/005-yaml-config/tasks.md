# Tasks: YAML Configuration File Support

**Input**: Design documents from `/specs/005-yaml-config/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Unit tests included per constitution (Testing & Validation principle).

**Organization**: Tasks grouped by user story for independent implementation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story (US1, US2, US3)
- Exact file paths included

---

## Phase 1: Setup

**Purpose**: Verify dependencies and project structure ready

- [x] T001 Verify PyYAML and Pydantic dependencies in pyproject.toml
- [x] T002 [P] Create tests/unit/ directory if not exists

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Base infrastructure that ALL user stories depend on

**CRITICAL**: No user story work can begin until BaseConfig is complete

- [x] T003 Create BaseConfig class in src/dprl/utils/config.py with
      model_config (populate_by_name, extra=forbid)
- [x] T004 Implement load_from_yaml() classmethod in src/dprl/utils/config.py
- [x] T005 Implement to_click_default_map() method in src/dprl/utils/config.py
- [x] T006 Implement config_option() decorator factory in
      src/dprl/utils/config.py
- [x] T007 Export BaseConfig and config_option from src/dprl/utils/__init__.py
- [x] T008 [P] Create unit tests for BaseConfig in
      tests/unit/test_base_config.py

**Checkpoint**: BaseConfig ready - user story implementation can begin

---

## Phase 3: User Story 1 - Load Configuration from YAML (P1) MVP

**Goal**: Users can run training with `--config config.yaml` instead of
multiple CLI args. CLI args override config values when both provided.

**Independent Test**: Create a YAML file with `epochs: 100`, run
`python examples/vpg_cartpole.py --config test.yaml`, verify epochs=100 used.

### Implementation for User Story 1

- [x] T009 [P] [US1] Create VPGConfig class in
      src/dprl/algorithms/vpg/config.py with fields: epochs, lr,
      hidden_layer_units (alias: hidden-layer-units),
      advantage_expression (alias: advantage-expression)
- [x] T010 [US1] Export VPGConfig from src/dprl/algorithms/vpg/__init__.py
- [x] T011 [US1] Update examples/vpg_cartpole.py to add @config_option(VPGConfig)
      decorator and --config CLI option
- [x] T012 [US1] Update examples/vpg_flappy_bird.py to add
      @config_option(VPGConfig) decorator and --config CLI option
- [x] T013 [P] [US1] Create unit tests for VPGConfig in
      tests/unit/test_vpg_config.py (valid config, type coercion, defaults)

**Checkpoint**: Config loading works. Test with:
`echo "epochs: 100" > test.yaml && python examples/vpg_cartpole.py --config test.yaml`

---

## Phase 4: User Story 2 - Validate Config and Report Errors (P2)

**Goal**: Invalid configs produce clear error messages listing valid options.

**Independent Test**: Create YAML with typo `epocs: 100`, run script, verify
error message shows "Valid fields: epochs, lr, hidden-layer-units,
advantage-expression".

### Implementation for User Story 2

- [x] T014 [US2] Add format_validation_error() function to
      src/dprl/utils/config.py that formats Pydantic ValidationError with
      valid fields list for extra_forbidden errors
- [x] T015 [US2] Update config_option() in src/dprl/utils/config.py to catch
      ValidationError and raise click.BadParameter with formatted message
- [x] T016 [US2] Add file-not-found error handling in config_option() for
      missing config files
- [x] T017 [US2] Add YAML syntax error handling in load_from_yaml() with
      helpful message
- [x] T018 [P] [US2] Add unit tests for validation errors in
      tests/unit/test_base_config.py (unknown field, invalid type,
      invalid choice, file not found)

**Checkpoint**: Invalid configs produce helpful errors. Test with:
`echo "epocs: 100" > bad.yaml && python examples/vpg_cartpole.py --config bad.yaml`

---

## Phase 5: User Story 3 - Generate Default Config Template (P3)

**Goal**: Users can generate commented YAML template with `--generate-config`.

**Independent Test**: Run `python examples/vpg_cartpole.py --generate-config`,
verify vpg_config_template.yaml created with defaults and comments.

### Implementation for User Story 3

- [x] T019 [US3] Implement generate_template() classmethod in
      src/dprl/utils/config.py using model_json_schema() for field descriptions
- [x] T020 [US3] Add generate_config_option() decorator factory in
      src/dprl/utils/config.py
- [x] T021 [US3] Export generate_config_option from
      src/dprl/utils/__init__.py
- [x] T022 [US3] Update examples/vpg_cartpole.py to add
      @generate_config_option(VPGConfig) decorator
- [x] T023 [US3] Update examples/vpg_flappy_bird.py to add
      @generate_config_option(VPGConfig) decorator
- [x] T024 [P] [US3] Add unit tests for template generation in
      tests/unit/test_base_config.py (file created, defaults present,
      comments present)

**Checkpoint**: Template generation works. Test with:
`python examples/vpg_cartpole.py --generate-config && cat vpg_config_template.yaml`

---

## Phase 6: User Story 4 - Save Config with Experiments (P1) 🎯 NEW

**Goal**: Automatically save training configuration alongside experiment
results for full reproducibility. Users can reload saved experiments and see
exactly what parameters were used (Constitution III: Reproducibility).

**Independent Test**: Run `vpg_cartpole.py --config config.yaml`, check that
`runs/exp_vpg_*/` folder contains both `policy.tar` and `config.yaml`.

### Tests for User Story 4

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T030 [P] [US4] Add test for `to_yaml()` method in
      tests/unit/test_base_config.py
- [x] T031 [P] [US4] Add test for config saving in save_experiment_details()
      in tests/unit/test_experiment_logger.py (create file if needed)
- [x] T032 [P] [US4] Add test for load_config_from_experiment() utility
      in tests/unit/test_experiment_logger.py

### Implementation for User Story 4

- [x] T033 [US4] Add `to_yaml()` method to BaseConfig class in
      src/dprl/utils/config.py
- [x] T034 [US4] Add optional `config: BaseConfig | None` parameter to
      save_experiment_details() in src/dprl/utils/experiment_logger.py
- [x] T035 [US4] Implement load_config_from_experiment() function in
      src/dprl/utils/experiment_logger.py
- [x] T036 [US4] Export load_config_from_experiment from
      src/dprl/utils/__init__.py
- [x] T037 [P] [US4] Update examples/vpg_cartpole.py to construct VPGConfig
      from CLI params and pass to save_experiment_details()
- [x] T038 [P] [US4] Update examples/vpg_flappy_bird.py to construct VPGConfig
      from CLI params and pass to save_experiment_details()

**Checkpoint**: Config saved with experiments; can be loaded for reproduction

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and cleanup

- [x] T025 Run all tests: `uv run pytest tests/unit/test_base_config.py
      tests/unit/test_vpg_config.py -v`
- [x] T026 Run linting: `uv run ruff check src/dprl/utils/config.py
      src/dprl/algorithms/vpg/config.py`
- [x] T027 Run type checking: `uv run mypy src/dprl/utils/config.py
      src/dprl/algorithms/vpg/config.py`
- [x] T028 Validate backward compatibility: run examples without --config
- [x] T029 Validate quickstart.md scenarios work as documented
- [x] T039 Run all tests including new US4 tests: `uv run pytest tests/ -v`
- [x] T040 Verify backward compat: old experiments without config.yaml still load
- [x] T041 Run full quickstart.md validation including config saving workflow

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies ✅ COMPLETE
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories ✅ COMPLETE
- **User Story 1 (Phase 3)**: Depends on Foundational ✅ COMPLETE
- **User Story 2 (Phase 4)**: Depends on User Story 1 ✅ COMPLETE
- **User Story 3 (Phase 5)**: Depends on Foundational ✅ COMPLETE
- **User Story 4 (Phase 6)**: Depends on Foundational (BaseConfig) 🎯 CURRENT
- **Polish (Phase 7)**: Depends on all user stories complete

### User Story Dependencies

- **US1 (P1)**: Depends on Foundational (BaseConfig) ✅ COMPLETE
- **US2 (P2)**: Depends on US1 (needs config loading) ✅ COMPLETE
- **US3 (P3)**: Depends on Foundational only ✅ COMPLETE
- **US4 (P1)**: Depends on Foundational (BaseConfig.to_yaml) - **NEW SCOPE**

### Parallel Opportunities

Within Phase 2 (Foundational): ✅ COMPLETE
- T008 can run parallel after T003-T007 structure is defined

Within Phase 3 (US1): ✅ COMPLETE
- T009 and T013 can run in parallel (different files)

Within Phase 4 (US2): ✅ COMPLETE
- T018 can run parallel with T014-T017

Within Phase 5 (US3): ✅ COMPLETE
- T024 can run parallel with T019-T023

Within Phase 6 (US4): 🎯 CURRENT
- T030, T031, T032 can run in parallel (different test files/functions)
- T037, T038 can run in parallel (different example files)

---

## Parallel Example: User Story 4 (Current)

```bash
# Launch all tests for US4 together:
Task: "Add test for to_yaml() in tests/unit/test_base_config.py"
Task: "Add test for config saving in tests/unit/test_experiment_logger.py"
Task: "Add test for load_config_from_experiment() utility"

# After implementation, launch example updates in parallel:
Task: "Update vpg_cartpole.py to pass config to save_experiment_details()"
Task: "Update vpg_flappy_bird.py to pass config to save_experiment_details()"
```

---

## Implementation Strategy

### Current Focus: User Story 4

US1-US3 are complete. Current implementation scope is US4 (config saving).

**Recommended execution order:**
1. Write failing tests T030-T032 (parallel)
2. Implement T033 (to_yaml method)
3. Implement T034-T036 (save/load functions)
4. Update examples T037-T038 (parallel)
5. Validate T039-T041

### Task Dependencies for US4

```
T030, T031, T032 (tests - parallel, write first, should FAIL)
    └── T033 (to_yaml method)
          └── T034 (add config param to save_experiment_details)
                └── T035 (load_config_from_experiment)
                      └── T036 (export)
                            └── T037, T038 (update examples - parallel)
                                  └── T039, T040, T041 (validation)
```

### Commit Strategy

- T030-T032 → Commit: "Add tests for config saving (failing)"
- T033 → Commit: "Add to_yaml() method to BaseConfig"
- T034-T035 → Commit: "Add config param to save_experiment_details"
- T036 → Commit: "Export load_config_from_experiment"
- T037-T038 → Commit: "Update examples to save config with experiments"
- T039-T041 → Commit: "Validate config saving feature complete"

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to user story for traceability
- Each user story independently testable
- Commit after each task or logical group
- Stop at any checkpoint to validate
- US4 maintains backward compatibility: config param is optional (None default)
- Old experiments without config.yaml still load correctly
