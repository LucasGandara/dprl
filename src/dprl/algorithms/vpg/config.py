"""
Configuration for Vanilla Policy Gradient (VPG) algorithm.
"""

from typing import Any, Literal

from pydantic import Field, field_validator

from dprl.utils.config import BaseConfig


class VPGConfig(BaseConfig):
    """
    Configuration for VPG training.

    This config defines all hyperparameters for the VPG algorithm.
    Use with @config_option(VPGConfig) to enable YAML config file support.
    """

    epochs: int = Field(
        default=50,
        ge=1,
        description="Number of epochs to train for",
    )

    lr: float = Field(
        default=0.001,
        gt=0,
        description="Learning rate",
    )

    hidden_layer_units: int = Field(
        default=64,
        ge=1,
        alias="hidden-layer-units",
        description="Number of units in the hidden layer",
    )

    advantage_expression: Literal[
        "total_reward", "reward_to_go", "baselined"
    ] = Field(
        default="reward_to_go",
        alias="advantage-expression",
        description="Advantage expression to use",
    )

    @field_validator("advantage_expression", mode="before")
    @classmethod
    def parse_advantage_expression(cls, v: Any) -> str:
        """Convert AdvantageExpression enum to string if needed."""
        if hasattr(v, "value"):
            return str(v.value)
        return str(v)
