import asdf
import astropy.units as u
import numpy as np
import pytest
from asdf.tests.helpers import yaml_to_asdf
from astropy.coordinates import EarthLocation, SkyCoord
from astropy.table import Column, MaskedColumn, NdarrayMixin, QTable, Table
from astropy.time import Time, TimeDelta
from numpy.testing import assert_array_equal

from asdf_astropy.testing.helpers import (
    assert_earth_location_equal,
    assert_sky_coord_equal,
    assert_time_delta_equal,
    assert_time_equal,
)


def assert_description_equal(a, b):
    if a in ("", None) and b in ("", None):
        return

    assert a == b


def assert_table_equal(a, b):
    assert type(a) == type(b)
    assert a.meta == b.meta

    assert len(a) == len(b)
    for row_a, row_b in zip(a, b):
        assert_array_equal(row_a, row_b)

    assert a.colnames == b.colnames
    for column_name in a.colnames:
        col_a = a[column_name]
        col_b = b[column_name]
        if isinstance(col_a, (Column, MaskedColumn)) and isinstance(col_b, (Column, MaskedColumn)):
            assert_description_equal(col_a.description, col_b.description)
            assert col_a.unit == col_b.unit
            assert col_a.meta == col_b.meta
            assert_array_equal(col_a.data, col_b.data)
            assert_array_equal(
                getattr(col_a, "mask", [False] * len(col_a)),
                getattr(col_b, "mask", [False] * len(col_b)),
            )


def assert_table_roundtrip(table, tmp_path):
    """
    Assert that a table can be written to an ASDF file and read back
    in without losing any of its essential properties.
    """
    file_path = tmp_path / "testable.asdf"

    with asdf.AsdfFile({"table": table}) as af:
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert_table_equal(table, af["table"])
        return af["table"]


def test_table(tmp_path):
    rows = [(1, 2.0, "x"), (4, 5.0, "y"), (5, 8.2, "z")]

    table = Table(rows=rows, names=("a", "b", "c"), dtype=("i4", "f8", "S1"))
    table.columns["a"].description = "RA"
    table.columns["a"].unit = "degree"
    table.columns["a"].meta = {"foo": "bar"}
    table.columns["c"].description = "Some description of some sort"

    assert_table_roundtrip(table, tmp_path)


def test_array_columns(tmp_path):
    data = np.array(
        [([[1, 2], [3, 4]], 2.0, "x"), ([[5, 6], [7, 8]], 5.0, "y"), ([[9, 10], [11, 12]], 8.2, "z")],
        dtype=[("a", "<i4", (2, 2)), ("b", "<f8"), ("c", "|S1")],
    )

    table = Table(data, copy=False)

    assert_table_roundtrip(table, tmp_path)


def test_structured_array_columns(tmp_path):
    rows = np.array(
        [((1, "a"), 2.0, "x"), ((4, "b"), 5.0, "y"), ((5, "c"), 8.2, "z")],
        dtype=[("a", [("a0", "<i4"), ("a1", "|S1")]), ("b", "<f8"), ("c", "|S1")],
    )

    table = Table(rows, copy=False)

    assert_table_roundtrip(table, tmp_path)


def test_table_row_order(tmp_path):
    data = np.array([(1, 2.0, "x"), (4, 5.0, "y"), (5, 8.2, "z")], dtype=[("a", "<i4"), ("b", "<f8"), ("c", "|S1")])

    table = Table(data, copy=False)
    table.columns["a"].description = "RA"
    table.columns["a"].unit = "degree"
    table.columns["a"].meta = {"foo": "bar"}
    table.columns["c"].description = "Some description of some sort"

    assert_table_roundtrip(table, tmp_path)


def test_table_inline(tmp_path):
    rows = [(1, 2.0, "x"), (4, 5.0, "y"), (5, 8.2, "z")]
    table = Table(rows=rows, names=("a", "b", "c"), dtype=("i4", "f8", "S1"))
    table.columns["a"].description = "RA"
    table.columns["a"].unit = "degree"
    table.columns["a"].meta = {"foo": "bar"}
    table.columns["c"].description = "Some description of some sort"

    with asdf.config_context() as config:
        config.array_inline_threshold = 64
        assert_table_roundtrip(table, tmp_path)


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

    buff = yaml_to_asdf(yaml)

    with pytest.raises(ValueError, match="Inconsistent data column lengths"):
        with asdf.open(buff):
            pass


def test_masked_table(tmp_path):
    rows = [(1, 2.0, "x"), (4, 5.0, "y"), (5, 8.2, "z")]
    table = Table(rows=rows, names=("a", "b", "c"), dtype=("i4", "f8", "S1"), masked=True)
    table.columns["a"].description = "RA"
    table.columns["a"].unit = "degree"
    table.columns["a"].meta = {"foo": "bar"}
    table.columns["a"].mask = [True, False, True]
    table.columns["c"].description = "Some description of some sort"

    assert_table_roundtrip(table, tmp_path)


def test_quantity_mixin(tmp_path):
    table = QTable()
    table["a"] = [1, 2, 3]
    table["b"] = ["x", "y", "z"]
    table["c"] = [2.0, 5.0, 8.2] * u.m

    assert_table_roundtrip(table, tmp_path)


def test_time_mixin(tmp_path):
    table = Table()
    table["a"] = [1, 2]
    table["b"] = ["x", "y"]
    table["c"] = Time(["2001-01-02T12:34:56", "2001-02-03T00:01:02"])

    result = assert_table_roundtrip(table, tmp_path)
    assert_time_equal(result["c"], table["c"])


def test_timedelta_mixin(tmp_path):
    table = Table()
    table["a"] = [1, 2]
    table["b"] = ["x", "y"]
    table["c"] = TimeDelta([1, 2] * u.day)

    result = assert_table_roundtrip(table, tmp_path)
    assert_time_delta_equal(result["c"], table["c"])


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
        assert_sky_coord_equal(af["table"]["c"], table["c"])


def test_earthlocation_mixin(tmp_path):
    table = Table()
    table["a"] = [1, 2]
    table["b"] = ["x", "y"]
    table["c"] = EarthLocation(x=[1, 2] * u.km, y=[3, 4] * u.km, z=[5, 6] * u.km)

    result = assert_table_roundtrip(table, tmp_path)
    assert_earth_location_equal(result["c"], table["c"])


def test_ndarray_mixin(tmp_path):
    table = Table()
    table["a"] = [1, 2]
    table["b"] = ["x", "y"]
    table["c"] = NdarrayMixin([5, 6])

    assert_table_roundtrip(table, tmp_path)


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
    buff = yaml_to_asdf(yaml)

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
