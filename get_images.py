# -*- coding: utf-8 -*-

# This file is part of PyBOSSA.
#
# PyBOSSA is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBOSSA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PyBOSSA.  If not, see <http://www.gnu.org/licenses/>.

import json
import asciitable


def get_iss_photos():
    """
    Gets public photos from ISS missions
    :arg string size: Size of the image from ISS mission
    :returns: A list of photos.
    :rtype: list
    """
    photos = []
    lista=asciitable.read('datosISS.csv') # comprobar formato del fichero

    for i in lista:
        mission=i['ISS-ID'].split('-E-')[0]
        pattern_s = "http://eol.jsc.nasa.gov/sseop/images/ESC/%s/%s/%s-E-%s.JPG" % (
            "small",
            mission,
            mission,
            i['ISS-ID'])
        pattern_b = "http://eol.jsc.nasa.gov/sseop/images/ESC/%s/%s/%s-E-%s.JPG" % (
            'large',
            mission,
            mission,
            i['ISS-ID'])
        link = "http://eol.jsc.nasa.gov/scripts/sseop/photo.pl?mission=%s&roll=E&frame=%s" % (
            mission,
            i['ISS-ID'])
        idISS = i['ISS-ID']

        nadirLon = str(i.citylon2)
            
            

        nadirLat = str(i.citylat2)
            
        focal = '50'
        
        tmp = dict(link_small=pattern_s,
                   link_big=pattern_b,
                   link=link,
                   idISS=idISS,
                   nadirLon=nadirLon,
                   nadirLat=nadirLat,
                   focal=focal
                   )
        photos.append(tmp)
    return photos

print get_iss_photos()
