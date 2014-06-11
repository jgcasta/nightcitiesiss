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
'''
    Modified to get informtation about ISS pictures metadada
'''

import json
import asciitable


def get_iss_photos():
    """
    Gets public metadata from ISS picture missions
    :arg string size: Size of the image from ISS mission
    :returns: A list of metadata photos.
    :rtype: list
    
    """
    photos = []

    lista=asciitable.read('demo.csv') 

    for i in lista:

        CoordFLAG = i['CoordFLAG']
    
        # only for CoordFLAG selected

        if str(CoordFLAG) == '5.0':
            tmpMission=i['ISS-ID'].split('-E-')
            mission = tmpMission[0]
            idIss = tmpMission[1]
 
            city = i['City']
            
            pattern_s = "http://eol.jsc.nasa.gov/sseop/images/ESC/%s/%s/%s-E-%s.JPG" % (
                "small",
                mission,
                mission,
                idIss)
            pattern_b = "http://eol.jsc.nasa.gov/sseop/images/ESC/%s/%s/%s-E-%s.JPG" % (
                'large',
                mission,
                mission,
                idIss)

            linkData = "http://eol.jsc.nasa.gov/scripts/sseop/photo.pl?mission=%s&roll=E&frame=%s" % (
                mission,
                idIss)
            idISS = idIss

            citylon = str(i['loncity'])
            

            citylat = str(i['latcity'])
            
            f = '50'
            
            tmp = dict(link_small=pattern_s,
                       link_big=pattern_b,
                       linkData=linkData,
                       idISS=idISS,
                       citylon=citylon,
                       citylat=citylat,
                       focal=f
                       )
            photos.append(tmp)
    return photos

get_iss_photos()
