from sys import version_info
from algorithm.parameters import params

def check_python_version():
    """
    Check the python version to ensure it is correct. PonyGE uses Python 3.

    :return: Nothing
    """

    if version_info.major < 3 or (version_info.minor < 5 and
                                  version_info.major == 3):
        s = "\nError: Python version not supported.\n" \
            "       Must use at least Python 3.5."
        raise Exception(s)


def function_builder(string: str):

    if params["GRAMMAR"] == "utility" or params["GRAMMAR"] == "linear":
        def function(my_payoff, opponent_payoff):
            res = eval(string)
            return res
    elif params["GRAMMAR"] == "convex_combination":
        def function(my_payoff, opponent_payoff):
            x = eval(string)
            res = my_payoff + x * opponent_payoff
            return res

    elif params["GRAMMAR"] == "assortative_known":
        def function(my_payoff, opponent_payoff):
            r = params["ASSORTATIVITY"]
            res = eval(string)
            return res

    else:
        raise ValueError("'GRAMMAR' param must be 'utility', 'linear', "
                         "or 'convex_combination'.")
    return function