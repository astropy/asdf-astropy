import asdf
import gwcs
import pytest
from astropy.wcs import WCS
from astropy.wcs.wcsapi import HighLevelWCSWrapper
from astropy.wcs.wcsapi.wrappers.sliced_wcs import SlicedLowLevelWCS
from pytest_lazy_fixtures import lf

from asdf_astropy.testing.helpers import assert_wcs_equal


@pytest.fixture
def wrapped_wcses(all_4d_wcses):
    return HighLevelWCSWrapper(all_4d_wcses)


@pytest.fixture
def wrapped_sliced_wcs(astropy_wcs_4d):
    return HighLevelWCSWrapper(SlicedLowLevelWCS(astropy_wcs_4d, 1))


@pytest.mark.parametrize("hl_wcs", [lf("wrapped_wcses"), lf("wrapped_sliced_wcs")])
def test_hllwcs_serialization(hl_wcs, tmp_path):
    file_path = tmp_path / "test_highlevelwcswrapper.asdf"
    with asdf.AsdfFile() as af:
        af["hl_wcs"] = hl_wcs
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        loaded_hl_wcs = af["hl_wcs"]
        if isinstance(loaded_hl_wcs, WCS):
            assert_wcs_equal(hl_wcs._low_level_wcs, loaded_hl_wcs._low_level_wcs)
        elif isinstance(loaded_hl_wcs, gwcs.WCS):
            assert loaded_hl_wcs == hl_wcs
