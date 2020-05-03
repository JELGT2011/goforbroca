from typing import List

score_to_sm2_value = {
    0: 0,
    1: 3,
    2: 5,
}


def sm2(x: List[int],
        alpha: float = 6.0,
        beta: float = -0.8,
        gamma: float = 0.28,
        delta: float = 0.02,
        theta: float = 0.2) -> float:
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
    return alpha * (max(1.3, 2.5 + weighted_history_sum)) ** (theta * num_consecutively_correct)


def scores_to_sm2(scores: List[int]) -> float:
    history = [score_to_sm2_value[score] for score in scores]
    return sm2(history)
