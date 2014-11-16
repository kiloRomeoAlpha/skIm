#!/usr/bin/env python

# $Id$
# ---------------------------------------------------------------------
__version__      = '$Revision$'[11:-3]
__version_date__ = '$Date$'[7:-3]
__author__       = "K.R. Anderson, <k.r.anderson@uva.nl>"
# ---------------------------------------------------------------------

import sys, glob
import os
from   os.path import basename, isdir, join
import getopt

def usage(mod):

    useBurp = '\n\tUsage: '+ mod + ' [options] obs\n\n\twhere "obs" is the name'\
	      ' of an observation output directory\n' + \
       '\tunder which the following structure is assumed:\n\n' + \
       '\tOBS/\n'+ \
       '\tOBS/logs/\n'+ \
       '\tOBS/parsets/\n'+ \
       '\tOBS/results/\n'+\
       '\tOBS/vds/\n\n'+ \
       '\twhere pipeline produced images exist under the "results/" directory.\n\n'+\
       '\t[options] allow only one keyword argument:\n\n' + \
       '\t--run=yyyy-mm-ddThh:mm:ss\n\n' + \
       '\twhere yyyy-mm-ddThh:mm:ss is an ISO 8601 standard time field format\n'+ \
       '\tand where that time represents a "results" subdirectory name, which is the\n'+ \
       '\tpipeline start time. A new directory output structure requires one\n'+ \
       '\t(1) and only one "--run=" keyword argument.  \n\n'+ \
       '\tImaging results see further dispensation under "results" via subdirectories\n'+ \
       '\tholding the images and demarcated by a pipeline runtime,'+ \
       '\n\n\teg., under\n\n' + \
       '\tL2009_13591_8/results/\n\n' + \
       '\twill be found subdirectories like,\n\n'+\
       '\t2009-10-13T13:43:09/\n' + \
       '\t2009-10-13T13:44:00/\n' + \
       '\t2009-10-13T13:44:49/\n' + \
       '\t2009-10-13T13:46:55/\n' + \
       '\t2009-10-13T15:26:51/\n\n' + \
       '\tExample: skim images for a particular pipeline run of L2009_13591_8\n\n'+ \
       '\t% skim --run=2009-10-13T13:44:49 /pipeline_runtime/jobs/L2009_13591_8\n\n'

    return useBurp


def handleCLargs(args):
    mod = basename(sys.argv[0])
    long_options = ['help',
		    'run='
		    ]
    try:
	opts, arg = getopt.getopt(sys.argv[1:],'',long_options)
    except getopt.GetoptError:
	sys.exit(usage(mod))

    if not arg:
	sys.exit(usage(mod))

    # Only ONE observation (argument) can be specified
    if len(arg) != 1:
       	sys.exit(usage(mod))

    observation = arg[0]
    cl_switches = []
    # cl_switches is left as a hook for handling possible future options,
    # options that do not exist at the moment. -kra, 21.10.2009.

    if opts:
	for o, a in opts:
	    if a:
		cl_switches.append(o+"="+a)
	    else:
		cl_switches.append(o)

	    if o in ("--help",):
		sys.exit(usage(mod))

	    if o in ("--run",):
		runTimeLabel = a
		imPath = join(observation,"results",runTimeLabel)
		if not isdir(imPath):
		    msg="\n\n\tError: Path to directory "+runTimeLabel+" not found.\n"
		    sys.exit(msg)
	    else:
		sys.exit(usage(mod))

    return observation, runTimeLabel


def mkSimpleFileName(obsName):
    obsId = obsName.split('_')[1]
    outFileName = 'L'+obsId+"_sky.h5"
    return outFileName


def mkOutFileName(obsName, pipeLabel):
    """Returns a LOFAR Sky Image filename for the passed observation name.
    obsName will be like L2009_NNNNN, where NNNNN will be the observation id,
    as specified in the input MS data.  Eventually, this function will extract
    the obsid from the ovservation image, rather than relying on the output
    Measurement Set name.

    -- See USG Document, LOFAR-USG-ICD-005, Naming Conventions, for further
    details.
    """
    obsBaseName = basename(obsName)
    obsId = obsBaseName.split('_')[1]
    outFileName = 'L'+obsId+"_sky.h5"
    fullOutFilePathName = join(obsName,"results",pipeLabel,outFileName)
    return fullOutFilePathName


def makePipeResultsPath(obsDir, pipeLabel):
    return join(obsDir,"results",pipeLabel)


def mkFitsImageList(pipeResults):
    """Method will return a 2-tuple, where element 0 will be the name of the
    averaged image found, if any, and a list of the observation's subband fits
    images.

    eg, return (aveImage, fitslist),

    where aveImage is either a filename string, or None.
    """
    fitsList = []
    aveIm = ''
    curdir=os.getcwd()
    os.chdir(pipeResults)
    imList = glob.glob("*.fits")
    aveIm, subbandImList = handleAveIm(imList)
    for im in subbandImList:
	fitsList.append(im)
    os.chdir(curdir)
    return (aveIm,fitsList)


def handleAveIm(imList):
    """If extant, pop an Averaged Image from the list of subband images.
    Returns a 2-tuple: average image filename, new list of only subband images.
    The returned tuple will look like,

    (aveIm, image_list),

    where,

    aveIm will be either a null string ('') or the 'filename' of a found average
    image.  'image_list' will be a nominal python list datatype.
    """
    aveIm = ''
    for i in range(len(imList)):
	if "ave" in imList[i]:
	    aveIm = imList.pop(i)
	    break
	else: pass
    return (aveIm, imList)


def finish(skyFile, logger):
    """Finish off the file."""
    print "Processing complete."
    print
    print "LOFAR Sky Image file form:"
    print
    print skyFile
    logger.debug("Processing complete.")
    logger.debug("LOFAR Sky Image file form:")
    logger.info(str(skyFile))
    skyFile.close()
    del skyFile
    return


