#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseActionResult
from random import randint


goalarray = []
failcount = 0
randcount = 0
faillock = 1


def goalcallback(goal):
	global goalarray, failcount
	goalarray.append(goal)
	if(len(goalarray) == 1):
		goalPub.publish(goalarray[0])

def resultcallback(result):
	global goalarray, failcount, randcount, faillock
	if(result.status.status == 3):
		failcount = 0
		faillock = 0
	elif(result.status.status == 4):
		failcount=failcount+1
		goalPub.publish(goalarray[randcount])
		if(failcount == 2):
			failcount = 0
			faillock = 0
	if(len(goalarray) >= 1 and faillock == 0):
		randcount = randint(0,len(goalarray)-1)
		goalPub.publish(goalarray[randcount])
		faillock = 1


if __name__ == '__main__':
	rospy.Subscriber("/move_base_simple/multiple_goals", PoseStamped, goalcallback)
	rospy.Subscriber("/move_base/result", MoveBaseActionResult, resultcallback)
	goalPub = rospy.Publisher('/move_base_simple/goal',PoseStamped, queue_size=1)
	rospy.init_node('random_patrolling_goals', anonymous=True)
	rospy.spin()
