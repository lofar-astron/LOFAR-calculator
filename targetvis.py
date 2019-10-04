from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
from astropy import units as u

def resolve_source(name):
   """For a given source name, use astroquery to find its coordinates"""
   try:
      query = Simbad.query_object(name)
      ra = query['RA'][0]
      dec= query['DEC'][0]
      coord = SkyCoord('{} {}'.format(ra, dec), unit=(u.hourangle, u.deg))
   except:
      return None
   return coord.to_string('hmsdms')
