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
    return parse_version(tag[tag.rfind("-") + 1 :])


def get_tag_name(tag):
    """
    Extract the name portion of a tag URI.

    Parameters
    ----------
    tag : str

    Returns
    -------
    str
    """
    return tag[tag.rfind("/") + 1 : tag.rfind("-")]
