from collections import namedtuple
from enum import Enum

VPGTrajectory = namedtuple("VPGTrajectory", ["rewards", "log_values"])


class AdvantageExpression(Enum):
    TOTAL_REWARD = "total_reward"
    REWARD_TO_GO = "reward_to_go"
    REWARD_TO_GO_BASELINED = "reward_to_go_baselined"


def calculate_advantages(
    rewards: list[float],
    rewards_to_go: list[float],
    values: list[float],
    advantage_expression: AdvantageExpression = AdvantageExpression.REWARD_TO_GO,
) -> list[float]:
    """Calculate the advantages for a trajectory

    Args:
        rewards_to_go (list[float]): List of rewards to go for a trajectory
        value_function (torch.nn.Module): Value function to use for policy
        advantage_expression (AdvantageExpression): Advantage expression to use

    Returns:
        list[float]: List of advantages for a trajectory
    """

    match advantage_expression:
        case AdvantageExpression.TOTAL_REWARD:
            return rewards
        case AdvantageExpression.REWARD_TO_GO:
            return rewards_to_go
        case AdvantageExpression.REWARD_TO_GO_BASELINED:
            return rewards_to_go - values
