
import asdf
from asdf.tests import helpers
from astropy import units
import pytest


@pytest.fixture(autouse=True)
def remove_astropy_extensions():
    """
    Disable the old astropy extension so that it doesn't
    confuse our test results.
    """
    with asdf.config_context() as config:
        config.remove_extension(package="astropy")
        yield


UNREPRESENTABLE_UNITS = {
    units.deg_C,
    units.dex,
    units.electron,
    units.littleh,
    units.mgy,
    units.nmgy,
    units.percent,
    units.Sun,
}

TEST_UNITS = [u for u in units.__dict__.values() if isinstance(u, units.UnitBase) and u not in UNREPRESENTABLE_UNITS]


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
