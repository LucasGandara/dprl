"""
Example of loading a saved VPG policy model and evaluating it on the CartPole environment.

This script will load one episode of your saved model and then render the metrics you set.

# Author: Lucas Gandara
# Date: 2026-01-15
"""

import click
import gymnasium
import numpy as np
import torch

from dprl.algorithms.vpg.vpg_utils import create_value_function
from dprl.utils import MetricsPlotter
from dprl.utils.experiment_logger import load_experiment_details

device = "cuda" if torch.cuda.is_available() else "cpu"
if device == "cuda":
    print("Using GPU")
else:
    print("Using CPU")


@click.command()
@click.option(
    "--model-path",
    default="runs/exp_/policy.tar",
    help="Path to the saved model.",
    type=str,
)
@click.option("--episodes", default=1, help="Number of episodes to evaluate.", type=int)
def vpg_cartpole_from_saved_model(model_path: str, episodes: int) -> None:
    """Load a saved VPG policy model and evaluate it on the CartPole environment."""
    with torch.serialization.safe_globals(
        [
            np.ndarray,
            np._core.multiarray._reconstruct,  # type: ignore[attr-defined]
            np.dtype,
            np.dtypes.Float64DType,
            np.dtypes.Float32DType,
            np.dtypes.UInt8DType,
        ]
    ):
        model_checkpoint = load_experiment_details(model_path)

    metrics_plotter = MetricsPlotter()
    assert model_checkpoint.rewards is not None
    assert model_checkpoint.losses is not None
    assert model_checkpoint.frames is not None
    assert model_checkpoint.advantages is not None
    metrics_plotter.add_metrics_via_dict(
        {
            "Episodes Returns": model_checkpoint.rewards.tolist(),
            "Episodes Losses": model_checkpoint.losses.tolist(),
            "Episodes Advantages": model_checkpoint.advantages.tolist(),
        }
    )
    metrics_plotter.add_video_from_frames(
        "Sample Episode Video",
        model_checkpoint.frames,
        fps=30,
        video_filename="sample_episode.mp4",
    )
    print(f"Video saved, total frames: {len(model_checkpoint.frames)}")

    env = gymnasium.make("CartPole-v1", render_mode="human")

    assert isinstance(env.observation_space, gymnasium.spaces.Box)
    assert isinstance(env.action_space, gymnasium.spaces.Discrete)

    input_size = env.observation_space.shape[0]
    output_size = int(env.action_space.n)

    value_function = create_value_function(input_size, output_size, 64).to(device)
    value_function.load_state_dict(model_checkpoint.policy_state_dict)
    value_function.eval()

    env.close()

    metrics_plotter.plot_metrics()


if __name__ == "__main__":
    vpg_cartpole_from_saved_model()
