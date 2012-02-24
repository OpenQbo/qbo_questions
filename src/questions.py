#!/usr/bin/env python
#
#Copyright (C) 2012 Openqbo Inc.
#
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.


import roslib; roslib.load_manifest('qbo_questions')
import rospy
from qbo_listen.msg import Listened
from qbo_talk.srv import Text2Speach
from qbo_system_info.srv import AskInfo

from qbo_face_tracking.msg import FacePosAndSize

global client_speak
global face_detected

def speak_this(text):
    global client_speak
    client_speak(str(text))

def listen_callback(data):
    global face_detected  
  
    sentence = data.msg
    rospy.loginfo("Listened: |"+sentence+"|")
   
    if not face_detected:
       rospy.loginfo("Ignoring last sentece because face was not detected")
       return
 
    if sentence=="HOW ARE YOU" or sentence == "I'M FINE AND YOU":
        speak_this("I'M FINE THANK YOU");
    elif sentence=="WHAT IS YOUR NAME" or sentence == "HELLO WHAT IS YOU NAME":
        speak_this("MY NAME IS QBO");
    elif sentence=="WHAT ARE YOU":
        speak_this("I AM QBO, A LOW COST ROBOTIC PLATFORM FOR ARTIFICIAL INTELLIGENT DEVELOPMENTS")

    elif sentence == "I'M GO TO PRESS A FRIEND OF MINE":
	speak_this("O K. Nice")

    elif sentence == "THANK YOU Q B O":
	speak_this("YOU WELl COME.")

    elif sentence == "GOOD BYE Q B O":
	speak_this("BYE BYE. NICE TO MEET YOU")

    elif sentence=="WHAT TIME IS IT":
        rospy.wait_for_service("/pluginsystem");
        service_pluginsystem = rospy.ServiceProxy('/pluginsystem', AskInfo)
        info = service_pluginsystem("hour")
        rospy.loginfo(info.info)
        speak_this(info.info)
    elif sentence=="WHAT DAY IS IT TODAY":
        rospy.wait_for_service("/pluginsystem");
        service_pluginsystem = rospy.ServiceProxy('/pluginsystem', AskInfo)
        info = service_pluginsystem("hdate")
        rospy.loginfo(info.info)
        speak_this(info.info)


def face_callback(data):
    global face_detected
    face_detected = data.face_detected	

def main():
    global client_speak
    global face_detected
    face_detected = False

    rospy.init_node('questions')
    rospy.loginfo("Starting questions node")
    client_speak = rospy.ServiceProxy("/Qbo/festivalSay", Text2Speach)
    subscribe=rospy.Subscriber("/listen/en_default", Listened, listen_callback)

    rospy.Subscriber("/qbo_face_tracking/face_pos_and_dist", FacePosAndSize, face_callback)


    
    rospy.spin()


if __name__ == '__main__':
    main()

