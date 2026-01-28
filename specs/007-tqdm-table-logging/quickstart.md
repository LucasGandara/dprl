# Quickstart: TQDM and Table Logging

## Basic Usage

### Default Behavior (TQDM Progress Bar)

Run training with default settings - progress bar is enabled automatically:

```bash
uv run python examples/vpg_cartpole.py --epochs 100
```

Output:
```
Training: 45%|████████████████                    | 45/100 [00:12<00:14]
         loss=0.0234 reward=195.0
```

### Disable Progress Bar

Use `--no-progress-bar` for minimal output:

```bash
uv run python examples/vpg_cartpole.py --epochs 100 --no-progress-bar
```

### Enable Table Logging

Log detailed metrics table every 20 epochs:

```bash
uv run python examples/vpg_cartpole.py --epochs 100 --table-log-freq 20
```

Output includes periodic tables:
```
┌────────────────────────────────┐
│   Training Metrics - Epoch 20  │
├────────────┬───────────────────┤
│ Metric     │ Value             │
├────────────┼───────────────────┤
│ Epoch      │ 20                │
│ Steps      │ 185               │
│ Loss       │ 0.0234            │
│ Reward     │ 185.0             │
│ Max Reward │ 195.0             │
│ Advantages │ 1234.5            │
└────────────┴───────────────────┘
```

## Configuration via YAML

Create a config file (`my_config.yaml`):

```yaml
# Training parameters
epochs: 200
lr: 0.001
hidden-layer-units: 128
advantage-expression: reward_to_go

# Logging options
progress-bar: true
table-log-freq: 25
```

Run with config:

```bash
uv run python examples/vpg_cartpole.py --config my_config.yaml
```

### Generate Config Template

Generate a template with all options:

```bash
uv run python examples/vpg_cartpole.py --generate-config
```

## CLI Overrides Config

CLI arguments take precedence over config file:

```bash
# Config has progress-bar: true, but CLI disables it
uv run python examples/vpg_cartpole.py \
    --config my_config.yaml \
    --no-progress-bar
```

## Programmatic Usage

```python
from dprl.utils.training_logger import TrainingLogger

# Create logger with config
with TrainingLogger(
    epochs=100,
    progress_bar=True,
    table_log_freq=20
) as logger:
    for epoch in range(100):
        # ... training code ...
        logger.update(
            epoch=epoch,
            loss=loss.item(),
            reward=sum(rewards),
            steps=len(rewards),
            advantages=advantages_sum,
        )
```
