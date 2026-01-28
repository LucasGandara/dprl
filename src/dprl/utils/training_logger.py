"""
Training logger with TQDM progress bar and Rich table support.

This module provides the TrainingLogger class for displaying training
progress with TQDM progress bars and periodic Rich table logging.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.console import Console
from rich.table import Table
from tqdm import tqdm

if TYPE_CHECKING:
    from types import TracebackType


class TrainingLogger:
    """
    Training logger with progress bar and table output.

    Provides TQDM progress bar updates and optional Rich table logging
    at configurable intervals during training loops.

    Example:
        with TrainingLogger(epochs=100, progress_bar=True) as logger:
            for epoch in range(100):
                # ... training code ...
                logger.update(
                    epoch=epoch,
                    loss=loss.item(),
                    reward=total_reward,
                    steps=num_steps,
                )
    """

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
        self.epochs = epochs
        self.progress_bar_enabled = progress_bar
        self.table_log_freq = table_log_freq
        self.console = Console()

        self.max_steps: int = 0
        self._pbar: tqdm | None = None

        if self.progress_bar_enabled:
            self._pbar = tqdm(
                total=epochs,
                desc="Training",
                unit="epoch",
            )

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
        if steps > self.max_steps:
            self.max_steps = steps

        if self._pbar is not None:
            self._pbar.set_postfix_str(
                f"reward={reward:>8.1f} | "
                f"loss={loss:>8.4f} | "
                f"max_steps={self.max_steps:>5}"
            )
            self._pbar.update(1)

        if self.table_log_freq > 0 and (epoch + 1) % self.table_log_freq == 0:
            self._log_table(
                epoch=epoch,
                loss=loss,
                reward=reward,
                steps=steps,
                advantages=advantages,
            )

    def _log_table(
        self,
        epoch: int,
        loss: float,
        reward: float,
        steps: int,
        advantages: float | None = None,
    ) -> None:
        """
        Print a Rich table with training metrics.

        Args:
            epoch: Current epoch number.
            loss: Policy gradient loss.
            reward: Sum of rewards.
            steps: Number of steps.
            advantages: Sum of advantages (optional).
        """
        table = Table(title=f"Training Metrics - Epoch {epoch + 1}")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Epoch", str(epoch + 1))
        table.add_row("Steps", str(steps))
        table.add_row("Max Steps", str(self.max_steps))
        table.add_row("Loss", f"{loss:.6f}")
        table.add_row("Reward", f"{reward:.2f}")

        if advantages is not None:
            table.add_row("Advantages", f"{advantages:.2f}")

        self.console.print(table)

    def close(self) -> None:
        """
        Clean up resources (close progress bar, etc.).

        Should be called at the end of training.
        """
        if self._pbar is not None:
            self._pbar.close()
            self._pbar = None

    def __enter__(self) -> TrainingLogger:
        """Context manager entry."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Context manager exit (calls close)."""
        self.close()
