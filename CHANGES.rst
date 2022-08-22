0.2.2 (2022-08-22)
------------------

- Add converter for the new ``Schechter1D`` model. [#67]
- Add CITATION file. [#71]
- Add migration and quick-start documentation guides, and update minimum Python version [#77]
- Update ``FrameConverter`` to enable the use of multiple tags. [#81]
- Bugfixes for ``astropy.time`` converters. [#86]
- Remove unnecessary ``tag:`` from schemas. [#103]
- Add converters for ``ModelBoundingBox`` and ``CompoundBoundingBox``. [#69]

0.2.1 (2022-04-18)
------------------

- Migrate documentation from ``astropy`` to ``asdf-astropy``. [#55]
- Pin astropy min version to 5.0.4. [#62]

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
