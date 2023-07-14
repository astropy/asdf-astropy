from asdf.extension import Converter
from asdf.tags.core.ndarray import NDArrayType


def _card_to_node(card):
    from astropy.io.fits import Undefined

    value = "" if isinstance(card.value, Undefined) else card.value

    if card.comment:
        return [card.keyword, value, card.comment]

    if value:
        return [card.keyword, value]

    if card.keyword:
        return [card.keyword]

    return []


class FitsConverter(Converter):
    def to_yaml_tree(self, obj, tag, ctx):
        from astropy.table import Table

        node = []
        for hdu in obj:
            header_node = [_card_to_node(c) for c in hdu.header.cards]
            hdu_node = {"header": header_node}

            if hdu.data is not None:
                if hdu.data.dtype.names is not None:
                    hdu_node["data"] = Table(hdu.data)
                else:
                    hdu_node["data"] = hdu.data

            node.append(hdu_node)

        return node

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.io import fits

        hdus = []
        first = True
        for hdu_node in node:
            header = fits.Header([fits.Card(*x) for x in hdu_node["header"]])

            data = hdu_node.get("data")
            if isinstance(data, NDArrayType):
                # TODO: Why doesn't NDArrayType work?  This needs some research
                # and documentation.
                data = data._make_array()

            if first:
                hdu = fits.PrimaryHDU(data=data, header=header)
                first = False
            elif data.dtype.names is not None:
                hdu = fits.BinTableHDU(data=data, header=header)
            else:
                hdu = fits.ImageHDU(data=data, header=header)

            hdus.append(hdu)

        return fits.HDUList(hdus)


class AsdfFitsConverter(FitsConverter):
    tags = ("tag:stsci.edu:asdf/fits/fits-*",)
    types = ()


class AstropyFitsConverter(FitsConverter):
    tags = ("tag:astropy.org:astropy/fits/fits-*",)
    types = ("astropy.io.fits.hdu.hdulist.HDUList",)
