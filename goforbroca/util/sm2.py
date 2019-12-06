from typing import List


def sm2(x: List[int], alpha: float = 6.0, beta: float = -0.8, gamma: float = 0.28, delta: float = 0.02,
        theta: float = 0.2) -> float:
    """
    Returns the number of days to delay the next review of an item by, fractionally, based on the history of answers
    Reference: https://gist.github.com/doctorpangloss/13ab29abd087dc1927475e560f876797
    x == 0: Incorrect, Hardest
    x == 1: Incorrect, Hard
    x == 2: Incorrect, Medium
    x == 3: Correct, Medium
    x == 4: Correct, Easy
    x == 5: Correct, Easiest
    @param x The history of answers in the above scoring.
    @param alpha tuning parameter
    @param beta tuning parameter
    @param gamma tuning parameter
    @param delta tuning parameter
    @param theta When larger, the delays for correct answers will increase.
    """
    assert all(0 <= x_i <= 5 for x_i in x)
    correct_x = [x_i >= 3 for x_i in x]
    # If you got the last question incorrect, just return 1
    if not correct_x[-1]:
        return 1.0

    # Calculate the latest consecutive answer streak
    num_consecutively_correct = 0
    for correct in reversed(correct_x):
        if correct:
            num_consecutively_correct += 1
        else:
            break

    weighted_history_sum = sum(beta + gamma * x_i + delta * x_i * x_i for x_i in x)
    return alpha * (max(1.3, 2.5 + weighted_history_sum)) ** (theta * num_consecutively_correct)
