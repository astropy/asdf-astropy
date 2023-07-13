from asdf.extension import Converter


class TimeDeltaConverter(Converter):
    @property
    def tags(self):
        return ["tag:astropy.org:astropy/time/timedelta-*"]

    @property
    def types(self):
        return ["astropy.time.core.TimeDelta"]

    def to_yaml_tree(self, obj, tag, ctx):
        return obj.info._represent_as_dict()

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.time.core import TimeDelta

        return TimeDelta.info._construct_from_dict(node)
