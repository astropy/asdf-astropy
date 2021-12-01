from astropy.tests.helper import assert_quantity_allclose


def assert_representation_equal(a, b):
    __tracebackhide__ = True

    assert type(a) is type(b)
    assert a.components == b.components
    for component in a.components:
        assert u.allclose(getattr(a, component), getattr(b, component))


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
