"""
Script that creates initial astropy manifest from the schemas
in the resources directory.  This file can be removed once
the format of the manifest files has been finalized.
"""
import argparse
from pathlib import Path

import yaml


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("schemas_path")
    parser.add_argument("output_path")
    return parser.parse_args()


class MultilineString(str):
    pass


def represent_multiline_string(dumper, data):
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")


if __name__ == "__main__":
    yaml.add_representer(MultilineString, represent_multiline_string)

    args = parse_args()

    manifest = {}

    manifest["id"] = "http://astropy.org/asdf/extensions/astropy/manifests/astropy-1.0"
    manifest["extension_uri"] = "http://astropy.org/asdf/extensions/astropy-1.0"
    manifest["title"] = "Astropy extension 1.0"
    manifest["description"] = MultilineString(
        "A set of tags for serializing astropy objects.  This does not include most\n"
        "model classes, which are handled by an implementation of the ASDF\n"
        "transform extension.",
    )
    manifest["asdf_standard_requirement"] = {
        "gte": "1.1.0",
    }
    manifest["tags"] = []

    for schema_path in Path(args.schemas_path).glob("**/*.yaml"):
        schema = yaml.safe_load(schema_path.read_bytes())
        tag_def = {
            "tag_uri": schema["id"].replace("http://astropy.org/schemas/astropy/", "tag:astropy.org:astropy/"),
            "schema_uri": schema["id"],
            "title": schema["title"].strip(),
        }

        if "tag" in schema:
            assert tag_def["tag_uri"] == schema["tag"]

        if "description" in schema:
            tag_def["description"] = MultilineString(schema["description"].strip())

        manifest["tags"].append(tag_def)

    with Path(args.output_path).open("w") as f:
        yaml.dump(manifest, f, sort_keys=False)
