#!/usr/bin/env python

# $Id$
# ---------------------------------------------------------------------
__version__      = '$Revision$'[11:-3]
__version_date__ = '$Date$'[7:-3]
__author__       = "K.R. Anderson, <k.r.anderson@uva.nl>"
# ---------------------------------------------------------------------

import sys
import skimUtils

from   os.path import join
import tables
import fitsHandlers
import groupNames
import attributeSets
import logging

#------------------------------ Initialize ----------------------------------#

def run(obs,runTimeLabel,logger):
    """Run it all."""
    lofarFileName       = skimUtils.mkOutFileName(obs,runTimeLabel)
    resultsPath         = skimUtils.makePipeResultsPath(obs,runTimeLabel)
    aveImage, imageList = skimUtils.mkFitsImageList(resultsPath)
    nameObj             = groupNames.GroupNames(imageList)
    nameStruct          = nameObj.makeGroupNames()

    # nameStruct is a structured tuple, wherein each tuple element has
    # the name of the sub-band, and the group names for all subgroups for
    # the particular sub-band image.
    #
    # eg., a record from this data structure:
    #
    # ('SB061','Image061','Sub-band061','skyData','Coordinates','Linear-coord',
    #  'Source', 'ProcessHist')

    #------------------------------ Root Group --------------------------------#
    logger.info("Building LOFAR Sky Image file ...")
    skyFile = tables.openFile(lofarFileName, mode="w", title="LOFAR Sky Image")
    root    = skyFile.root

    # Populate Root attributes.

    attributes = attributeSets.AttributeSets()
    attributes.initHeader('Root', obs=obs, nimages=len(imageList))
    rootHeader = attributes.attributeSet('Root')

    for key, val in rootHeader:
	root.key = val

    #------------------------------ Syslog Group ------------------------------#
    # All Sky Images will have a SysLog group at root level.
    # See LOFAR-USG-ICD-004, et al for specification.

    syslog = skyFile.createGroup(root, "SysLog", title = "Root System Log")
    attributes.initHeader('Syslog')
    syslogHeader = attributes.attributeSet('Syslog')

    for key, value in syslogHeader:
	syslog.key = value

    #---------------------------- Average Image Group -------------------------#
    # If average image found in the output.
    if aveImage != '':
	logger.debug("Got average image, " + str(aveImage) + "handling ...")
	aName     = join(resultsPath,aveImage)
	aveImroot =  skyFile.createGroup(root,"AverageImages",title = "Image Sums")
	atom      = tables.Float32Atom()
	dataChunk, dataShape = fitsHandlers.slingData(aName)
	filters   = tables.Filters()
	cArr = skyFile.createCArray(aveImroot,
				    "averageImage",
				    atom,
				    dataShape,
				    filters=filters,
				    title="Incoherent Sum Image"
				    )
	cArr[:,:] = dataChunk
    else: pass

    #------------------------------ Image Groups ------------------------------#
    # First build level is the image group sub-group.
    for sBand in nameStruct:
	imGroup = sBand[1]
	logger.debug("Got file " + str(sBand[-1]))
        logger.debug("Glomming " + str(imGroup) + " onto Root group...")
	imroot = skyFile.createGroup(root, imGroup, title = sBand[2])
	attributes.initHeader('Image')
	imHeader = attributes.attributeSet('Image')
	for key, value in imHeader:
	    imroot.key = value
	logger.debug("success!")
	logger.debug("glomming data to image group..." + str(imGroup))
	# append associated sub-groups to this new Image Group
	for newGroup in sBand[3:7]:
	    #---------------------------- Data Group ------------------------#
	    if "Data" in newGroup:
		logger.debug("Datagroup found...")
		logger.debug("Image group is " + str(imGroup)+ ";" + \
			     " Data group is " + str(newGroup))
		datasetHook = skyFile.createGroup(imroot, newGroup, title=newGroup)
		datasetName = "ImageDataArray_"+sBand[0]
		attributes.initHeader('skyData')
		attributes.dataHeader["DATASETNAME"] = datasetName
		dataHeader = attributes.attributeSet('skyData')
		for key, value in dataHeader:
		    datasetHook.key = value
	    #---------------------- Dataset Arrays ------------------------#
	        fName = join(resultsPath, sBand[-1])
		atom  = tables.Float32Atom()
		dataChunk, dataShape = fitsHandlers.slingData(fName)
		filters   = tables.Filters()
		logger.debug("populating dataset arrays ...")
		cArr = skyFile.createCArray(datasetHook,
					    datasetName,
					    atom,
					    dataShape,
					    filters=filters,
					    title=newGroup)
		cArr[:,:] = dataChunk
		continue
	    #----------------------- Coord Group ------------------------#
            # Coord groups require one of <'linear','direction','tabular','

            if "Coord" in newGroup:
		logger.debug("Coorindate group found. ...")
		logger.debug("glomming Coordinates groups...")
		logger.debug("groups glommed: " + str(imroot) + str(newGroup))
		coordroot = skyFile.createGroup(imroot, newGroup, title = newGroup)
		attributes.initHeader('Coordinates')
		coordsHeader = attributes.attributeSet('Coordinates')

		for key, value in coordsHeader:
		    coordroot.key = value
		logger.debug("made coordroot group")
                # this is the sub band identifier: +sBand[0][2:]
                skyFile.createGroup(coordroot,"LinearCoord", \
				    title = "Linear Coordinates, Subband "+sBand[0][2:])
		continue
	#---------------------- Source Group ------------------------#
	    if "Source" in newGroup:
		logger.debug("Source group found. Building...")
		sourceHook = skyFile.createGroup(imroot, newGroup, title = newGroup)
		attributes.initHeader('Source')
		sourceHeader = attributes.attributeSet('Source')
		for key, value in sourceHeader:
		    sourceHook.key = value
		continue
	#---------------------- ProcHist Group ----------------------#
	    if "ProcessHist" in newGroup:
		logger.debug("Process History group found.  Building ...")
		prochistHook =  skyFile.createGroup(imroot, newGroup, title = newGroup)
		attributes.initHeader('ProcessHist')
		prochistHeader = attributes.attributeSet('ProcessHist')
		for key, value in prochistHeader:
		    prochistHook.key = value
		continue
    skimUtils.finish(skyFile,logger)


if __name__ == '__main__':
    # Initalise a default logger
    logging.basicConfig(format="%(message)s")
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    #--------------------------------------------------------------------------#
    #                           Handle Cl Options
    ##-------------------------------------------------------------------------#

    obs, runTimeLabel = skimUtils.handleCLargs(sys.argv)

    #--------------------------------------------------------------------------#
    #                         End Handle Cl Options
    ##-------------------------------------------------------------------------#

    # start run() function
    run(obs, runTimeLabel, logger)
    skimUtils.finish(skyFile, logger)
    sys.exit("Done")


