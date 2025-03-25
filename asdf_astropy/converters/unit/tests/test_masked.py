import importlib.resources

import asdf
import numpy as np
import pytest
from astropy import units as u
from astropy.utils.masked import Masked

from asdf_astropy.converters.utils import MaskedClassesRequireAstropy71Error
from asdf_astropy.tests import only_if_astropy_lt_7_1, skip_if_astropy_lt_7_1

from . import resources

MaskedQuantity = Masked(u.Quantity)


@only_if_astropy_lt_7_1
def test_masked_quantity_raises():
    with pytest.raises(MaskedClassesRequireAstropy71Error):
        with asdf.open(importlib.resources.files(resources) / "test.asdf"):
            pass


@skip_if_astropy_lt_7_1
def test_masked_quantity(tmp_path):
    data = [1, 2, 3]
    mask = [False, False, True]
    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["quantity"] = Masked(data, mask) * u.yottamole
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert isinstance(af["quantity"], MaskedQuantity)
        assert af["quantity"].unit == u.yottamole
        # FIXME: ASTROPY_LT_7_1: move import to module scope once we depend on astropy >= 7.1
        from astropy.utils.masked import get_data_and_mask

        result_data, result_mask = get_data_and_mask(af["quantity"].value)
        np.testing.assert_array_equal(result_data, data)
        np.testing.assert_array_equal(result_mask, mask)
