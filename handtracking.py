import cv2
import time
import mediapipe as mp


cap = cv2.VideoCapture(0)

mpHand=mp.solutions.hands
hands=mpHand.Hands()
mpDraw=mp.solutions.drawing_utils


while True:
    success,img=cap.read()
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(imgRGB)
    print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img,handLms,mpHand.HAND_CONNECTIONS)

            for id,lm in enumerate(handLms.landmark):
                h, w, c=img.shape
                cx, cy=int(lm.x*w), int(lm.y*h)


                if id==0:
                    cv2.circle(img,(cx,cy),15,(255,0,0),cv2.FILLED)

    cv2.imshow("image",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break