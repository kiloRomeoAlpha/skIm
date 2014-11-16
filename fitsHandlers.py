# $Id$
# ---------------------------------------------------------------------
__version__      = '$Revision$'[11:-3]
__version_date__ = '$Date$'[7:-3]
__author__       = "K.R. Anderson, <k.r.anderson@uva.nl>"
# ---------------------------------------------------------------------

import pyfits

def slingData(fName):
    """Ufunc gets a subband tuple from nameStruct data structure,
    which is of the form,
    ('SB000', 'Image000', 'Sub-band 000', 'Data', 'Coordinates',
    'Source', 'ProcessHist', 'SB0.fits'),
    and opens the fits image, slings back the ndarray, closes things up."""

    fob  = pyfits.open(fName)
    dataChunk = fob[0].data[0,0,:,:] #2D slice of the 1,1,2048,2048 array
    fob.close()
    del fob
    return dataChunk, dataChunk.shape

def slingHeader(fName):
    """Ufunc gets a subband tuple from the nameStruct data structure,
    which is of the form,
    ('SB000', 'Image000', 'Sub-band 000', 'Data', 'Coordinates',
    'Source', 'ProcessHist', 'SB0.fits'),
    opens the fits image, slings back the header, closes things up.
    """
    fob  = pyfits.open(fName)
    fHeader = fob[0].header.ascardlist()
    fob.close()
    del fob
    return fHeader

