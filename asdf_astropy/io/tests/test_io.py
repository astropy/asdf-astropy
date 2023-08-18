import unittest.mock as mk

import asdf
import pytest
from astropy.table import Table

from asdf_astropy.io.connect import read_table, write_table


def make_table():
    a = [1, 4, 5]
    b = [2.0, 5.0, 8.2]
    c = ["x", "y", "z"]
    return Table([a, b, c], names=("a", "b", "c"), meta={"name": "first table"})


def test_table_io(tmp_path):
    tmp_file = tmp_path / "table.asdf"

    table = make_table()

    table.write(tmp_file)

    # Simple sanity check using ASDF directly
    with asdf.open(tmp_file) as af:
        assert "data" in af
        assert isinstance(af["data"], Table)
        assert all(af["data"] == table)

    # Now test using the table reader
    new_t = Table.read(tmp_file)
    assert all(new_t == table)


def test_table_io_custom_key(tmp_path):
    tmp_file = tmp_path / "table.asdf"

    table = make_table()

    table.write(tmp_file, data_key="something")

    # Simple sanity check using ASDF directly
    with asdf.open(tmp_file) as af:
        assert "something" in af
        assert "data" not in af
        assert isinstance(af["something"], Table)
        assert all(af["something"] == table)

    # Now test using the table reader
    with pytest.raises(KeyError):
        new_t = Table.read(tmp_file)

    new_t = Table.read(tmp_file, data_key="something")
    assert all(new_t == table)


def test_table_io_custom_tree(tmp_path):
    tmp_file = tmp_path / "table.asdf"

    table = make_table()

    def make_custom_tree(tab):
        return {"foo": {"bar": tab}}

    table.write(tmp_file, make_tree=make_custom_tree)

    # Simple sanity check using ASDF directly
    with asdf.open(tmp_file) as af:
        assert "foo" in af
        assert "bar" in af["foo"]
        assert "data" not in af
        assert all(af["foo"]["bar"] == table)

    # Now test using table reader
    with pytest.raises(KeyError):
        new_t = Table.read(tmp_file)

    def find_table(asdffile):
        return asdffile["foo"]["bar"]

    new_t = Table.read(tmp_file, find_table=find_table)
    assert all(new_t == table)


def test_read_table_error(tmp_path):
    file_name = tmp_path / "table.asdf"

    with pytest.raises(ValueError, match="Options 'data_key' and 'find_table' are not compatible"):
        read_table(file_name, data_key=mk.MagicMock(), find_table=mk.MagicMock())


def test_write_table_error(tmp_path):
    file_name = tmp_path / "table.asdf"

    with pytest.raises(ValueError, match="Options 'data_key' and 'make_tree' are not compatible"):
        write_table(mk.MagicMock(), file_name, data_key=mk.MagicMock(), make_tree=mk.MagicMock())
