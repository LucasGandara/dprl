"""
Utility functions for deep reinforcement learning.
"""

import logging
import random
from pathlib import Path
from typing import Any

import numpy as np
import torch

from .config import (
    BaseConfig,
    config_option,
    format_validation_error,
    generate_config_option,
)
from .experiment_logger import (
    load_config_from_experiment,
    save_experiment_details,
)
from .metrics_plotter import MetricsPlotter
from .training_logger import TrainingLogger


def set_seed(seed: int = 42):
    """
    Set random seeds for reproducible results.

    Args:
        seed: Random seed value
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)

    # For deterministic behavior (may reduce performance)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def setup_logging(
    log_file: str | None = None, level: str = "INFO"
) -> logging.Logger:
    """
    Set up logging configuration.

    Args:
        log_file: Optional log file path
        level: Logging level

    Returns:
        Configured logger
    """
    logger = logging.getLogger("dprl")
    logger.setLevel(getattr(logging, level.upper()))

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def count_parameters(model: torch.nn.Module) -> int:
    """
    Count the number of trainable parameters in a model.

    Args:
        model: PyTorch model

    Returns:
        Number of trainable parameters
    """
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def save_config(config: dict[str, Any], path: str):
    """
    Save configuration to a YAML file.

    Args:
        config: Configuration dictionary
        path: Path to save the config file
    """
    import yaml

    Path(path).parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, indent=2)


def load_config(path: str) -> dict[str, Any]:
    """
    Load configuration from a YAML file.

    Args:
        path: Path to the config file

    Returns:
        Configuration dictionary
    """
    import yaml

    with open(path) as f:
        result = yaml.safe_load(f)
        if result is None:
            return {}
        return dict(result)


def get_device() -> torch.device:
    """
    Get the appropriate device (CPU/GPU).

    Returns:
        torch.device object
    """
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif torch.backends.mps.is_available():  # Apple Silicon
        return torch.device("mps")
    else:
        return torch.device("cpu")


__all__ = [
    "BaseConfig",
    "config_option",
    "count_parameters",
    "format_validation_error",
    "generate_config_option",
    "get_device",
    "load_config",
    "load_config_from_experiment",
    "load_experiment_details",
    "MetricsPlotter",
    "save_config",
    "save_experiment_details",
    "set_seed",
    "setup_logging",
    "TrainingLogger",
]
