#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseActionResult

goalarray = []
failcount = 0


def goalcallback(goal):
	global goalarray, failcount
	goalarray.append(goal)
	if(len(goalarray) == 1):
		goalPub.publish(goalarray[0])

def resultcallback(result):
	global goalarray, failcount
	if(result.status.status == 3):
		goalarray.pop(0)
		failcount = 0
	elif(result.status.status == 4):
		failcount=failcount+1
		if(failcount == 2):
			goalarray.pop(0)
			failcount = 0
	if(len(goalarray) >= 1):
		goalPub.publish(goalarray[0])


if __name__ == '__main__':
	rospy.Subscriber("/move_base_simple/multiple_goals", PoseStamped, goalcallback)
	rospy.Subscriber("/move_base/result", MoveBaseActionResult, resultcallback)
	goalPub = rospy.Publisher('/move_base_simple/goal',PoseStamped, queue_size=1)
	rospy.init_node('multiple_goals', anonymous=True)
	rospy.spin()
