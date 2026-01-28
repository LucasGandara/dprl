# Data Model: TQDM and Table Logging

**Feature**: 007-tqdm-table-logging
**Date**: 2026-01-28

## Entities

### 1. LoggingConfig (Extension to VPGConfig)

Configuration fields for controlling training output. These fields extend the
existing `VPGConfig` class.

| Field | Type | Default | Validation | Description |
|-------|------|---------|------------|-------------|
| `progress_bar` | bool | True | - | Enable TQDM progress bar |
| `table_log_freq` | int | 0 | >= 0 | Log table every N epochs (0=disabled) |

**Pydantic Implementation**:
```python
progress_bar: bool = Field(
    default=True,
    alias="progress-bar",
    description="Show TQDM progress bar during training",
)

table_log_freq: int = Field(
    default=0,
    ge=0,
    alias="table-log-freq",
    description="Log metrics table every N epochs (0 to disable)",
)
```

**State transitions**: None (configuration is immutable after loading)

---

### 2. TrainingLogger

Utility class managing progress bar and table output during training loops.

| Attribute | Type | Description |
|-----------|------|-------------|
| `console` | Console | Rich console for output |
| `pbar` | tqdm | Progress bar instance (optional) |
| `progress_bar_enabled` | bool | Whether progress bar is active |
| `table_log_freq` | int | Frequency for table logging |
| `metrics_history` | dict | Accumulated metrics for display |

**Methods**:
| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `__init__` | epochs, progress_bar, table_log_freq | - | Initialize logger |
| `update` | epoch, loss, reward, steps, advantages | - | Update progress bar |
| `log_table` | epoch | - | Print metrics table |
| `close` | - | - | Clean up resources |

**Lifecycle**:
1. Created at start of training with config
2. `update()` called each epoch
3. `log_table()` called when epoch % table_log_freq == 0
4. `close()` called at end of training

---

### 3. MetricsSnapshot

Data structure for metrics at a given epoch (used internally by TrainingLogger)

| Field | Type | Description |
|-------|------|-------------|
| `epoch` | int | Current epoch number |
| `steps` | int | Steps taken in this epoch |
| `loss` | float | Policy gradient loss |
| `reward` | float | Sum of rewards this epoch |
| `max_reward` | float | Best reward seen so far |
| `advantages` | float | Sum of advantages this epoch |

---

## Relationships

```
VPGConfig
  └── contains logging fields (progress_bar, table_log_freq)

TrainingLogger
  ├── uses Console (Rich)
  ├── uses tqdm (progress bar)
  └── uses MetricsSnapshot (internal data)

vpg_cartpole.py (training script)
  ├── creates VPGConfig (with logging fields)
  └── creates TrainingLogger (using config)
```

---

## Validation Rules

1. `table_log_freq` must be non-negative integer
2. If `table_log_freq` > total epochs, no tables are logged (valid behavior)
3. `progress_bar` boolean controls TQDM display
4. CLI `--no-progress-bar` overrides config `progress_bar: true`

---

## YAML Configuration Example

```yaml
# VPGConfig Configuration
epochs: 100
lr: 0.001
hidden-layer-units: 64
advantage-expression: reward_to_go

# Logging configuration
progress-bar: true
table-log-freq: 20
```
