import unittest.mock as mk

import asdf
import numpy as np
import pytest
from asdf.testing.helpers import yaml_to_asdf
from astropy import units as u
from astropy.coordinates import (
    CIRS,
    FK4,
    FK5,
    GCRS,
    ICRS,
    ITRS,
    Angle,
    CartesianRepresentation,
    FK4NoETerms,
    Galactic,
    Galactocentric,
    Latitude,
    Longitude,
    PrecessedGeocentric,
    SphericalRepresentation,
)
from astropy.time import Time

from asdf_astropy.converters.coordinates.frame import FrameConverter, LegacyICRSConverter
from asdf_astropy.testing.helpers import assert_frame_equal


def create_frames():
    test_data = {
        "ra": 1 * u.deg,
        "dec": 2 * u.deg,
    }

    return [
        CIRS(),
        CIRS(**test_data),
        CIRS(**test_data, obstime=Time("J2005")),
        FK4(),
        FK4(**test_data),
        FK4(**test_data, obstime=Time("B1950")),
        FK4NoETerms(),
        FK4NoETerms(**test_data),
        FK4NoETerms(**test_data, obstime=Time("J1975")),
        FK5(),
        FK5(**test_data),
        FK5(**test_data, equinox="J2005"),
        FK5(**test_data, equinox="2011-01-01T00:00:00"),
        Galactic(l=47.37 * u.degree, b=+6.32 * u.degree),
        Galactocentric(
            x=np.linspace(-10.0, 10.0, 100) * u.kpc,
            y=np.linspace(-10.0, 10.0, 100) * u.kpc,
            z=np.zeros(100) * u.kpc,
            z_sun=15 * u.pc,
        ),
        GCRS(),
        GCRS(**test_data),
        GCRS(**test_data, obsgeoloc=CartesianRepresentation([1, 2, 3], unit=u.m)),
        ICRS(**test_data),
        ICRS(ra=Longitude(25, unit=u.deg), dec=Latitude(45, unit=u.deg)),
        ICRS(ra=Longitude(25, unit=u.deg, wrap_angle=Angle(1.5, unit=u.rad)), dec=Latitude(45, unit=u.deg)),
        ICRS(ra=[0, 1, 2] * u.deg, dec=[3, 4, 5] * u.deg),
        ITRS(SphericalRepresentation(lon=12.3 * u.deg, lat=45.6 * u.deg, distance=1 * u.km)),
        PrecessedGeocentric(),
        PrecessedGeocentric(**test_data),
        PrecessedGeocentric(**test_data, equinox="B1975"),
    ]


@pytest.mark.parametrize("frame", create_frames())
def test_serialization(frame, tmp_path):
    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["frame"] = frame
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert_frame_equal(af["frame"], frame)


def test_tags():
    converter = FrameConverter(["tag1", "tag2"], "test")
    assert converter.tags == ["tag1", "tag2"]


def test_legacy_icrs_serialize():
    converter = LegacyICRSConverter()

    ra = 25
    dec = 45

    frame = ICRS(ra=Longitude(ra, unit=u.deg), dec=Latitude(dec, unit=u.deg))
    node = converter.to_yaml_tree(frame, mk.MagicMock(), mk.MagicMock())

    assert node["ra"]["value"] == ra
    assert node["ra"]["unit"] == "deg"
    assert node["ra"]["wrap_angle"] == 360 * u.deg

    assert node["dec"]["value"] == dec
    assert node["dec"]["unit"] == "deg"


def test_legacy_icrs_deseialize():
    example = """!<tag:astropy.org:astropy/coordinates/frames/icrs-1.0.0>
    ra:
      value: 25
      unit: deg
      wrap_angle: !unit/quantity-1.1.0
        value: 360
        unit: deg
    dec:
      value: 45
      unit: deg"""
    truth = ICRS(ra=Longitude(25, unit=u.deg), dec=Latitude(45, unit=u.deg))

    buff = yaml_to_asdf(f"example: {example.strip()}", version="1.5.0")
    with asdf.AsdfFile() as af:
        af._open_impl(af, buff, mode="rw")
        assert_frame_equal(af["example"], truth)
