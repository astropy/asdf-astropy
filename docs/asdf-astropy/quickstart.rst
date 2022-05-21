.. _quickstart:

***********
Quick-Start
***********

**asdf-astropy** is intended to be an extension library for **ASDF** to enable support
for the **astropy** package.  It is intended to be used in conjunction with both the
**ASDF** and **astropy** packages. To this end, the **asdf-astropy** package typically
only needs to be installed in order to provide its functionality.

A quick example of **ASDF**
===========================

The **ASDF** format is a way of saving nested structures to **yaml**, where some of
the stored data can be stored in a binary format. Thus, one typically structures
an **ASDF** file as a dictionary, with key/value pairs.

For example if one wanted to store a `~astropy.modeling.functional_models.Gaussian1D` model in
an **ASDF** file::

    from asdf import AsdfFile
    from astropy.modeling.models import Gaussian1D

    # Create a Gaussian1D model
    model = Gaussian1D(amplitude=10.4, mean=3.2, stddev=0.1)

    # Create a tree structure for the ASDF file, and write it.
    tree = {'gaussian_model': model}
    ff = AsdfFile(tree)
    ff.write_to("hello_world.asdf")

    # One can also create the file first, and then modify it directly.
    ff = AsdfFile()
    ff.tree['gaussian_model'] = model
    ff.write_to("hello_world.asdf")

To open the existing file one can use the top-level `asdf.open` method directly
or as a context manager::

    import asdf

    ff = asdf.open("hello_world.asdf")

    # As a context manager
    with asdf.open("hello_world.asdf") as ff:
        ...

In either case the file ``ff`` will be an `asdf.AsdfFile` object which is accessible just
like a Python dictionary. **ASDF** will fully realize all of the objects stored within
the file automatically. For example, to access the model stored in the file ``ff['gaussian_model']``
will be a `~astropy.modeling.functional_models.Gaussian1D` object exactly matching the model written
originally.

One can also update an existing file. For example, if one wanted to update the ``hello_world.asdf``
file with a `~astropy.coordinates.SkyCoord` object::

    import asdf
    from astropy import units as u
    from astropy.coordinates import SkyCoord

    # Create a SkyCoord object
    coord = SkyCoord(ra=10.625*u.degree, dec=41.2*u.degree, frame='icrs')

    with asdf.open("hello_world.asdf", mode='rw') as af:
        af.tree['skycoord'] = coord
        af.update()

In the same way that the `~astropy.modeling.functional_models.Gaussian1D` model round-tripped, the
`~astropy.coordinates.SkyCoord` object will also round-trip.

Further Reading
===============

For further getting started material on **ASDF** see, :ref:`asdf:overview`. If one
wants to find more examples of how to write an **astropy** `~astropy.table.Table`
to **ASDF** files, see :ref:`table`.
