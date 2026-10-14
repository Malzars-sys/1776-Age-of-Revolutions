"""Compatibility entry point for the current regional infrastructure validator.

The previous suite assumed unconditional upgrades. Its regression cases
are retained in the new shortage-aware, actual-script AST fixture suite.
These checks do not execute the Victoria 3 engine.
"""
from validate_regional_infrastructure_shortage import run


def run_tests():
    return run()


if __name__ == '__main__':
    run_tests()
