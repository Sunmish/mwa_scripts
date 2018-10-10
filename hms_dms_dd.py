#! /usr/bin/env python

from astropy.coordinates import SkyCoord
from astropy import units as u

import sys

def convert_to_dd(coords, frame="icrs", equinox="J2000.0"):
    """Perform some checks then, if needed, convert to decimal degrees."""

    ra, dec = coords

    if isinstance(ra, str):
        # hh:mm:ss? hh mm ss? hhHmmMssS?
        if any(delim in ra for delim in [":", " ", "h"]):
            ra_unit = u.hourangle
        elif any(delim in ra for delim in ["m", "s"]):
            raise ValueError("RA input is ambiguous.")
        else:
            ra_unit = u.deg
    else:
        ra_unit = u.deg

    c = SkyCoord(ra, dec, unit=(ra_unit, u.deg), frame=frame, equinox=equinox)

    return c.ra.value, c.dec.value  # degrees


def main():

    r_hms = sys.argv[1]
    d_dms = sys.argv[2]

    ra, dec = convert_to_dd((r_hms, d_dms))

    print ra
    print dec


if __name__ == "__main__":
    main()
