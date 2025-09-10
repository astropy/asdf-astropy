import pytest
from astropy.wcs import WCS
from pytest_lazy_fixtures import lf


@pytest.fixture
def gwcs_4d_identity_units():
    examples = pytest.importorskip("gwcs.examples")
    return examples.gwcs_4d_identity_units()


@pytest.fixture
def astropy_wcs_4d():
    wcs = WCS(naxis=4)
    wcs.wcs.ctype = "RA---CAR", "DEC--CAR", "FREQ", "TIME"
    wcs.wcs.cunit = "deg", "deg", "Hz", "s"
    wcs.wcs.cdelt = -2.0, 2.0, 3.0e9, 1
    wcs.wcs.crval = 4.0, 0.0, 4.0e9, 3
    wcs.wcs.crpix = 6.0, 7.0, 11.0, 11.0
    wcs.wcs.cname = "Right Ascension", "Declination", "Frequency", "Time"
    return wcs


@pytest.fixture(
    params=[
        lf("gwcs_4d_identity_units"),
        lf("astropy_wcs_4d"),
    ],
)
def all_4d_wcses(request):
    return request.param
