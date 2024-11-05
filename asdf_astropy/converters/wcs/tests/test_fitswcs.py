import numpy as np
import pytest
from astropy.wcs import WCS, DistortionLookupTable, Sip

from asdf_astropy.testing.helpers import assert_wcs_roundtrip


def create_sip_distortion_wcs():
    rng = np.random.default_rng(42)
    wcs = WCS(naxis=2)
    wcs.wcs.crval = [251.29, 57.58]
    wcs.wcs.cdelt = [1, 1]
    wcs.wcs.crpix = [507, 507]
    wcs.wcs.pc = np.array([[7.7e-6, 3.3e-5], [3.7e-5, -6.8e-6]])
    wcs._naxis = [1014, 1014]
    wcs.wcs.ctype = ["RA---TAN-SIP", "DEC--TAN-SIP"]

    # Generate random SIP coefficients
    a = rng.uniform(low=-1e-5, high=1e-5, size=(5, 5))
    b = rng.uniform(low=-1e-5, high=1e-5, size=(5, 5))

    # Assign SIP coefficients
    wcs.sip = Sip(a, b, None, None, wcs.wcs.crpix)
    wcs.wcs.set()

    return wcs


def create_tabular_wcs():
    # Creates a WCS object with distortion lookup tables
    img_world_wcs = WCS(naxis=2)
    img_world_wcs.wcs.crpix = 1, 1
    img_world_wcs.wcs.crval = 0, 0
    img_world_wcs.wcs.cdelt = 1, 1

    # Create maps with zero distortion except at one particular pixel
    x_dist_array = np.zeros((25, 25))
    x_dist_array[10, 20] = 0.5
    map_x = DistortionLookupTable(
        x_dist_array.astype(np.float32),
        (5, 10),
        (10, 20),
        (2, 2),
    )
    y_dist_array = np.zeros((25, 25))
    y_dist_array[10, 5] = 0.7
    map_y = DistortionLookupTable(
        y_dist_array.astype(np.float32),
        (5, 10),
        (10, 20),
        (3, 3),
    )

    img_world_wcs.cpdis1 = map_x
    img_world_wcs.cpdis2 = map_y

    return img_world_wcs


@pytest.mark.parametrize("version", ["1.5.0", "1.6.0"])
@pytest.mark.parametrize("wcs_gen", [create_tabular_wcs, create_sip_distortion_wcs])
def test_roundtrip(wcs_gen, tmp_path, version):
    wcs = wcs_gen()
    assert_wcs_roundtrip(wcs, tmp_path, version)
