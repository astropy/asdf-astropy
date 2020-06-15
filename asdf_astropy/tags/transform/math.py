# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-

from astropy.modeling import math_functions
from .basic import TransformConverter


__all__ = ['NpUfuncConverter']


math_classes = []


def make_math_classes():
    for name in math_functions.__all__:
        math_classes.append(getattr(math_functions, name))


make_math_classes()


class NpUfuncConverter(TransformConverter):
    tags = {"http://asdf-format.org/schemas/transform/math_functions-2.0.0",
            "tag:stsci.edu:asdf/transform/math_functions-1.0.0",
            }
    types = set(math_classes)

    def from_tree_transform(self, node):
        klass_name = math_functions._make_class_name(node['func_name'])
        klass = getattr(math_functions, klass_name)
        return klass()

    def to_tree_transform(self, model):
        return {'func_name': model.func.__name__}
