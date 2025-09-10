import asdf
import numpy as np
import pytest
from astropy.wcs.wcsapi.wrappers.sliced_wcs import SlicedLowLevelWCS
from pytest_lazy_fixtures import lf

from asdf_astropy.testing.helpers import assert_wcs_equal


@pytest.fixture(
    params=[
        1,
        [slice(None), slice(None), slice(None), 10],
        [slice(3), slice(None), slice(None), 10],
        [Ellipsis, slice(5, 10)],
        np.s_[:, 2, 3, :],
    ],
)
def slices(request):
    return request.param


@pytest.fixture
def sliced_wcses(astropy_wcs_4d, slices):
    return SlicedLowLevelWCS(astropy_wcs_4d, slices)


@pytest.fixture
def nested_sliced_wcs(astropy_wcs_4d):
    return SlicedLowLevelWCS(SlicedLowLevelWCS(astropy_wcs_4d, slice(None)), [slice(3), slice(None), slice(None), 10])


@pytest.mark.parametrize("sl_wcs", [lf("sliced_wcses"), lf("nested_sliced_wcs")])
def test_sliced_wcs_serialization(sl_wcs, tmp_path):
    file_path = tmp_path / "test_slicedwcs.asdf"
    with asdf.AsdfFile() as af:
        af["sl_wcs"] = sl_wcs
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        loaded_sl_wcs = af["sl_wcs"]
        assert_wcs_equal(sl_wcs._wcs, loaded_sl_wcs._wcs)
        assert sl_wcs._slices_array == loaded_sl_wcs._slices_array
