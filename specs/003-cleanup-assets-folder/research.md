# Research: Cleanup Assets Folder

**Date**: 2026-01-26
**Feature**: 003-cleanup-assets-folder

## Research Questions

### 1. How to hook into Dash server shutdown?

**Decision**: Use `atexit` module combined with signal handlers

**Rationale**:
- Dash runs on Flask/Werkzeug which doesn't expose a clean shutdown hook
- `atexit` handlers run when the Python interpreter exits normally
- Signal handlers (SIGINT, SIGTERM) catch Ctrl+C and kill commands
- This combination covers all shutdown scenarios: normal exit, keyboard interrupt, programmatic stop
- Uses stdlib only (per Constitution Principle V: Simplicity & YAGNI)

**Alternatives considered**:
- Flask `@app.teardown_appcontext`: Only runs per-request, not on server shutdown
- Werkzeug shutdown endpoint: Requires HTTP request to trigger, not automatic
- Context managers: Would require changing the API (using `with` statement) - violates Principle I (User-First)

### 2. How to safely delete a directory with contents?

**Decision**: Use `shutil.rmtree()` with custom error handler

**Rationale**:
- `shutil.rmtree(path, onerror=handler)` allows graceful error handling
- Can catch permission errors, files in use, etc. without crashing
- Cross-platform compatible (Windows, Linux, macOS)
- Standard library, no additional dependencies (per Principle V)

**Alternatives considered**:
- `os.remove()` + `os.rmdir()`: Requires manual recursion, more error-prone
- `pathlib.Path.rmdir()`: Only works on empty directories
- Third-party libraries (send2trash): Unnecessary complexity for temporary files

### 3. How to display styled error messages to users?

**Decision**: Use Rich `Console` with styled panels

**Rationale**:
- Rich is already a project dependency (v14.2.0, per constitution Technology Stack)
- `Console.print()` with `Panel` provides clear, visually distinct messages
- Color coding: red for errors, yellow for paths
- Cross-platform terminal support
- Satisfies Principle I requirement: "Error messages MUST be actionable and point to solutions"

**Implementation approach**:
```python
from rich.console import Console
from rich.panel import Panel

console = Console()

# On cleanup failure:
console.print(Panel(
    f"[bold red]Cleanup failed![/bold red]\n\n"
    f"Could not delete: [yellow]{path}[/yellow]\n\n"
    f"Please delete this folder manually.",
    title="⚠️ Manual Action Required",
    border_style="red"
))
```

### 4. How to handle multiple MetricsPlotter instances?

**Decision**: Track assets folder path per instance, clean up only what was created

**Rationale**:
- Each `MetricsPlotter` instance stores `self.caller_dir` (already implemented)
- Track whether this instance created the assets folder via a flag
- Only attempt cleanup if this instance created the folder
- Prevents race conditions and accidental deletion of shared resources

**Implementation approach**:
- Add `self._assets_created = False` flag
- Set to `True` when `add_video_from_frames()` creates the folder
- Only run cleanup if `self._assets_created is True`

### 5. How to handle cleanup during abnormal termination?

**Decision**: Register cleanup with both `atexit` and signal handlers

**Rationale**:
- `atexit` handles normal program exit
- `signal.signal(SIGINT, handler)` handles Ctrl+C
- `signal.signal(SIGTERM, handler)` handles `kill` command
- Cleanup function should be idempotent (safe to call multiple times)

**Edge cases handled**:
- `SIGKILL` (kill -9): Cannot be caught, cleanup won't run (acceptable)
- Power failure: Cannot be handled, cleanup won't run (acceptable)
- Multiple Ctrl+C presses: Idempotent cleanup prevents errors

## Technical Decisions Summary

| Area | Decision | Constitution Alignment |
|------|----------|------------------------|
| Shutdown hook | `atexit` + signal handlers | V. Simplicity (stdlib) |
| Directory deletion | `shutil.rmtree()` with error handler | V. Simplicity (stdlib) |
| User feedback | Rich Console with styled Panel | I. User-First (actionable errors) |
| Instance tracking | `_assets_created` flag per instance | V. Simplicity (no abstractions) |
| Error handling | Catch all exceptions, display path, don't crash | I. User-First (actionable errors) |

## Constitution Compliance Summary

| Principle | Compliance |
|-----------|------------|
| I. User-First API Design | ✅ Automatic cleanup; actionable error messages |
| II. Gymnasium Compatibility | N/A (not environment/algorithm related) |
| III. Reproducibility | N/A (post-visualization cleanup) |
| IV. Testing & Validation | ✅ Unit tests planned for cleanup logic |
| V. Simplicity & YAGNI | ✅ All stdlib except Rich (existing dep) |
