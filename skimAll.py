#!/usr/bin/env python

# $Id$
# ---------------------------------------------------------------------
__version__      = '$Revision$'[11:-3]
__version_date__ = '$Date$'[7:-3]
__author__       = "K.R. Anderson, <k.r.anderson@uva.nl>"
# ---------------------------------------------------------------------

import logging
import skim_functionals
import skimUtils

def buildSkim(obs,runTimeLabel):
    """Build the whole file, pass an observation name and a runTimeLabel
    indicating a directory under an observation's results directory.
    """
    # skimValues is a tuple like
    # (lofarFileName, resultsPath, aveImage, imageList, nameStruct)

    skimValues    = skim_functionals.initialize(obs,runTimeLabel)
    lofarFileName = skimValues[0]
    resultsPath   = skimValues[1]
    aveImage      = skimValues[2]
    imageList     = skimValues[3]
    nameStruct    = skimValues[4]
    attributes    = skimValues[5]

    skimFileOb0 = skim_functionals.buildRoot(obs,lofarFileName,len(imageList))
    skimFileOb1 = skim_functionals.buidSysLog(skimFileOb0)
    #del skimFileOb0
    skimFileOb2 = skim_functionals.buidAveIm(skimFileOb1, aveImage)
    #del skimFileOb1
    skimFileOb3 = skim_functionals.buildImageGrps(skimFileOb2, nameStruct)
    finish(skimFileOb3)
    return

if __name__ == '__main__':
    # Initalise a default logger
    logging.basicConfig(format="%(message)s")
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    #--------------------------------------------------------------------------#
    #                             Handle Cl Options
    ##-------------------------------------------------------------------------#

    obs, runTimeLabel = skimUtils.handleCLargs(sys.argv)

    #--------------------------------------------------------------------------#
    #                             End Handle Cl Options
    ##-------------------------------------------------------------------------#

    # start run() function
    buildSkim(obs,runTimeLabel)
    sys.exit("Done")
