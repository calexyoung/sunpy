from __future__ import absolute_import

"""
SunPy Map objects are constructed using the special :function:`Map()`
function. ::

>>> map = sunpy.Map('file.fits')

The result of a call to `Map` will be either a generic 
:class:`sunpy.map.BaseMap` object, or a subclass of :class:`sunpy.map.BaseMap` 
which deals with a specific type of data, e.g. :class:`AIAMap` or 
:class:`LASCOMap`.
"""
#pylint: disable=W0401

__all__ = ["sources", "mapcube"]
__author__ = "Keith Hughitt"
__email__ = "keith.hughitt@nasa.gov"

import sys
import pyfits
from sunpy.map.sources import *
from sunpy.map.basemap import BaseMap
from sunpy.map.basemap import UnrecognizedDataSouceError

#pylint: disable=C0103,E1101
def Map(input_):
    """Map class factory
    
    Attempts to determine the type of data associated with input and returns
    an instance of either the generic BaseMap class or a subclass of BaseMap
    such as AIAMap, EUVIMap, etc.
    
    Parameters
    ----------
    input_ : filepath, data array
        The data source used to create the map object. This can be either a
        filepath to an image, a 2d list, or an ndarray.
        
    Returns
    -------
    out : BaseMap
        Returns a BaseMap or BaseMap subclass instance
        
    Notes
    -----
    PyFITS
        [1] Due to the way PyFITS works with images the header dictionary may
        differ depending on whether is accessed before or after the fits[0].data
        is requested. If the header is read before the data then the original
        header will be returned. If the header is read after the data has been
        accessed then the data will have been scaled and a modified header
        reflecting these changes will be returned: BITPIX may differ and
        BSCALE and B_ZERO may be dropped in the modified version.
        
        [2] The verify('fix') call attempts to handle violations of the FITS
        standard. For example, nan values will be converted to "nan" strings.
        Attempting to cast a pyfits header to a dictionary while it contains
        invalid header tags will result in an error so verifying it early on
        makes the header easier to work with later.
    References
    ----------
    | http://stackoverflow.com/questions/456672/class-factory-in-python
    | http://stsdas.stsci.edu/download/wikidocs/The_PyFITS_Handbook.pdf
    """
    if isinstance(input_, basestring):
        fits = pyfits.open(input_)
        fits.verify('silentfix')        
        data = fits[0].data
        header = fits[0].header

        for cls in BaseMap.__subclasses__():
            if cls.is_datasource_for(header):
                return cls(data, header)
        raise UnrecognizedDataSouceError

    else:
        return BaseMap(input_)
