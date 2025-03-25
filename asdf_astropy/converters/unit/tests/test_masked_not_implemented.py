import importlib.resources

import asdf
import pytest
from astropy import units as u
from astropy.utils.masked import Masked

from asdf_astropy.tests.versions import ASTROPY_LT_7_1

if not ASTROPY_LT_7_1:
    pytest.skip(reason="MaskedQuantity support was added in astropy 7.1", allow_module_level=True)

from . import resources

MaskedQuantity = Masked(u.Quantity)


def test_masked_quantity_raises():
    with pytest.raises(NotImplementedError):
        with asdf.open(importlib.resources.files(resources) / "test.asdf"):
            pass
