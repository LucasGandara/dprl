"""
Train a VPG agent on Flappy Bird.
This program uses click to parse command line arguments.
to run it use: python vpg_flappy_bird.py --epochs 800 --lr 0.001 --hidden-layer-units 64 --advantage-expression reward_to_go
After 500 epochs the agent performs well

# Author: Lucas Gandara
# Date: 2025-10-03
"""

import click
import gymnasium
import torch

from dprl.algorithms.vpg import (
    AdvantageExpression,
    VPGConfig,
    calculate_advantages,
)
from dprl.algorithms.vpg.vpg_utils import (
    calculate_rewards_to_go,
    collect_trajectory,
    create_value_function,
)
from dprl.envs.flappy_bird import FlappyBird
from dprl.utils import TrainingLogger, save_experiment_details
from dprl.utils.config import config_option, generate_config_option

device = "cuda" if torch.cuda.is_available() else "cpu"
if device == "cuda":
    print("Using GPU")
else:
    print("Using CPU")


@click.command()
@config_option(VPGConfig)
@generate_config_option(VPGConfig)
@click.option("--epochs", default=50, help="Number of epochs to train for.")
@click.option("--lr", default=0.001, help="Learning rate.")
@click.option(
    "--hidden-layer-units",
    default=4,
    type=int,
    help="Number of units in the hidden layer.",
)
@click.option(
    "--advantage-expression",
    default="reward_to_go",
    help="Advantage expression to use.",
)
@click.option(
    "--progress-bar/--no-progress-bar",
    default=True,
    help="Show TQDM progress bar during training.",
)
@click.option(
    "--table-log-freq",
    default=0,
    type=int,
    help="Log metrics table every N epochs (0 to disable).",
)
def vpg_fappy_bird(
    epochs: int,
    hidden_layer_units: int,
    lr: float,
    advantage_expression: str,
    progress_bar: bool,
    table_log_freq: int,
):
    """Train a VPG agent on Flappy Bird."""
    assert advantage_expression in [
        e.value for e in AdvantageExpression
    ], "Invalid advantage expression"

    print(f"VPG on Flappy Bird with {hidden_layer_units} hidden layer units")
    print(f"Training for {epochs} epochs...")
    print(f"Using advantage expression: {advantage_expression}")

    env = FlappyBird(render_mode="human")

    # Setup
    # Setup step
    assert isinstance(env.action_space, gymnasium.spaces.Discrete)
    assert isinstance(env.observation_space, gymnasium.spaces.Dict)

    input_size = len(env.observation_space)
    output_size = env.action_space.n

    print(f"Input size: {input_size}")
    print(f"Output size: {output_size}")

    # 1. Input: initial policy parameters theta(0), initial value function parameters phi(0)
    # Neutal network is going to replace the value function.
    value_function = create_value_function(
        input_size, output_size, hidden_layer_units
    ).to(device)
    optimizer = torch.optim.Adam(value_function.parameters(), lr=lr)

    # 2. iteration
    with TrainingLogger(
        epochs=epochs,
        progress_bar=progress_bar,
        table_log_freq=table_log_freq,
    ) as logger:
        for epoch in range(epochs):
            # 3: Collect a set of trajectories.
            trajectory = collect_trajectory(env, value_function, device)
            epoch_reward = sum(trajectory.rewards)

            # 4. Calculate rewards to go
            rewards_to_go = calculate_rewards_to_go(trajectory.rewards)

            # 5. Compute Advantage estimates
            advantages = calculate_advantages(
                trajectory.rewards,
                rewards_to_go,
                trajectory.values,
                advantage_expression=AdvantageExpression(advantage_expression),
            )
            advantages = torch.as_tensor(advantages).to(device)
            advantages_sum = float(advantages.cpu().numpy().sum())

            # 6. Estimate policy gradients
            log_values = torch.stack(trajectory.log_values).to(device)
            loss = -torch.mean(log_values * advantages)

            # 7. Compute policy update
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

            # Update progress bar and optionally log table
            logger.update(
                epoch=epoch,
                loss=loss.item(),
                reward=epoch_reward,
                steps=len(trajectory.rewards),
                advantages=advantages_sum,
            )

    # Construct config from effective CLI parameters for reproducibility
    config = VPGConfig(
        epochs=epochs,
        lr=lr,
        hidden_layer_units=hidden_layer_units,
        advantage_expression=advantage_expression,
        progress_bar=progress_bar,
        table_log_freq=table_log_freq,
    )

    save_experiment_details(
        name="vpg_flappy",
        policy=value_function,
        config=config,
    )

    env = FlappyBird(render_mode="human")

    for _ in range(2):
        collect_trajectory(env, value_function)


if __name__ == "__main__":
    vpg_fappy_bird()
