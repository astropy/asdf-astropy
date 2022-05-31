from datetime import datetime

import asdf
import numpy as np
import pytest
from astropy import units as u
from astropy.coordinates import EarthLocation
from astropy.time import Time

from asdf_astropy.testing.helpers import assert_time_equal


def create_times():
    return [
        Time(1950.0, format="byear"),
        Time("B1950.0", format="byear_str"),
        Time(
            [1, 2],
            location=EarthLocation(x=[1, 2] * u.m, y=[3, 4] * u.m, z=[5, 6] * u.m),
            format="cxcsec",
        ),
        Time(datetime(2000, 1, 2, 12, 0, 0), format="datetime"),
        Time(2000.45, format="decimalyear"),
        Time("2000-01-01T00:00:00.000", format="fits"),
        Time(630720013.0, format="gps"),
        Time("2000-01-01 00:00:00.000", format="iso"),
        Time("2000-01-01T00:00:00.000", format="isot"),
        Time(2451544.5, format="jd"),
        Time(2000.0, format="jyear"),
        Time(
            "J2000.000",
            location=EarthLocation(x=6378100 * u.m, y=0 * u.m, z=0 * u.m),
            format="jyear_str",
        ),
        Time(51544.0, format="mjd"),
        # Time(730120.0003703703, format="plot_date"),
        Time(np.arange(100), format="unix"),
        Time(946684800.0, format="unix_tai"),
        Time("2000:001:00:00:00.000", format="yday"),
        Time("2000-01-01T00:00:00.000"),
        Time({"year": 2010, "month": 3, "day": 1}, format="ymdhms"),
        Time(np.datetime64("2000-01-01T01:01:01"), format="datetime64"),
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
