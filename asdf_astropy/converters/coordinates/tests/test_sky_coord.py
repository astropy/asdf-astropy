import asdf
import astropy.units as u
import numpy as np
import pytest
from astropy.coordinates import FK4, ICRS, Galactic, Longitude, SkyCoord

from asdf_astropy.testing.helpers import assert_sky_coord_equal


def create_sky_coords():
    # These are cribbed directly from the Examples section of
    # https://docs.astropy.org/en/stable/api/astropy.coordinates.SkyCoord.html
    return [
        # Defaults to ICRS frame
        SkyCoord(10, 20, unit="deg"),
        # Vector of 3 coords
        SkyCoord([1, 2, 3], [-30, 45, 8], frame="icrs", unit="deg"),
        # FK4 frame
        SkyCoord(
            ["1:12:43.2 +1:12:43", "1 12 43.2 +1 12 43"],
            frame=FK4,
            unit=(u.deg, u.hourangle),
            obstime="J1992.21",
        ),
        # Galactic frame
        SkyCoord("1h12m43.2s +1d12m43s", frame=Galactic),
        SkyCoord(frame="galactic", l="1h12m43.2s", b="+1d12m43s"),
        # With ra and dec
        SkyCoord(
            Longitude([1, 2, 3], unit=u.deg),
            np.array([4.5, 5.2, 6.3]) * u.deg,
            frame="icrs",
        ),
        SkyCoord(
            frame=ICRS,
            ra=Longitude([1, 2, 3], unit=u.deg),
            dec=np.array([4.5, 5.2, 6.3]) * u.deg,
            obstime="2001-01-02T12:34:56",
        ),
        # With overridden frame defaults
        SkyCoord(FK4(1 * u.deg, 2 * u.deg), obstime="J2010.11", equinox="B1965"),
        # Cartesian
        SkyCoord(w=0, u=1, v=2, unit="kpc", frame="galactic", representation_type="cartesian"),
        # Vector frame
        SkyCoord([ICRS(ra=1 * u.deg, dec=2 * u.deg), ICRS(ra=3 * u.deg, dec=4 * u.deg)]),
        # 2D obstime
        SkyCoord([1, 2], [3, 4], [5, 6], unit="deg,deg,m", frame="fk4", obstime=["J1990.5", "J1991.5"]),
        # Radial velocity
        SkyCoord(ra=1 * u.deg, dec=2 * u.deg, radial_velocity=10 * u.km / u.s),
        # Proper motion
        SkyCoord(ra=1 * u.deg, dec=2 * u.deg, pm_ra_cosdec=2 * u.mas / u.yr, pm_dec=1 * u.mas / u.yr),
    ]


@pytest.mark.parametrize("coord", create_sky_coords())
def test_serialization(coord, tmp_path):
    file_path = tmp_path / "test.asdf"

    with asdf.AsdfFile() as af:
        af["coord"] = coord
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert_sky_coord_equal(af["coord"], coord)


def test_serializaton_extra_attribute(tmp_path):
    coord = SkyCoord(10 * u.deg, 20 * u.deg, equinox="2011-01-01T00:00", frame="fk4").transform_to("icrs")

    file_path = tmp_path / "test.asdf"

    with asdf.AsdfFile() as af:
        af["coord"] = coord
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert_sky_coord_equal(af["coord"], coord)
        assert hasattr(af["coord"], "equinox")
