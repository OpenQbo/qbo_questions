import roslib; roslib.load_manifest('qbo_questions')
import rospy

from qbo_system_info.srv import AskInfo

def hour():
    rospy.wait_for_service("/pluginsystem");
    service_pluginsystem = rospy.ServiceProxy('/pluginsystem', AskInfo)
    info = service_pluginsystem("hour")
    rospy.loginfo(info.info)
    return info.info

def date():
    rospy.wait_for_service("/pluginsystem");
    service_pluginsystem = rospy.ServiceProxy('/pluginsystem', AskInfo)
    info = service_pluginsystem("hdate")
    rospy.loginfo(info.info)
    return info.info
