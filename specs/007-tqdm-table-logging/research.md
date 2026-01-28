# Research: TQDM and Table Logging

**Feature**: 007-tqdm-table-logging
**Date**: 2026-01-28

## Research Tasks

### 1. TQDM Integration with Rich

**Question**: How to integrate TQDM with existing Rich usage in the codebase?

**Decision**: Use `tqdm.rich` for seamless integration with Rich console.

**Rationale**: The `tqdm.rich` module provides a drop-in replacement for
standard tqdm that renders using Rich's progress bar components. This ensures
visual consistency with existing Rich usage (experiment_logger.py,
metrics_plotter.py) and avoids conflicts when mixing tqdm and Rich output.

**Alternatives considered**:
- Standard tqdm: Would conflict with Rich console output, potential flickering
- Custom Rich Progress: More code, reinvents tqdm functionality
- Both Rich Progress + tqdm: Unnecessary complexity

**Best practices**:
```python
from tqdm.rich import tqdm

for epoch in tqdm(range(epochs), desc="Training"):
    # training loop
    pbar.set_postfix(loss=loss, reward=max_reward)
```

---

### 2. Rich Table for Metrics Display

**Question**: Best pattern for periodic table logging during training?

**Decision**: Use Rich `Table` with `Console.print()` at configurable intervals.

**Rationale**: Rich Table provides formatted, aligned output that works well
in terminals. The existing codebase already imports Rich Console in
`metrics_plotter.py` and uses `rich.print()` in `experiment_logger.py`.

**Implementation pattern**:
```python
from rich.console import Console
from rich.table import Table

def log_metrics_table(epoch, metrics, console):
    table = Table(title=f"Training Metrics - Epoch {epoch}")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    for name, value in metrics.items():
        table.add_row(name, f"{value:.4f}")
    console.print(table)
```

---

### 3. Configuration Extension Pattern

**Question**: How to add logging config fields to VPGConfig?

**Decision**: Add logging fields directly to VPGConfig with appropriate
defaults matching the "TQDM by default" requirement.

**Rationale**: Follows existing pattern in VPGConfig. Fields can use Pydantic's
Field with aliases for CLI integration. Default `progress_bar=True` and
`table_log_freq=0` (disabled) meets the spec requirement.

**Fields to add**:
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

---

### 4. Non-TTY Fallback Behavior

**Question**: How should logging behave in non-interactive environments?

**Decision**: TQDM handles this automatically; Rich can detect TTY as well.

**Rationale**: `tqdm` automatically disables progress bars when not running in
a TTY (e.g., piped output, CI environments). Rich's Console also detects TTY
and adjusts output accordingly. No special handling needed.

**Verification**:
```python
# tqdm will not show progress bar when:
# - stdout is redirected to a file
# - running in CI (no TTY)
# - explicitly disabled via disable=True
```

---

### 5. Integration Points in Training Scripts

**Question**: Where to integrate logging in vpg_cartpole.py and similar?

**Decision**: Wrap the epoch loop with tqdm; add table logging inside the loop.

**Current code** (line 76-104 in vpg_cartpole.py):
```python
for epoch in range(epochs):
    # ... training code ...
    print(f"Epoch {epoch}, steps: {len(trajectory.rewards)}, Loss: {loss}")
```

**Proposed change**:
```python
from tqdm.rich import tqdm

pbar = tqdm(range(epochs), desc="Training", disable=not progress_bar)
for epoch in pbar:
    # ... training code ...
    pbar.set_postfix(
        loss=f"{loss.item():.4f}",
        reward=f"{max_reward:.1f}"
    )
    if table_log_freq > 0 and (epoch + 1) % table_log_freq == 0:
        log_metrics_table(epoch, metrics, console)
```

---

### 6. Dependency Check

**Question**: Is tqdm already a project dependency?

**Decision**: Need to add tqdm to project dependencies via pyproject.toml.

**Rationale**: Checked pyproject.toml - tqdm is not currently listed. It's a
widely-used, well-maintained package that aligns with the constitution's
dependency policy.

**Action**: Add `tqdm>=4.66.0` to dependencies in pyproject.toml.

---

## Summary

All research questions resolved. Key decisions:
1. Use `tqdm.rich` for progress bars (integrates with existing Rich usage)
2. Use Rich Table for periodic metrics display
3. Add config fields to VPGConfig with sensible defaults
4. No special non-TTY handling needed (libraries handle it)
5. Minimal changes to training scripts (wrap loop, add table call)
6. Add tqdm dependency to pyproject.toml
