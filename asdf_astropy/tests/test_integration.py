import io
import sys
import warnings
from pathlib import Path

import asdf
import pytest
import yaml


def test_resources():
    resources_root = Path(__file__).parent.parent / "resources"
    resource_manager = asdf.get_config().resource_manager

    for resource_path in resources_root.glob("**/*.yaml"):
        with resource_path.open("rb") as f:
            resource_content = f.read()
        resource = yaml.safe_load(resource_content)
        resource_uri = resource["id"]
        assert resource_manager[resource_uri] == resource_content


def test_manifests():
    manifests_root = Path(__file__).parent.parent / "resources" / "manifests"
    resource_manager = asdf.get_config().resource_manager

    for manifest_path in manifests_root.glob("*.yaml"):
        with manifest_path.open("rb") as f:
            manifest_content = f.read()
        manifest = yaml.safe_load(manifest_content)

        manifest_schema = asdf.schema.load_schema("asdf://asdf-format.org/core/schemas/extension_manifest-1.0.0")

        # The manifest must be valid against its own schema:
        asdf.schema.validate(manifest, schema=manifest_schema)

        for tag_definition in manifest["tags"]:
            # The tag's schema must be available:
            assert tag_definition["schema_uri"] in resource_manager


def test_extensions():
    package_and_uri_pairs = {(e.package_name, e.extension_uri) for e in asdf.get_config().extensions}

    assert ("asdf-astropy", "asdf://astropy.org/astropy/extensions/astropy-1.0.0") in package_and_uri_pairs
    assert ("asdf-astropy", "asdf://asdf-format.org/transform/extensions/transform-1.0.0") in package_and_uri_pairs
    assert ("asdf-astropy", "asdf://asdf-format.org/transform/extensions/transform-1.1.0") in package_and_uri_pairs
    assert ("asdf-astropy", "asdf://asdf-format.org/transform/extensions/transform-1.2.0") in package_and_uri_pairs
    assert ("asdf-astropy", "asdf://asdf-format.org/transform/extensions/transform-1.3.0") in package_and_uri_pairs
    assert ("asdf-astropy", "asdf://asdf-format.org/transform/extensions/transform-1.4.0") in package_and_uri_pairs
    assert ("asdf-astropy", "asdf://asdf-format.org/transform/extensions/transform-1.5.0") in package_and_uri_pairs


_ASTROPY_MODULES = [
    "astropy.coordinates",
    "astropy.io",
    "astropy.modeling",
    "astropy.table",
    "astropy.time",
    "astropy.units",
]


@pytest.fixture
def _clean_astropy_imports():
    """Temporally unload all astropy modules used by asdf-astropy"""

    # If any astropy or asdf_astropy modules are already imported
    # remove them from sys.modules so we can later in this test check
    # if those modules were imported. We have to store these as
    # many submodules will reference or use types defined in other
    # submodules
    previous_modules = {}
    for name in sys.modules.copy():
        if name.startswith("asdf_astropy") or any(name.startswith(m) for m in _ASTROPY_MODULES):
            previous_modules[name] = sys.modules[name]
            del sys.modules[name]

    # Register a module finder that just raises an exception if
    # one of the tracked astropy modules is imported
    class _Finder:
        def find_spec(self, modulename, path=None, target=None):
            if any(modulename.startswith(m) for m in _ASTROPY_MODULES):
                msg = f"attempt to import astropy submodule({modulename}) during integration"
                raise Exception(msg)  # noqa: TRY002

    sys.meta_path.insert(0, _Finder())

    # Setup complete return the test
    yield

    # Restore the previously imported modules. This is necessary as other code
    # may have already used the modules we removed from the cache (astropy.constants
    # defines some quantities).
    for name, previous_module in previous_modules.items():
        sys.modules[name] = previous_module
    if isinstance(sys.meta_path[0], _Finder):
        sys.meta_path.pop(0)


@pytest.mark.usefixtures("_clean_astropy_imports")
def test_no_astropy_import():
    """
    Confirm that none of the ASDF plugins import astropy modules
    at import time.
    """

    from asdf_astropy import integration

    integration.get_resource_mappings()
    integration.get_extensions()

    assert not any(k for k in sys.modules if any(k.startswith(m) for m in _ASTROPY_MODULES))


def test_no_core_extension_overwrite():
    """
    Check that this package (even though it implements converters for core types)
    does not overwrite the core extension provided by asdf
    """
    import astropy.units as u

    # define a tree with a unit that will be serialized by this package
    # the tree itself will be serialized by asdf (which should result in
    # including asdf as a used extension)
    tree = {"meter": u.m}

    bio = io.BytesIO()
    asdf.AsdfFile(tree).write_to(bio)
    bio.seek(0)

    with asdf.open(bio) as af:
        packages = [ext["software"]["name"] for ext in af.tree["history"]["extensions"]]
        # check that both asdf and asdf-astropy are recorded as being used to
        # generate the file
        assert "asdf" in packages
        assert "asdf-astropy" in packages


def test_no_warnings_for_astropy_manifest_files():
    """
    asdf-astropy 0.5.0 wrote files with astropy.org manifests
    that were compounds of core and astropy types. These types are
    now handled by different extensions. This test checks that files
    generated with the no longer used astropy.org manifests open without
    warnings.
    """
    file_contents = io.BytesIO(
        b"""#ASDF 1.0.0
#ASDF_STANDARD 1.5.0
%YAML 1.1
%TAG ! tag:stsci.edu:asdf/
--- !core/asdf-1.1.0
asdf_library: !core/software-1.0.0 {author: The ASDF Developers, homepage: 'http://github.com/asdf-format/asdf',
  name: asdf, version: 3.3.0}
history:
  extensions:
  - !core/extension_metadata-1.0.0
    extension_class: asdf.extension._manifest.ManifestExtension
    extension_uri: asdf://asdf-format.org/core/extensions/core-1.5.0
    manifest_software: !core/software-1.0.0 {name: asdf_standard, version: 1.1.1}
    software: !core/software-1.0.0 {name: asdf, version: 3.3.0}
  - !core/extension_metadata-1.0.0
    extension_class: asdf_astropy._manifest.CompoundManifestExtension
    extension_uri: asdf://astropy.org/core/extensions/core-1.5.0
    software: !core/software-1.0.0 {name: asdf-astropy, version: 0.5.0}
u: !unit/unit-1.0.0 m
...""",
    )
    with warnings.catch_warnings():
        # make sure warnings are errors
        warnings.simplefilter("error")
        with asdf.open(file_contents) as af:
            assert af["u"]  # we don't care about the contents here
