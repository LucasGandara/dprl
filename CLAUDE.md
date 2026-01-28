# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## Project Overview

DPRL is a deep reinforcement learning toolkit providing algorithms, custom environments, and utilities for training RL agents. Built on PyTorch and Gymnasium.

## Development Commands

```bash
# Install dependencies (uses uv - required)
uv sync

# Install with dev dependencies
uv sync --all-extras

# Run example training script
uv run python examples/vpg_cartpole.py --epochs 800 --lr 0.001

# Run tests
uv run pytest tests/

# Linting and formatting
uv run ruff check src/
uv run black src/
uv run mypy src/
```

## Architecture

### Source Layout (`src/dprl/`)

- **algorithms/**: RL algorithm implementations
  - `vpg/`: Vanilla Policy Gradient with advantage estimation variants (total reward, reward-to-go, baselined)

- **envs/**: Custom Gymnasium-compatible environments
  - `flappy_bird/`: Pygame-based FlappyBird environment
  - `snake/`: Snake game with RL-compatible interface
  - `__init__.py`: Environment factory (`make_env()`) and wrappers (`NormalizeObservation`, `ClipAction`)

- **utils/**: Training utilities
  - `experiment_logger.py`: Save/load model checkpoints with `save_experiment_details()` and `load_experiment_details()`
  - `metrics_plotter.py`: Dash-based visualization with `MetricsPlotter` class for metrics and video playback

### Key Patterns

- Custom environments implement the Gymnasium `Env` interface with `reset()`, `step()`, `render()`
- Models are saved as PyTorch state dicts via `torch.save()` to `runs/` directory
- VPG uses `VPGTrajectory` namedtuple to collect rewards and log probabilities
- `AdvantageExpression` enum controls advantage calculation method

### Examples (`examples/`)

Training scripts using Click CLI:
- `vpg_cartpole.py`: VPG on CartPole with configurable hyperparameters
- `vpg_flappy_bird.py`: VPG on custom FlappyBird environment
- `vpg_cartpole_from_saved_model.py`: Load and visualize saved models

## Testing

```bash
# Run all tests
uv run pytest tests/

# Run tests with verbose output
uv run pytest tests/ -v

# Run only unit tests
uv run pytest tests/unit/

# Run a specific test file
uv run pytest tests/unit/test_metrics_plotter_cleanup.py

# Run tests with coverage report
uv run pytest tests/ --cov=dprl --cov-report=term-missing
```

Test files are located in `tests/` with subdirectories for different test types:
- `tests/unit/`: Unit tests for individual components

## Development Workflow

- Prefer using `uv` over pip/poetry for all package management
- Experiment outputs are saved to `runs/` directory with timestamps
- GPU support via PyTorch CUDA (auto-detected)
- Lines should not be larger than 80 character across all files.

## Active Technologies
- Python 3.13 + Dash 3.3.0, Rich 14.2.0 (already in project), shutil (stdlib) (003-cleanup-assets-folder)
- Local filesystem (assets folder in caller's directory) (003-cleanup-assets-folder)
- Python 3.13 (per constitution) + Dash 3.3.0, Rich 14.2.0, shutil (stdlib) (003-cleanup-assets-folder)
- Python ≥3.13 + Click ≥8.0.0 (CLI), PyYAML ≥6.0 (YAML parsing) (005-yaml-config)
- Local filesystem (YAML config files) (005-yaml-config)
- Python ≥3.13 + Click ≥8.0.0 (CLI), PyYAML ≥6.0 (parsing), (005-yaml-config)
- Python ≥3.13 + Click ≥8.0.0, PyYAML ≥6.0, Pydantic, PyTorch (005-yaml-config)
- Local filesystem (`runs/` directory) (005-yaml-config)

## Recent Changes
- 003-cleanup-assets-folder: Added Python 3.13 + Dash 3.3.0, Rich 14.2.0 (already in project), shutil (stdlib)
