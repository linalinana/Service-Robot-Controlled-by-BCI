#!/usr/bin/env python
#-*- coding:UTF-8 -*-
import rospy
import math
from std_msgs.msg import String
from std_msgs.msg import Float64
from ch11_dynamixel.msg import pos

class Loop:
    def __init__(self):
	rospy.on_shutdown(self.cleanup)

	self.joint1 = rospy.Publisher('/arm_shoulder_pan_joint/command',Float64)
	self.joint2 = rospy.Publisher('/arm_shoulder_lift_joint/command',Float64)
	self.joint3 = rospy.Publisher('/arm_elbow_flex_joint/command',Float64)
	self.joint4 = rospy.Publisher('/arm_wrist_flex_joint/command',Float64)
	self.joint5 = rospy.Publisher('/gripper_joint/command',Float64)

	self.arm_state_pub = rospy.Publisher('/arm_state', String) 

	self.x = 0
	self.y = 0
	self.z = 10

	self.grasp = 1
	# initialize
	self.armsub = 0
	self.a2 = 0.105
	self.a3 = 0.105
	self.a4 = 0.09
	self.arm_length = 0.3
	self.label = -1
	def callback_pos (data_pos):         
		rospy.loginfo(rospy.get_caller_id() + "I heard that coordinate is %s", data_pos)
		self.grasp = 1
		self.x = data_pos.x
		self.y = data_pos.y
		self.z = data_pos.z
        # adding program
	def callback_img (data_img):          	
		if data_img.data.find('release') > -1:
			rospy.loginfo( "I heard that the robot has reached cupboard")
			self.armsub = 1
		else:
			self.armsub = 0
	def callback_label (data_label): #if begin to grasp or release,from img progam 
		if data_label.data.find('zero') > -1:
			self.label = 0
		if data_label.data.find('one') > -1:
			self.label = 1
		if data_label.data.find('two') > -1:
			self.label = 2
		if data_label.data.find('three') > -1:
			self.label = 3
		else:
			self.label = -1
		print  data_label.data
	# adding program above
	rospy.Subscriber("position_xyz_center", gps, callback_pos)
	rospy.loginfo("Subscribe to topic pos.....")
	rospy.sleep(1)
	#adding program
	rospy.Subscriber("obj_label", String, callback_label)
	rospy.loginfo("Subscribe to topic obj_label.....")
	rospy.sleep(1)

	rospy.Subscriber("img2arm_release", String, callback_img)
	rospy.loginfo("Subscribe to topic image2arm.....")
	rospy.sleep(1)

	# Define five poses
	self.pos1 = Float64()
	self.pos2 = Float64()
	self.pos3 = Float64()
	self.pos4 = Float64()
	self.pos5 = Float64()
	# Initial gesture of robot arm
	self.pos1 = 1.5
	self.pos2 = 1.9
	self.pos3 = -1.57
	self.pos4 = 0.6
	self.pos5 = -0.5

	self.joint5.publish(self.pos5)
	rospy.sleep(1)
	self.joint4.publish(self.pos4)
	rospy.sleep(1)
	self.joint3.publish(self.pos3)
	rospy.sleep(1)
	self.joint1.publish(self.pos1)
	rospy.sleep(1)
	self.joint2.publish(self.pos2)
	rospy.sleep(1)
	rospy.loginfo("gesture of robot arm Initialized....")
	
	while not rospy.is_shutdown():
		if self.grasp == 1:

			self.obj_dis  =math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
			while self.arm_length < self.obj_dis:
				rospy.loginfo("This coordinate is out of my location......")
				rospy.sleep(1)

			rospy.loginfo("X coordinate is .... ")
			print self.x
			rospy.loginfo("Y coordinate is ....") #print y coordinate
			print self.y
			rospy.loginfo("Z coordinate is .... ")
			print self.z
			rospy.loginfo("Calculate new joint angles ......")


			# calculate new joint angles
			self.theta1 = - math.atan2(self.x,self.y) + 0.15
			self.l = math.hypot(self.x,self.y) - self.a4
			self.l1 = math.hypot(self.l,self.z)
			print self.l1
			self.cosfai = self.l1 / (2 * self.a2)
			rospy.loginfo("cosfai is ....") 
			print self.cosfai
			if  self.cosfai > 1:
				self.cosfai = 1
			self.fai = math.acos(self.cosfai)
			self.theta = math.atan2(self.z,self.l)
			self.theta2 = math.pi / 2 - self.theta - self.fai
			self.theta4 = self.theta - self.fai
			self.theta3 = 2 * self.fai
			self.theta5 = 0.8

			self.pos1 = self.theta1
			self.pos2 = self.theta2
			self.pos3 = self.theta3
			self.pos4 = self.theta4
			self.pos5 = self.theta5

			rospy.loginfo("The rotation angle of joint one.....")
			print self.theta1
			rospy.loginfo("The rotation angle of joint two.....")
			print self.theta2
			rospy.loginfo("The rotation angle of joint three.....")
			print self.theta3
			rospy.loginfo("The rotation angle of joint four.....")
			print self.theta5
			rospy.loginfo("The rotation angle of joint five.....")
			print self.theta5

			self.joint2.publish(1.57)    
			rospy.sleep(1)
			self.joint4.publish(-1.57)
			rospy.sleep(3)
			self.joint3.publish(-1.2)
			rospy.sleep(3)
			#
			self.joint1.publish(self.pos1)
			rospy.sleep(3)
			# 	
			self.joint5.publish(self.pos5)
			rospy.sleep(2)
			self.joint2.publish(self.pos2)
			rospy.sleep(2)
			self.joint3.publish(self.pos3)
			rospy.sleep(2)
			self.joint4.publish(self.pos4)
			rospy.sleep(3)
			
			rospy.loginfo("Catched the object ......")
			

			self.pos1 = 0
			self.pos2 = 1.2
			self.pos3 =-1.3
			self.pos4 = -0.2
			print self.label
			if self.label == 0:
				self.pos5 = -0.25
			if self.label == 1:
				self.pos5 = -0.25
			if self.label == 2:
				self.pos5 = 0.25
			if self.label == 3:
				self.pos5 = -0.25
			else :
				self.pos5 = -0.3
			print self.pos5 
			
			#self.joint2.publish(1.3)
			self.joint3.publish(0.2)
			self.joint4.publish(0)
			self.joint5.publish(self.pos5)
			rospy.sleep(3)
			self.joint1.publish(self.pos1)
			self.joint2.publish(self.pos2)
			self.joint3.publish(self.pos3)
			self.joint4.publish(self.pos4)
			
			rospy.loginfo("Lift up the goods for 3 seconds ......")
			rospy.sleep(3) #15 before
			self.ifgrasped = "grasped"
			self.arm_state_pub.publish(self.ifgrasped)
			self.grasp = 0

		if self.armsub == 1:
			rospy.loginfo("Ready for releasing the goods")
			self.pos1 = 0
			self.pos2 = 0.8
			self.pos3 = -0.7
			self.pos4 = 1.2
			self.pos5 = 0.6
			self.joint1.publish(self.pos1)
			rospy.sleep(1)
			self.joint2.publish(self.pos2)
			rospy.sleep(1)
			self.joint3.publish(self.pos3)
			rospy.sleep(1)
			self.joint4.publish(self.pos4)
			rospy.sleep(1)
			self.joint5.publish(self.pos5)
			rospy.loginfo("Release the goods ......")
			rospy.sleep(5)
			
			self.armsub = 0
			self.ifreleased = "released"
			self.arm_state_pub.publish(self.ifreleased)
			
			self.pos1 = Float64()
			self.pos2 = Float64()
			self.pos3 = Float64()
			self.pos4 = Float64()
			self.pos5 = Float64()
			# Initial gesture of robot arm
			self.pos1 = 1.5
			self.pos2 = 1.57
			self.pos3 = -1.57
			self.pos4 = 0.6
			self.pos5 = -0.5
			
			self.joint5.publish(self.pos5)
			rospy.sleep(1)
			self.joint4.publish(self.pos4)
			rospy.sleep(1)
			self.joint3.publish(self.pos3)
			rospy.sleep(1)
			#self.joint2.publish(0.5)
			#rospy.sleep(1)
			self.joint1.publish(self.pos1)
			rospy.sleep(1)
			self.joint2.publish(self.pos2)
			rospy.sleep(1)
			rospy.loginfo("reset turtlebot arm....")	

    def cleanup(self):
        rospy.loginfo("Shutting down turtlebot arm....")

if __name__=="__main__":

    rospy.init_node('arm_grasp')
    try:
        Loop()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

