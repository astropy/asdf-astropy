from asdf.extension import Converter


class RepresentationConverter(Converter):
    tags = ["tag:astropy.org:astropy/coordinates/representation-*"]

    types = [
        "astropy.coordinates.representation.CartesianDifferential",
        "astropy.coordinates.representation.CartesianRepresentation",
        "astropy.coordinates.representation.CylindricalDifferential",
        "astropy.coordinates.representation.CylindricalRepresentation",
        "astropy.coordinates.representation.PhysicsSphericalDifferential",
        "astropy.coordinates.representation.PhysicsSphericalRepresentation",
        "astropy.coordinates.representation.RadialDifferential",
        "astropy.coordinates.representation.RadialRepresentation",
        "astropy.coordinates.representation.SphericalCosLatDifferential",
        "astropy.coordinates.representation.SphericalDifferential",
        "astropy.coordinates.representation.SphericalRepresentation",
        "astropy.coordinates.representation.UnitSphericalCosLatDifferential",
        "astropy.coordinates.representation.UnitSphericalDifferential",
        "astropy.coordinates.representation.UnitSphericalRepresentation",
    ]

    def to_yaml_tree(self, obj, tag, ctx):
        components = {}
        for c in obj.components:
            value = getattr(obj, "_" + c, None)
            if value is not None:
                components[c] = value

        return {
            "type": type(obj).__name__,
            "components": components,
        }

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.coordinates import representation

        return getattr(representation, node["type"])(**node["components"])
