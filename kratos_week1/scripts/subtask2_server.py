#!/usr/bin/env python3

import sys
import rospy
from geometry_msgs.msg import Twist
from kratos_week1.srv import States, StatesResponse

class BotState:
    def __init__(self):
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.bot_state = 0
        self.dir = 0
        self.velocity = Twist()
        self.rate = rospy.Rate(1)

    def Move(self, dir):
        self.velocity.linear.x = dir / 10
        self.velocity.angular.z = 0

    def Rotate(self, dir):
        self.velocity.linear.x = 0
        self.velocity.angular.z = dir / 10

    def Stop(self, dir):
        self.velocity.linear.x = 0
        self.velocity.angular.z = 0
    
    def publisher(self):
        while not rospy.is_shutdown():
            self.pub.publish(self.velocity)
            self.rate.sleep()

    def server(self, request):
        self.request = request
        self.dir = request.dir
        self.bot_state = request.state
        rospy.loginfo('States called')
        if self.request.state == "Move":
            self.Move(self.dir)
            return StatesResponse(True)
        elif self.request.state == "Rotate":
            self.Rotate(self.dir)
            return StatesResponse(True)
        elif self.request.state == "Stop":
            self.Stop(self.dir)
            return StatesResponse(True)
        else:
            return StatesResponse(False)


def main():
    rospy.init_node('turtlebot_state_server')
    turtlebot = BotState()
    serv = rospy.Service('bot_state', States, turtlebot.server)
    print("Server is ready.")
    turtlebot.publisher()
    rospy.spin()

if __name__ == '__main__':
    main()