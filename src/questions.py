#!/usr/bin/env python
#
#Copyright (C) 2012 Thecorpora Inc.
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

from qbo_face_msgs.msg import FacePosAndDist

import random


global client_speak
global face_detected

global voice_SP 
global voice_EN
global lang

def speak_this(text):
    global client_speak
    client_speak(str(text))

def listen_callback(data):
    global face_detected  
    global dialogue
    sentence = data.msg
    rospy.loginfo("Listened: |"+sentence+"|")
   
    if not face_detected:
       rospy.loginfo("Ignoring last sentece because face was not detected")
       return


    if sentence in dialogue:
        output = dialogue[sentence]
        speak_this(random.choice(output))


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
    elif sentence=="DO YOU SPEAK SPANISH":
        rospy.wait_for_service("/qbo_talk/festival_language");
        service_change_voice_language = rospy.ServiceProxy('/qbo_talk/festival_language', Text2Speach)
        service_change_voice_language("JuntaDeAndalucia_es_sf_diphone")
        speak_this("un poquito. Estoy aprendiendo")
        service_change_voice_language("cmu_us_awb_arctic_clunits")


def face_callback(data):
    global face_detected
    face_detected = data.face_detected	

def main():
    global client_speak
    global face_detected
    global voice_EN
    global voice_SP
    global lang

    voice_SP = "JuntaDeAndalucia_es_sf_diphone"
    voice_EN = "cmu_us_awb_arctic_clunits"
    lang = rospy.get_param("/qbo_questions/language", "en")


    face_detected = False

    # We load the dialgues from the config folder
    global dialogue
    dialogue = {}

    path = roslib.packages.get_pkg_dir("qbo_questions")
    f = open(path+'/config/dialogues_'+lang)    
    for line in f.readlines():
        try:
            line = line.replace("\n","")
            parts = line.split(">>>")

            dialogue_input = parts[0].upper()
            dialogue_output = parts[1].upper()

        
            # we check wheter the input line alreayd exists, if so, we add to its own list
            if dialogue_input in dialogue:                
                dialogue[dialogue_input].append(dialogue_output)
            else:
                #dialogue_input does not exist
                dialogue[dialogue_input] = [dialogue_output]
        except Exception:
            pass        

    f.close()    

    print "Dialog => "+str(dialogue)

    rospy.init_node('questions')
    rospy.loginfo("Starting questions node")

 
    changeLang = rospy.ServiceProxy("/qbo_talk/festival_language", Text2Speach)
    client_speak = rospy.ServiceProxy("/qbo_talk/festival_say", Text2Speach)


    #Set Julius & Festival language
    if lang=="es":
        #Julius
        subscribe=rospy.Subscriber("/listen/es_questions", Listened, listen_callback)
        
        #Festival
        changeLang(voice_SP)
    else:
        #Julius
        subscribe=rospy.Subscriber("/listen/en_questions", Listened, listen_callback)

        #Festival
        changeLang(voice_EN)

    rospy.Subscriber("/qbo_face_tracking/face_pos_and_dist", FacePosAndDist, face_callback)



    
    rospy.spin()




def roskill_handler():
    #Reached this point we are about to quit this node, but we need to restart the voice, just in case
    #it was changed, so:
    global lang
    print "::Finishing Qbo_questions::"
    if lang != "en":
        rospy.init_node('questions')
        #We set the deafult voice to english
        changeLang = rospy.ServiceProxy("/qbo_talk/festival_language", Text2Speach)
        changeLang(voice_EN)






rospy.on_shutdown(roskill_handler)

if __name__ == '__main__':
    main()

