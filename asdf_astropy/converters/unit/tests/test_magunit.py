import asdf
import pytest
from astropy import units
from astropy.table import Column


def create_builtin_units():
    return {u for u in list(units.__dict__.values()) if isinstance(u, units.MagUnit)}


@pytest.mark.parametrize("unit", create_builtin_units())
@pytest.mark.filterwarnings("ignore::astropy.units.core.UnitsWarning")
def test_builtin_serialization(unit, tmp_path):
    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["unit"] = unit
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert af["unit"].is_equivalent(unit)

    with file_path.open() as f:
        assert "tag:astropy.org:astropy/units/magunit-" in f.read()


def create_magunits():
    magunits = []
    for u in units.__dict__.values():
        if isinstance(u, units.UnitBase) and not isinstance(u, units.MagUnit):
            try:
                magunit = units.mag(u)
            except units.UnitConversionError:
                pass
            else:
                magunits.append(magunit)

    return frozenset(magunits)


@pytest.mark.parametrize("unit", create_magunits())
@pytest.mark.filterwarnings("ignore::astropy.units.core.UnitsWarning")
def test_magunit_serialization(unit, tmp_path):
    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["unit"] = unit
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert af["unit"].is_equivalent(unit)

    with file_path.open() as f:
        assert "tag:astropy.org:astropy/units/magunit-" in f.read()


def test_magunit_in_column(tmp_path):
    column = Column([1, 2, 3], unit=units.function.ABmag, name="foo")

    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["column"] = column
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        # the column unit tests already cover the other attributes
        assert af["column"].unit == column.unit
