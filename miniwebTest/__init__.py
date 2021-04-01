from .uunittest import main as run_unit_tests
from .routeTest import *
from .middlewareTest import *
from .controllerTest import *
from .messageTest import *


def run_all_tests():
    """
    Function for run all unit tests.
    :return: None
    """
    run_unit_tests("miniwebTest")
