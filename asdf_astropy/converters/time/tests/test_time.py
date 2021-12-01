import pytest

import asdf
from astropy.coordinates import EarthLocation
from astropy.time import Time
from astropy import units as u
import numpy as np

from asdf_astropy.testing.helpers import assert_time_equal


def create_times():
    return [
        Time(np.arange(100), format="unix"),
        Time(
            [1, 2],
            location=EarthLocation(x=[1, 2] * u.m, y=[3, 4] * u.m, z=[5, 6] * u.m),
            format="cxcsec",
        ),
        Time(
            "J2000.000",
            location=EarthLocation(x=6378100 * u.m, y=0 * u.m, z=0 * u.m),
            format="jyear_str",
        ),
        Time("2000-01-01T00:00:00.000"),
        Time(["2001-01-02T12:34:56", "2001-02-03T00:01:02"]),
    ]


@pytest.mark.parametrize("time", create_times())
@pytest.mark.parametrize("version", asdf.versioning.supported_versions)
def test_serialization(time, version, tmp_path):
    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile(version=version) as af:
        af["time"] = time
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert_time_equal(af["time"], time)
