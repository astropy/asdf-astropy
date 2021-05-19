
import warnings

import asdf
from asdf.tests import helpers
from astropy import units
import pytest


def vounit_compatible(unit):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=units.UnitsWarning)
        try:
            unit.to_string(format="vounit")
            return True
        except Exception:
            return False


TEST_UNITS = [u for u in list(units.__dict__.values()) if isinstance(u, units.UnitBase) and vounit_compatible(u)]


@pytest.mark.parametrize("unit", TEST_UNITS)
# Ignore warnings due to VOUnit deprecations
@pytest.mark.filterwarnings("ignore::astropy.units.core.UnitsWarning")
def test_serialization(unit, tmp_path):
    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["unit"] = unit
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert af["unit"].is_equivalent(unit)


def test_read():
    yaml = """
unit: !unit/unit-1.0.0 "2.1798721  10-18kg m2 s-2"
    """
    buff = helpers.yaml_to_asdf(yaml)
    with asdf.open(buff) as af:
        assert af["unit"].is_equivalent(units.Ry)
