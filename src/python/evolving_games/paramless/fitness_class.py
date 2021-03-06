"""
Created on 2019-05-10
@summary: A file that defines classes for fitness objects that overload
a number of operators to maintain generality of the fitness comparison in
paramless.evolution_step
@author: snpardy
"""


class Exhaustive(list):
    """
    Operations are overwritten so that they're performed on all fitnesses in the fitness list.
    If two lists are given, the corresponding fitness from each list are compared/summed/etc.
    E.g. all fitness values in one must be greater than the corresponding fitness
    value in the other.
    @todo: change to subclass numpy array
    """

    def __gt__(self, other):

        if isinstance(other, Exhaustive):
            # if comparing two Fitness objects, every fitness much be greater
            # than the corresponding fitness in other
            for s, o in zip(self, other):
                if not s > o:
                    break
            else:
                return True
            return False

        else:
            # if comparing to something else (e.g. float) every fitness element
            # must be greater than other
            for s in self:
                if not s > other:
                    break
            else:
                return True
            return False

    def __lt__(self, other):
        if isinstance(other, Exhaustive):
            # if comparing two Fitness objects, every fitness much be less than
            # the corresponding fitness in other
            for s, o in zip(self, other):
                if not s < o:
                    break
            else:
                return True
            return False

        else:
            # if comparing to something else (e.g. float) every fitness element
            # must be less than other
            for s in self:
                if not s < other:
                    break
            else:
                return True
            return False

    def __ge__(self, other):
        if type(other) == type(self):
            # if comparing two Fitness objects, every fitness much be greater than
            # the corresponding fitness in other
            for s, o in zip(self, other):
                if not s >= o:
                    break
            else:
                return True
            return False

        else:
            # if comparing to something else (e.g. float) every fitness element
            # must be greater than other
            for s in self:
                if not s >= other:
                    break
            else:
                return True
            return False

    def __le__(self, other):
        if isinstance(other, Exhaustive):
            # if comparing two Fitness objects, every fitness much be less than
            # or equal to the corresponding fitness in other
            for s, o in zip(self, other):
                if not s <= o:
                    break
            else:
                return True
            return False

        else:
            # if comparing to something else (e.g. float) every fitness element
            # must be less than or equal to other
            for s in self:
                if not s <= other:
                    break
            else:
                return True
            return False

    def __sub__(self, other):
        if isinstance(other, Exhaustive):
            return Exhaustive([s_i - o_i for s_i, o_i in zip(self, other)])
        else:
            return NotImplemented

    def __add__(self, other):
        if isinstance(other, Exhaustive):
            return Exhaustive([s_i + o_i for s_i, o_i in zip(self, other)])
        else:
            return NotImplemented

    def __abs__(self):
        return Exhaustive([abs(x) for x in self])
