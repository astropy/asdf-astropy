import asdf
import numpy as np
import pytest
from astropy.wcs.wcsapi.wrappers.sliced_wcs import SlicedLowLevelWCS

from asdf_astropy.testing.helpers import assert_wcs_equal


@pytest.fixture(
    params=[
        lambda wcs: SlicedLowLevelWCS(wcs, 1),
        lambda wcs: SlicedLowLevelWCS(wcs, [slice(None), slice(None), slice(None), 10]),
        lambda wcs: SlicedLowLevelWCS(SlicedLowLevelWCS(wcs, slice(None)), [slice(3), slice(None), slice(None), 10]),
        lambda wcs: SlicedLowLevelWCS(wcs, [Ellipsis, slice(5, 10)]),
        lambda wcs: SlicedLowLevelWCS(wcs, np.s_[:, 2, 3, :]),
    ],
)
def sl_wcs(astropy_wcs_4d, request):
    return request.param(astropy_wcs_4d)


def test_sliced_wcs_serialization(sl_wcs, tmp_path):
    file_path = tmp_path / "test_slicedwcs.asdf"
    with asdf.AsdfFile() as af:
        af["sl_wcs"] = sl_wcs
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        loaded_sl_wcs = af["sl_wcs"]
        assert_wcs_equal(sl_wcs._wcs, loaded_sl_wcs._wcs)
        assert sl_wcs._slices_array == loaded_sl_wcs._slices_array
