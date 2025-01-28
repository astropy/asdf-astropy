import warnings

import asdf
import astropy.units as u
import numpy as np
import pytest
from asdf.testing.helpers import yaml_to_asdf
from astropy.coordinates import EarthLocation, SkyCoord
from astropy.table import NdarrayMixin, QTable, Table
from astropy.time import Time, TimeDelta
from numpy.testing import assert_array_equal

from asdf_astropy.testing import helpers


def assert_description_equal(a, b):
    message = (
        "asdf_astropy.converters.table.tests.test_table.assert_description_equal is deprecated."
        "Use asdf_astropy.testing.helpers.assert_description_equal instead."
    )
    warnings.warn(message, DeprecationWarning, stacklevel=2)

    return helpers.assert_description_equal(a, b)


def assert_table_equal(a, b):
    message = (
        "asdf_astropy.converters.table.tests.test_table.assert_table_equal is deprecated."
        "Use asdf_astropy.testing.helpers.assert_table_equal instead."
    )
    warnings.warn(message, DeprecationWarning, stacklevel=2)

    return helpers.assert_table_equal(a, b)


def assert_table_roundtrip(table, tmp_path):
    message = (
        "asdf_astropy.converters.table.tests.test_table.assert_table_roundtrip is deprecated."
        "Use asdf_astropy.testing.helpers.assert_table_roundtrip instead."
    )
    warnings.warn(message, DeprecationWarning, stacklevel=2)

    return helpers.assert_table_roundtrip(table, tmp_path)


def test_deprecations(tmp_path):
    rows = [(1, 2.0, "x"), (4, 5.0, "y"), (5, 8.2, "z")]

    table = Table(rows=rows, names=("a", "b", "c"), dtype=("i4", "f8", "S1"))
    table.columns["a"].description = "RA"
    table.columns["a"].unit = "degree"
    table.columns["a"].meta = {"foo": "bar"}
    table.columns["c"].description = "Some description of some sort"

    # Test assert_description_equal deprecation
    with pytest.warns(DeprecationWarning, match=".*assert_description_equal.*"):
        assert_description_equal("a", "a")

    # Test assert_table_equal deprecation
    with pytest.warns(DeprecationWarning, match=".*assert_table_equal.*"):
        assert_table_equal(table, table)

    # Test assert_table_roundtrip deprecation
    with pytest.warns(DeprecationWarning, match=".*assert_table_roundtrip.*"):
        assert_table_roundtrip(table, tmp_path)


def test_table(tmp_path):
    rows = [(1, 2.0, "x"), (4, 5.0, "y"), (5, 8.2, "z")]

    table = Table(rows=rows, names=("a", "b", "c"), dtype=("i4", "f8", "S1"))
    table.columns["a"].description = "RA"
    table.columns["a"].unit = "degree"
    table.columns["a"].meta = {"foo": "bar"}
    table.columns["c"].description = "Some description of some sort"

    helpers.assert_table_roundtrip(table, tmp_path)


def test_array_columns(tmp_path):
    data = np.array(
        [([[1, 2], [3, 4]], 2.0, "x"), ([[5, 6], [7, 8]], 5.0, "y"), ([[9, 10], [11, 12]], 8.2, "z")],
        dtype=[("a", "<i4", (2, 2)), ("b", "<f8"), ("c", "|S1")],
    )

    table = Table(data, copy=False)

    helpers.assert_table_roundtrip(table, tmp_path)


def test_structured_array_columns(tmp_path):
    rows = np.array(
        [((1, "a"), 2.0, "x"), ((4, "b"), 5.0, "y"), ((5, "c"), 8.2, "z")],
        dtype=[("a", [("a0", "<i4"), ("a1", "|S1")]), ("b", "<f8"), ("c", "|S1")],
    )

    table = Table(rows, copy=False)

    helpers.assert_table_roundtrip(table, tmp_path)


def test_table_row_order(tmp_path):
    data = np.array([(1, 2.0, "x"), (4, 5.0, "y"), (5, 8.2, "z")], dtype=[("a", "<i4"), ("b", "<f8"), ("c", "|S1")])

    table = Table(data, copy=False)
    table.columns["a"].description = "RA"
    table.columns["a"].unit = "degree"
    table.columns["a"].meta = {"foo": "bar"}
    table.columns["c"].description = "Some description of some sort"

    helpers.assert_table_roundtrip(table, tmp_path)


# once asdf 2.14.x can be dropped and the minimum updated 2.15.0 this warning
# filter can be removed
@pytest.mark.filterwarnings(
    "ignore:`product` is deprecated as of NumPy 1.25.0, and will be removed in "
    "NumPy 2.0. Please use `prod` instead.:DeprecationWarning",
)
def test_table_inline(tmp_path):
    rows = [(1, 2.0, "x"), (4, 5.0, "y"), (5, 8.2, "z")]
    table = Table(rows=rows, names=("a", "b", "c"), dtype=("i4", "f8", "S1"))
    table.columns["a"].description = "RA"
    table.columns["a"].unit = "degree"
    table.columns["a"].meta = {"foo": "bar"}
    table.columns["c"].description = "Some description of some sort"

    with asdf.config_context() as config:
        config.array_inline_threshold = 64
        helpers.assert_table_roundtrip(table, tmp_path)


def test_mismatched_columns():
    yaml = """
table: !<tag:astropy.org:astropy/table/table-1.0.0>
  columns:
  - !core/column-1.0.0
    data: !core/ndarray-1.0.0
      data: [0, 1, 2]
    name: a
  - !core/column-1.0.0
    data: !core/ndarray-1.0.0
      data: [0, 1, 2, 3]
    name: b
  colnames: [a, b]
    """

    buff = yaml_to_asdf(yaml, version="1.5.0")

    with pytest.raises(ValueError, match="Inconsistent data column lengths"), asdf.open(buff):
        pass


def test_masked_table(tmp_path):
    rows = [(1, 2.0, "x"), (4, 5.0, "y"), (5, 8.2, "z")]
    table = Table(rows=rows, names=("a", "b", "c"), dtype=("i4", "f8", "S1"), masked=True)
    table.columns["a"].description = "RA"
    table.columns["a"].unit = "degree"
    table.columns["a"].meta = {"foo": "bar"}
    table.columns["a"].mask = [True, False, True]
    table.columns["c"].description = "Some description of some sort"

    helpers.assert_table_roundtrip(table, tmp_path)


def test_quantity_mixin(tmp_path):
    table = QTable()
    table["a"] = [1, 2, 3]
    table["b"] = ["x", "y", "z"]
    table["c"] = [2.0, 5.0, 8.2] * u.m

    helpers.assert_table_roundtrip(table, tmp_path)


def test_time_mixin(tmp_path):
    table = Table()
    table["a"] = [1, 2]
    table["b"] = ["x", "y"]
    table["c"] = Time(["2001-01-02T12:34:56", "2001-02-03T00:01:02"])

    result = helpers.assert_table_roundtrip(table, tmp_path)
    helpers.assert_time_equal(result["c"], table["c"])


def test_timedelta_mixin(tmp_path):
    table = Table()
    table["a"] = [1, 2]
    table["b"] = ["x", "y"]
    table["c"] = TimeDelta([1, 2] * u.day)

    result = helpers.assert_table_roundtrip(table, tmp_path)
    helpers.assert_time_delta_equal(result["c"], table["c"])


def test_skycoord_mixin(tmp_path):
    table = Table()
    table["a"] = [1, 2]
    table["b"] = ["x", "y"]
    table["c"] = SkyCoord([1, 2], [3, 4], unit="deg,deg", frame="fk4", obstime="J1990.5")

    # We can't use our assert_table_roundtrip helper because
    # astropy 4.0.x does not include an __eq__ method for SKyCoord.
    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["table"] = table
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        helpers.assert_sky_coord_equal(af["table"]["c"], table["c"])


def test_earthlocation_mixin(tmp_path):
    table = Table()
    table["a"] = [1, 2]
    table["b"] = ["x", "y"]
    table["c"] = EarthLocation(x=[1, 2] * u.km, y=[3, 4] * u.km, z=[5, 6] * u.km)

    result = helpers.assert_table_roundtrip(table, tmp_path)
    helpers.assert_earth_location_equal(result["c"], table["c"])


def test_ndarray_mixin(tmp_path):
    table = Table()
    table["a"] = [1, 2]
    table["b"] = ["x", "y"]
    table["c"] = NdarrayMixin([5, 6])

    result = helpers.assert_table_roundtrip(table, tmp_path)
    assert isinstance(result["c"], NdarrayMixin)


def test_asdf_table():
    yaml = """
table: !core/table-1.0.0
  columns:
    - !core/column-1.0.0
      data: !core/ndarray-1.0.0
        data: [1, 2, 3]
        datatype: float64
        shape: [3]
      description: RA
      meta: {foo: bar}
      name: a
      unit: !unit/unit-1.0.0 deg
    - !core/column-1.0.0
      data: !core/ndarray-1.0.0
        data: [4, 5, 6]
        datatype: float64
        shape: [3]
      description: DEC
      name: b
    - !core/column-1.0.0
      data: !core/ndarray-1.0.0
        data: [d, e, f]
        datatype: [ascii, 1]
        shape: [3]
      description: The target name
      name: c
    """
    buff = yaml_to_asdf(yaml, version="1.5.0")

    with asdf.open(buff) as af:
        table = af["table"]
        assert isinstance(table, Table)

        assert table["a"].name == "a"
        assert table["a"].description == "RA"
        assert table["a"].meta == {"foo": "bar"}
        assert table["a"].unit == u.deg
        assert_array_equal(table["a"].data, np.array([1, 2, 3], dtype=np.float64))

        assert table["b"].name == "b"
        assert table["b"].description == "DEC"
        assert_array_equal(table["b"].data, np.array([4, 5, 6], dtype=np.float64))

        assert table["c"].name == "c"
        assert table["c"].description == "The target name"
        assert_array_equal(table["c"].data, np.array([b"d", b"e", b"f"]))
