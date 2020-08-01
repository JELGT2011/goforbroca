from typing import List

from goforbroca.util.math import clamp

score_to_sm2_value = {
    0: 0,
    1: 3,
    2: 5,
}


# TODO: tune parameters per user and/or word
def sm2(
        x: List[int],
        alpha: float = 6.0,
        beta: float = -0.8,
        gamma: float = 0.28,
        delta: float = 0.02,
        theta: float = 0.2,
        min_score: float = (1 / 24) * (1 / 60) * 5,
        max_score: float = 180,
) -> float:
    """
    Implements the Supermemo 2 algorithm.
    Reference: https://gist.github.com/doctorpangloss/13ab29abd087dc1927475e560f876797
    """

    correct_x = [x_i >= 3 for x_i in x]

    # TODO: tune this based on answer history
    if not correct_x[-1]:
        return min_score

    # Calculate the latest consecutive answer streak
    num_consecutively_correct = 0
    for correct in reversed(correct_x):
        if not correct:
            break
        num_consecutively_correct += 1

    weighted_history_sum = sum(beta + gamma * x_i + delta * x_i * x_i for x_i in x)
    calculated_score = alpha * weighted_history_sum ** (theta * num_consecutively_correct)
    return clamp(calculated_score, max_score, min_score)


def scores_to_sm2(scores: List[int]) -> float:
    x = [score_to_sm2_value[score] for score in scores]
    return sm2(x)
