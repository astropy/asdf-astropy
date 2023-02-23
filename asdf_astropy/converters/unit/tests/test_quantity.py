import asdf
import numpy as np
import pytest
from asdf.testing import helpers
from astropy import units
from astropy.units import Quantity
from numpy.testing import assert_array_equal


def create_quantities():
    return [
        # Scalar:
        Quantity(2.71828, units.kpc),
        # Non-float scalar:
        Quantity(7, units.K, dtype=np.int32),
        # Single element array:
        Quantity([3.14159], units.kg),
        # Multiple element array:
        Quantity([x * 2.3081 for x in range(10)], units.ampere),
        # Multiple dimension array:
        Quantity(np.arange(100, dtype=np.float64).reshape(5, 20), units.km),
        # Non-float array:
        Quantity(np.zeros((5, 5), dtype=np.uint16), units.cm, dtype=np.uint16),
    ]


@pytest.mark.parametrize("quantity", create_quantities())
def test_serialization(quantity, tmp_path):
    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["quantity"] = quantity
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert (af["quantity"].value == quantity.value).all()
        assert af["quantity"].dtype == quantity.dtype
        assert (af["quantity"] == quantity).all()


def test_read_untagged_unit():
    value = 2.71828
    yaml = f"""
quantity: !unit/quantity-1.1.0
  value: {value}
  unit: kpc
    """
    buff = helpers.yaml_to_asdf(yaml)
    with asdf.open(buff) as af:
        assert af["quantity"].value == value
        assert af["quantity"].unit.is_equivalent(units.kpc)


def test_read_tagged_unit():
    value = 2.71828
    yaml = f"""
quantity: !unit/quantity-1.1.0
  value: {value}
  unit: !unit/unit-1.0.0 kpc
    """
    buff = helpers.yaml_to_asdf(yaml)
    with asdf.open(buff) as af:
        assert af["quantity"].value == value
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


def test_memmap(tmp_path):
    """
    Test that memmap (copy_arrays=False) works with quantities.

    Unfortunately, this is not a simple `isinstance(obj, np.memmap)`
    Instead it requires a more complicated check.
    """
    file_path = tmp_path / "test.asdf"
    quantity = Quantity(np.arange(100, dtype=np.float64).reshape(5, 20), units.km)

    new_value = 42.14 * units.cm
    new_quantity = quantity.copy()
    new_quantity[-1, -1] = new_value

    # Write initial ASDF file
    with asdf.AsdfFile() as af:
        af.tree = {"quantity": quantity}
        af.write_to(file_path)

    # Update a value in the ASDF file
    with asdf.open(file_path, mode="rw", copy_arrays=False) as af:
        assert (af.tree["quantity"] == quantity).all()
        assert af.tree["quantity"][-1, -1] != new_value

        af.tree["quantity"][-1, -1] = new_value

        assert af.tree["quantity"][-1, -1] == new_value
        assert (af.tree["quantity"] != quantity).any()
        assert (af.tree["quantity"] == new_quantity).all()

    with asdf.open(file_path, mode="rw", copy_arrays=False) as af:
        assert af.tree["quantity"][-1, -1] == new_value
        assert (af.tree["quantity"] != quantity).any()
        assert (af.tree["quantity"] == new_quantity).all()


def test_no_memmap(tmp_path):
    """
    Test that turning off memmap (copy_arrays=True) works as expected for quantities
    """
    file_path = tmp_path / "test.asdf"
    quantity = Quantity(np.arange(100, dtype=np.float64).reshape(5, 20), units.km)

    new_value = 42.14 * units.cm
    new_quantity = quantity.copy()
    new_quantity[-1, -1] = new_value

    # Write initial ASDF file
    with asdf.AsdfFile() as af:
        af.tree = {"quantity": quantity}
        af.write_to(file_path)

    # Update a value in the ASDF file
    with asdf.open(file_path, mode="rw", copy_arrays=True) as af:
        assert (af.tree["quantity"] == quantity).all()
        assert af.tree["quantity"][-1, -1] != new_value

        af.tree["quantity"][-1, -1] = new_value

        assert af.tree["quantity"][-1, -1] == new_value
        assert (af.tree["quantity"] != quantity).any()
        assert (af.tree["quantity"] == new_quantity).all()

    with asdf.open(file_path, mode="rw", copy_arrays=True) as af:
        assert af.tree["quantity"][-1, -1] != new_value
        assert (af.tree["quantity"] != new_quantity).any()
        assert (af.tree["quantity"] == quantity).all()
