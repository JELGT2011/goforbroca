from typing import List

import matplotlib.pyplot as plt

from goforbroca.util.sm2 import sm2

minutes_in_a_day = 24 * 60


def standard_sm2(scores: List[int]) -> float:
    return sm2(scores, alpha=6.0, beta=-0.8, gamma=0.28, delta=0.02, theta=0.2)


def main():
    scores = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    t = [i + 1 for i in range(len(scores))]
    standard = [standard_sm2(scores[:i + 1]) for i in range(len(scores))]
    delays = [sm2(scores[:i + 1]) for i in range(len(scores))]

    print(f'standard (days) = {standard}')
    print(f'delays (days) = {delays}')
    print(f'standard (minutes) = {[n * minutes_in_a_day for n in standard]}')
    print(f'delays (minutes) = {[n * minutes_in_a_day for n in delays]}')

    fig, ax = plt.subplots()
    ax.plot(t, standard, color='blue', marker='o')
    ax.plot(t, delays, color='red', marker='o')
    ax.set_xlabel('attempts')
    ax.set_ylabel('delay (days)')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    main()
