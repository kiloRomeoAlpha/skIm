# $Id$
# ---------------------------------------------------------------------
__version__      = '$Revision$'[11:-3]
__version_date__ = '$Date$'[7:-3]
__author__       = "K.R. Anderson, <k.r.anderson@uva.nl>"
# ---------------------------------------------------------------------

from pyrap.tables import table

def slingData(fName):
    """Ufunc gets a full path file name, opens the casa image,
    slings back the ndarray, closes things up.
    """
    fob  = table(fName)
    dataChunk = fob.getcol('map')
    fob.close()
    del fob
    return dataChunk, dataChunk.shape

def slingHeader(fName):
    """Ufunc gets a full path file name, opens the casa image,
    slings back the 'map' column header, closes things up.
    """
    fob  = table(fName)
    casaKeys = fob.getkeywords()
    fob.close()
    del fob

    # some imagined function "translate" will convert the hideous
    # casa image keyword structure into a standard, flat key-val
    # dictionary or tuple.

    fHeader = translate(casaKeys)
    return fHeader
