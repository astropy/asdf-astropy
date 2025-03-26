import asdf
import numpy as np
import pytest
from astropy import units as u
from astropy.utils.masked import Masked

from asdf_astropy.tests.versions import ASTROPY_LT_7_1

if ASTROPY_LT_7_1:
    pytest.skip(reason="MaskedQuantity support was added in astropy 7.1", allow_module_level=True)
else:
    from astropy.utils.masked import get_data_and_mask

MaskedQuantity = Masked(u.Quantity)


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
