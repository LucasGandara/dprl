import os
import pickle
from datetime import datetime
from typing import Any, Optional

import numpy as np
import rich
import torch
from pydantic import BaseModel, ConfigDict
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

BASE_DIR = "runs"


class CheckpointMetadata(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra="forbid")

    policy_state_dict: dict[str, Any]
    rewards: Optional[np.typing.NDArray[Any]]
    losses: Optional[np.typing.NDArray[Any]]
    frames: Optional[np.typing.NDArray[Any]]


def save_experiment_details(
    policy: torch.nn.Module,
    aditional_data: dict[str, Optional[np.ndarray]] = {},
    name: str = "",
) -> None:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"{BASE_DIR}/exp_{name}_{timestamp}"

    os.makedirs(folder_name, exist_ok=True)
    policy_path = os.path.join(folder_name, "policy.tar")

    # Build dict with policy and any provided optional data
    save_dict = {"policy_state_dict": policy.state_dict()}
    save_dict.update({k: v for k, v in aditional_data.items() if v is not None})

    torch.save(save_dict, policy_path)
    print(f"Experiment details saved in folder: {folder_name}")


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
        syntax = Syntax(suggested_code, "python", theme="monokai", line_numbers=False)

        # Print error with suggestion
        console.print("\n[bold red]Error:[/bold red] Failed to load experiment details")
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
