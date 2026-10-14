from asdf.extension import Converter

_COSMOLOGY_CLASSES = (
    "FlatLambdaCDM",
    "Flatw0waCDM",
    "Flatw0wzCDM",
    "FlatwCDM",
    "FlatwpwaCDM",
    "LambdaCDM",
    "w0waCDM",
    "w0wzCDM",
    "wCDM",
    "wpwaCDM",
)


class CosmologyConverter(Converter):
    tags = ("tag:astropy.org:astropy/cosmology/cosmology-*",)
    types = tuple(f"astropy.cosmology.{name}" for name in _COSMOLOGY_CLASSES)

    def to_yaml_tree(self, obj, tag, ctx):
        node = obj.to_format("mapping", cosmology_as_str=True)
        node["meta"] = dict(node["meta"])
        return node

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.cosmology import Cosmology

        node = {k: _with_cosmology_unit(v) for k, v in node.items()}
        node["meta"] = {k: _with_cosmology_unit(v) for k, v in node.get("meta", {}).items()}
        return Cosmology.from_format(node, format="mapping")


def _with_cosmology_unit(value):
    """Re-parse units (e.g. redshift) that asdf could not recognize because
    astropy.cosmology.units are not enabled by default."""
    # ponytail: only top-level params and meta values, recurse if nested meta needs it
    from astropy.cosmology import units as cu
    from astropy.units import Quantity, Unit, UnrecognizedUnit, add_enabled_units

    if isinstance(value, Quantity) and isinstance(value.unit, UnrecognizedUnit):
        with add_enabled_units(cu):
            return Quantity(value.value, Unit(value.unit.name))
    return value
