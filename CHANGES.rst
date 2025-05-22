0.8.0 (unreleased)
------------------

- drop support for python 3.10 and numpy 1.24. [#255]
- remove soon to be deprecated and non-working use of astropy TestRunner. [#263]
- Add support for masked quantities, angles, and coordinates for astropy >= 7.1. [#253]
- Add support for asdf-transform-schemas 0.6 and asdf-coordinates-schemas 0.4. [#279]

0.7.1 (2025-02-12)
------------------

- register blank ASDF extensions to prevent warnings for
  ASDF files generated with asdf-astropy 0.5.0. [#258]

0.7.0 (2024-11-13)
------------------

- strip None factor for spectral_density in equivalency converter
  to avoid deprecation warnings for astropy 7. [#229]

- drop support for python 3.9. [#232]

- replace usages of ``copy_arrays`` with ``memmap`` [#230]

- require asdf 2.14.4 [#241]

- Add support for astropy.nddata.uncertainty classes [#239]

- Add support for astropy.wcs.WCS and astropy.wcs.wcsapi.SlicedLowLevelWCS [#246]

0.6.1 (2024-04-05)
------------------

- update ``copy`` usage in ``Quantity`` converter to
  deal with astropy 6.1 changes. [#224]

0.6.0 (2024-03-13)
------------------

- Add python 3.12 support. [#219]
- Update ASDF standard 1.6.0 support. [#219]
- Increase minimum versions for ``asdf-coordinates-schemas``
  ``asdf-transform-schemas`` and list ``asdf-standard`` as
  a dependency. [#219]

0.5.0 (2023-11-15)
------------------

- Drop support for Python 3.8 in accordance with NEP 29. [#180]
- Update ``RepresentationConverter`` for new class paths in astropy [#181]
- Update Converters so that all Class Variables are immutable [#188]
- Remove ``oldest-supported-numpy`` from ``pyproject.toml`` ``build-system``
  as this was never needed and will cause problems building on python 3.12 betas. [#193]
- Use unique uri for extensions that implement converters for core asdf types [#199]
- Add support for astropy.table.NdarrayMixin [#200]
- Update angle converters for new class paths in astropy [#207]

0.4.0 (2023-03-20)
------------------

- Update pins for ``asdf``, ``asdf-coordinates-schemas``, ``numpy``, and ``packaging``. [#164]
- Add serialization support for non-VOunits. [#142]
- Add serialization support for ``MagUnit`` based units. [#146]
- Document and add ``assert_model_roundtrip`` and ``assert_table_roundtrip`` to
  ``asdf_astropy.testing.helpers``. [#170]

0.3.0 (2022-11-29)
------------------

- Update citations. [#111]
- Switch to using ``pyproject.toml`` for package configuration. [#106]
- Fix bug with ``memmap`` of ``Quantity`` objects. [#125]
- Drop support for ``numpy-1.18``. [#116]
- Fix bug with ``str`` representations of ``astropy.time`` objects. [#132]
- Fix bug in preserving the ``dtype`` of ``Quantity`` objects. [#131]

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
