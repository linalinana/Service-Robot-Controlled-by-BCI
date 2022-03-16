#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
import socket
import rospy
from geometry_msgs.msg import Twist
import time
from math import pi
from std_msgs.msg import String
from std_msgs.msg import Int64
from topic_demo.msg import gps

IP_ADDR = "190.168.1.116"
PORT = 56346
class MoveGrab():
    def __init__(self):
        rospy.init_node('obj_and_move',anonymous=False)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.init_server()
        rospy.loginfo("client connect successfully.......")
        #rospy.on_shutdown(self.shutdown)
        self.rec_motion = []
        self.cmd_vel = rospy.Publisher('/cmd_vel_mux/input/teleop',Twist,queue_size=5) 
        self.pubgrab = rospy.Publisher('object_label', String, queue_size=1)
        self.rate = 20
        self.r = rospy.Rate(self.rate)
        rospy.loginfo("turtlesim init successful......")
        self.level = 1

    def init_server(self, ip_addr=IP_ADDR, port=PORT):
        self.client.bind((ip_addr, port))
        self.client.listen(1)
        self.conn, addr = self.client.accept()
        print "connect with"
        print addr
    
    def shutdown(self):
        rospy.loginfo("stop the turtlesim......")
        print self.rec_motion
        self.cmd_vel.publish(Twist())
        self.r.sleep()
        # self.client.close()

    def go_forward(self):
        linear_speed = 0.1
        linear_distance = 0.2
        linear_tm = linear_distance/linear_speed
        vel = Twist()
        vel.linear.x = linear_speed
        ticks = int(linear_tm*self.rate)
        for i in range(ticks):
            self.cmd_vel.publish(vel)
            self.r.sleep()
        self.cmd_vel.publish(Twist())
        self.r.sleep()

    def go_backward(self):
        linear_speed = -0.1
        linear_distance = -0.2
        linear_tm = linear_distance/linear_speed
        vel = Twist()
        vel.linear.x = linear_speed
        ticks = int(linear_tm*self.rate)
        for i in range(ticks):
            self.cmd_vel.publish(vel)
            self.r.sleep()
        self.cmd_vel.publish(Twist())
        self.r.sleep()

    def turn_right(self):
        angular_angle = -pi/2
        angular_tm = 1.0
        angular_speed = angular_angle/angular_tm
        vel=Twist()
        vel.angular.z = angular_speed
        ticks = int(angular_tm*self.rate)
        for i in range(ticks):
            self.cmd_vel.publish(vel)
            self.r.sleep()
        self.cmd_vel.publish(Twist())
        self.r.sleep()

    def turn_left(self):
        angular_angle = pi/2
        angular_tm = 1.0
        angular_speed = angular_angle/angular_tm
        vel=Twist()
        vel.angular.z = angular_speed
        ticks=int(angular_tm*self.rate)
        for i in range(ticks):
            self.cmd_vel.publish(vel)
            self.r.sleep()
        self.cmd_vel.publish(Twist())
        self.r.sleep()

    def stop(self):
        self.cmd_vel.publish(Twist())
        self.r.sleep()

    def move(self):
        while True:

            # data, addr = self.client.recvfrom(1024)
            data = self.conn.recv(1024)
            print data
            self.rec_motion.append(data)
            # data = str(data, 'utf-8')
            if not data:
                break

            if data=='zero':
                rospy.loginfo("object 1")
                self.pubgrab.publish("milk")
                self.r.sleep()
            elif data=='one':
                rospy.loginfo("object 2")
                self.pubgrab.publish("juice")
                self.r.sleep()
            elif data=='two':
                rospy.loginfo("object 3")
                self.pubgrab.publish("tea")
                self.r.sleep()
            elif data=='three':
                rospy.loginfo("object 4")
                self.pubgrab.publish("coffee")
                self.r.sleep()
            elif data=='1':
                rospy.loginfo("forward")
                self.go_forward()
            elif data=='2':
                rospy.loginfo("backward")
                self.go_backward()
            elif data=='3':
                rospy.loginfo("turn left")
                self.turn_left()
            elif data=='4':
                rospy.loginfo("turn right")
                self.turn_right()
            elif data=='5':
                rospy.loginfo("ready to grab")
            
            else:
                rospy.loginfo("else stop")
                self.stop()
            time.sleep(1.0)


if __name__ == '__main__':
    try:
        obj = MoveGrab()
        obj.move()
    except:
        rospy.loginfo("node terminated")