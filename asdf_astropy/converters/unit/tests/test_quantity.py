import pytest

import asdf
from asdf.tests import helpers
from astropy import units
from astropy.units import Quantity
import numpy as np
from numpy.testing import assert_array_equal


TEST_QUANTITIES = [
    # Scalar:
    Quantity(2.71828, units.kpc),
    # Single element array:
    Quantity([3.14159], units.kg),
    # Multiple element array:
    Quantity([x * 2.3081 for x in range(10)], units.ampere),
    # Multiple dimension array:
    Quantity(np.arange(100, dtype=np.float64).reshape(5, 20), units.km),
]


@pytest.mark.parametrize("quantity", TEST_QUANTITIES)
def test_serialization(quantity, tmp_path):
    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["quantity"] = quantity
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert (af["quantity"] == quantity).all()


def test_read_untagged_unit():
    yaml = """
quantity: !unit/quantity-1.1.0
  value: 2.71828
  unit: kpc
    """
    buff = helpers.yaml_to_asdf(yaml)
    with asdf.open(buff) as af:
        assert af["quantity"].value == 2.71828
        assert af["quantity"].unit.is_equivalent(units.kpc)


def test_read_tagged_unit():
    yaml = """
quantity: !unit/quantity-1.1.0
  value: 2.71828
  unit: !unit/unit-1.0.0 kpc
    """
    buff = helpers.yaml_to_asdf(yaml)
    with asdf.open(buff) as af:
        assert af["quantity"].value == 2.71828
        assert af["quantity"].unit.is_equivalent(units.kpc)


def test_read_array_value():
    yaml = """
quantity: !unit/quantity-1.1.0
  value: !core/ndarray-1.0.0 [1.0, 2.0, 3.0, 4.0]
  unit: km
    """
    buff = helpers.yaml_to_asdf(yaml)
    with asdf.open(buff) as af:
        assert_array_equal(af["quantity"].value, np.array([1.0, 2.0, 3.0, 4.0]))
        assert af["quantity"].unit.is_equivalent(units.km)
