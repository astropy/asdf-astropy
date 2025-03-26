import asdf
import numpy as np
import pytest
from asdf.testing import helpers
from astropy import units
from astropy.units import Quantity
from astropy.utils.introspection import minversion
from numpy.testing import assert_array_equal

from asdf_astropy.tests.versions import ASTROPY_GE_7_1


def asdf_open_memory_mapping_kwarg(memmap: bool) -> dict:
    if minversion("asdf", "3.1.0"):
        return {"memmap": memmap}
    return {"copy_arrays": not memmap}


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
    buff = helpers.yaml_to_asdf(yaml, version="1.5.0")
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
    buff = helpers.yaml_to_asdf(yaml, version="1.5.0")
    with asdf.open(buff) as af:
        assert af["quantity"].value == value
        assert af["quantity"].unit.is_equivalent(units.kpc)


def test_read_array_value():
    yaml = """
quantity: !unit/quantity-1.1.0
  value: !core/ndarray-1.0.0 [1.0, 2.0, 3.0, 4.0]
  unit: km
    """
    buff = helpers.yaml_to_asdf(yaml, version="1.5.0")
    with asdf.open(buff) as af:
        assert_array_equal(af["quantity"].value, np.array([1.0, 2.0, 3.0, 4.0]))
        assert af["quantity"].unit.is_equivalent(units.km)


def test_memmap(tmp_path):
    """
    Test that memmap (memmap=True) works with quantities.

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
    with asdf.open(file_path, mode="rw", **asdf_open_memory_mapping_kwarg(memmap=True)) as af:
        assert (af.tree["quantity"] == quantity).all()
        assert af.tree["quantity"][-1, -1] != new_value

        af.tree["quantity"][-1, -1] = new_value

        assert af.tree["quantity"][-1, -1] == new_value
        assert (af.tree["quantity"] != quantity).any()
        assert (af.tree["quantity"] == new_quantity).all()

    with asdf.open(file_path, mode="rw", **asdf_open_memory_mapping_kwarg(memmap=True)) as af:
        assert af.tree["quantity"][-1, -1] == new_value
        assert (af.tree["quantity"] != quantity).any()
        assert (af.tree["quantity"] == new_quantity).all()


def test_no_memmap(tmp_path):
    """
    Test that turning off memmap (memmap=False) works as expected for quantities
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
    with asdf.open(file_path, mode="rw", **asdf_open_memory_mapping_kwarg(memmap=False)) as af:
        assert (af.tree["quantity"] == quantity).all()
        assert af.tree["quantity"][-1, -1] != new_value

        af.tree["quantity"][-1, -1] = new_value

        assert af.tree["quantity"][-1, -1] == new_value
        assert (af.tree["quantity"] != quantity).any()
        assert (af.tree["quantity"] == new_quantity).all()

    with asdf.open(file_path, mode="rw", **asdf_open_memory_mapping_kwarg(memmap=False)) as af:
        assert af.tree["quantity"][-1, -1] != new_value
        assert (af.tree["quantity"] != new_quantity).any()
        assert (af.tree["quantity"] == quantity).all()


@pytest.mark.skipif(ASTROPY_GE_7_1, reason="MaskedQuantity support was added in astropy 7.1")
def test_masked_quantity_raises():
    yaml = """
quantity: !unit/quantity-1.1.0
  unit: !unit/unit-1.0.0 Ymol
  value: !core/ndarray-1.0.0
    data: [1.0, 2.0, null]
    mask: !core/ndarray-1.0.0
      data: [false, false, true]
      datatype: bool8
      shape: [3]
    datatype: float64
    shape: [3]
"""
    buff = helpers.yaml_to_asdf(yaml, version="1.5.0")
    with pytest.raises(NotImplementedError, match="MaskedQuantity support requires astropy 7.1 or later"):
        asdf.open(buff)
