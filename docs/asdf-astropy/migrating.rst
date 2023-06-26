.. _migrating:

Migrating from **astropy.io.misc.asdf** to **asdf-astropy**
===========================================================

For the majority of users, migrating from **astropy.io.misc.asdf** to **asdf-astropy**
requires no code changes at all. Instead, all users need to do is include **asdf-astropy**
as an additional dependency to their package.

This is because when the **asdf-astropy** package is installed, it will automatically be used
by **ASDF** when serializing and deserializing **astropy** objects. This occurs seamlessly because
the interface used by **asdf-astropy** to extend **ASDF** is given preference over the one used by
**astropy.io.misc.asdf** (which is currently deprecated).

.. note::

    When **ASDF** version 3.0 is released, the interface used by **astropy.io.misc.asdf** will
    be removed. This means that using **ASDF** with **astropy** will stop functioning unless
    **asdf-astropy** is installed.

The only users of **astropy.io.misc.asdf** that need to do any code migration aside from adding
an **asdf-astropy** dependency are those who directly use the objects (based on **asdf.types.CustomType**)
defined in **astropy.io.misc.asdf** to create their own **ASDF** `~asdf.extension._converter.Converter`
extensions. Clear instructions on how to create the new converter extensions for **ASDF** can be found
in :ref:`asdf:extending_converters`.
