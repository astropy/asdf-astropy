

import pytest

import asdf
from astropy import units as u
from astropy.cosmology import parameters, realizations


# TODO! something that tests every cosmology class
TEST_COSMOLOGIES = (getattr(realizations, n) for n in parameters.available)


def assert_cosmo_equal(a, b):
    __tracebackhide__ = True

    assert a == b
    assert a.meta == b.meta


@pytest.mark.parametrize("cosmo", TEST_COSMOLOGIES)
def test_serialization(cosmo, tmp_path):
    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["cosmo"] = cosmo
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert_cosmo_equal(af["cosmo"], cosmo)
