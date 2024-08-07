import asdf
import pytest
from astropy.wcs import WCS


def create_wcs():
    header = {
        "CTYPE1": "TIME",
        "CUNIT1": "min",
        "CDELT1": 0.4,
        "CRPIX1": 0,
        "CRVAL1": 0,
        "CTYPE2": "WAVE",
        "CUNIT2": "Angstrom",
        "CDELT2": 0.2,
        "CRPIX2": 0,
        "CRVAL2": 0,
        "CTYPE3": "HPLT-TAN",
        "CUNIT3": "arcsec",
        "CDELT3": 20,
        "CRPIX3": 0,
        "CRVAL3": 0,
        "CTYPE4": "HPLN-TAN",
        "CUNIT4": "arcsec",
        "CDELT4": 5,
        "CRPIX4": 5,
        "CRVAL4": 0,
    }
    return WCS(header)


@pytest.mark.parametrize("wcs", [create_wcs()])
def test_wcs_serialization(wcs, tmp_path):
    file_path = tmp_path / "test_wcs.asdf"
    with asdf.AsdfFile() as af:
        af["wcs"] = wcs
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        loaded_wcs = af["wcs"]

    assert wcs.to_header() == loaded_wcs.to_header()
