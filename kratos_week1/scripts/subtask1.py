#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

class BotState:
    def __init__(self):
        self.velocity = Twist()
        self.bot_velocities = [self.velocity.linear.x, self.velocity.angular.z]
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.rate = rospy.Rate(1)

    def Move(self):
        self.velocity.linear.x = self.dir / 10
        self.velocity.angular.z = 0
        self.state = "Move"
        self.bot_velocities = [self.velocity.linear.x, self.velocity.angular.z]
    
    def Rotate(self):
        self.velocity.linear.x = 0
        self.velocity.angular.z = self.dir / 10
        self.state = "Rotate"
        self.bot_velocities = [self.velocity.linear.x, self.velocity.angular.z]
    
    def Stop(self):
        self.velocity.linear.x = 0
        self.velocity.angular.z = 0
        self.state = "Stop"
        self.bot_velocities = [self.velocity.linear.x, self.velocity.angular.z]

    def publish(self):
        self.count = 0
        while not rospy.is_shutdown():
            if self.count <= 10:
                self.count += 1
                self.dir = 1
                self.Move()
                self.pub.publish(self.velocity)
                self.rate.sleep()
            elif self.count > 10 and self.count <= 20:
                self.count += 1
                self.dir = -1
                self.Rotate()
                self.pub.publish(self.velocity)
                self.rate.sleep()
            
            elif self.count > 20 and self.count <= 30:
                self.count += 1
                self.dir = 0
                self.Stop()
                self.pub.publish(self.velocity)
                self.rate.sleep()
                if self.count == 30:
                    self.count = 0

if __name__ == '__main__':
    rospy.init_node('turtlebot3_velocities')
    turtlebot = BotState()
    turtlebot.publish()
    
