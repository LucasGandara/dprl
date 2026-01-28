"""
Unit tests for VPGConfig class.
"""

from pathlib import Path

import pytest
from pydantic import ValidationError

from dprl.algorithms.vpg import VPGConfig


class TestVPGConfig:
    """Tests for VPGConfig class."""

    def test_default_values(self):
        """Config should use defaults when no values provided."""
        config = VPGConfig()
        assert config.epochs == 50
        assert config.lr == 0.001
        assert config.hidden_layer_units == 64
        assert config.advantage_expression == "reward_to_go"

    def test_custom_values(self):
        """Config should accept custom values."""
        config = VPGConfig(
            epochs=100,
            lr=0.01,
            hidden_layer_units=128,
            advantage_expression="baselined",
        )
        assert config.epochs == 100
        assert config.lr == 0.01
        assert config.hidden_layer_units == 128
        assert config.advantage_expression == "baselined"

    def test_alias_hidden_layer_units(self):
        """Config should accept hidden-layer-units alias."""
        config = VPGConfig(**{"hidden-layer-units": 256})
        assert config.hidden_layer_units == 256

    def test_alias_advantage_expression(self):
        """Config should accept advantage-expression alias."""
        config = VPGConfig(**{"advantage-expression": "total_reward"})
        assert config.advantage_expression == "total_reward"

    def test_type_coercion_epochs(self):
        """Config should coerce string epochs to int."""
        config = VPGConfig(epochs="100")
        assert config.epochs == 100
        assert isinstance(config.epochs, int)

    def test_type_coercion_lr(self):
        """Config should coerce string lr to float."""
        config = VPGConfig(lr="0.01")
        assert config.lr == 0.01
        assert isinstance(config.lr, float)

    def test_invalid_epochs_zero(self):
        """Config should reject epochs < 1."""
        with pytest.raises(ValidationError) as exc_info:
            VPGConfig(epochs=0)

        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert "greater than or equal to 1" in errors[0]["msg"]

    def test_invalid_lr_zero(self):
        """Config should reject lr <= 0."""
        with pytest.raises(ValidationError) as exc_info:
            VPGConfig(lr=0)

        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert "greater than 0" in errors[0]["msg"]

    def test_invalid_lr_negative(self):
        """Config should reject negative lr."""
        with pytest.raises(ValidationError) as exc_info:
            VPGConfig(lr=-0.001)

        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert "greater than 0" in errors[0]["msg"]

    def test_invalid_hidden_layer_units_zero(self):
        """Config should reject hidden_layer_units < 1."""
        with pytest.raises(ValidationError) as exc_info:
            VPGConfig(hidden_layer_units=0)

        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert "greater than or equal to 1" in errors[0]["msg"]

    def test_invalid_advantage_expression(self):
        """Config should reject invalid advantage expression."""
        with pytest.raises(ValidationError) as exc_info:
            VPGConfig(advantage_expression="invalid")

        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert (
            "total_reward" in errors[0]["msg"]
            or "reward_to_go" in errors[0]["msg"]
            or "baselined" in errors[0]["msg"]
        )

    def test_extra_fields_forbidden(self):
        """Config should reject unknown fields."""
        with pytest.raises(ValidationError) as exc_info:
            VPGConfig(unknown_param=123)

        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "extra_forbidden"


class TestVPGConfigYaml:
    """Tests for VPGConfig YAML loading."""

    def test_load_valid_yaml(self, tmp_path: Path):
        """Should load valid YAML config."""
        config_file = tmp_path / "vpg_config.yaml"
        config_file.write_text(
            """
epochs: 100
lr: 0.01
hidden-layer-units: 128
advantage-expression: baselined
"""
        )

        config = VPGConfig.load_from_yaml(config_file)
        assert config.epochs == 100
        assert config.lr == 0.01
        assert config.hidden_layer_units == 128
        assert config.advantage_expression == "baselined"

    def test_load_partial_yaml(self, tmp_path: Path):
        """Should use defaults for missing fields."""
        config_file = tmp_path / "vpg_config.yaml"
        config_file.write_text("epochs: 200\n")

        config = VPGConfig.load_from_yaml(config_file)
        assert config.epochs == 200
        assert config.lr == 0.001  # default
        assert config.hidden_layer_units == 64  # default
        assert config.advantage_expression == "reward_to_go"  # default

    def test_load_empty_yaml(self, tmp_path: Path):
        """Should use all defaults for empty YAML."""
        config_file = tmp_path / "vpg_config.yaml"
        config_file.write_text("")

        config = VPGConfig.load_from_yaml(config_file)
        assert config.epochs == 50
        assert config.lr == 0.001
        assert config.hidden_layer_units == 64
        assert config.advantage_expression == "reward_to_go"


class TestVPGConfigClickDefaultMap:
    """Tests for VPGConfig Click integration."""

    def test_default_map_uses_aliases(self):
        """Default map should use hyphenated aliases."""
        config = VPGConfig(hidden_layer_units=256, advantage_expression="baselined")
        default_map = config.to_click_default_map()

        assert default_map["hidden-layer-units"] == 256
        assert default_map["advantage-expression"] == "baselined"

    def test_default_map_all_fields(self):
        """Default map should include all fields."""
        config = VPGConfig()
        default_map = config.to_click_default_map()

        assert "epochs" in default_map
        assert "lr" in default_map
        assert "hidden-layer-units" in default_map
        assert "advantage-expression" in default_map


class TestVPGConfigTemplateGeneration:
    """Tests for VPGConfig template generation."""

    def test_generates_template(self, tmp_path: Path):
        """Should create template file."""
        output_path = tmp_path / "template.yaml"
        VPGConfig.generate_template(output_path)

        assert output_path.exists()

    def test_template_includes_defaults(self, tmp_path: Path):
        """Template should include default values."""
        output_path = tmp_path / "template.yaml"
        VPGConfig.generate_template(output_path)

        content = output_path.read_text()
        assert "epochs: 50" in content
        assert "lr: 0.001" in content
        assert "hidden-layer-units: 64" in content
        assert "advantage-expression: reward_to_go" in content

    def test_template_includes_comments(self, tmp_path: Path):
        """Template should include field descriptions."""
        output_path = tmp_path / "template.yaml"
        VPGConfig.generate_template(output_path)

        content = output_path.read_text()
        assert "# Number of epochs" in content
        assert "# Learning rate" in content
