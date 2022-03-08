from astropy import units
from astropy.coordinates import EarthLocation
from astropy.tests.helper import assert_quantity_allclose
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


def assert_hdu_list_equal(a, b):
    assert len(a) == len(b)
    for hdu_a, hdu_b in zip(a, b):
        assert_array_equal(hdu_a.data, hdu_b.data)
        assert len(hdu_a.header.cards) == len(hdu_b.header.cards)
        for card_a, card_b in zip(hdu_a.header.cards, hdu_b.header.cards):
            assert tuple(card_a) == tuple(card_b)


def assert_model_equal(a, b):
    """
    Assert that two model instances are equivalent.
    """
    if a is None and b is None:
        return

    assert a.__class__ == b.__class__

    assert a.name == b.name
    assert a.inputs == b.inputs
    assert a.input_units == b.input_units
    assert a.outputs == b.outputs
    assert a.input_units_allow_dimensionless == b.input_units_allow_dimensionless
    assert a.input_units_equivalencies == b.input_units_equivalencies

    assert_array_equal(a.parameters, b.parameters)

    try:
        a_bounding_box = a.bounding_box
    except NotImplementedError:
        a_bounding_box = None

    try:
        b_bounding_box = b.bounding_box
    except NotImplementedError:
        b_bounding_box = None

    assert a_bounding_box == b_bounding_box

    assert a.fixed == b.fixed
    assert a.bounds == b.bounds

    assert_model_equal(a._user_inverse, b._user_inverse)
