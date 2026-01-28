# Feature Specification: TQDM and Table Logging for Training

**Feature Branch**: `007-tqdm-table-logging`
**Created**: 2026-01-28
**Status**: Draft
**Input**: User description: "Support TQDM progress bars and Rich table logging"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - TQDM Progress Bar (Priority: P1)

A researcher starts training a VPG agent and wants to see real-time progress
with key metrics displayed inline. The default behavior should show a TQDM
progress bar with epoch count, current loss, and max reward gained.

**Why this priority**: This is the most basic logging improvement that provides
immediate value for all training runs. Without progress indication, users have
no way to estimate completion time or monitor training health.

**Independent Test**: Can be fully tested by running `vpg_cartpole.py` and
observing the progress bar updates in terminal. Delivers immediate value for
monitoring training progress.

**Acceptance Scenarios**:

1. **Given** a user runs training with default settings, **When** training
   starts, **Then** a TQDM progress bar appears showing epoch progress, current
   loss, and max reward.
2. **Given** a user runs training with `--no-progress-bar`, **When** training
   starts, **Then** only minimal epoch logging appears (fallback behavior).
3. **Given** a user has TQDM disabled in config, **When** training starts,
   **Then** progress bar is not shown regardless of CLI flag.

---

### User Story 2 - Table Logging (Priority: P2)

A researcher wants detailed metrics displayed periodically during training in
a formatted table. They configure logging to show a Rich table every N epochs
with comprehensive statistics.

**Why this priority**: Provides deeper insight into training dynamics for users
who need more than the progress bar metrics. Builds on P1 functionality.

**Independent Test**: Can be tested by running training with `--table-log-freq
10` and verifying formatted tables appear every 10 epochs.

**Acceptance Scenarios**:

1. **Given** a user sets `--table-log-freq 10`, **When** epoch 10, 20, 30, etc.
   complete, **Then** a Rich table displays with epoch, loss, reward, steps,
   and other configured metrics.
2. **Given** a user sets `table_log_freq: 5` in YAML config, **When** training
   runs, **Then** tables appear every 5 epochs.
3. **Given** a user does not specify table logging, **When** training runs,
   **Then** no periodic tables are displayed (only progress bar).

---

### User Story 3 - Configuration Integration (Priority: P3)

A researcher wants to configure all logging options via YAML config file or
CLI arguments, with CLI taking precedence over config file values.

**Why this priority**: Enables reproducible experiments and convenient
customization. Depends on P1 and P2 being implemented first.

**Independent Test**: Can be tested by creating a config file with logging
settings and verifying they are applied correctly when training starts.

**Acceptance Scenarios**:

1. **Given** a YAML config with `progress_bar: true` and `table_log_freq: 20`,
   **When** user runs training with that config, **Then** progress bar shows
   and tables appear every 20 epochs.
2. **Given** a YAML config with `progress_bar: true`, **When** user runs
   training with `--no-progress-bar`, **Then** CLI flag overrides config
   and progress bar is disabled.
3. **Given** `--generate-config` is run, **When** template is generated,
   **Then** logging options are included with descriptive comments.

---

### Edge Cases

- What happens when terminal does not support TQDM (non-TTY)? Graceful fallback
- How does system handle very short training (< 5 epochs) with table logging?
- What if table_log_freq is larger than total epochs?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display TQDM progress bar by default during training
- **FR-002**: Progress bar MUST show current epoch, loss, and max reward
- **FR-003**: System MUST support `--no-progress-bar` CLI flag to disable TQDM
- **FR-004**: System MUST support `--table-log-freq N` to log table every N
  epochs
- **FR-005**: Table MUST display epoch, steps, loss, reward, and advantages
- **FR-006**: Logging config MUST be loadable from YAML config file
- **FR-007**: CLI arguments MUST override config file values for logging
- **FR-008**: System MUST use Rich library for table formatting (already in
  project)
- **FR-009**: Generated config templates MUST include logging options

### Key Entities

- **TrainingLogger**: Manages progress bar and table output during training
- **LoggingConfig**: Configuration fields for progress bar and table logging

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users see training progress without any additional configuration
- **SC-002**: Table logging works when configured via CLI or YAML
- **SC-003**: All existing training scripts (vpg_cartpole, vpg_flappy_bird)
  support the new logging
- **SC-004**: Line length compliance (< 80 chars) maintained in all new code
