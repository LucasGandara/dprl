"""
Unit tests for BaseConfig class and related utilities.
"""

from pathlib import Path
from typing import Literal

import pytest
from pydantic import Field, ValidationError

from dprl.utils.config import (
    BaseConfig,
    config_option,
    format_validation_error,
    generate_config_option,
)


class SampleConfig(BaseConfig):
    """Sample config for testing."""

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
        description="Training or evaluation mode",
    )


class TestBaseConfig:
    """Tests for BaseConfig class."""

    def test_default_values(self):
        """Config should use defaults when no values provided."""
        config = SampleConfig()
        assert config.epochs == 50
        assert config.lr == 0.001
        assert config.hidden_units == 64
        assert config.mode == "train"

    def test_custom_values(self):
        """Config should accept custom values."""
        config = SampleConfig(epochs=100, lr=0.01, hidden_units=128, mode="eval")
        assert config.epochs == 100
        assert config.lr == 0.01
        assert config.hidden_units == 128
        assert config.mode == "eval"

    def test_alias_support(self):
        """Config should accept values using aliases."""
        config = SampleConfig(**{"hidden-units": 256})
        assert config.hidden_units == 256

    def test_type_coercion(self):
        """Config should coerce string values to correct types."""
        config = SampleConfig(epochs="100", lr="0.01")
        assert config.epochs == 100
        assert config.lr == 0.01

    def test_extra_fields_forbidden(self):
        """Config should reject unknown fields."""
        with pytest.raises(ValidationError) as exc_info:
            SampleConfig(unknown_field=123)

        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "extra_forbidden"

    def test_invalid_type(self):
        """Config should reject values with wrong type."""
        with pytest.raises(ValidationError) as exc_info:
            SampleConfig(epochs="not a number")

        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert "int" in errors[0]["msg"].lower()

    def test_invalid_literal(self):
        """Config should reject invalid literal values."""
        with pytest.raises(ValidationError) as exc_info:
            SampleConfig(mode="invalid")

        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert "train" in errors[0]["msg"] or "eval" in errors[0]["msg"]

    def test_constraint_violation(self):
        """Config should reject values violating constraints."""
        with pytest.raises(ValidationError) as exc_info:
            SampleConfig(epochs=0)

        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert "greater than or equal to 1" in errors[0]["msg"]


class TestLoadFromYaml:
    """Tests for load_from_yaml method."""

    def test_load_valid_yaml(self, tmp_path: Path):
        """Should load valid YAML config."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text("epochs: 100\nlr: 0.01\n")

        config = SampleConfig.load_from_yaml(config_file)
        assert config.epochs == 100
        assert config.lr == 0.01
        assert config.hidden_units == 64  # default

    def test_load_with_alias(self, tmp_path: Path):
        """Should load YAML with aliased keys."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text("hidden-units: 256\n")

        config = SampleConfig.load_from_yaml(config_file)
        assert config.hidden_units == 256

    def test_load_empty_yaml(self, tmp_path: Path):
        """Should use defaults for empty YAML."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text("")

        config = SampleConfig.load_from_yaml(config_file)
        assert config.epochs == 50
        assert config.lr == 0.001

    def test_file_not_found(self, tmp_path: Path):
        """Should raise FileNotFoundError for missing file."""
        config_file = tmp_path / "nonexistent.yaml"

        with pytest.raises(FileNotFoundError):
            SampleConfig.load_from_yaml(config_file)

    def test_invalid_yaml_syntax(self, tmp_path: Path):
        """Should raise error for malformed YAML."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text("epochs: [invalid yaml")

        with pytest.raises(Exception):
            SampleConfig.load_from_yaml(config_file)

    def test_validation_error_on_load(self, tmp_path: Path):
        """Should raise ValidationError for invalid values."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text("unknown_key: 123\n")

        with pytest.raises(ValidationError):
            SampleConfig.load_from_yaml(config_file)


class TestToClickDefaultMap:
    """Tests for to_click_default_map method."""

    def test_default_map_uses_aliases(self):
        """Should use aliases in default_map."""
        config = SampleConfig(hidden_units=128)
        default_map = config.to_click_default_map()

        assert "hidden-units" in default_map
        assert default_map["hidden-units"] == 128

    def test_default_map_contains_all_fields(self):
        """Should include all fields in default_map."""
        config = SampleConfig()
        default_map = config.to_click_default_map()

        assert "epochs" in default_map
        assert "lr" in default_map
        assert "hidden-units" in default_map
        assert "mode" in default_map


class TestGenerateTemplate:
    """Tests for generate_template method."""

    def test_generates_file(self, tmp_path: Path):
        """Should create template file."""
        output_path = tmp_path / "template.yaml"
        SampleConfig.generate_template(output_path)

        assert output_path.exists()

    def test_includes_defaults(self, tmp_path: Path):
        """Template should include default values."""
        output_path = tmp_path / "template.yaml"
        SampleConfig.generate_template(output_path)

        content = output_path.read_text()
        assert "epochs: 50" in content
        assert "lr: 0.001" in content
        assert "hidden-units: 64" in content

    def test_includes_comments(self, tmp_path: Path):
        """Template should include field descriptions as comments."""
        output_path = tmp_path / "template.yaml"
        SampleConfig.generate_template(output_path)

        content = output_path.read_text()
        assert "# Number of epochs" in content
        assert "# Learning rate" in content

    def test_includes_valid_values_for_literal(self, tmp_path: Path):
        """Template should show valid values for Literal fields."""
        output_path = tmp_path / "template.yaml"
        SampleConfig.generate_template(output_path)

        content = output_path.read_text()
        assert "train" in content and "eval" in content


class TestFormatValidationError:
    """Tests for format_validation_error function."""

    def test_formats_extra_forbidden(self):
        """Should format extra field error with valid fields list."""
        try:
            SampleConfig(unknown=123)
        except ValidationError as e:
            msg = format_validation_error(e, "config.yaml", SampleConfig)

        assert "Configuration Error in 'config.yaml'" in msg
        assert "unknown" in msg
        assert "Extra inputs are not permitted" in msg
        assert "Valid fields:" in msg

    def test_formats_type_error(self):
        """Should format type error with message."""
        try:
            SampleConfig(epochs="not a number")
        except ValidationError as e:
            msg = format_validation_error(e, "config.yaml", SampleConfig)

        assert "epochs" in msg
        assert "int" in msg.lower() or "integer" in msg.lower()


class TestToYaml:
    """Tests for to_yaml method."""

    def test_saves_to_yaml_file(self, tmp_path: Path):
        """Should create YAML file at specified path."""
        config = SampleConfig(epochs=100, lr=0.01)
        output_path = tmp_path / "config.yaml"

        config.to_yaml(output_path)

        assert output_path.exists()

    def test_yaml_contains_values(self, tmp_path: Path):
        """YAML file should contain config values."""
        config = SampleConfig(epochs=100, lr=0.01, hidden_units=128, mode="eval")
        output_path = tmp_path / "config.yaml"

        config.to_yaml(output_path)

        content = output_path.read_text()
        assert "epochs: 100" in content
        assert "lr: 0.01" in content
        assert "hidden-units: 128" in content
        assert "mode: eval" in content

    def test_yaml_uses_aliases(self, tmp_path: Path):
        """YAML should use hyphenated aliases for keys."""
        config = SampleConfig(hidden_units=256)
        output_path = tmp_path / "config.yaml"

        config.to_yaml(output_path)

        content = output_path.read_text()
        assert "hidden-units: 256" in content
        assert "hidden_units" not in content

    def test_yaml_is_valid_and_loadable(self, tmp_path: Path):
        """Saved YAML should be loadable by load_from_yaml."""
        original = SampleConfig(epochs=200, lr=0.005, hidden_units=512)
        output_path = tmp_path / "config.yaml"

        original.to_yaml(output_path)
        loaded = SampleConfig.load_from_yaml(output_path)

        assert loaded.epochs == original.epochs
        assert loaded.lr == original.lr
        assert loaded.hidden_units == original.hidden_units
