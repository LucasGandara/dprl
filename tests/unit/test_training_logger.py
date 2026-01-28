"""
Unit tests for TrainingLogger.
"""

from unittest.mock import MagicMock, patch

import pytest

from dprl.utils.training_logger import TrainingLogger


class TestTrainingLoggerInit:
    """Tests for TrainingLogger initialization."""

    def test_init_with_progress_bar_enabled(self) -> None:
        """Progress bar should be created when enabled."""
        with patch("dprl.utils.training_logger.tqdm") as mock_tqdm:
            mock_pbar = MagicMock()
            mock_tqdm.return_value = mock_pbar

            logger = TrainingLogger(
                epochs=100,
                progress_bar=True,
                table_log_freq=0,
            )

            assert logger.progress_bar_enabled is True
            assert logger.epochs == 100
            assert logger.table_log_freq == 0
            mock_tqdm.assert_called_once_with(
                total=100,
                desc="Training",
                unit="epoch",
            )
            logger.close()

    def test_init_with_progress_bar_disabled(self) -> None:
        """Progress bar should not be created when disabled."""
        with patch("dprl.utils.training_logger.tqdm") as mock_tqdm:
            logger = TrainingLogger(
                epochs=100,
                progress_bar=False,
                table_log_freq=0,
            )

            assert logger.progress_bar_enabled is False
            assert logger._pbar is None
            mock_tqdm.assert_not_called()
            logger.close()


class TestTrainingLoggerUpdate:
    """Tests for TrainingLogger update method."""

    def test_update_sets_postfix(self) -> None:
        """Update should set postfix on progress bar."""
        with patch("dprl.utils.training_logger.tqdm") as mock_tqdm:
            mock_pbar = MagicMock()
            mock_tqdm.return_value = mock_pbar

            logger = TrainingLogger(epochs=10, progress_bar=True)
            logger.update(
                epoch=0,
                loss=0.5,
                reward=100.0,
                steps=50,
            )

            mock_pbar.set_postfix_str.assert_called_once()
            postfix_str = mock_pbar.set_postfix_str.call_args[0][0]
            assert "loss=" in postfix_str
            assert "reward=" in postfix_str
            assert "max_steps=" in postfix_str
            mock_pbar.update.assert_called_once_with(1)
            logger.close()

    def test_update_tracks_max_steps(self) -> None:
        """Update should track maximum steps across epochs."""
        logger = TrainingLogger(epochs=10, progress_bar=False)

        logger.update(epoch=0, loss=0.5, reward=50.0, steps=10)
        assert logger.max_steps == 10

        logger.update(epoch=1, loss=0.4, reward=100.0, steps=25)
        assert logger.max_steps == 25

        logger.update(epoch=2, loss=0.3, reward=75.0, steps=20)
        assert logger.max_steps == 25

        logger.close()


class TestTrainingLoggerTableLogging:
    """Tests for TrainingLogger table logging."""

    def test_table_logging_at_interval(self) -> None:
        """Table should be logged at specified intervals."""
        logger = TrainingLogger(
            epochs=20,
            progress_bar=False,
            table_log_freq=5,
        )

        with patch.object(logger, "_log_table") as mock_log_table:
            for epoch in range(20):
                logger.update(
                    epoch=epoch,
                    loss=0.5,
                    reward=100.0,
                    steps=50,
                )

            assert mock_log_table.call_count == 4
            call_epochs = [
                call[1]["epoch"] for call in mock_log_table.call_args_list
            ]
            assert call_epochs == [4, 9, 14, 19]

        logger.close()

    def test_table_logging_disabled_when_freq_zero(self) -> None:
        """Table should not be logged when frequency is zero."""
        logger = TrainingLogger(
            epochs=20,
            progress_bar=False,
            table_log_freq=0,
        )

        with patch.object(logger, "_log_table") as mock_log_table:
            for epoch in range(20):
                logger.update(
                    epoch=epoch,
                    loss=0.5,
                    reward=100.0,
                    steps=50,
                )

            mock_log_table.assert_not_called()

        logger.close()


class TestTrainingLoggerContextManager:
    """Tests for TrainingLogger context manager."""

    def test_context_manager_closes_properly(self) -> None:
        """Context manager should close progress bar on exit."""
        with patch("dprl.utils.training_logger.tqdm") as mock_tqdm:
            mock_pbar = MagicMock()
            mock_tqdm.return_value = mock_pbar

            with TrainingLogger(epochs=10, progress_bar=True) as logger:
                assert logger._pbar is not None

            mock_pbar.close.assert_called_once()


class TestVPGConfigLoggingFields:
    """Tests for logging fields in VPGConfig."""

    def test_config_fields_in_vpg_config(self) -> None:
        """VPGConfig should include logging fields."""
        from dprl.algorithms.vpg import VPGConfig

        config = VPGConfig(
            epochs=100,
            lr=0.001,
            progress_bar=True,
            table_log_freq=10,
        )

        assert config.progress_bar is True
        assert config.table_log_freq == 10

    def test_config_defaults(self) -> None:
        """VPGConfig should have correct logging defaults."""
        from dprl.algorithms.vpg import VPGConfig

        config = VPGConfig()

        assert config.progress_bar is True
        assert config.table_log_freq == 0
