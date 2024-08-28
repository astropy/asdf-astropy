import asdf
import numpy as np
import pytest
from astropy import wcs


def create_sip_distortion_wcs():
    rng = np.random.default_rng()
    twcs = wcs.WCS(naxis=2)
    twcs.wcs.crval = [251.29, 57.58]
    twcs.wcs.cdelt = [1, 1]
    twcs.wcs.crpix = [507, 507]
    twcs.wcs.pc = np.array([[7.7e-6, 3.3e-5], [3.7e-5, -6.8e-6]])
    twcs._naxis = [1014, 1014]
    twcs.wcs.ctype = ["RA---TAN-SIP", "DEC--TAN-SIP"]

    # Generate random SIP coefficients
    a = rng.uniform(low=-1e-5, high=1e-5, size=(5, 5))
    b = rng.uniform(low=-1e-5, high=1e-5, size=(5, 5))

    # Assign SIP coefficients
    twcs.sip = wcs.Sip(a, b, None, None, twcs.wcs.crpix)
    twcs.wcs.set()

    # Creates a WCS object with distortion lookup tables
    img_world_wcs = wcs.WCS(naxis=2)
    img_world_wcs.wcs.crpix = 1, 1
    img_world_wcs.wcs.crval = 0, 0
    img_world_wcs.wcs.cdelt = 1, 1

    # Create maps with zero distortion except at one particular pixel
    x_dist_array = np.zeros((25, 25))
    x_dist_array[10, 20] = 0.5
    map_x = wcs.DistortionLookupTable(
        x_dist_array.astype(np.float32),
        (5, 10),
        (10, 20),
        (2, 2),
    )
    y_dist_array = np.zeros((25, 25))
    y_dist_array[10, 5] = 0.7
    map_y = wcs.DistortionLookupTable(
        y_dist_array.astype(np.float32),
        (5, 10),
        (10, 20),
        (3, 3),
    )

    img_world_wcs.cpdis1 = map_x
    img_world_wcs.cpdis2 = map_y

    return (twcs, img_world_wcs)


@pytest.mark.parametrize("wcs", create_sip_distortion_wcs())
@pytest.mark.filterwarnings("ignore::astropy.wcs.wcs.FITSFixedWarning")
@pytest.mark.filterwarnings(
    "ignore:Some non-standard WCS keywords were excluded:astropy.utils.exceptions.AstropyWarning",
)
def test_wcs_serialization(wcs, tmp_path):
    file_path = tmp_path / "test_wcs.asdf"
    with asdf.AsdfFile() as af:
        af["wcs"] = wcs
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        loaded_wcs = af["wcs"]
        assert wcs.to_header() == loaded_wcs.to_header()


@pytest.mark.xfail(reason="Tabular WCS serialization is currently not supported")
def test_tabular_wcs_serialization(tab_wcs_2di, tmp_path):
    file_path = tmp_path / "test_wcs.asdf"
    with asdf.AsdfFile() as af:
        af["wcs"] = tab_wcs_2di
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        loaded_wcs = af["wcs"]
        assert tab_wcs_2di.to_header() == loaded_wcs.to_header()
