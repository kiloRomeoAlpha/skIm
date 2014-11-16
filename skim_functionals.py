#!/usr/bin/env python

# $Id$
# ---------------------------------------------------------------------
__version__      = '$Revision$'[11:-3]
__version_date__ = '$Date$'[7:-3]
__author__       = "K.R. Anderson, <k.r.anderson@uva.nl>"
# ---------------------------------------------------------------------

from   os.path import join
import tables
import fitsHandlers
import groupNames
import attributeSets
import skimUtils

def initialize(obs, runTimeLabel):
    """Initial setup for building a skim file.  nameStruct below is a structured
    tuple, wherein each tuple element has the name of the sub-band, and the
    group names for all subgroups for the particular sub-band image.

    eg., a record from a nameStruct data structure:

    ('SB061','Image061','Sub-band061','skyData',
    'Coordinates','Linear-coord','Source', 'ProcessHist')
    """

    lofarFileName       = skimUtils.mkOutFileName(obs,runTimeLabel)
    resultsPath         = skimUtils.makePipeResultsPath(obs,runTimeLabel)
    aveImage, imageList = skimUtils.mkFitsImageList(resultsPath)
    nameObj             = groupNames.GroupNames(imageList)
    nameStruct          = nameObj.makeGroupNames()
    attrs               = attributeSets.AttributeSets()
    return (lofarFileName, resultsPath, aveImage, imageList, nameStruct, attrs)


def buildRoot(obs, lofarFileName, nimages, attrs):
    skyFile     = tables.openFile(lofarFileName, mode="w", title="LOFAR Sky Image")
    root        = skyFile.root
    attributues = attrs
    attributes.initHeader('Root',obs=obs, nimages=nimages)
    rootHeader = attributes.attributeSet('Root')
    for key, val in rootHeader:
	root.key = val
    return skyFile


def buildSysLog(skyFile, attrs):
    """ All Sky Images will have a SysLog group at root level.
    See LOFAR-USG-ICD-004, et al for specification.
    """
    root = skyFile.root
    attributes = attrs
    syslog = skyFile.createGroup(root, "SysLog", title = "Root System Log")
    attributes.initHeader('Syslog')
    syslogHeader = attributes.attributeSet('Syslog')
    for key, value in syslogHeader:
	syslog.key = value
    return skyFile


def buildAveIm(skyFile, aveImage):
    """Find an average image in output results, if there.
    """
    root = skyFile.root
    if aveImage != '':
	print "Got average image,",aveImage,"handling ...\n"
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
    return skyFile


def buildImageGrps(skyFile, nameStruct):
    print "Root built. \nAttaching image groups now..."
    root = skyFile.root
    for sBand in nameStruct:
	imGroup = sBand[1]
	print "Got file "+ sBand[-1]+ ".\nGlomming ",imGroup," onto ",root,"... \n\n"
	imroot = skyFile.createGroup(root, imGroup, title = sBand[2])
	attributes.initHeader('Image')
	imHeader = attributes.attributeSet('Image')
	for key, value in imHeader:
	    imroot.key = value
	print "success!"
	print "glomming data to image group...", imGroup

	# append associated sub-groups to this new Image Group

	for newGroup in sBand[3:7]:
	    # Data groups require a dataset space
	    if "Data" in newGroup:
		print "Datagroup found..."
		print "Image group is",imGroup+";"," Data group is",newGroup,"\n\n"
		buildDataGrp(skyFile,imroot,sBand)
		continue
	    elif "Coord" in newGroup:
		print "Coorindate group found. ...\n"
		print "glomming Coordinates groups...\n"
		print "Groups glommed:",imroot, newGroup
		buildCoordGrp(skyFile,imroot,sBand)
		continue
	    #---------------------- Source Group ------------------------#
	    elif "Source" in newGroup:
		print "Source group found.  building ...\n"
		buildSourceGrp(skyFile,imroot,sBand)
		continue
	    #---------------------- ProcHist Group ----------------------#
	    elif "ProcessHist" in newGroup:
		print "Process History group found. building ...\n"
		buildProcGrp(skyFile,imroot, sBand, resultsPath)
    return skyFile


def buildDataGrp(skyFile, imroot, sBand, resultsPath):
    """ Build a full data group, with a populated dataset array."""
    newGroup    = sBand[3:7]
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
	print "populating dataset arrays ..."
	cArr = skyFile.createCArray(datasetHook,
				    datasetName,
				    atom,
				    dataShape,
				    filters=filters,
				    title=newGroup)
	cArr[:,:] = dataChunk
    return skyFile

def buildCoordGrp(skyFile, imroot, sBand):
    newGroup = sBand[3:7]
    coordroot = skyFile.createGroup(imroot, newGroup, title = newGroup)
    attributes.initHeader('Coordinates')
    coordsHeader = attributes.attributeSet('Coordinates')
    for key, value in coordsHeader:
	coordroot.key = value
	# this is the sub band identifier: +sBand[0][2:]
	skyFile.createGroup(coordroot,"LinearCoord", \
			    title = "Linear Coordinates, Subband "+sBand[0][2:])
	continue
    return


def buildSourceGrp(skyFile, imroot, sBand):
    sourceHook = skyFile.createGroup(imroot, newGroup, title = newGroup)
    attributes.initHeader('Source')
    sourceHeader = attributes.attributeSet('Source')
    for key, value in sourceHeader:
	sourceHook.key = value
    return

def buildProcHist(skyFile, imroot, sBand):
    prochistHook =  skyFile.createGroup(imroot, newGroup, title = newGroup)
    attributes.initHeader('ProcessHist')
    prochistHeader = attributes.attributeSet('ProcessHist')
    for key, value in prochistHeader:
	prochistHook.key = value
    return

