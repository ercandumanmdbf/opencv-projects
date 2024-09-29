from time import ctime

import cv2
import mediapipe as mp
import time

mpPose=mp.solutions.pose
pose=mpPose.Pose()
mpDraw=mp.solutions.drawing_utils

cap=cv2.VideoCapture("dancealone.mp4")

cTime=0
pTime=0
while True:
    success,frame=cap.read()
    imgRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=pose.process(imgRGB)
    print(results.pose_landmarks)

    if results.pose_landmarks:
        mpDraw.draw_landmarks(frame,results.pose_landmarks,mpPose.POSE_CONNECTIONS)


    for id,lm in enumerate(results.pose_landmarks.landmark):
        h,w,c=frame.shape
        print(id,lm)
        cx,cy=int(lm.x*w),int(lm.y*h)

        if id==11:
            cv2.circle(frame,(cx,cy),11,(255,0,0),cv2.FILLED)

    ctime=time.time()
    fps=1/(ctime-pTime)
    pTime=ctime
    cv2.putText(frame,f"FPS: {int(fps)}",(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

    cv2.imshow("Pose Detection",frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break