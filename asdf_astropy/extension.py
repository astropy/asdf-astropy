# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-

import os

from asdf.extension import AsdfExtension, BuiltinExtension
from asdf.util import filepath_to_url

# Make sure that all tag implementations are imported by the time we create
# the extension class so that _astropy_asdf_types is populated correctly. We
# could do this using __init__ files, except it causes pytest import errors in
# the case that asdf is not installed.
'''
from .tags.coordinates.angle import *  # noqa
from .tags.coordinates.frames import *  # noqa
from .tags.coordinates.earthlocation import *  # noqa
from .tags.coordinates.skycoord import *  # noqa
from .tags.coordinates.representation import *  # noqa
from .tags.coordinates.spectralcoord import *  # noqa
from .tags.fits.fits import *  # noqa
from .tags.table.table import *  # noqa
from .tags.time.time import *  # noqa
from .tags.time.timedelta import *  # noqa
'''
from .tags.transform.basic import *  # noqa
from .tags.transform.compound import *  # noqa
from .tags.transform.functional_models import *  # noqa
from .tags.transform.physical_models import *  # noqa
from .tags.transform.math import *  # noqa
from .tags.transform.polynomial import *  # noqa
from .tags.transform.powerlaws import *  # noqa
from .tags.transform.projections import *  # noqa
from .tags.transform.tabular import *  # noqa
'''
from .tags.unit.quantity import *  # noqa
from .tags.unit.unit import *  # noqa
from .tags.unit.equivalency import *  # noqa
'''
from .types import _astropy_types, _astropy_asdf_types, _asdf_format_types


__all__ = ['AsdfFormatExtension', 'AstropyExtension', 'AstropyAsdfExtension']


ASTROPY_SCHEMA_URI_BASE = 'http://asdf-format.org/schemas/'

import asdf_transform_schemas
asdf_transform_path = asdf_transform_schemas.__path__[0]

SCHEMA_PATH = os.path.abspath(
    os.path.join(asdf_transform_path, 'schemas'))
ASTROPY_URL_MAPPING = [(ASTROPY_SCHEMA_URI_BASE,
                        filepath_to_url(SCHEMA_PATH + '/{url_suffix}.yaml'))]

'''
# This extension is used to register custom types that have both tags and
# schemas defined by Astropy.
class AstropyExtension(AsdfExtension):
    @property
    def types(self):
        return _astropy_types

    @property
    def tag_mapping(self):
        return [('tag:astropy.org:astropy',
                 ASTROPY_SCHEMA_URI_BASE + 'astropy{tag_suffix}')]

    @property
    def url_mapping(self):
        return ASTROPY_URL_MAPPING


# This extension is used to register custom tag types that have schemas defined
# by ASDF, but have tag implementations defined in astropy.
class AstropyAsdfExtension(BuiltinExtension):
    @property
    def types(self):
        return _astropy_asdf_types
'''


class AsdfFormatExtension(BuiltinExtension):
    @property
    def types(self):
        return _asdf_format_types
