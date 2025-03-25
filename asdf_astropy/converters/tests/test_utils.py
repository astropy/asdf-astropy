import pytest

from asdf_astropy.converters.utils import import_masked_type
from asdf_astropy.tests.versions import ASTROPY_LT_7_1


def test_import_masked_type():
    with pytest.raises(NotImplementedError if ASTROPY_LT_7_1 else AttributeError):
        import_masked_type("ThisClassDoesNotExist")
