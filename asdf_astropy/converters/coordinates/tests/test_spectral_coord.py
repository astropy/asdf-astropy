import warnings

import pytest

# No spectral_coordinate module in astropy 4.0.x
pytest.importorskip("astropy.coordinates.spectral_coordinate")

import asdf
from astropy import units as u
from astropy.coordinates import SpectralCoord, ICRS, Galactic
from astropy.coordinates.spectral_coordinate import NoVelocityWarning
from astropy.tests.helper import assert_quantity_allclose

from asdf_astropy.testing.helpers import assert_frame_equal


TEST_COORDS = [
    # Scalar
    SpectralCoord(565 * u.nm),
    # Vector
    SpectralCoord([100, 200, 300] * u.GHz),
]

with warnings.catch_warnings():
    warnings.simplefilter("ignore", NoVelocityWarning)
    TEST_COORDS.append(
        # With observer and target
        SpectralCoord(
            10 * u.GHz,
            observer=ICRS(1 * u.km, 2 * u.km, 3 * u.km, representation_type="cartesian"),
            target=Galactic(10 * u.deg, 20 * u.deg, distance=30 * u.pc)
        )
    )


@pytest.mark.filterwarnings("ignore::astropy.coordinates.spectral_coordinate.NoVelocityWarning")
@pytest.mark.parametrize("coord", TEST_COORDS)
def test_serialization(coord, tmp_path):
    file_path = tmp_path / "test.asdf"

    with asdf.AsdfFile() as af:
        af["coord"] = coord
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert type(af["coord"]) is type(coord)
        assert_quantity_allclose(af["coord"].quantity, coord.quantity)
        assert_frame_equal(af["coord"].observer, coord.observer)
        assert_frame_equal(af["coord"].target, coord.target)
