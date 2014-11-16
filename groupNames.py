# $Id$
# ---------------------------------------------------------------------
__version__      = '$Revision$'[11:-3]
__version_date__ = '$Date$'[7:-3]
__author__       = "K.R. Anderson, <k.r.anderson@uva.nl>"
# ---------------------------------------------------------------------


class GroupNames(object)
    """Container and method(s) to build the full set of group names
    for all groups in a skim file."""

    def __init__(self, imageList, coordType="Linear-coord"):
        self.nims      = len(imageList)
        self.coordType = coordType
        self.imageList = imageList

    def makeGroupNames(self):
        """Make the group names for all image group groups for each
        sub-band image The final entry per record is the present fits
        file name, which will not have the inserted zeros of our
        spec'd subband indices.  We must open the file as it is
        originally named.
        """

        self.imGroupNames = []
	sortedSubBands    = self.subBandList()
        for band in sortedSubBands:
	    if band == '000':
		self.imGroupNames.append( ("SB"+band,
					   "Image"+band,
					   "Sub-band "+band,
					   "skyData",
					   "Coordinates",
					   "Source",
					   "ProcessHist",
					   "SB0.fits")
					  )
            else: self.imGroupNames.append( ("SB"+band,
				      "Image"+band,
				      "Sub-band "+band,
				      "skyData",
				      "Coordinates",
				      "Source",
				      "ProcessHist",
				       "SB" +band.lstrip('0') +".fits")
				      )
        return self.imGroupNames

    def subBandList(self):
	"""Returns a sorted list of 'filled' subband names ('SB000','SB001',...).
	I.e. fits image files appear as 'SB0.fits,' SB09.fits,' 'SB243.fits'
	This method will do a fill on those file names so that 'SB0.fits'
	becomes 'SB000.fits,' which allows for easy iteration and sorting.
	"""
	newSubBandIds = []
	for im in self.imageList:
	    unitID       = []
	    filledUnitID = []
	    subBandId = ''
	    fileId = im.split('.')[0]
	    try: unitID.append(int(fileId[-3]))
	    except ValueError: pass
	    try: unitID.append(int(fileId[-2]))
	    except ValueError: pass
	    try: unitID.append(int(fileId[-1]))
	    except ValueError:
		msg = "Error: Parse on filename, "+im+". No parseable subband ID found.\n\n"
		raise ValueError(msg)
	    # unitID is now a list like [1,7,2], or even [2].  Concatenate!
	    for n in unitID:
		subBandId = subBandId + str(n)
	    newSubBandIds.append(subBandId.rjust(3,"0"))
	newSubBandIds.sort()
	return newSubBandIds
