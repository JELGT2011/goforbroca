from typing import List

score_to_sm2_value = {
    0: 0,
    1: 3,
    2: 5,
}


# original parameter values:
#   alpha: float = 6.0,
#   beta: float = -0.8,
#   gamma: float = 0.28,
#   delta: float = 0.02,
#   theta: float = 0.2,
def sm2(
        x: List[int],
        alpha: float = 0.015,
        beta: float = -0.5,
        gamma: float = 0.35,
        delta: float = 0.04,
        theta: float = 0.25,
        min_score: float = 1.3,
        max_score: float = 180,
        given_score: float = 2.5,
) -> float:
    """
    Implements the Supermemo 2 algorithm.
    Reference: https://gist.github.com/doctorpangloss/13ab29abd087dc1927475e560f876797
    """

    correct_x = [x_i >= 3 for x_i in x]

    # TODO: tune this based on answer history
    if not correct_x[-1]:
        return 1.0

    # Calculate the latest consecutive answer streak
    num_consecutively_correct = 0
    for correct in reversed(correct_x):
        if not correct:
            break
        num_consecutively_correct += 1

    weighted_history_sum = sum(beta + gamma * x_i + delta * x_i * x_i for x_i in x)
    base = max(min_score, given_score + weighted_history_sum)
    calculated_score = alpha * base ** (theta * num_consecutively_correct)
    return min(max_score, calculated_score)


def scores_to_sm2(scores: List[int]) -> float:
    x = [score_to_sm2_value[score] for score in scores]
    return sm2(x)
