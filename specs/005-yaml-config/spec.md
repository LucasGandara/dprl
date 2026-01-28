# Feature Specification: YAML Configuration File Support

**Feature Branch**: `005-yaml-config`
**Created**: 2026-01-27
**Status**: Draft
**Input**: User description: "The CLI receives too many arguments,
user should be able to create a yaml file with the allowed configurations.User
should receive a feedback of the allowed configurations if any config is wrong.
User should be able to create a template with the default config values."

## Clarifications

### Session 2026-01-27

- Q: Should config file and CLI args be mutually exclusive or allow override?
  → A: CLI override - allow both, CLI args override config values when combined.
- Q: Where should config models live - examples or algorithm modules?
  → A: Algorithm modules. Each algorithm (e.g., VPG) owns its config model.
       Use SOLID/OOP for reusability across algorithms.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Load Configuration from YAML File (Priority: P1)

A user wants to run a training experiment using pre-defined settings stored in
a configuration file as an alternative to typing numerous command-line
arguments. They create or reuse a YAML file containing all training parameters
and pass it to the CLI. Users may also combine config files with CLI arguments,
where CLI arguments override config file values for fine-tuning.

**Why this priority**: This is the core functionality that addresses the
primary pain point of too many CLI arguments. Without this, users must manually
type all parameters every time they run an experiment.

**Independent Test**: Can be fully tested by creating a YAML config file and running the training script with `--config config.yaml`. The script should use all values from the config file.

**Acceptance Scenarios**:

1. **Given** a valid YAML config file exists with `epochs: 100` and `lr: 0.01`, **When** user runs `python vpg_cartpole.py --config config.yaml`, **Then** the training uses 100 epochs and learning rate 0.01
2. **Given** a YAML config file exists, **When** user also provides a CLI argument (e.g., `--epochs 50`), **Then** the CLI argument overrides the config file value
3. **Given** no config file is specified, **When** user runs the script with CLI arguments only, **Then** the script works exactly as before (backward compatible)

---

### User Story 2 - Validate Configuration and Report Errors (Priority: P2)

A user provides a YAML configuration file that contains an invalid configuration option (e.g., a typo in a key name or an invalid value). The system should clearly inform the user what went wrong and what the valid options are.

**Why this priority**: Error feedback is critical for usability. Without clear error messages, users waste time debugging configuration issues. This story depends on P1 (loading configs) being implemented.

**Independent Test**: Can be tested by providing a YAML file with an invalid key (e.g., `epocs` instead of `epochs`) and verifying the error message lists valid options.

**Acceptance Scenarios**:

1. **Given** a YAML config with an unknown key `epocs: 100`, **When** user runs the script, **Then** an error message displays: "Unknown configuration option 'epocs'. Valid options are: epochs, lr, hidden-layer-units, advantage-expression"
2. **Given** a YAML config with an invalid value `advantage-expression: invalid_method`, **When** user runs the script, **Then** an error message displays the valid values for that option
3. **Given** a YAML config with a wrong data type `epochs: "not a number"`, **When** user runs the script, **Then** an error message indicates the expected type

---

### User Story 3 - Generate Default Configuration Template (Priority: P3)

A new user wants to quickly get started with a configuration file but doesn't know all the available options. They run a command to generate a template YAML file pre-filled with all available options and their default values, with descriptive comments.

**Why this priority**: This is a convenience feature that helps new users discover available options. The core functionality (P1, P2) works without this, but this improves the user experience significantly.

**Independent Test**: Can be tested by running a command like `python vpg_cartpole.py --generate-config` and verifying it creates a valid YAML template with defaults.

**Acceptance Scenarios**:

1. **Given** user wants to generate a config template, **When** user runs `python vpg_cartpole.py --generate-config`, **Then** a YAML file is created with all available options set to their default values
2. **Given** user generates a config template, **When** inspecting the generated file, **Then** each option has a comment describing what it does
3. **Given** a template is generated, **When** user runs the script with the generated template (no modifications), **Then** the behavior is identical to running with no config (defaults applied)

---

### Edge Cases

- What happens when the config file path doesn't exist? → Clear error message stating file not found
- What happens when the YAML file is malformed (syntax error)? → Clear error message with line number if possible
- What happens when the config file is empty? → Use all default values (equivalent to no config)
- How does the system handle extra whitespace or different YAML formatting styles? → Standard YAML parser handles this transparently
- What happens when both `--config` and all CLI arguments are provided? → CLI arguments take precedence for any conflicting values

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept a `--config` CLI option that specifies a path to a YAML configuration file
- **FR-002**: System MUST load and parse configuration values from the specified YAML file
- **FR-003**: System MUST validate that all configuration keys in the YAML file are recognized options
- **FR-004**: System MUST validate that all configuration values have the correct data type
- **FR-005**: System MUST display a clear error message listing all valid configuration options when an unknown option is provided
- **FR-006**: System MUST display a clear error message with valid values when an option has an invalid value
- **FR-007**: System MUST allow CLI arguments to override values specified in the configuration file
- **FR-008**: System MUST maintain backward compatibility (existing CLI usage without config files continues to work)
- **FR-009**: System MUST provide a `--generate-config` option that creates a template YAML file with default values
- **FR-010**: System MUST include descriptive comments in generated template files explaining each option
- **FR-011**: System MUST display a helpful error message when the specified config file does not exist
- **FR-012**: System MUST display a helpful error message when the YAML file contains syntax errors

### Key Entities

- **Configuration File**: A YAML file containing key-value pairs for training parameters. Recognized keys include: epochs, lr (learning rate), hidden-layer-units, advantage-expression
- **Configuration Option**: A named parameter with a default value, data type constraint, optional valid value set, and help description
- **Validation Error**: Information about why a configuration is invalid, including the problematic key/value and guidance for correction

## Assumptions

- The configuration file format is YAML (human-readable, supports comments)
- Configuration models are per-algorithm (e.g., VPGConfig), not per-script
- Each algorithm module owns its config model; examples import from algorithms
- Base config class provides reusable SOLID-compliant loading/generation logic
- The generated template file will be written to the current directory with a
  default name (e.g., `vpg_config_template.yaml`)
- Standard YAML 1.1/1.2 parsing rules apply

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can run a complete training experiment by specifying only a single `--config` argument instead of multiple CLI arguments
- **SC-002**: 100% of invalid configuration keys result in an error message that lists all valid options
- **SC-003**: 100% of invalid configuration values result in an error message that explains the valid values or types
- **SC-004**: Users can generate a working configuration template with a single command
- **SC-005**: All existing CLI commands without config files continue to work identically (zero breaking changes)
