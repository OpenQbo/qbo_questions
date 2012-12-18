#!/usr/bin/env python
#
#Copyright (C) 2012 Thecorpora Inc.
#
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

import rospy
import json
from qbo_internet_services.srv import InternetService

def location(sentence,language):
    rospy.wait_for_service("/internetservices");
    service_iservices = rospy.ServiceProxy('/internetservices', InternetService)
    info = service_iservices("location","")
    decodedData=json.loads(info.info)
    if type(decodedData) is dict:
        city=decodedData['city']
        country=decodedData['country']
    else:
        print "Not valid JSON recived"
    response="We are in "+city+", in "+country
    rospy.loginfo(response)
    return response

