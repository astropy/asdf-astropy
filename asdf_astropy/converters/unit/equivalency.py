from asdf.extension import Converter


class EquivalencyConverter(Converter):
    tags = ["tag:astropy.org:astropy/units/equivalency-*"]

    types = ["astropy.units.equivalencies.Equivalency"]

    def to_yaml_tree(self, obj, tag, ctx):
        results = []

        for name, kwargs in zip(obj.name, obj.kwargs):
            kwargs_names = []
            kwargs_values = []
            for kwargs_name, kwargs_value in kwargs.items():
                kwargs_names.append(kwargs_name)
                kwargs_values.append(kwargs_value)

            results.append({
                "name": name,
                "kwargs_names": kwargs_names,
                "kwargs_values": kwargs_values,
            })

        return results

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.units import equivalencies

        components = []
        for equivalency_node in node:
            equivalency_method = getattr(equivalencies, equivalency_node["name"])
            kwargs = dict(zip(equivalency_node["kwargs_names"], equivalency_node["kwargs_values"]))
            components.append(equivalency_method(**kwargs))

        return sum(components[1:], components[0])
