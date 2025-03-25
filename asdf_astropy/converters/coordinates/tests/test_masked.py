import asdf
import numpy as np
import pytest
from astropy import units as u
from astropy.coordinates import Angle, Latitude, Longitude, SkyCoord
from astropy.utils.masked import Masked

from asdf_astropy.testing.helpers import skip_if_astropy_lt_7_1


@pytest.mark.parametrize("angle_class", [Angle, Latitude, Longitude])
@skip_if_astropy_lt_7_1
def test_masked_angle(tmp_path, angle_class):
    masked_class = Masked(angle_class)
    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["angle"] = Masked(angle_class([1, 2, 3] * u.deg), [False, False, True])
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert isinstance(af["angle"], masked_class)


@skip_if_astropy_lt_7_1
def test_masked_skycoord(tmp_path):
    ra_deg = [0, 1, 2]
    dec_deg = [2, 1, 0]
    mask = [False, False, True]
    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["coord"] = SkyCoord(Masked(ra_deg, mask), Masked(dec_deg, mask), unit=u.deg)
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert af["coord"].ra.unit == u.deg
        assert af["coord"].dec.unit == u.deg
        # FIXME: ASTROPY_LT_7_1: move import to module scope once we depend on astropy >= 7.1
        from astropy.utils.masked import get_data_and_mask

        out_data, out_mask = get_data_and_mask(af["coord"].ra.deg)
        np.testing.assert_array_equal(out_data, ra_deg)
        np.testing.assert_array_equal(out_mask, mask)
        out_data, out_mask = get_data_and_mask(af["coord"].dec.deg)
        np.testing.assert_array_equal(out_data, dec_deg)
        np.testing.assert_array_equal(out_mask, mask)
