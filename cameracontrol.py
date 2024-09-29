#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import cv2
import mediapipe as mp

class RobotNavigation():
    def __init__(self):
        rospy.init_node('robot_navigation', anonymous=True)
        
        self.pub=rospy.Publisher("cmd_vel",Twist,queue_size=10)
        self.velocity=Twist()

    def move_forward(self):
        self.velocity.linear.x = 0.5
        self.velocity.angular.z = 0
        self.pub.publish(self.velocity)
        print("Moving forward")

    def stop(self):
        self.velocity.linear.x = 0
        self.velocity.angular.z = 0
        self.pub.publish(self.velocity)
        print("Stopping")

    def move_backward(self):
        self.velocity.linear.x = -0.5
        self.velocity.angular.z = 0
        self.pub.publish(self.velocity)
        print("Moving backward")

    def rotate_left(self):
        self.velocity.linear.x = 0
        self.velocity.angular.z = 0.5
        self.pub.publish(self.velocity)
        print("Rotating left")

    def rotate_right(self):
        self.velocity.linear.x = 0
        self.velocity.angular.z = -0.5
        self.pub.publish(self.velocity)
        print("Rotating right")

    def hand_track(self):
        #camera settings size and which camera is used for tracking
        cap=cv2.VideoCapture(0)
        cap.set(propId=3,value=640)
        cap.set(propId=4,value=480)


        #hand tracking objects
        mpHand=mp.solutions.hands
        hands=mpHand.Hands()
        mpDraw=mp.solutions.drawing_utils

        tipIDs=[4,8,12,16,20] #top points of each finger

        while True:
            success, img=cap.read()

            # Convert image to RGB
            imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

            # Feed image to hand tracking model
            results=hands.process(imgRGB)

            lmList=[]
            # If hands are detected
            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:

                    # Draw hand landmarks
                    mpDraw.draw_landmarks(img, handLms, mpHand.HAND_CONNECTIONS)

                    # Extract hand coordinates
                    for id, lm in enumerate(handLms.landmark):
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        lmList.append([id, cx, cy])

            if len(lmList)>0:
                fingers=[]

                #tumb count
                if lmList[tipIDs[0]][1] > lmList[tipIDs[0]-1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                #other 4 fingers

                for id in range(1,5):
                    if lmList[tipIDs[id]][2] < lmList[tipIDs[id]-2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                #print(fingers)
                totalFinger=fingers.count(1)
                #print("Total number of fingers detected: ", totalFinger)

                if totalFinger==1:
                    self.move_forward()
                elif totalFinger==2:
                    self.move_backward()
                elif totalFinger==5:
                    self.stop()
                elif totalFinger==3:
                    self.rotate_left()
                elif totalFinger==4:
                    self.rotate_right()

        

if __name__ == '__main__':
    try:
        robot_nav = RobotNavigation()
        robot_nav.hand_track()
        cv2.imshow("Video",img)   
    except rospy.ROSInterruptException:
        pass


        








