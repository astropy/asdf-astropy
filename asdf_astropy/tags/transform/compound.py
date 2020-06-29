# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
from asdf import tagged
from asdf.tests.helpers import assert_tree_match
from .basic import TransformConverter
from astropy.modeling.core import Model, CompoundModel
from astropy.modeling.models import Identity, Mapping, Const1D


__all__ = ['CompoundConverter', 'RemapAxesConverter']


_operator_to_tag_mapping = {
    '+':  'add',
    '-':  'subtract',
    '*':  'multiply',
    '/':  'divide',
    '**': 'power',
    '|':  'compose',
    '&':  'concatenate',
    'fix_inputs': 'fix_inputs'
}


_tag_to_method_mapping = {
    'add':         '__add__',
    'subtract':    '__sub__',
    'multiply':    '__mul__',
    'divide':      '__truediv__',
    'power':       '__pow__',
    'compose':     '__or__',
    'concatenate': '__and__',
    'fix_inputs':  'fix_inputs'
}


class CompoundConverter(TransformConverter):
    tags = {"http://asdf-format.org/schemas/transform/add-2.0.0",
            "http://asdf-format.org/schemas/transform/subtract-2.0.0",
            "http://asdf-format.org/schemas/transform/multiply-2.0.0",
            "http://asdf-format.org/schemas/transform/divide-2.0.0",
            "http://asdf-format.org/schemas/transform/power-2.0.0",
            "http://asdf-format.org/schemas/transform/compose-2.0.0",
            "http://asdf-format.org/schemas/transform/concatenate-2.0.0",
            "http://asdf-format.org/schemas/transform/fix_inputs-2.0.0",
            "tag:stsci.edu:asdf/transform/add-1.0.0",
            "tag:stsci.edu:asdf/transform/add-1.1.0",
            "tag:stsci.edu:asdf/transform/add-1.2.0",
            "tag:stsci.edu:asdf/transform/subtract-1.0.0",
            "tag:stsci.edu:asdf/transform/subtract-1.1.0",
            "tag:stsci.edu:asdf/transform/subtract-1.2.0",
            "tag:stsci.edu:asdf/transform/multiply-1.0.0",
            "tag:stsci.edu:asdf/transform/multiply-1.1.0",
            "tag:stsci.edu:asdf/transform/multiply-1.2.0",
            "tag:stsci.edu:asdf/transform/divide-1.0.0",
            "tag:stsci.edu:asdf/transform/divide-1.1.0",
            "tag:stsci.edu:asdf/transform/divide-1.2.0",
            "tag:stsci.edu:asdf/transform/power-1.0.0",
            "tag:stsci.edu:asdf/transform/power-1.1.0",
            "tag:stsci.edu:asdf/transform/power-1.2.0",
            "tag:stsci.edu:asdf/transform/compose-1.0.0",
            "tag:stsci.edu:asdf/transform/compose-1.1.0",
            "tag:stsci.edu:asdf/transform/compose-1.2.0",
            "tag:stsci.edu:asdf/transform/concatenate-1.0.0",
            "tag:stsci.edu:asdf/transform/concatenate-1.1.0",
            "tag:stsci.edu:asdf/transform/concatenate-1.2.0",
            "tag:stsci.edu:asdf/transform/fix_inputs-1.1.0",
            "tag:stsci.edu:asdf/transform/fix_inputs-1.2.0",
            }
    types = {CompoundModel}

    def from_tree_transform(self, node):
        tag = node._tag[node._tag.rfind('/')+1:]
        tag = tag[:tag.rfind('-')]
        oper = _tag_to_method_mapping[tag]
        left = node['forward'][0]
        if not isinstance(left, Model):
            raise TypeError("Unknown model type '{0}'".format(
                node['forward'][0]._tag))
        right = node['forward'][1]
        if (not isinstance(right, Model) and
                not (oper == 'fix_inputs' and isinstance(right, dict))):
            raise TypeError("Unknown model type '{0}'".format(
                node['forward'][1]._tag))
        if oper == 'fix_inputs':
            right = dict(zip(right['keys'], right['values']))
            model = CompoundModel('fix_inputs', left, right)
        else:
            model = getattr(left, oper)(right)
        return model

    def to_tree_transform(self, model):
        left = model.left

        if isinstance(model.right, dict):
            right = {
                'keys': list(model.right.keys()),
                'values': list(model.right.values())
            }
        else:
            right = model.right

        node = {
            'forward': [left, right]
        }

        try:
            tag_name = ('http://asdf-format.org/schemas/transform/' +
                        _operator_to_tag_mapping[model.op] + '-2.0.0')
        except KeyError:
            raise ValueError(f"Unknown operator '{model.op}'")

        node = tagged.tag_object(tag_name, node)

        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert_tree_match(a.left, b.left)
        assert_tree_match(a.right, b.right)


class RemapAxesConverter(TransformConverter):
    tags = {"http://asdf-format.org/schemas/transform/remap_axes-2.0.0",
            "tag:stsci.edu:asdf/transform/remap_axes-1.0.0",
            "tag:stsci.edu:asdf/transform/remap_axes-1.1.0",
            "tag:stsci.edu:asdf/transform/remap_axes-1.2.0",
            "tag:stsci.edu:asdf/transform/remap_axes-1.3.0",
            }

    types = {Mapping}

    def from_tree_transform(self, node):
        mapping = node['mapping']
        n_inputs = node.get('n_inputs')
        if all([isinstance(x, int) for x in mapping]):
            return Mapping(tuple(mapping), n_inputs)

        if n_inputs is None:
            n_inputs = max([x for x in mapping
                            if isinstance(x, int)]) + 1

        transform = Identity(n_inputs)
        new_mapping = []
        i = n_inputs
        for entry in mapping:
            if isinstance(entry, int):
                new_mapping.append(entry)
            else:
                new_mapping.append(i)
                transform = transform & Const1D(entry.value)
                i += 1
        return transform | Mapping(new_mapping)

    def to_tree_transform(self, model):
        node = {'mapping': list(model.mapping)}
        if model.n_inputs > max(model.mapping) + 1:
            node['n_inputs'] = model.n_inputs
        return node

    def assert_equal(self, a, b):
        TransformConverter.assert_equal(a, b)
        assert a.mapping == b.mapping
        assert(a.n_inputs == b.n_inputs)
