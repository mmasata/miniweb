from .uunittest import main as run_unit_tests
from .routeTest import *
from .middlewareTest import *


def run_all_tests():
    run_unit_tests("miniwebTest")
