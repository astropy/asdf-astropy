import asdf
import pytest
from astropy import units as u
from astropy.time import Time, TimeDelta

from asdf_astropy.testing.helpers import assert_time_delta_equal


def create_time_deltas():
    result = [
        TimeDelta([1, 2] * u.day),
    ]

    for format_ in TimeDelta.FORMATS:
        result.append(TimeDelta(Time.now() - Time.now(), format=format_))

    for scale in [*list(TimeDelta.SCALES), None]:
        result.append(TimeDelta(0.125 * u.day, scale=scale))

    return result


@pytest.mark.parametrize("time_delta", create_time_deltas())
def test_serialization(time_delta, tmp_path):
    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["time_delta"] = time_delta
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert_time_delta_equal(af["time_delta"], time_delta)
