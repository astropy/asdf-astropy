# Packages may add whatever they like to this file, but
# should keep this content at the top.
# ----------------------------------------------------------------------------
from ._astropy_init import *  # noqa: F403

# ----------------------------------------------------------------------------

def configure_core_table_support(asdf_config):
    from .extensions import CORE_TABLE_EXTENSIONS

    for extension in CORE_TABLE_EXTENSIONS:
        asdf_config.add_extension(extension)
