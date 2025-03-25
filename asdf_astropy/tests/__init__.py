import astropy
import pytest
from packaging.version import Version

ASTROPY_LT_7_1 = Version(astropy.__version__) < Version("7.1.dev")
only_if_astropy_lt_7_1 = pytest.mark.skipif(not ASTROPY_LT_7_1, reason="This test requires astropy >= 7.1.dev")
skip_if_astropy_lt_7_1 = pytest.mark.skipif(ASTROPY_LT_7_1, reason="This test requires astropy < 7.1.dev")
