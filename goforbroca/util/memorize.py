from collections import Counter
from typing import List, Optional

import numpy as np

right = -0.0061
wrong = -0.0802
bias = 7.2145

# TODO: tune parameter per user and/or word
alpha = 2 * 0.051345788818587285

Q = 1.0  # parameter q defined in eq. 8 in the paper.
T = 10.0  # number of days in the future to generate reviewing timeself.

score_to_memorize_wrong = frozenset([0])
score_to_memorize_correct = frozenset([1, 2])


def intensity(t, n_t):
    return 1.0 / np.sqrt(Q) * (1 - np.exp(-n_t * t))


# TODO: either I broke this while reverse engineering it from its previously convoluted state,
#   or there is something wrong this algorithm
def memorize(n_t) -> Optional[float]:
    """
    Implements the memorize algorithm.
    Reference: https://github.com/Networks-Learning/memorize
    """

    t = 0
    while True:
        max_int = 1.0 / np.sqrt(Q)
        t_ = np.random.exponential(1 / max_int)
        if t_ + t > T:
            return None

        t = t + t_
        proposed_int = intensity(t, n_t)
        if np.random.uniform(0, 1, 1)[0] < proposed_int / max_int:
            return t


def scores_to_memorize(scores: List[int]) -> float:
    counter = Counter(scores)
    n_correct = sum(v for k, v in counter.items() if k in score_to_memorize_correct)
    n_wrong = sum(v for k, v in counter.items() if k in score_to_memorize_wrong)
    n_t = alpha ** (-(right * n_correct + wrong * n_wrong))
    return memorize(n_t)
