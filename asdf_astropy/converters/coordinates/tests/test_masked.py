import asdf
import numpy as np
import pytest
from astropy import units as u
from astropy.coordinates import Angle, EarthLocation, Latitude, Longitude, SkyCoord
from astropy.utils.masked import Masked

from asdf_astropy.tests.versions import ASTROPY_GE_7_1

if ASTROPY_GE_7_1:
    from astropy.utils.masked import get_data_and_mask
else:
    pytest.skip(reason="MaskedQuantity support was added in astropy 7.1", allow_module_level=True)


@pytest.mark.parametrize("angle_class", [Angle, Latitude, Longitude])
def test_masked_angle(tmp_path, angle_class):
    angle = [1, 2, 3]
    mask = [False, False, True]
    masked_class = Masked(angle_class)
    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["angle"] = Masked(angle_class(angle * u.deg), mask)
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert isinstance(af["angle"], masked_class)
        out_data, out_mask = get_data_and_mask(af["angle"].to_value(u.deg))
        np.testing.assert_array_equal(out_data, angle)
        np.testing.assert_array_equal(out_mask, mask)


def test_masked_skycoord(tmp_path):
    ra_deg = [0.0, 1.0, 2.0]
    dec_deg = [2.0, 1.0, 0.0]
    mask = [False, False, True]
    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["coord"] = SkyCoord(Masked(ra_deg, mask), Masked(dec_deg, mask), unit=u.deg)
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert af["coord"].ra.unit == u.deg
        assert af["coord"].dec.unit == u.deg

        out_data, out_mask = get_data_and_mask(af["coord"].ra.deg)
        np.testing.assert_array_equal(out_data, ra_deg)
        np.testing.assert_array_equal(out_mask, mask)
        out_data, out_mask = get_data_and_mask(af["coord"].dec.deg)
        np.testing.assert_array_equal(out_data, dec_deg)
        np.testing.assert_array_equal(out_mask, mask)


def test_masked_earth_location(tmp_path):
    x = [0.0, 1.0, 2.0]
    y = [2.0, 1.0, 0.0]
    z = [1.0, 2.0, 0.0]
    mask = [False, False, True]
    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["loc"] = EarthLocation.from_geocentric(Masked(x * u.m, mask), Masked(y * u.m, mask), Masked(z * u.m, mask))
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert af["loc"].x.unit == u.m
        assert af["loc"].y.unit == u.m
        assert af["loc"].z.unit == u.m

        out_data, out_mask = get_data_and_mask(af["loc"].x.to_value(u.m))
        np.testing.assert_array_equal(out_data, x)
        np.testing.assert_array_equal(out_mask, mask)
        out_data, out_mask = get_data_and_mask(af["loc"].y.to_value(u.m))
        np.testing.assert_array_equal(out_data, y)
        np.testing.assert_array_equal(out_mask, mask)
        out_data, out_mask = get_data_and_mask(af["loc"].z.to_value(u.m))
        np.testing.assert_array_equal(out_data, z)
        np.testing.assert_array_equal(out_mask, mask)
