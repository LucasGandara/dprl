"""
Utils files for VPG algorithm

Author: Lucas Gandara
"""

import gymnasium
import torch

from .vpg import VPGTrajectory


def create_value_function(
    input_size: int, output_size: int, hidden_layer_units: int = 64
) -> torch.nn.Module:
    """Create the value function model

    Args:
        input_size (int): Number of features in the (flat) observation tensor
        output_size (int): Number of actions
        hidden_layer_units (int): Number of units in the hidden layer

    Returns:
        nn.Module: Simple MLP model
    """

    return torch.nn.Sequential(
        torch.nn.Linear(in_features=input_size, out_features=hidden_layer_units),
        torch.nn.ReLU(),
        torch.nn.Linear(in_features=hidden_layer_units, out_features=output_size),
    )


def collect_trajectory(
    env: gymnasium.Env,
    value_function: torch.nn.Module,
    device: str = "cpu",
) -> VPGTrajectory:
    """Collect a trajectory from the environment

    Args:
        env (gymnasium.Env): Environment to collect a trajectory from
        value_function (torch.nn.Module): Value function to use for policy
    """

    observation, _ = env.reset()

    episode_return = 0.0
    rewards = []
    log_values = []

    while True:
        observation_as_tensor = torch.as_tensor(observation, dtype=torch.float32).to(
            device
        )
        value = value_function(observation_as_tensor)
        policy = torch.distributions.Categorical(logits=value)
        action = policy.sample().item()
        log_probability_action = policy.log_prob(torch.as_tensor(action).to(device))

        observation, reward, done, _, _ = env.step(action)

        log_values.append(log_probability_action.to("cpu"))
        rewards.append(float(reward))

        episode_return += float(reward)

        if done:
            break

    return VPGTrajectory(rewards=rewards, log_values=log_values)


def calculate_rewards_to_go(rewards: list[float]) -> list[float]:
    """Calculate the rewards to go for a trajectory

    Args:
        rewards (list[float]): List of rewards for a trajectory

    Returns:
        list[float]: List of rewards to go for a trajectory
    """
    rewards_to_go = []
    running_add = 0
    for reward in reversed(rewards):
        running_add = reward * 0.99 + running_add
        rewards_to_go.append(running_add)
    return rewards_to_go[::-1]  # reverse the list
