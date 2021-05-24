import asdf
from asdf.tests.helpers import yaml_to_asdf
from astropy.io import fits
import numpy as np
from numpy.testing import assert_array_equal
import pytest

from asdf_astropy.testing.helpers import assert_hdu_list_equal


HDUL = fits.HDUList()
HEADER = fits.Header([
    ("FOO", "BAR", "BAZ"),
    ("SOMENUM", "11.0"),
    ("EMPTY",)
])
HDUL.append(fits.PrimaryHDU(header=HEADER))
HDUL.append(fits.ImageHDU(data=np.arange(100)))

HDUL_WITH_TABLE = fits.HDUList()
HDUL_WITH_TABLE.append(
    fits.BinTableHDU.from_columns(
        np.array([(0, 1), (2, 3)], dtype=[("A", int), ("B", int)])
    )
)

TEST_HDULS = [
    HDUL,
    HDUL_WITH_TABLE,
]


@pytest.mark.parametrize("hdul", TEST_HDULS)
def test_serialization(hdul, tmp_path):
    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["hdul"] = hdul
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert_hdu_list_equal(af["hdul"], hdul)


def test_asdf_tag():
    yaml = """
hdul: !fits/fits-1.0.0
  - header:
      - [SIMPLE, true, conforms to FITS standard]
      - [BITPIX, 8, array data type]
      - [NAXIS, 0, number of array dimensions]
      - [EXTEND, true]
      - []
      - ['', Top Level MIRI Metadata]
      - []
      - [DATE, '2013-08-30T10:49:55.070373', The date this file was created (UTC)]
      - [FILENAME, MiriDarkReferenceModel_test.fits, The name of the file]
      - [TELESCOP, JWST, The telescope used to acquire the data]
      - []
      - ['', Information about the observation]
      - []
      - [DATE-OBS, '2013-08-30T10:49:55.000000', The date the observation was made (UTC)]
  - data: !core/ndarray-1.0.0
      data: [2, 3, 3, 4]
      datatype: float32
      shape: [4]
    header:
      - [XTENSION, IMAGE, Image extension]
      - [BITPIX, -32, array data type]
      - [NAXIS, 4, number of array dimensions]
      - [NAXIS1, 4]
      - [NAXIS2, 3]
      - [NAXIS3, 3]
      - [NAXIS4, 2]
      - [PCOUNT, 0, number of parameters]
      - [GCOUNT, 1, number of groups]
      - [EXTNAME, SCI, extension name]
      - [BUNIT, DN, Units of the data array]
  - data: !core/ndarray-1.0.0
      data: [5, 6, 7, 8]
      datatype: int64
      shape: [4]
    header:
      - [XTENSION, IMAGE, Image extension]
      - [BITPIX, -32, array data type]
      - [NAXIS, 4, number of array dimensions]
      - [NAXIS1, 4]
      - [NAXIS2, 3]
      - [NAXIS3, 3]
      - [NAXIS4, 2]
      - [PCOUNT, 0, number of parameters]
      - [GCOUNT, 1, number of groups]
      - [EXTNAME, ERR, extension name]
      - [BUNIT, DN, Units of the error array]
    """

    buff = yaml_to_asdf(yaml)
    with asdf.open(buff) as af:
        hdul = af["hdul"]
        assert len(hdul) == 3
        assert hdul[0].header["FILENAME"] == "MiriDarkReferenceModel_test.fits"
        assert hdul[0].data is None
        assert hdul[1].header["EXTNAME"] == "SCI"
        assert_array_equal(hdul[1].data, np.array([2, 3, 3, 4], dtype=np.float32))
        assert hdul[2].header["EXTNAME"] == "ERR"
        assert_array_equal(hdul[2].data, np.array([5, 6, 7, 8], dtype=np.int64))
