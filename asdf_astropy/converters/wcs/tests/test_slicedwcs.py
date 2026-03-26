import asdf
import numpy as np
import pytest
from astropy.wcs import WCS
from astropy.wcs.wcsapi.wrappers.sliced_wcs import SlicedLowLevelWCS

from asdf_astropy.testing.helpers import assert_wcs_equal


def create_wcs():
    wcs = WCS(naxis=4)
    wcs.wcs.ctype = "RA---CAR", "DEC--CAR", "FREQ", "TIME"
    wcs.wcs.cunit = "deg", "deg", "Hz", "s"
    wcs.wcs.cdelt = -2.0, 2.0, 3.0e9, 1
    wcs.wcs.crval = 4.0, 0.0, 4.0e9, 3
    wcs.wcs.crpix = 6.0, 7.0, 11.0, 11.0
    wcs.wcs.cname = "Right Ascension", "Declination", "Frequency", "Time"

    wcs0 = SlicedLowLevelWCS(wcs, 1)
    wcs1 = SlicedLowLevelWCS(wcs, [slice(None), slice(None), slice(None), 10])
    wcs3 = SlicedLowLevelWCS(SlicedLowLevelWCS(wcs, slice(None)), [slice(3), slice(None), slice(None), 10])
    wcs_ellipsis = SlicedLowLevelWCS(wcs, [Ellipsis, slice(5, 10)])
    wcs2 = SlicedLowLevelWCS(wcs, np.s_[:, 2, 3, :])
    return [wcs0, wcs1, wcs2, wcs_ellipsis, wcs3]


@pytest.mark.parametrize("sl_wcs", create_wcs())
def test_sliced_wcs_serialization(sl_wcs, tmp_path):
    file_path = tmp_path / "test_slicedwcs.asdf"
    with asdf.AsdfFile() as af:
        af["sl_wcs"] = sl_wcs
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        loaded_sl_wcs = af["sl_wcs"]
        assert_wcs_equal(sl_wcs._wcs, loaded_sl_wcs._wcs)
        assert sl_wcs._slices_array == loaded_sl_wcs._slices_array
