# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-

from numpy.testing import assert_array_equal

from astropy.modeling import projections, rotations
from .basic import TransformConverter
from . import _parameter_to_value


__all__ = ['AffineConverter', 'Rotate2DConverter', 'Rotate3DConverter',
           'RotationSequenceConverter']


class AffineConverter(TransformConverter):
    tags = {"http://asdf-format.org/schemas/transform/affine-2.0.0",
            "tag:stsci.edu:asdf/transform/affine-1.0.0",
            "tag:stsci.edu:asdf/transform/affine-1.1.0",
            "tag:stsci.edu:asdf/transform/affine-1.2.0",
            "tag:stsci.edu:asdf/transform/affine-1.3.0",
            }

    types = {projections.AffineTransformation2D}

    def from_tree_transform(self, node):
        matrix = node['matrix']
        translation = node['translation']
        if matrix.shape != (2, 2):
            raise NotImplementedError(
                "asdf currently only supports 2x2 (2D) rotation transformation "
                "matrices")
        if translation.shape != (2,):
            raise NotImplementedError(
                "asdf currently only supports 2D translation transformations.")

        return projections.AffineTransformation2D(
            matrix=matrix, translation=translation)

    def to_tree_transform(self, model):
        return {'matrix': _parameter_to_value(model.matrix),
                'translation': _parameter_to_value(model.translation)}

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (a.__class__ == b.__class__)
        assert_array_equal(a.matrix, b.matrix)
        assert_array_equal(a.translation, b.translation)


class Rotate2DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/rotate2d-2.0.0",
            "tag:stsci.edu:asdf/transform/rotate2d-1.0.0",
            "tag:stsci.edu:asdf/transform/rotate2d-1.1.0",
            "tag:stsci.edu:asdf/transform/rotate2d-1.2.0",
            "tag:stsci.edu:asdf/transform/rotate2d-1.3.0",
            }

    types = {rotations.Rotation2D}

    def from_tree_transform(self, node):
        return rotations.Rotation2D(node['angle'])

    def to_tree_transform(self, model):
        return {'angle': _parameter_to_value(model.angle)}

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, rotations.Rotation2D) and
                isinstance(b, rotations.Rotation2D))
        assert_array_equal(a.angle, b.angle)


class Rotate3DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/rotate3d-2.0.0",
            "tag:stsci.edu:asdf/transform/rotate3d-1.0.0",
            "tag:stsci.edu:asdf/transform/rotate3d-1.1.0",
            "tag:stsci.edu:asdf/transform/rotate3d-1.2.0",
            "tag:stsci.edu:asdf/transform/rotate3d-1.3.0",
            }

    types = {rotations.RotateNative2Celestial,
             rotations.RotateCelestial2Native,
             rotations.EulerAngleRotation}

    def from_tree_transform(self, node):
        if node['direction'] == 'native2celestial':
            return rotations.RotateNative2Celestial(node["phi"],
                                                    node["theta"],
                                                    node["psi"])
        elif node['direction'] == 'celestial2native':
            return rotations.RotateCelestial2Native(node["phi"],
                                                    node["theta"],
                                                    node["psi"])
        else:
            return rotations.EulerAngleRotation(node["phi"],
                                                node["theta"],
                                                node["psi"],
                                                axes_order=node["direction"])

    def to_tree_transform(self, model):
        if isinstance(model, rotations.RotateNative2Celestial):
            try:
                node = {"phi": _parameter_to_value(model.lon),
                        "theta": _parameter_to_value(model.lat),
                        "psi": _parameter_to_value(model.lon_pole),
                        "direction": "native2celestial"
                        }
            except AttributeError:
                node = {"phi": model.lon,
                        "theta": model.lat,
                        "psi": model.lon_pole,
                        "direction": "native2celestial"
                        }
        elif isinstance(model, rotations.RotateCelestial2Native):
            try:
                node = {"phi": _parameter_to_value(model.lon),
                        "theta": _parameter_to_value(model.lat),
                        "psi": _parameter_to_value(model.lon_pole),
                        "direction": "celestial2native"
                        }
            except AttributeError:
                node = {"phi": model.lon,
                        "theta": model.lat,
                        "psi": model.lon_pole,
                        "direction": "celestial2native"
                        }
        else:
            node = {"phi": _parameter_to_value(model.phi),
                    "theta": _parameter_to_value(model.theta),
                    "psi": _parameter_to_value(model.psi),
                    "direction": model.axes_order
                    }

        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert a.__class__ == b.__class__
        if a.__class__.__name__ == "EulerAngleRotation":
            assert_array_equal(a.phi, b.phi)
            assert_array_equal(a.psi, b.psi)
            assert_array_equal(a.theta, b.theta)
        else:
            assert_array_equal(a.lon, b.lon)
            assert_array_equal(a.lat, b.lat)
            assert_array_equal(a.lon_pole, b.lon_pole)


class RotationSequenceConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/rotate_sequence_3d-2.0.0",
            "tag:stsci.edu:asdf/transform/rotate_sequence_3d-1.0.0",
            }

    types = {rotations.RotationSequence3D,
             rotations.SphericalRotationSequence}

    def from_tree_transform(self, node):
        angles = node['angles']
        axes_order = node['axes_order']
        rotation_type = node['rotation_type']
        if rotation_type == 'cartesian':
            return rotations.RotationSequence3D(angles, axes_order=axes_order)
        elif rotation_type == 'spherical':
            return rotations.SphericalRotationSequence(angles, axes_order=axes_order)
        else:
            raise ValueError(f"Unrecognized rotation_type: {rotation_type}")

    def to_tree_transform(self, model):
        node = {'angles': list(model.angles.value)}
        node['axes_order'] = model.axes_order
        if isinstance(model, rotations.SphericalRotationSequence):
            node['rotation_type'] = "spherical"
        elif isinstance(model, rotations.RotationSequence3D):
            node['rotation_type'] = "cartesian"
        else:
            raise ValueError(f"Cannot serialize model of type {type(model)}")
        return node

    def assert_equal(self, a, b):
        TransformConverter.assert_equal(a, b)
        assert a.__class__.__name__ == b.__class__.__name__
        assert_array_equal(a.angles, b.angles)
        assert a.axes_order == b.axes_order


class GenericProjectionConverter(TransformConverter):

    def from_tree_transform(self, node):
        args = []
        for param_name, default in self.params:
            args.append(node.get(param_name, default))

        for c in self.types:
            if c.name.lower().split('_')[0].startswith(node['direction']):
                return c(*args)
        raise TypeError("Unable to initialize {self}")

    def to_tree_transform(self, model):
        node = {}
        node['direction'] = model.__class__.__name__.lower().split('_')[0]

        for param_name, default in self.params:
            val = getattr(model, param_name).value
            if val != default:
                node[param_name] = val
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert a.__class__ == b.__class__


_generic_projections = {
    'zenithal_perspective': ('ZenithalPerspective', (('mu', 0.0), ('gamma', 0.0)), '1.2.0'),
    'gnomonic': ('Gnomonic', (), None),
    'stereographic': ('Stereographic', (), None),
    'slant_orthographic': ('SlantOrthographic', (('xi', 0.0), ('eta', 0.0)), None),
    'zenithal_equidistant': ('ZenithalEquidistant', (), None),
    'zenithal_equal_area': ('ZenithalEqualArea', (), None),
    'airy': ('Airy', (('theta_b', 90.0),), '1.2.0'),
    'cylindrical_perspective': ('CylindricalPerspective', (('mu', 0.0), ('lam', 0.0)), '1.2.0'),
    'cylindrical_equal_area': ('CylindricalEqualArea', (('lam', 0.0),), '1.2.0'),
    'plate_carree': ('PlateCarree', (), None),
    'mercator': ('Mercator', (), None),
    'sanson_flamsteed': ('SansonFlamsteed', (), None),
    'parabolic': ('Parabolic', (), None),
    'molleweide': ('Molleweide', (), None),
    'hammer_aitoff': ('HammerAitoff', (), None),
    'conic_perspective': ('ConicPerspective', (('sigma', 0.0), ('delta', 0.0)), '1.2.0'),
    'conic_equal_area': ('ConicEqualArea', (('sigma', 0.0), ('delta', 0.0)), '1.2.0'),
    'conic_equidistant': ('ConicEquidistant', (('sigma', 0.0), ('delta', 0.0)), '1.2.0'),
    'conic_orthomorphic': ('ConicOrthomorphic', (('sigma', 0.0), ('delta', 0.0)), '1.2.0'),
    'bonne_equal_area': ('BonneEqualArea', (('theta1', 0.0),), '1.2.0'),
    'polyconic': ('Polyconic', (), None),
    'tangential_spherical_cube': ('TangentialSphericalCube', (), None),
    'cobe_quad_spherical_cube': ('COBEQuadSphericalCube', (), None),
    'quad_spherical_cube': ('QuadSphericalCube', (), None),
    'healpix': ('HEALPix', (('H', 4.0), ('X', 3.0)), None),
    'healpix_polar': ('HEALPixPolar', (), None)
}


def make_projection_types():
    for tag_name, (name, params, version) in _generic_projections.items():
        class_name = f'{name}Converter'

        type_names = {f'Pix2Sky_{name}',
                      f'Sky2Pix_{name}'
                      }

        types = set([getattr(projections, name) for name in type_names])

        tags = {f"http://asdf-format.org/schemas/transform/{tag_name}-2.0.0",
                f"tag:stsci.edu:asdf/transform/{tag_name}-1.0.0",
                f"tag:stsci.edu:asdf/transform/{tag_name}-1.1.0",
                f"tag:stsci.edu:asdf/transform/{tag_name}-1.2.0",
                f"tag:stsci.edu:asdf/transform/{tag_name}-1.3.0",
                }

        members = {'name': f'transform/{tag_name}',
                   'types': types,
                   'tags': tags,
                   'params': params}

        globals()[class_name] = type(
            str(class_name),
            (GenericProjectionConverter,),
            members)

        __all__.append(class_name)


make_projection_types()
