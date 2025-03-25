import pytest

from asdf_astropy.converters.utils import import_masked_type
from asdf_astropy.tests.versions import ASTROPY_LT_7_1

if not ASTROPY_LT_7_1:
    pytest.skip(reason="MaskedQuantity support was added in astropy 7.1", allow_module_level=True)


def test_import_masked_type():
    with pytest.raises(AttributeError):
        import_masked_type("ThisClassDoesNotExist")
