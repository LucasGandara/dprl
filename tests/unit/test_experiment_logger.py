"""
Unit tests for experiment_logger module config saving functionality.
"""

from pathlib import Path
from typing import Literal
from unittest.mock import MagicMock

import numpy as np
import pytest
import torch
from pydantic import Field

from dprl.utils.config import BaseConfig
from dprl.utils.experiment_logger import (
    load_config_from_experiment,
    save_experiment_details,
)


class SampleConfig(BaseConfig):
    """Test config for experiment logger tests."""

    epochs: int = Field(default=50, ge=1, description="Number of epochs")
    lr: float = Field(default=0.001, gt=0, description="Learning rate")
    hidden_units: int = Field(
        default=64,
        ge=1,
        alias="hidden-units",
        description="Hidden layer units",
    )
    mode: Literal["train", "eval"] = Field(
        default="train",
        description="Training mode",
    )


class MockPolicy(torch.nn.Module):
    """Simple mock policy for testing."""

    def __init__(self):
        super().__init__()
        self.linear = torch.nn.Linear(4, 2)

    def forward(self, x):
        return self.linear(x)


class TestSaveExperimentDetailsWithConfig:
    """Tests for config saving in save_experiment_details."""

    def test_saves_config_yaml_alongside_policy(self, tmp_path: Path, monkeypatch):
        """Config should be saved as config.yaml in experiment folder."""
        monkeypatch.setattr(
            "dprl.utils.experiment_logger.BASE_DIR", str(tmp_path)
        )

        policy = MockPolicy()
        config = SampleConfig(epochs=100, lr=0.01)

        save_experiment_details(name="test", policy=policy, config=config)

        # Find the created experiment folder
        exp_folders = list(tmp_path.glob("exp_test_*"))
        assert len(exp_folders) == 1

        config_path = exp_folders[0] / "config.yaml"
        assert config_path.exists()

    def test_config_yaml_contains_correct_values(
        self, tmp_path: Path, monkeypatch
    ):
        """Saved config.yaml should contain the config values."""
        monkeypatch.setattr(
            "dprl.utils.experiment_logger.BASE_DIR", str(tmp_path)
        )

        policy = MockPolicy()
        config = SampleConfig(epochs=200, lr=0.005, hidden_units=128)

        save_experiment_details(name="test", policy=policy, config=config)

        exp_folders = list(tmp_path.glob("exp_test_*"))
        config_path = exp_folders[0] / "config.yaml"
        content = config_path.read_text()

        assert "epochs: 200" in content
        assert "lr: 0.005" in content
        assert "hidden-units: 128" in content

    def test_no_config_when_none_provided(self, tmp_path: Path, monkeypatch):
        """No config.yaml should be created when config is None."""
        monkeypatch.setattr(
            "dprl.utils.experiment_logger.BASE_DIR", str(tmp_path)
        )

        policy = MockPolicy()

        save_experiment_details(name="test", policy=policy)

        exp_folders = list(tmp_path.glob("exp_test_*"))
        config_path = exp_folders[0] / "config.yaml"
        assert not config_path.exists()

    def test_backward_compatible_without_config(
        self, tmp_path: Path, monkeypatch
    ):
        """Function should work without config param (backward compat)."""
        monkeypatch.setattr(
            "dprl.utils.experiment_logger.BASE_DIR", str(tmp_path)
        )

        policy = MockPolicy()

        # Should not raise
        save_experiment_details(
            name="test",
            policy=policy,
            aditional_data={"rewards": np.array([1, 2, 3])},
        )

        exp_folders = list(tmp_path.glob("exp_test_*"))
        assert len(exp_folders) == 1
        assert (exp_folders[0] / "policy.tar").exists()


class TestLoadConfigFromExperiment:
    """Tests for load_config_from_experiment function."""

    def test_loads_config_from_experiment_folder(self, tmp_path: Path):
        """Should load config from experiment folder path."""
        # Create experiment folder with config
        exp_folder = tmp_path / "exp_test_20260127_120000"
        exp_folder.mkdir()

        config = SampleConfig(epochs=150, lr=0.002)
        config.to_yaml(exp_folder / "config.yaml")

        loaded = load_config_from_experiment(str(exp_folder), SampleConfig)

        assert loaded is not None
        assert loaded.epochs == 150
        assert loaded.lr == 0.002

    def test_loads_config_from_policy_tar_path(self, tmp_path: Path):
        """Should load config when given path to policy.tar file."""
        exp_folder = tmp_path / "exp_test_20260127_120000"
        exp_folder.mkdir()

        config = SampleConfig(epochs=250, hidden_units=512)
        config.to_yaml(exp_folder / "config.yaml")
        (exp_folder / "policy.tar").touch()  # Create dummy policy file

        loaded = load_config_from_experiment(
            str(exp_folder / "policy.tar"), SampleConfig
        )

        assert loaded is not None
        assert loaded.epochs == 250
        assert loaded.hidden_units == 512

    def test_returns_none_when_config_missing(self, tmp_path: Path):
        """Should return None for old experiments without config.yaml."""
        exp_folder = tmp_path / "exp_old_20260101_000000"
        exp_folder.mkdir()
        (exp_folder / "policy.tar").touch()

        loaded = load_config_from_experiment(str(exp_folder), SampleConfig)

        assert loaded is None

    def test_backward_compat_old_experiments(self, tmp_path: Path):
        """Old experiments without config should still be loadable."""
        exp_folder = tmp_path / "exp_legacy_20250101_000000"
        exp_folder.mkdir()

        # No config.yaml, just policy
        (exp_folder / "policy.tar").touch()

        # Should not raise, just return None
        result = load_config_from_experiment(str(exp_folder), SampleConfig)
        assert result is None
