import pytest

from asdf_astropy.converters.utils import import_masked_type
from asdf_astropy.tests import skip_if_astropy_lt_7_1


@skip_if_astropy_lt_7_1
def test_import_masked_type():
    with pytest.raises(AttributeError):
        import_masked_type("ThisClassDoesNotExist")
