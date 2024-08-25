import warnings

import asdf
import pytest
from astropy.io import fits
from astropy.utils.data import download_file
from astropy.wcs import WCS, FITSFixedWarning


def create_wcs():
    urls = [
        "http://data.astropy.org/tutorials/FITS-cubes/reduced_TAN_C14.fits",
        "http://data.astropy.org/tutorials/FITS-images/HorseHead.fits",
    ]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FITSFixedWarning)
        return [WCS(fits.open(download_file(url, cache=True))[0].header) for url in urls]


@pytest.mark.filterwarnings("ignore::astropy.wcs.wcs.FITSFixedWarning")
@pytest.mark.parametrize("wcs", create_wcs())
def test_wcs_serialization(wcs, tmp_path):
    file_path = tmp_path / "test_wcs.asdf"
    with asdf.AsdfFile() as af:
        af["wcs"] = wcs
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        loaded_wcs = af["wcs"]
        assert wcs.to_header() == loaded_wcs.to_header()
