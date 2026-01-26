# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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

## Development Workflow

- Prefer using `uv` over pip/poetry for all package management
- Experiment outputs are saved to `runs/` directory with timestamps
- GPU support via PyTorch CUDA (auto-detected)
