"""
VPG Algorithm

This module contains the implementation of the VPG algorithm.
"""

from .vpg import AdvantageExpression, VPGTrajectory, calculate_advantages

__all__ = ["AdvantageExpression", "VPGTrajectory", "calculate_advantages"]

# keep this list sorted
assert __all__ == sorted(__all__)
