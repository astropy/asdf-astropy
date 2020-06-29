# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-

import numpy as np
from numpy.testing import assert_array_equal

from astropy.modeling import tabular
from astropy import units as u
from .basic import TransformConverter

__all__ = ['TabularConverter']


class TabularConverter(TransformConverter):
    tags = {"http://asdf-format.org/schemas/transform/tabular-2.0.0",
            "tag:stsci.edu:asdf/transform/tabular-1.0.0",
            "tag:stsci.edu:asdf/transform/tabular-1.1.0",
            "tag:stsci.edu:asdf/transform/tabular-1.2.0",
            }
    types = {tabular.Tabular2D, tabular.Tabular1D}

    def from_tree_transform(self, node):
        lookup_table = node.pop("lookup_table")
        dim = lookup_table.ndim
        fill_value = node.pop("fill_value", None)
        if dim == 1:
            # The copy is necessary because the array is memory mapped.
            points = (node['points'][0][:],)
            model = tabular.Tabular1D(points=points, lookup_table=lookup_table,
                                      method=node['method'], bounds_error=node['bounds_error'],
                                      fill_value=fill_value)
        elif dim == 2:
            points = tuple([p[:] for p in node['points']])
            model = tabular.Tabular2D(points=points, lookup_table=lookup_table,
                                      method=node['method'], bounds_error=node['bounds_error'],
                                      fill_value=fill_value)

        else:
            tabular_class = tabular.tabular_model(dim)
            points = tuple([p[:] for p in node['points']])
            model = tabular_class(points=points, lookup_table=lookup_table,
                                  method=node['method'], bounds_error=node['bounds_error'],
                                  fill_value=fill_value)

        return model

    def to_tree_transform(self, model):
        node = {}
        node["fill_value"] = model.fill_value
        node["lookup_table"] = model.lookup_table
        node["points"] = [p for p in model.points]
        node["method"] = str(model.method)
        node["bounds_error"] = model.bounds_error
        return node

    def assert_equal(self, a, b):
        if isinstance(a.lookup_table, u.Quantity):
            assert u.allclose(a.lookup_table, b.lookup_table)
            assert u.allclose(a.points, b.points)
            for i in range(len(a.bounding_box)):
                assert u.allclose(a.bounding_box[i], b.bounding_box[i])
        else:
            assert_array_equal(a.lookup_table, b.lookup_table)
            assert_array_equal(a.points, b.points)
            assert_array_equal(a.bounding_box, b.bounding_box)
        assert (a.method == b.method)
        if a.fill_value is None:
            assert b.fill_value is None
        elif np.isnan(a.fill_value):
            assert np.isnan(b.fill_value)
        else:
            assert(a.fill_value == b.fill_value)
        assert(a.bounds_error == b.bounds_error)
