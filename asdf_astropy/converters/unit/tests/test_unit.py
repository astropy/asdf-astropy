import warnings

import asdf
import pytest
from asdf.testing import helpers
from astropy import units


def vounit_compatible(unit):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=units.UnitsWarning)
        try:
            unit.to_string(format="vounit")
        except Exception:  # noqa: BLE001
            return False

        return True


def create_vounits():
    return sorted(
        {u for u in list(units.__dict__.values()) if isinstance(u, units.UnitBase) and vounit_compatible(u)},
        key=str,
    )


def create_non_vounits():
    return sorted(
        {u for u in list(units.__dict__.values()) if isinstance(u, units.UnitBase) and not vounit_compatible(u)},
        key=str,
    )


@pytest.mark.parametrize("unit", create_vounits())
def test_vounit_serialization(unit, tmp_path):
    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["unit"] = unit
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert af["unit"].is_equivalent(unit)

    with asdf.open(file_path, _force_raw_types=True) as af:
        assert isinstance(af["unit"], asdf.tagged.TaggedString)
        assert af["unit"]._tag.startswith("tag:stsci.edu:asdf/unit/unit-")


@pytest.mark.parametrize("unit", create_non_vounits())
def test_non_vounit_serialization(unit, tmp_path):
    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["unit"] = unit
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert af["unit"].is_equivalent(unit)

    with asdf.open(file_path, _force_raw_types=True) as af:
        assert isinstance(af["unit"], asdf.tagged.TaggedString)
        assert af["unit"]._tag.startswith("tag:astropy.org:astropy/units/unit-")


def test_read():
    yaml = """
unit: !unit/unit-1.0.0 "2.1798721  10-18kg m2 s-2"
    """
    buff = helpers.yaml_to_asdf(yaml)
    with asdf.open(buff) as af:
        assert af["unit"].is_equivalent(units.Ry)
