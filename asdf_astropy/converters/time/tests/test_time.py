import unittest.mock as mk
from datetime import datetime

import asdf
import numpy as np
import pytest
from asdf.testing.helpers import yaml_to_asdf
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
        Time(Time("2000-01-01T00:00:00.000").plot_date, format="plot_date"),  # astropy/astropy#14080
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


def create_examples():
    return [
        {"example": '!time/time-1.1.0 "2000-12-31T13:05:27.737"', "truth": Time("2000-12-31T13:05:27.737")},
        {"example": '!time/time-1.1.0 "2001:003:04:05:06.789"', "truth": Time("2001:003:04:05:06.789")},
        {"example": "!time/time-1.1.0 B2000.0", "truth": Time("B2000.0")},
        {
            "example": """!time/time-1.1.0
          value: 2000.0
          format: byear""",
            "truth": Time(2000.0, format="byear"),
        },
        {
            "example": """!time/time-1.1.0
          ["2000-12-31T13:05:27.737", "2000-12-31T13:06:38.444"]""",
            "truth": Time(["2000-12-31T13:05:27.737", "2000-12-31T13:06:38.444"]),
        },
        {
            "example": """!time/time-1.1.0
          value: !core/ndarray-1.0.0
            data: [2000, 2001]
            datatype: float64
          format: jyear""",
            "truth": Time([2000, 2001], format="jyear"),
        },
        {
            "example": """!time/time-1.1.0
          value: !core/ndarray-1.0.0
          value: 2000.0
          format: jyear
          scale: tdb
          location:
            x: !unit/quantity-1.1.0
              value: 6378100
              unit: !unit/unit-1.0.0 m
            y: !unit/quantity-1.1.0
              value: 0
              unit: !unit/unit-1.0.0 m
            z: !unit/quantity-1.1.0
              value: 0
              unit: !unit/unit-1.0.0 m
          format: jyear""",
            "truth": Time(
                2000.0,
                location=EarthLocation(x=6378100 * u.m, y=0 * u.m, z=0 * u.m),
                scale="tdb",
                format="jyear",
            ),
        },
    ]


@pytest.mark.parametrize("example", create_examples())
def test_read_examples(example):
    buff = yaml_to_asdf(f"example: {example['example'].strip()}", version="1.5.0")
    with asdf.AsdfFile() as af:
        af._open_impl(af, buff, mode="rw")
        assert np.all(af["example"] == example["truth"])


def test_error():
    from asdf_astropy.converters.time.time import TimeConverter

    with mk.patch("asdf_astropy.converters.time.time._ASTROPY_FORMAT_TO_ASDF_FORMAT") as mock_time:
        mock_time.get.return_value = "Bad time"

        example = "2000-01-01 00:00:00.000"
        with pytest.raises(ValueError, match=f"ASDF time '{example}' is not one of the recognized implicit formats"):
            TimeConverter().from_yaml_tree(example, mk.MagicMock(), mk.MagicMock())


def create_formats():
    from astropy.time.formats import TIME_FORMATS

    formats = []
    for format_ in TIME_FORMATS:
        if format_ == "stardate":
            # stardate is not a documented format for astropy
            # https://docs.astropy.org/en/latest/time/index.html#time-format
            continue
        new = Time("B2000.0")
        new.format = format_
        formats.append(new)

    return formats


@pytest.mark.parametrize("time", create_formats())
def test_formats(time, tmp_path):
    atol = 1 * u.day if "jyear" in time.format else 1e-08 * u.day

    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["time"] = time
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert af["time"].isclose(time, atol=atol)
        assert af["time"].format == time.format


def create_str_formats():
    return [
        Time("2000-01-01 00:00:00.000", format="iso"),
        Time("B2000.0", scale="utc", format="byear_str"),
        Time("J2000.000", scale="utc", format="jyear_str"),
        Time("2000:001:00:00:00.000", format="yday"),
    ]


@pytest.mark.parametrize("time", create_str_formats())
def test_str_format(time, tmp_path):
    """Test times that should serialize as strings"""

    file_path = tmp_path / "test.asdf"

    with asdf.AsdfFile() as af:
        af["time"] = time
        af.write_to(file_path)

    with asdf.open(file_path, _force_raw_types=True) as af:
        assert isinstance(af["time"], str)
        assert str(af["time"]) == time.value

    atol = 1 * u.day if "jyear" in time.format or "byear" in time.format else 1e-08 * u.day

    with asdf.open(file_path) as af:
        assert af["time"].isclose(time, atol=atol)
        assert af["time"].format == time.format
