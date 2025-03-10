"""
Helpers for testing astropy objects in ASDF files.
"""

import numpy as np


def assert_earth_location_equal(a, b):
    """
    Assert earth location objects are equal.
    """
    __tracebackhide__ = True

    assert (a == b).all()


def assert_representation_equal(a, b):
    """
    Assert representation objects are equal.
    """
    from astropy import units

    __tracebackhide__ = True

    assert type(a) is type(b)
    assert a.components == b.components
    for component in a.components:
        assert units.allclose(getattr(a, component), getattr(b, component))


def assert_sky_coord_equal(a, b):
    """
    Assert sky coordinate objects are equal.
    """
    __tracebackhide__ = True

    assert a.is_equivalent_frame(b)
    assert a.representation_type is b.representation_type
    assert a.shape == b.shape

    assert_representation_equal(a.data, b.data)


def assert_frame_equal(a, b):
    """
    Assert frame objects are equal.
    """
    __tracebackhide__ = True

    assert type(a) is type(b)

    if a is None:
        return

    if a.has_data:
        assert b.has_data
        assert_representation_equal(a.data, b.data)
    else:
        return


def assert_spectral_coord_equal(a, b):
    """
    Assert spectral coordinate objects are equal.
    """
    from astropy.tests.helper import assert_quantity_allclose

    __tracebackhide__ = True

    assert type(a) is type(b)
    assert_quantity_allclose(a.quantity, b.quantity)
    assert_frame_equal(a.observer, b.observer)
    assert_frame_equal(a.target, b.target)


def assert_time_equal(a, b):
    """
    Assert time objects are equal
    """
    from astropy.coordinates import EarthLocation

    assert a.format == b.format
    assert a.scale == b.scale

    assert isinstance(a.location, type(b.location))
    if isinstance(a.location, EarthLocation):
        assert_earth_location_equal(a.location, b.location)
    else:
        assert a.location == b.location

    if a.format == "plot_date":
        np.testing.assert_array_almost_equal(a.value, b.value)
    else:
        np.testing.assert_array_equal(a, b)


def assert_time_delta_equal(a, b):
    """
    Assert time delta objects are equal
    """
    np.testing.assert_array_equal(a.jd, b.jd)
    np.testing.assert_array_equal(a.jd2, b.jd2)
    np.testing.assert_array_equal(a.sec, b.sec)


def assert_hdu_list_equal(a, b):
    """
    Assert fits hdulists are equal.
    """
    assert len(a) == len(b)
    for hdu_a, hdu_b in zip(a, b):
        np.testing.assert_array_equal(hdu_a.data, hdu_b.data)
        assert len(hdu_a.header.cards) == len(hdu_b.header.cards)
        for card_a, card_b in zip(hdu_a.header.cards, hdu_b.header.cards):
            assert tuple(card_a) == tuple(card_b)


def assert_description_equal(a, b):
    """
    Assert table descriptions are equal.
    """
    if a in ("", None) and b in ("", None):
        return

    assert a == b


def assert_table_equal(a, b):
    """
    Assert astropy tables are equal.
    """
    from astropy.table import Column, MaskedColumn

    assert type(a) is type(b)
    assert a.meta == b.meta

    assert len(a) == len(b)
    for row_a, row_b in zip(a, b):
        np.testing.assert_array_equal(row_a, row_b)

    assert a.colnames == b.colnames
    for column_name in a.colnames:
        col_a = a[column_name]
        col_b = b[column_name]
        if isinstance(col_a, (Column, MaskedColumn)) and isinstance(col_b, (Column, MaskedColumn)):
            assert_description_equal(col_a.description, col_b.description)
            assert col_a.unit == col_b.unit
            assert col_a.meta == col_b.meta
            np.testing.assert_array_equal(col_a.data, col_b.data)
            np.testing.assert_array_equal(
                getattr(col_a, "mask", [False] * len(col_a)),
                getattr(col_b, "mask", [False] * len(col_b)),
            )


def assert_wcs_equal(a, b):
    from asdf.tags.core.ndarray import NDArrayType

    from asdf_astropy.converters.wcs.wcs import _WCS_ATTRS

    assert type(a) is type(b)
    assert_hdu_list_equal(a.to_fits(relax=True), b.to_fits(relax=True))
    for attr in _WCS_ATTRS:
        in_a = hasattr(a, attr)
        in_b = hasattr(b, attr)
        assert in_a == in_b
        if not in_a:
            continue
        a_val = getattr(a, attr)
        b_val = getattr(b, attr)
        if isinstance(a_val, (np.ndarray, NDArrayType)) or isinstance(b_val, (np.ndarray, NDArrayType)):
            np.testing.assert_array_equal(a_val, b_val)
        else:
            assert a_val == b_val


def assert_table_roundtrip(table, tmp_path):
    """
    Assert that a table can be written to an ASDF file and read back
    in without losing any of its essential properties.
    """
    import asdf

    file_path = tmp_path / "testable.asdf"

    with asdf.AsdfFile({"table": table}) as af:
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert_table_equal(table, af["table"])
        return af["table"]


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

    np.testing.assert_array_equal(a.parameters, b.parameters)

    assert a._user_bounding_box == b._user_bounding_box
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


def assert_bounding_box_roundtrip(bounding_box, tmp_path, version=None):
    """
    Assert that a bounding_box can be written to an ASDF file and read back
    in without losing any of its essential properties.
    """
    import asdf

    path = str(tmp_path / "test.asdf")

    with asdf.AsdfFile({"bounding_box": bounding_box}, version=version) as af:
        af.write_to(path)

    with asdf.open(path) as af:
        assert bounding_box == af["bounding_box"](bounding_box._model)


def assert_model_roundtrip(model, tmp_path, version=None):
    """
    Assert that a model can be written to an ASDF file and read back
    in without losing any of its essential properties.
    """
    import asdf

    path = str(tmp_path / "test.asdf")

    with asdf.AsdfFile({"model": model}, version=version) as af:
        af.write_to(path)

    with asdf.open(path) as af:
        assert_model_equal(model, af["model"])
        return af["model"]


def assert_wcs_roundtrip(wcs, tmp_path, version=None):
    import asdf

    path = str(tmp_path / "test.asdf")

    with asdf.AsdfFile({"wcs": wcs}, version=version) as af:
        af.write_to(path)

    with asdf.open(path) as af:
        assert_wcs_equal(wcs, af["wcs"])
