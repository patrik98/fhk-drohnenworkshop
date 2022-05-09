import math
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_srvs.srv import Empty


# 2 dimensionale Ebene: x, y
# yaw = Ausrichtung
x = 0.0
y = 0.0
yaw = 0.0


def poseCallback(pose_message):
    # Globale Variablen aktualisieren
    global x, y, yaw
    
    x = pose_message.x
    y = pose_message.y
    yaw = pose_message.theta

    # rospy.loginfo(x)
    # rospy.loginfo(y)
    # rospy.loginfo(yaw)


def distance_2d(p1, p2):
    """
        Euklidischer Abstand: Abstand zweier Punkte in der Ebene
        Formel: math.sqrt( (q1 - p1)**2 + ... + (qn - pn)**2 )
        2-Dimensional (n=2) -> Euklidischer Abstand entspricht Satz des Pythagoras
        https://de.wikipedia.org/wiki/Euklidischer_Abstand

        Abstand von x0,y0 zu momentanem x,y
    """
    global x, y

    return  abs( math.sqrt( (x - p1)**2 + (y - p2)**2 ) )


def move(speed, distance, is_forward=True):
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

    rate = rospy.Rate(10) #hz

    velocity_msg = Twist()

    global x, y
    x0 = x
    y0 = y

    if (is_forward):
        velocity_msg.linear.x = abs(speed)
    else:
        velocity_msg.linear.x -= abs(speed)

    distance_moved = 0.0

    while not rospy.is_shutdown():
        if distance_moved + abs(speed) <= distance:
            velocity_publisher.publish(velocity_msg)
            distance_moved = distance_2d(x0, y0)
        else:
            velocity_msg.linear.x = 0
            velocity_publisher.publish(velocity_msg)
            
        # rospy.loginfo(x)
        rospy.loginfo("distance moved: " + str(distance_moved))

        rate.sleep()


def go_to(goal_x, goal_y):
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

    rate = rospy.Rate(10) #hz

    velocity_msg = Twist()

    global x, y, yaw

    while not rospy.is_shutdown():
        distance = distance_2d(goal_x, goal_y)

        LINEAR_CONSTANT_SPEED = 0.5
        linear_speed = distance * LINEAR_CONSTANT_SPEED
        
        ANGULAR_CONSTANT_SPEED = 3.0
        desired_angle = math.atan2(goal_y - y, goal_x - x)
        angular_speed = (desired_angle - yaw) * ANGULAR_CONSTANT_SPEED
	
        if distance > 0.01:
            velocity_msg.linear.x = linear_speed
            velocity_msg.angular.z = angular_speed
            velocity_publisher.publish(velocity_msg)
        else:
            velocity_msg.linear.x = 0
            velocity_msg.angular.z = 0
            velocity_publisher.publish(velocity_msg)
        

        # rospy.loginfo(linear_speed)
        # rospy.loginfo(desired_angle)
        # rospy.loginfo(distance)
        
        rate.sleep()


if __name__ == '__main__':
    try:
        rospy.init_node('my_turtlesim_node', anonymous=True)
        subscriber = rospy.Subscriber('/turtle1/pose', Pose, poseCallback)
        
        # sleep, sonst sind x, y initial 0
        rospy.sleep(2.0)
        
        move(1.0, 4.0, True)
        # go_to(1.0, 7)
    except rospy.ROSInterruptException:
        pass
