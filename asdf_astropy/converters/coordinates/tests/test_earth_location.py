import asdf
import pytest
from astropy import units as u
from astropy.coordinates import EarthLocation, Latitude, Longitude
from astropy.coordinates.earth import ELLIPSOIDS
from astropy.units import Quantity


def create_earth_locations():
    longitude = Longitude([0.0, 45.0, 90.0, 135.0, 180.0, -180, -90, -45], u.deg, wrap_angle=180 * u.deg)
    latitude = Latitude([+0.0, 30.0, 60.0, +90.0, -90.0, -60.0, -30.0, 0.0], u.deg)
    height = Quantity([0.1, 0.5, 1.0, -0.5, -1.0, +4.2, -11.0, -0.1], u.m)
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
