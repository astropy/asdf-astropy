from pathlib import Path
import sys

import yaml
import asdf


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
    manifests_root = (
        Path(__file__).parent.parent / "resources" / "manifests"
    )
    resource_manager = asdf.get_config().resource_manager

    for manifest_path in manifests_root.glob("*.yaml"):
        with manifest_path.open("rb") as f:
            manifest_content = f.read()
        manifest = yaml.safe_load(manifest_content)

        manifest_schema = asdf.schema.load_schema(
            "asdf://asdf-format.org/core/schemas/extension_manifest-1.0.0"
        )

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


def test_no_astropy_import():
    """
    Confirm that none of the ASDF plugins import astropy.modeling
    at import time.
    """
    keys = [k for k in sys.modules.keys() if k.startswith("astropy.modeling") or k.startswith("asdf_astropy")]
    for key in keys:
        del sys.modules[key]

    from asdf_astropy import integration
    integration.get_resource_mappings()
    integration.get_extensions()

    assert not any(k for k in sys.modules.keys() if k.startswith("astropy.modeling"))
