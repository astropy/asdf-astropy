import asdf
import numpy as np
import pytest
from asdf.testing.helpers import yaml_to_asdf
from astropy.io import fits
from numpy.testing import assert_array_equal

from asdf_astropy.testing.helpers import assert_hdu_list_equal


def create_hduls():
    hdul = fits.HDUList()
    header = fits.Header([("FOO", "BAR", "BAZ"), ("SOMENUM", "11.0"), ("EMPTY",)])
    hdul.append(fits.PrimaryHDU(header=header))
    hdul.append(fits.ImageHDU(data=np.arange(100)))

    hdul_with_table = fits.HDUList()
    hdul_with_table.append(fits.BinTableHDU.from_columns(np.array([(0, 1), (2, 3)], dtype=[("A", int), ("B", int)])))

    return [hdul, hdul_with_table]


@pytest.mark.parametrize("hdul", create_hduls())
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

    buff = yaml_to_asdf(yaml, version="1.5.0")
    with asdf.open(buff) as af:
        hdul = af["hdul"]
        assert len(hdul) == 3  # noqa: PLR2004
        assert hdul[0].header["FILENAME"] == "MiriDarkReferenceModel_test.fits"
        assert hdul[0].data is None
        assert hdul[1].header["EXTNAME"] == "SCI"
        assert_array_equal(hdul[1].data, np.array([2, 3, 3, 4], dtype=np.float32))
        assert hdul[2].header["EXTNAME"] == "ERR"
        assert_array_equal(hdul[2].data, np.array([5, 6, 7, 8], dtype=np.int64))
