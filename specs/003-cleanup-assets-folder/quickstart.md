# Quickstart: Assets Folder Cleanup

## Overview

The `MetricsPlotter` class now automatically cleans up the `assets` folder when the visualization session ends. This prevents temporary video files from accumulating in your project directory.

## Behavior

### Automatic Cleanup

When you close the Dash dashboard (Ctrl+C or programmatic stop), the `assets` folder and all its contents are automatically deleted. No code changes required.

```python
from dprl.utils.metrics_plotter import MetricsPlotter
import numpy as np

plotter = MetricsPlotter()

# Add some metrics
plotter.add_metric("reward", [1.0, 2.0, 3.0])

# Add a video (creates assets/ folder)
frames = np.random.randint(0, 255, (100, 480, 640, 3), dtype=np.uint8)
plotter.add_video_from_frames("training", frames, fps=30)

# Start visualization
plotter.plot_metrics()

# When you press Ctrl+C or close the server:
# - assets/ folder is automatically deleted
# - Directory returns to pre-visualization state
```

### Cleanup Failure Handling

If cleanup fails (e.g., a file is locked by another process), you'll see a clear error message with the exact path and instructions:

```
╭─────────────────────────────────────────────────────────╮
│ ⚠️  Manual Action Required                              │
│                                                          │
│ Cleanup failed!                                          │
│                                                          │
│ Could not delete: /path/to/your/project/assets          │
│                                                          │
│ Please delete this folder manually.                      │
╰─────────────────────────────────────────────────────────╯
```

## No API Changes

This feature adds automatic cleanup behavior. Your existing code continues to work unchanged.

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| No videos added | No cleanup needed, no messages shown |
| Folder already deleted | Cleanup succeeds silently |
| File locked by another process | Error message with exact path shown |
| Multiple Ctrl+C presses | Safe, cleanup only runs once |
| Session crash/error | Cleanup still attempts to run |

## Testing

Verify cleanup works correctly:

```bash
# Run tests
uv run pytest tests/unit/test_metrics_plotter_cleanup.py -v
```
