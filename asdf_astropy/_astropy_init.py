import os

from astropy.tests.runner import TestRunner

__all__ = ["__version__", "test"]

from ._version import version as __version__

# Create the test function for self test
test = TestRunner.make_test_runner_in(os.path.dirname(__file__))
