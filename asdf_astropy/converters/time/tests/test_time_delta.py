
import pytest

import asdf

from asdf_astropy.testing.helpers import assert_time_delta_equal

from astropy import units as u
from astropy.time import Time, TimeDelta


TEST_TIME_DELTAS = [
    TimeDelta([1, 2] * u.day),
]

for format in TimeDelta.FORMATS.keys():
    TEST_TIME_DELTAS.append(TimeDelta(Time.now() - Time.now(), format=format))

for scale in list(TimeDelta.SCALES) + [None]:
    TEST_TIME_DELTAS.append(TimeDelta(0.125, scale=scale))


@pytest.mark.parametrize("time_delta", TEST_TIME_DELTAS)
def test_serialization(time_delta, tmp_path):
    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["time_delta"] = time_delta
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert_time_delta_equal(af["time_delta"], time_delta)
