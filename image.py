import pywcs
import pyfits

from hyperion.model import ModelOutput
from hyperion.util.constants import pc

m = ModelOutput('input_lessdense.rtout')
wav, nufnu = m.get_image(group=1, inclination=0, distance=300 * pc)

# Initialize WCS information
wcs = pywcs.WCS(naxis=2)

# Use the center of the image as projection center
wcs.wcs.crpix = [nufnu.shape[2] / 2. + 0.5,
                 nufnu.shape[1] / 2. + 0.5]

# Set the coordinates of the image center
wcs.wcs.crval = [233.4452, 1.2233]

# Set the pixel scale (in deg/pix)
wcs.wcs.cdelt = [1./3600., 1./3600.]

# Set the coordinate system
wcs.wcs.ctype = ['GLON-CAR', 'GLAT-CAR']

# And produce a FITS header
header = wcs.to_header()

# Write out to a file including the new header
pyfits.writeto('image_slice_wcs.fits', nufnu[:, :, 0], header,
               clobber=True)