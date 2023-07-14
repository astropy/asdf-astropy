from asdf.extension import Converter


class RepresentationConverter(Converter):
    tags = ("tag:astropy.org:astropy/coordinates/representation-*",)
    types = (
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
        # classes were moved in https://github.com/astropy/astropy/pull/14792
        "astropy.coordinates.representation.cartesian.CartesianDifferential",
        "astropy.coordinates.representation.cartesian.CartesianRepresentation",
        "astropy.coordinates.representation.cylindrical.CylindricalDifferential",
        "astropy.coordinates.representation.cylindrical.CylindricalRepresentation",
        "astropy.coordinates.representation.spherical.PhysicsSphericalDifferential",
        "astropy.coordinates.representation.spherical.PhysicsSphericalRepresentation",
        "astropy.coordinates.representation.spherical.RadialDifferential",
        "astropy.coordinates.representation.spherical.RadialRepresentation",
        "astropy.coordinates.representation.spherical.SphericalCosLatDifferential",
        "astropy.coordinates.representation.spherical.SphericalDifferential",
        "astropy.coordinates.representation.spherical.SphericalRepresentation",
        "astropy.coordinates.representation.spherical.UnitSphericalRepresentation",
        "astropy.coordinates.representation.spherical.UnitSphericalDifferential",
        "astropy.coordinates.representation.spherical.UnitSphericalCosLatDifferential",
    )

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
