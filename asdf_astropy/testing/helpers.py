from astropy.coordinates import EarthLocation
from astropy.tests.helper import assert_quantity_allclose
from astropy import units
from numpy.testing import assert_array_equal


def assert_earth_location_equal(a, b):
    __tracebackhide__ = True

    assert (a == b).all()


def assert_representation_equal(a, b):
    __tracebackhide__ = True

    assert type(a) is type(b)
    assert a.components == b.components
    for component in a.components:
        assert units.allclose(getattr(a, component), getattr(b, component))


def assert_sky_coord_equal(a, b):
    __tracebackhide__ = True

    assert a.is_equivalent_frame(b)
    assert a.representation_type is b.representation_type
    assert a.shape == b.shape

    assert_representation_equal(a.data, b.data)


def assert_frame_equal(a, b):
    __tracebackhide__ = True

    assert type(a) is type(b)

    if a is None:
        return

    assert_representation_equal(a.data, b.data)


def assert_spectral_coord_equal(a, b):
    __tracebackhide__ = True

    assert type(a) is type(b)
    assert_quantity_allclose(a.quantity, b.quantity)
    assert_frame_equal(a.observer, b.observer)
    assert_frame_equal(a.target, b.target)


def assert_time_equal(a, b):
    assert a.format == b.format
    assert a.scale == b.scale

    assert type(a.location) == type(b.location)
    if isinstance(a.location, EarthLocation):
        assert_earth_location_equal(a.location, b.location)
    else:
        assert a.location == b.location

    assert_array_equal(a, b)


def assert_time_delta_equal(a, b):
    assert_array_equal(a.jd, b.jd)
    assert_array_equal(a.jd2, b.jd2)
    assert_array_equal(a.sec, b.sec)
