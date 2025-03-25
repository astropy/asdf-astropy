import importlib.resources

import asdf
import pytest
from astropy import units as u
from astropy.utils.masked import Masked

from asdf_astropy.converters.utils import MaskedClassesRequireAstropy71Error

# FIXME: ASTROPY_LT_7_1: Remove once we depend on astropy >= 7.1.
from asdf_astropy.tests import skip_if_astropy_lt_7_1 as pytestmark  # noqa: F401

from . import resources

MaskedQuantity = Masked(u.Quantity)


def test_masked_quantity_raises():
    with pytest.raises(MaskedClassesRequireAstropy71Error):
        with asdf.open(importlib.resources.files(resources) / "test.asdf"):
            pass
