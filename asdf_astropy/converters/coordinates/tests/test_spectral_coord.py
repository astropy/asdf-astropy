import warnings

import asdf
import pytest
from astropy import units as u
from astropy.coordinates import ICRS, Galactic, SpectralCoord
from astropy.coordinates.spectral_coordinate import NoVelocityWarning

from asdf_astropy.testing.helpers import assert_spectral_coord_equal


def create_spectral_coords():
    result = [
        # Scalar
        SpectralCoord(565 * u.nm),
        # Vector
        SpectralCoord([100, 200, 300] * u.GHz),
    ]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", NoVelocityWarning)
        result.append(
            # With observer and target
            SpectralCoord(
                10 * u.GHz,
                observer=ICRS(1 * u.km, 2 * u.km, 3 * u.km, representation_type="cartesian"),
                target=Galactic(10 * u.deg, 20 * u.deg, distance=30 * u.pc),
            ),
        )

    return result


@pytest.mark.filterwarnings("ignore::astropy.coordinates.spectral_coordinate.NoVelocityWarning")
@pytest.mark.parametrize("coord", create_spectral_coords())
def test_serialization(coord, tmp_path):
    file_path = tmp_path / "test.asdf"

    with asdf.AsdfFile() as af:
        af["coord"] = coord
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert_spectral_coord_equal(af["coord"], coord)
