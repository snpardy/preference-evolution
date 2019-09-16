from paramless.utilitySurface import UtilitySurface
import numpy as np


def test_selfless():
    s = UtilitySurface.selfless(10, .1)
    for opp_payoff in s.opponent_payoff:
        my_payoff = np.random.choice(s.my_payoff)
        assert opp_payoff == s.get_utility_by_payoff(my_payoff, opp_payoff)


def test_selfish():
    s = UtilitySurface.selfish(10, .1)
    for my_payoff in s.my_payoff:
        opp_payoff = np.random.choice(s.opponent_payoff)
        assert my_payoff == s.get_utility_by_payoff(my_payoff, opp_payoff)


def test_random():
    # don't really know how to test this.
    pass

def test_real_number_payoffs():
    x = np.arange(0, 10, .3, dtype=float)
    y = np.arange(0, 10, .3, dtype=float)
    selfish = UtilitySurface.selfish(10, 0.3)
    selfless = UtilitySurface.selfless(10, 0.3)
    for i, my_payoff in enumerate(x):
        for j, opp_payoff in enumerate(y):
            assert selfish.get_utility_by_payoff(my_payoff, opp_payoff) == my_payoff
            assert selfless.get_utility_by_payoff(my_payoff, opp_payoff) == opp_payoff
