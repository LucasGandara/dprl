import os
import pickle
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional

import numpy as np
import numpy.typing as npt
import rich
import torch
from pydantic import BaseModel, ConfigDict, field_validator
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

if TYPE_CHECKING:
    from dprl.utils.config import BaseConfig

BASE_DIR = "runs"


class CheckpointMetadata(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        json_encoders={
            np.ndarray: lambda v: v.tolist(),
        },
    )

    policy_state_dict: dict[str, Any]
    rewards: npt.NDArray | None = None
    advantages: npt.NDArray | None = None
    losses: npt.NDArray | None = None
    frames: npt.NDArray | None = None

    @classmethod
    @field_validator("rewards", "advantages", "losses", "frames", mode="before")
    def ensure_numpy_array(cls, v):
        if v is not None and not isinstance(v, np.ndarray):
            return np.array(v)
        return v


def save_experiment_details(
    policy: torch.nn.Module,
    aditional_data: dict[str, np.ndarray | None] | None = None,
    name: str = "",
    config: Optional["BaseConfig"] = None,
) -> None:
    """
    Save experiment checkpoint with optional configuration.

    Args:
        policy: The trained policy network.
        aditional_data: Optional metrics (rewards, losses, etc.).
        name: Experiment name prefix.
        config: Optional config to save for reproducibility.
    """
    if aditional_data is None:
        aditional_data = {}

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"{BASE_DIR}/exp_{name}_{timestamp}"

    os.makedirs(folder_name, exist_ok=True)
    policy_path = os.path.join(folder_name, "policy.tar")

    # Build dict with policy and any provided optional data
    save_dict = {"policy_state_dict": policy.state_dict()}
    save_dict.update({k: v for k, v in aditional_data.items() if v is not None})

    torch.save(save_dict, policy_path)

    # Save config if provided
    if config is not None:
        config_path = Path(folder_name) / "config.yaml"
        config.to_yaml(config_path)

    rich.print(
        f"[green]Experiment details saved in folder: {folder_name}[/green]"
    )


def load_experiment_details(path: str) -> CheckpointMetadata:
    try:
        policy_state_dict = torch.load(path, weights_only=True)
        checkpoint = CheckpointMetadata(**policy_state_dict)
        rich.print(
            "[bold yellow]Warning:[/bold yellow] Do not forget to call model.eval() after loading the model"
        )
        return checkpoint

    except FileNotFoundError:
        rich.print(
            f"[bold red]Failed to load experiment details[/bold red].\nFile not found: {path}"
        )
        exit(1)
    except pickle.UnpicklingError as e:
        console = Console()
        suggested_code = """with torch.serialization.safe_globals([np.ndarray, np._core.multiarray._reconstruct, np.dtype, np.dtypes.Float64DType, np.dtypes.UInt8DType,]):
        model_data = load_experiment_details(*args)"""
        syntax = Syntax(
            suggested_code, "python", theme="monokai", line_numbers=False
        )

        # Print error with suggestion
        console.print(
            "\n[bold red]Error:[/bold red] Failed to load experiment details"
        )
        console.print(f"[yellow]{str(e)}[/yellow]\n")

        console.print(
            Panel(
                syntax,
                title="[bold blue]Suggested Fix: add safe variables context before loading[/bold blue]",
                subtitle="Use safe_globals context manager",
                border_style="blue",
            )
        )
        exit(1)


def load_config_from_experiment(
    experiment_path: str,
    config_class: type["BaseConfig"],
) -> Optional["BaseConfig"]:
    """
    Load configuration from a saved experiment.

    Args:
        experiment_path: Path to experiment folder or policy.tar file.
        config_class: The config class to use for validation.

    Returns:
        Loaded config if config.yaml exists, None otherwise.
    """
    folder = Path(experiment_path)
    if folder.is_file():
        folder = folder.parent

    config_path = folder / "config.yaml"
    if config_path.exists():
        return config_class.load_from_yaml(config_path)
    return None
