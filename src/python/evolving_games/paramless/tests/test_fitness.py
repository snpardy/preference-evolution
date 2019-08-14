import fitness as f


def test_exhaustive_abs():
    """
    fitness.Exhaustive.__abs__() performs abs on all elements in list.
    __abs__ is not implemented for standard lists
    """
    a = [-1, -6, 7]
    abs_a = [1, 6, 7]
    exhaustive_a = f.Exhaustive(a)
    assert abs_a == abs(exhaustive_a)


def test_exhaustive_sub():
    """
    fitness.Exhaustive.__sub__() performs sub between all corresponding elements of list in
    fitness objects given.
    __sub__ is not implemented for standard lists
    """
    fitness_a = f.Exhaustive([3, 8, 3])
    fitness_b = f.Exhaustive([2, 5, 1])

    assert fitness_a - fitness_b == f.Exhaustive([1, 3, 2])


def test_exhaustive_lt():
    """
    Standard lists are compared the same as strings so [1,2,3] < [2,5,1] because 123 < 251.
    Exhaustive fitness compares elements individually and all elements must be less than.
    It is not true that Exhaustive([1,2,3]} < Exhaustive([2,5,1])
    :return:
    """
    # Comparing two Exhaustive fitness objects.
    fitness_a = f.Exhaustive([1, 2, 3])
    fitness_b = f.Exhaustive([2, 5, 1])
    assert not fitness_a < fitness_b

    # If comparing fitness object with something else, (e.g. int) then each element is
    # compared. Comparing standard list with int throws an error.
    assert 5 < f.Exhaustive([7, 9, 23])
    assert not 2 < f.Exhaustive([1, 1, 6])


def test_exhaustive_gt():
    """
    All elements in one fitness object must be greater than the corresponding element in the
    other fitness object.
    All elements in the fitness object must be greater than the value of the single element
    given.
    """
    # Comparing two Exhaustive fitness objects.
    fitness_a = f.Exhaustive([3, 7, 9])
    fitness_b = f.Exhaustive([1, 2, 5])
    fitness_c = f.Exhaustive([4, 9, 1])
    assert fitness_a > fitness_b
    assert not fitness_c > fitness_b

    # If comparing fitness object with something else, (e.g. int) then each element is
    # compared. Comparing standard list with int throws an error.
    assert 5 > f.Exhaustive([2, 4, 3])
    assert not 2 > f.Exhaustive([1, 1, 6])
