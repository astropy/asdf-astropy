import astropy
from packaging.version import Version

ASTROPY_LT_7_1 = Version(astropy.__version__) < Version("7.1.dev")
