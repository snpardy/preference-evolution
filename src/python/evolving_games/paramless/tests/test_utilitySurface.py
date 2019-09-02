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