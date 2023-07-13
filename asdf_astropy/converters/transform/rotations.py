from .core import TransformConverterBase, parameter_to_value


class Rotate3DConverter(TransformConverterBase):
    """
    ASDF support for serializing rotation models that
    use the rotate3d tag.
    """

    tags = ("tag:stsci.edu:asdf/transform/rotate3d-*",)
    types = (
        "astropy.modeling.rotations.RotateNative2Celestial",
        "astropy.modeling.rotations.RotateCelestial2Native",
        "astropy.modeling.rotations.EulerAngleRotation",
    )

    def to_yaml_tree_transform(self, model, tag, ctx):
        from astropy.modeling import rotations

        if isinstance(model, rotations.RotateNative2Celestial):
            node = {
                "phi": parameter_to_value(model.lon),
                "theta": parameter_to_value(model.lat),
                "psi": parameter_to_value(model.lon_pole),
                "direction": "native2celestial",
            }
        elif isinstance(model, rotations.RotateCelestial2Native):
            node = {
                "phi": parameter_to_value(model.lon),
                "theta": parameter_to_value(model.lat),
                "psi": parameter_to_value(model.lon_pole),
                "direction": "celestial2native",
            }
        else:
            node = {
                "phi": parameter_to_value(model.phi),
                "theta": parameter_to_value(model.theta),
                "psi": parameter_to_value(model.psi),
                "direction": model.axes_order,
            }

        return node

    def from_yaml_tree_transform(self, node, tag, ctx):
        from astropy.modeling import rotations

        if node["direction"] == "native2celestial":
            return rotations.RotateNative2Celestial(node["phi"], node["theta"], node["psi"])

        if node["direction"] == "celestial2native":
            return rotations.RotateCelestial2Native(node["phi"], node["theta"], node["psi"])

        return rotations.EulerAngleRotation(node["phi"], node["theta"], node["psi"], axes_order=node["direction"])


class RotationSequenceConverter(TransformConverterBase):
    """
    ASDF support for serializing rotation sequence models.
    """

    tags = ("tag:stsci.edu:asdf/transform/rotate_sequence_3d-*",)
    types = (
        "astropy.modeling.rotations.RotationSequence3D",
        "astropy.modeling.rotations.SphericalRotationSequence",
    )

    def to_yaml_tree_transform(self, model, tag, ctx):
        from astropy.modeling import rotations

        node = {"angles": list(model.angles.value)}
        node["axes_order"] = model.axes_order
        if isinstance(model, rotations.SphericalRotationSequence):
            node["rotation_type"] = "spherical"
        elif isinstance(model, rotations.RotationSequence3D):
            node["rotation_type"] = "cartesian"
        else:
            msg = f"Cannot serialize model of type {type(model)}"
            raise TypeError(msg)
        return node

    def from_yaml_tree_transform(self, node, tag, ctx):
        from astropy.modeling import rotations

        angles = node["angles"]
        axes_order = node["axes_order"]
        rotation_type = node["rotation_type"]
        if rotation_type == "cartesian":
            return rotations.RotationSequence3D(angles, axes_order=axes_order)

        if rotation_type == "spherical":
            return rotations.SphericalRotationSequence(angles, axes_order=axes_order)

        msg = f"Unrecognized rotation_type: {rotation_type}"
        raise ValueError(msg)
