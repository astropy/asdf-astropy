0.2.0 (2022-03-08)
------------------

- Add support for serialization and deserialization of input_units_equivalencies
  for astropy models. [#37]
- Bugfix for units_mapping schema's property name conflicts. Changes:
  - ``inputs`` to ``unit_inputs``
  - ``outputs`` to ``unit_outputs`` [#39]
- Add converter support for Cosine1D, Tangent1D, ArcSine1D, ArcCosine1D, ArcTangent1D
  models. [#42]
- Add converter for Spline1D model. [#43]
- Add astropy Table connector for ASDF. [#47]
- Move assert_model_equal to helpers module. [#50]
- Fix warnings raised during testing. [#52]

0.1.2 (2021-12-14)
------------------

- Fix bug in Table deserializer when meta is absent from the ASDF. [#36]

0.1.1 (2021-12-04)
------------------

- Retrieve coordinates schemas from asdf-coordinates-schemas. [#35]

0.1.0 (2021-12-01)
------------------

- Initial release.
