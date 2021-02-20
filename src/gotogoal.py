#!/usr/bin/env python
import rospy
from geometry_msgs.msg  import Twist
from turtlesim.srv import *
from std_srvs.srv import *
from turtlesim.msg import Pose
from math import pow,atan2,sqrt
import sys
PI = 3.1415926535897



def moveToTarget(distance, isForward):
    # Starts a new node
    #rospy.init_node('robot_cleaner', anonymous=True)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()
    
    #Receiveing the user's input
    print("Let's move your robot")
    speed = 5 #input("Input your speed:")
    #distance = input("Type your distance:")
    #isForward = input("Foward?: ")
    
    #Checking if the movement is forward or backwards
    if isForward:
        vel_msg.linear.x = abs(speed)
    else:
        vel_msg.linear.x = -abs(speed)
    #Since we are moving just in x-axis
	vel_msg.linear.y = 0
	vel_msg.linear.z = 0
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0
	vel_msg.angular.z = 0
    if not rospy.is_shutdown():
    
		t0 = float(rospy.Time.now().to_sec())
		current_distance = 0
        #Loop to move the turtle in an specified distance
		while(float(current_distance) < float(distance)):
            #Publish the velocity
			velocity_publisher.publish(vel_msg)
            #Takes actual time to velocity calculus
			t1=float(rospy.Time.now().to_sec())
            #Calculates distancePoseStamped
			current_distance= speed*(t1-t0)
        #After the loop, stops the robot
		vel_msg.linear.x = 0
	#Force the robot to stop
		velocity_publisher.publish(vel_msg)
        #clear()
    
    #rospy.spin()

def rotate(angle, clockwise):

    #Starts a new node
    #rospy.init_node('robot_cleaner', anonymous=True)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    # Receiveing the user's input
    print("Let's rotate your robot")
    speed = 20 #input("Input your speed (degrees/sec):")
    #angle = input("Type your distance (degrees):")
    #clockwise = 1 #input("Clowkise?: ") #True or false

    #Converting from angles to radians
    angular_speed = speed*2*PI/360
    relative_angle = float(float(angle)*2*PI/360)

    #We wont use linear components
    vel_msg.linear.x=0
    vel_msg.linear.y=0
    vel_msg.linear.z=0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0

    # Checking if our movement is CW or CCW
    if clockwise:
        vel_msg.angular.z = -abs(angular_speed)
    else:
        vel_msg.angular.z = abs(angular_speed)
    # Setting the current time for distance calculus
    t0 = rospy.Time.now().to_sec()
    current_angle = 0

    while(current_angle < relative_angle):
        velocity_publisher.publish(vel_msg)
        t1 = rospy.Time.now().to_sec()
        current_angle = angular_speed*(t1-t0)


    #Forcing our robot to stop
    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)
    #rospy.ServiceProxy('/clear', Empty)
    #rospy.spin()

def move_circle(sec , speed, rot):
	pub = rospy.Publisher('/turtle1/cmd_vel',Twist, queue_size = 10)
	vel_msg = Twist()
	#speed = 2
	radius = 20

	#print "Your wish is my command"
	#print "If you want to quit and watch me draw squares, Ctl-c me"


	vel_msg.linear.x = speed
	vel_msg.linear.y = 0
	vel_msg.linear.z = 0
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0
	vel_msg.angular.z = float(rot)
	t0 = rospy.Time.now().to_sec()
	#Move Robot in circle

	t1 = rospy.Time.now().to_sec()
	while(t1-t0 <= float(sec)):
		pub.publish(vel_msg)
		t1 = rospy.Time.now().to_sec()
	
	vel_msg.linear.x = 0	
	vel_msg.angular.z = 0
	pub.publish(vel_msg)	

def move_circle_server():

	s = rospy.Service( 'move_circle', MoveCircle, handle_move_circle )
	rospy.spin()
    
def drawA():
	rotate(70, 0)
	moveToTarget(4, 1)
	rotate(130, 1)
	moveToTarget(4, 1)
	moveToTarget(2, 0)
	rotate(116, 1)	
	moveToTarget(1.7, 1)
	killTurtle("turtle1")
def drawZ():
	moveToTarget(4,1)
	rotate(126,1)
	moveToTarget(5,1)
	rotate(126,0)
	moveToTarget(3,1)
	killTurtle("turtle1")
def drawC():
	move_circle(1, 2, 1)
	move_circle(0.77, -2, -1)
	rotate(95,1)
	moveToTarget(0.75, 1)
	moveToTarget(0.675, 0)
	rotate(95, 0)
	move_circle(5*0.77,-2, -1)
	killTurtle("turtle1")
def drawG():
	move_circle(5*0.805, -2, -1)
	move_circle(6*0.7318, 2, 1)
	rotate(56,0)
	moveToTarget(1.2, 1)
	rotate(90,0)
	moveToTarget(1.2,1)
	killTurtle("turtle1")
def drawB():
	rotate(94.5, 0)
	moveToTarget(4,1)
	rotate(90, 1)
	moveToTarget(1,1)
	move_circle(0.777, 4, -4)
	moveToTarget(1,1)
	rotate(180,1)
	moveToTarget(1.34,1)
	move_circle(0.777, 4, -4)
	moveToTarget(1.34,1)
	killTurtle("turtle1")
if __name__ == '__main__':
	try:
		rospy.init_node('robot_cleaner', anonymous=True)
		clear = rospy.ServiceProxy('/clear', Empty)
		killTurtle = rospy.ServiceProxy('/kill', Kill)
        
		val = input('bir harf giriniz(A,B,C,G,Z):')
		if val == 'A':
			drawA()
		elif val == 'B':
			drawB()
		elif val == 'C':
			drawC()
		elif val == 'G':
			drawG()
		elif val == 'Z':
			drawZ()
		elif val == '.':
			sys.exit()
		else:
			print "yanlis harf"
	except rospy.ROSInterruptException: pass
