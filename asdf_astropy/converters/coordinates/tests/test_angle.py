import asdf
import numpy as np
import pytest
from astropy import units as u
from astropy.coordinates import Angle, Latitude, Longitude


def create_angles():
    return [
        Angle(100, u.deg),
        Angle([100, 120, 150], u.deg),
        Angle([[90, 100, 110], [100, 120, 150]], u.deg),
        Angle(np.arange(100).reshape(5, 2, 10), u.deg),
        Latitude(10, u.deg),
        Longitude(-100, u.deg, wrap_angle=180 * u.deg),
    ]


@pytest.mark.parametrize("angle", create_angles())
def test_serialization(angle, tmp_path):
    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["angle"] = angle
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert (af["angle"] == angle).all()
