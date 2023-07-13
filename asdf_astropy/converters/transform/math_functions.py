from .core import TransformConverterBase

_MODEL_NAMES = [
    "AbsoluteUfunc",
    "AddUfunc",
    "ArccosUfunc",
    "ArccoshUfunc",
    "ArcsinUfunc",
    "ArcsinhUfunc",
    "Arctan2Ufunc",
    "ArctanUfunc",
    "ArctanhUfunc",
    "CbrtUfunc",
    "CosUfunc",
    "CoshUfunc",
    "Deg2radUfunc",
    # DivideUfunc is an alias for True_divideUfunc
    "DivmodUfunc",
    "Exp2Ufunc",
    "ExpUfunc",
    "Expm1Ufunc",
    "FabsUfunc",
    "Floor_divideUfunc",
    "FmodUfunc",
    "HypotUfunc",
    "Log10Ufunc",
    "Log1pUfunc",
    "Log2Ufunc",
    "LogUfunc",
    "Logaddexp2Ufunc",
    "LogaddexpUfunc",
    # ModUfunc is an alias for RemainderUfunc
    "MultiplyUfunc",
    "NegativeUfunc",
    "PositiveUfunc",
    "PowerUfunc",
    "Rad2degUfunc",
    "ReciprocalUfunc",
    "RemainderUfunc",
    "RintUfunc",
    "SinUfunc",
    "SinhUfunc",
    "SqrtUfunc",
    "SquareUfunc",
    "SubtractUfunc",
    "TanUfunc",
    "TanhUfunc",
    "True_divideUfunc",
]


class MathFunctionsConverter(TransformConverterBase):
    """
    ASDF support for serializing the math functions models,
    each of which corresponds to a numpy ufunc.
    """

    tags = ("tag:stsci.edu:asdf/transform/math_functions-*",)
    types = tuple("astropy.modeling.math_functions." + m for m in _MODEL_NAMES)

    def to_yaml_tree_transform(self, model, tag, ctx):
        return {"func_name": model.func.__name__}

    def from_yaml_tree_transform(self, node, tag, ctx):
        from astropy.modeling import math_functions

        klass_name = math_functions._make_class_name(node["func_name"])
        klass = getattr(math_functions, klass_name)
        return klass()
