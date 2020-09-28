from packaging.version import parse as parse_version


def parse_tag_version(tag):
    """
    Parse the version portion of the tag into a comparable
    version object.

    Parameters
    ----------
    tag : str

    Returns
    -------
    packaging.version.Version
    """
    return parse_version(tag[tag.rfind("-") + 1:])
