"""
Train a VPG agent on CartPole.
This program uses click to parse command line arguments.
to run it use: python vpg_cartpole.py --epochs 800 --lr 0.001 --hidden-layer-units 64 --advantage-expression reward_to_go
After 500 epochs the agent performs well

# Author: Lucas Gandara
# Date: 2025-10-03
"""

import pathlib

import click
import gymnasium
import numpy as np
import torch
from moviepy.video.io import ImageSequenceClip

from dprl.algorithms.vpg import AdvantageExpression, calculate_advantages
from dprl.algorithms.vpg.vpg_utils import (
    calculate_rewards_to_go,
    collect_trajectory,
    create_value_function,
)
from dprl.utils import save_experiment_details

device = "cuda" if torch.cuda.is_available() else "cpu"
if device == "cuda":
    print("Using GPU")
else:
    print("Using CPU")


@click.command()
@click.option("--epochs", default=50, help="Number of epochs to train for.")
@click.option("--lr", default=0.001, help="Learning rate.")
@click.option(
    "--hidden-layer-units", default=64, help="Number of units in the hidden layer."
)
@click.option(
    "--advantage-expression",
    default="reward_to_go",
    help="Advantage expression to use.",
)
def vpg_cartpole(epochs: int, hidden_layer_units, lr, advantage_expression) -> None:
    """Train a VPG agent on CartPole."""
    assert advantage_expression in [
        e.value for e in AdvantageExpression
    ], "Invalid advantage expression"

    print(f"VPG on Gymnasium CartPole-v1 with {hidden_layer_units} hidden layer units")
    print(f"Training for {epochs} epochs...")
    print(f"Using advantage expression: {advantage_expression}")

    env = gymnasium.make("CartPole-v1", render_mode=None)

    # 0. Setup step
    assert isinstance(env.action_space, gymnasium.spaces.Discrete)
    assert isinstance(env.observation_space, gymnasium.spaces.Box)

    input_size = env.observation_space.shape[0]
    output_size = int(env.action_space.n)

    # 0.1 Variables to log
    trajectory_rewards_history = []
    trajectory_losses_history = []
    trajectory_advantages_history = []

    # 1. Input: initial policy parameters theta(0), initial value function parameters phi(0)
    # Neutal network is going to replace the value function.
    value_function = create_value_function(
        input_size, output_size, hidden_layer_units
    ).to(device)
    optimizer = torch.optim.Adam(value_function.parameters(), lr=lr)

    # 2. iteration
    for epoch in range(epochs):
        # 3: Collect a set of trajectories.
        trajectory = collect_trajectory(env, value_function, device)
        trajectory_rewards_history.append(np.sum(trajectory.rewards))

        # 4. Calculate rewards to go
        rewards_to_go = calculate_rewards_to_go(trajectory.rewards)

        # 5. Compute Advantage estimates
        advantages = calculate_advantages(
            trajectory.rewards,
            rewards_to_go,
            value_function,
            advantage_expression=AdvantageExpression(advantage_expression),
        )
        advantages = torch.as_tensor(advantages).to(device)
        trajectory_advantages_history.append(advantages.cpu().numpy().sum())

        # 6. Estimate policy gradients
        log_values = torch.stack(trajectory.log_values).to(device)
        loss = -torch.mean(log_values * advantages)
        trajectory_losses_history.append(loss.item())

        # 7. Compute policy update
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        print(f"Epoch {epoch}, steps: {len(trajectory.rewards)}, Loss: {loss.item()}")

        if len(trajectory.rewards) > 5000:
            break

    env = gymnasium.make("CartPole-v1", render_mode="rgb_array")

    # Collect frames
    frames = []
    done = False
    observation, _ = env.reset()
    while not done:
        observation_as_tensor = torch.as_tensor(observation, dtype=torch.float32).to(
            device
        )
        value = value_function(observation_as_tensor)
        policy = torch.distributions.Categorical(logits=value)
        action = policy.sample().item()

        observation, _, terminated, _, _ = env.step(action)
        frame = env.render()
        frames.append(frame)

        if terminated:
            done = True

    save_experiment_details(
        name="vpg",
        policy=value_function,
        aditional_data={
            "rewards": np.array(trajectory_rewards_history),
            "losses": np.array(trajectory_losses_history),
            "advantages": np.array(trajectory_advantages_history),
            "frames": np.array(frames),
        },
    )

    input("Press Enter to watch the trained agent...")
    env = gymnasium.make("CartPole-v1", render_mode="human")
    collect_trajectory(env, value_function, device=device)


if __name__ == "__main__":
    vpg_cartpole()
