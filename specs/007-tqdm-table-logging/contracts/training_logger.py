"""
Contract: TrainingLogger API

This file defines the interface for the TrainingLogger class.
Implementation should follow this contract exactly.
"""

from typing import Protocol


class TrainingLoggerProtocol(Protocol):
    """Protocol defining the TrainingLogger interface."""

    def __init__(
        self,
        epochs: int,
        progress_bar: bool = True,
        table_log_freq: int = 0,
    ) -> None:
        """
        Initialize the training logger.

        Args:
            epochs: Total number of training epochs.
            progress_bar: Whether to show TQDM progress bar.
            table_log_freq: Log metrics table every N epochs (0=disabled).
        """
        ...

    def update(
        self,
        epoch: int,
        loss: float,
        reward: float,
        steps: int,
        advantages: float | None = None,
    ) -> None:
        """
        Update progress bar and optionally log metrics table.

        Args:
            epoch: Current epoch number (0-indexed).
            loss: Policy gradient loss for this epoch.
            reward: Sum of rewards for this epoch.
            steps: Number of steps taken in this epoch.
            advantages: Sum of advantages (optional).
        """
        ...

    def close(self) -> None:
        """
        Clean up resources (close progress bar, etc.).

        Should be called at the end of training.
        """
        ...

    def __enter__(self) -> "TrainingLoggerProtocol":
        """Context manager entry."""
        ...

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit (calls close)."""
        ...
