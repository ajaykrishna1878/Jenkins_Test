#!/usr/bin/env python3

import sys
import rospy
from geometry_msgs.msg import Twist
from kratos_week1.srv import States

rospy.init_node('turtlebot_state_client')

def get_state(state, dir):
    rospy.wait_for_service('bot_state')
    the_client = rospy.ServiceProxy('bot_state', States)
    user_data = the_client(state, dir)
    return user_data.success

if __name__ == '__main__':
    if len(sys.argv) == 3:
        state = str(sys.argv[1])
        dir = int(sys.argv[2])
    else:
        print("%s [state dir]"%sys.argv[0])
        sys.exit()
    print(state, dir, get_state(state, dir))
