import pytest

import asdf
from astropy import units as u
from astropy.units import Quantity
from astropy.coordinates import EarthLocation, Longitude, Latitude
from astropy.coordinates.earth import ELLIPSOIDS

from asdf_astropy.testing.helpers import assert_earth_location_equal


def create_earth_locations():
    longitude = Longitude([0., 45., 90., 135., 180., -180, -90, -45], u.deg, wrap_angle=180 * u.deg)
    latitude = Latitude([+0., 30., 60., +90., -90., -60., -30., 0.], u.deg)
    height = Quantity([0.1, 0.5, 1.0, -0.5, -1.0, +4.2, -11., -.1], u.m)
    position = (longitude, latitude, height)

    result = [
        EarthLocation(lat=34.4900 * u.deg, lon=-104.221800 * u.deg, height=40 * u.km),
        EarthLocation(*EarthLocation.from_geodetic(*position).to_geocentric()),
    ]

    result.extend([EarthLocation.from_geodetic(*position, ellipsoid=e) for e in ELLIPSOIDS])

    return result


@pytest.mark.parametrize("earth_location", create_earth_locations())
def test_serialization(earth_location, tmp_path):
    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["earth_location"] = earth_location
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert (af["earth_location"] == earth_location).all()


@pytest.fixture
def builtin_site_registry():
    orig_sites = getattr(EarthLocation, "_site_registry", None)
    EarthLocation._get_site_registry(force_builtin=True)
    yield
    EarthLocation._site_registry = orig_sites


def test_earthlocation_site(tmp_path, builtin_site_registry):
    earth_location = EarthLocation.of_site("greenwich")

    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["earth_location"] = earth_location
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert_earth_location_equal(af["earth_location"], earth_location)
