#!/usr/bin/env python

# $Id$
# ---------------------------------------------------------------------
__version__      = '$Revision$'[11:-3]
__version_date__ = '$Date$'[7:-3]
__author__       = "K.R. Anderson, <k.r.anderson@uva.nl>"
# ---------------------------------------------------------------------

import skimUtils
from os.path import basename
from sys import exit

class AttributeSets(object):

    def __init__(self):
        """LOFAR Sky Image Attributes, ref. LOFAR-USG-ICD-004, v0.9.
	The dictionaries are provided to allow easy adjustments to a skim file group
	header.  Once those headers are filled, the attribute set lists import the
	relevent dictionary content, while preserving the order of the attributes.

	Generally, this class and associated methods will be used in this usual
	manner:

	atts = attributeSets.AttributeSets()
	atts.initHeader('Root', obs=observation, nimages=len(imageList))
	newHeader = atts.attributeSet('Root')

       	Adjustment, additions to any and all group headers is possible through
	access to the various Set List instances provided by the AttributeSets()
	constructor.

	Eg.,
	Set an attribute and value in the Root header:

	atts.rootHeader['NEWKEYWORD'] = newKeyWordValue

	A call to the attributeSet method on the root group after this adjustement will
	then return the header set containing the new and or adjusted header keywords
	values.

	Attributes can also be accessed, set, and or adjusted through the
	methods,

	setAttr(key,val)
	getAttr(key)
	delAttr(key)

	"""

        #----------------------------------------------------------#
	# Class attributes defining permissible values in root header
	# attributes,
	#
	# ANTENNA_SET
	# FILTER_SELECTION
	#
	#----------------------------------------------------------#

	self.antennaSetList      = ["LBA_INNER",
				    "LBA_OUTER",
				    "LBA_SPARSE",
				    "LBA_X",
				    "LBA_Y",
				    "HBA_ONE",
				    "HBA_TWO",
				    "HBA_BOTH"
				    ]

	self.filterSelectionList = ["LBH_10_80",
				    "LBH_30_80",
				    "HB_100_190",
				    "HB_170_230",
				    "HB_210_240"
				    ]

        #----------------------------------------------------------#
	# Initialize all group header dictionaries.
	#----------------------------------------------------------#

	self.rootHeader   = {}
	self.syslogHeader = {}
	self.imageHeader  = {}
	self.dataHeader   = {}
	self.coordHeader  = {}
	self.sourceHeader = {}
	self.processhistHeader = {}

        #----------------------------------------------------------#
	# Initialize group header Set Lists. These lists enforce
	# ordered presentation of group attributes.
        #----------------------------------------------------------#

	self.rootSetList = ["GROUPTYPE",
			    "FILENAME",
			    "FILETYPE",
			    "TELESCOPE",
			    "PROJECT_ID",
			    "PROJECT_TITLE",
			    "OBSERVER",
			    "OBSERVATION_ID",
			    "OBSERVATION_TIMESYS",
			    "OBSERVATION_DATE_START",
			    "OBSERVATION_DATE_END",
			    "ANTENNA_SET",
			    "FILTER_SELECTION",
			    "CLOCK_FREQUENCY",
			    "TARGET",
			    "SYSTEM_VERSION",
			    "PIPELINE_NAME",
			    "NOF_STATIONS",
			    "STATIONS_LIST",
			    "IMGROUPS",
			    "NOF_IMAGES",
			    "ORIGFILE",
			    "NOTES",
			    ]

	self.syslogSetList = ["GROUPTYPE"]

	self.imageSetList  = ["GROUPTYPE",
			      "COORDINATESGROUP",
			      "DATAGROUP",
			      "SOURCEGROUP",
			      "PROCESSHISTGROUP",
			      ]

	self.coordSetList = ["GROUPTYPE",
			     "EQUINOX",
			     "SYSTEM_RADEC",
			     "REF_LOCATION_VALUE",
			     "REF_LOCATION_UNIT",
			     "REF_LOCATION_FRAME",
			     "NOF_COORDINATES",
			     "NOF_AXES",
			     "COORDINATE_TYPES",
			     ]

	self.dataSetList = ["GROUTYPE",
			    "DATASET",
			    "DATASETNAME",
			    "WCSINFO",
			    ]

	self.sourceSetList = ["GROUPTYPE",
			      "DATASET",
			      "NSOURCES",
			      ]

	self.processhistSetList = ["GROUPTYPE"]


    def initHeader(self, groupType, obs=None, nimages=None):
	"""Populate a particular attribute set for a passed groupType

	where,

	obs:           the observation name,
	nimages:       number of subband images in obs.
	groupType:     the LOFAR defined group whose attributes are to be populated.

	In a LOFAR Sky Image, this string value will be one of,

	'Root'
	'Syslog'
	'Image'
	'skyData'
	'Source'
	'ProcessHist'
	'Coordinates'

	See LOFAR-USG-ICD-004, Table 2: LOFAR Group Type Listing, for further details.
	"""

        if groupType == 'Root':
	    try:
		origFile = basename(obs)
	    except:
		raise IOError, 'A call for Root must supply two (2) keyword arguments.'
	    fileName = skimUtils.mkSimpleFileName(obs)
	    obsId    = origFile.split('_')[1]
	    self.rootHeader["GROUPTYPE"]           = 'Root'
	    self.rootHeader["FILENAME"]            = fileName
	    self.rootHeader["FILETYPE"]            = 'sky'
	    self.rootHeader["TELESCOPE"]           = 'LOFAR'
	    self.rootHeader["PROJECT_ID"]          = 'Sky Image Dev'
	    self.rootHeader["PROJECT_TITLE"]       = 'HDF5 Skim Test'
	    self.rootHeader["OBSERVER"]            = 'The Krell'
	    self.rootHeader["OBSERVATION_ID"]      = obsId
	    self.rootHeader["OBSERVATION_TIMESYS"] = 'UTC'
	    self.rootHeader["IMGROUPS"]            = 'true'
	    self.rootHeader["NOF_IMAGES"]          = nimages
	    self.rootHeader["ORIGFILE"]            = origFile

	elif groupType == 'Syslog':
	    self.syslogHeader["GROUPTYPE"] = 'Syslog'

	elif groupType == 'Image':
	    self.imageHeader["GROUPTYPE"]        = 'Image'
	    self.imageHeader["COORDINATESGROUP"] = 'Coordinates'
	    self.imageHeader["DATAGROUP"]        = 'skyData'
	    self.imageHeader["SOURCEGROUP"]      = 'Source'
	    self.imageHeader["PROCESSHISTGROUP"] = 'ProcessHist'

	elif groupType == 'Coordinates':
	    self.coordHeader["GROUPTYPE"]          = 'Coordinates'
	    self.coordHeader["EQUINOX"]            = 'J2000'
	    self.coordHeader["SYSTEM_RADEC"]       = 'FK5'
	    self.coordHeader["REF_LOCATION_VALUE"] = None
	    self.coordHeader["REF_LOCATION_UNIT"]  = ''
	    self.coordHeader["REF_LOCATION_FRAME"] = ''
	    self.coordHeader["NOF_COORDINATES"]    = None
	    self.coordHeader["NOF_AXES"]           = 4
	    self.coordHeader["COORDINATE_TYPES"]   = None

	elif groupType == 'skyData':
	    self.dataHeader["GROUTYPE"]    = 'skyData'
	    self.dataHeader["DATASET"]     = 'true'
	    self.dataHeader["DATASETNAME"] = ''
	    self.dataHeader["WCSINFO"]     = '../Coordinates'

	elif groupType == 'Source':
	    self.sourceHeader["GROUPTYPE"] = 'Source'
	    self.sourceHeader["DATASET"]   = 'Source List'
	    self.sourceHeader["NSOURCES"]  = ''

	elif groupType == 'ProcessHist':
	    self.processhistHeader["GROUPTYPE"] = 'ProcessHist'

	else:
	    msg="\n!Fatal Error: Passed groupType, "+groupType+", undefined.\n\n" + \
		 "Permissable values of groupType:\n" + \
		 "Root, Syslog, Image, Coordinates, skyData, Source, ProcessHist\n" + \
		 "See Document LOFAR-USG-ICD-004 for details.\n"
	    exit(msg)

	return

    def attributeSet(self, group):
	"""Returns an ordered list of header key-values tuples for a passed group
	type (group).  First call the initHeader() method, which provides an attribute
	template with a pre-defined skeleton set of attributes for the passed group.

	Furthermore, once all group attributes have been set, this method converts the
	unordered header (dictionary) of attributes into a strictly ordered list of
	attributes for a given group type.  That order is specified in the LOFAR Common
	Attributes section of the LOFAR Sky Image interface control document,
	LOFAR-USG-ICD-004.
	"""

	attributeSetList = []

	if group == "Root":
	    headKeys = self.rootHeader.keys()
	    for key in self.rootSetList:
		if key in headKeys:
		    attributeSetList.append((key, self.rootHeader[key]))
		else:
		    attributeSetList.append((key,''))

	elif group == 'Syslog':
	    headKeys = self.syslogHeader.keys()
	    for key in self.syslogSetList:
		if key in headKeys:
		    attributeSetList.append((key, self.syslogHeader[key]))
		else:
		    attributeSetList.append((key,''))

	elif group == 'Image':
	    headKeys = self.imageHeader.keys()
	    for key in self.imageSetList:
		if key in headKeys:
		    attributeSetList.append((key, self.imageHeader[key]))
		else:
		    attributeSetList.append((key,''))

	elif group == 'Coordinates':
	    headKeys = self.coordHeader.keys()
	    for key in self.coordSetList:
		if key in headKeys:
		    attributeSetList.append((key, self.coordHeader[key]))
		else:
		    attributeSetList.append((key,''))

	elif group == 'skyData':
	    headKeys = self.dataHeader.keys()
	    for key in self.dataSetList:
		if key in headKeys:
		    attributeSetList.append((key, self.dataHeader[key]))
		else:
		    attributeSetList.append((key,''))

	elif group == 'Source':
	    headKeys = self.sourceHeader.keys()
	    for key in self.sourceSetList:
		if key in headKeys:
		    attributeSetList.append((key, self.sourceHeader[key]))
		else:
		    attributeSetList.append((key,''))

	elif group == 'ProcessHist':
	    headKeys = self.processhistHeader.keys()
	    for key in self.processhistSetList:
		if key in headKeys:
		    attributeSetList.append((key, self.processhistHeader[key]))
		else:
		    attributeSetList.append((key,''))

	else:
	    msg="Fatal Error: Passed Grouptype "+group+" undefined.\n\n"
	    exit(msg)

	return attributeSetList

