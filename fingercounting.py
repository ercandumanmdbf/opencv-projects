import cv2
import mediapipe as mp

cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

mpHand=mp.solutions.hands
hands=mpHand.Hands()
mpDraw=mp.solutions.drawing_utils

tipIds=[4,8,12,16,20]

while True:
    success,img=cap.read()
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(imgRGB)
    #print(results.multi_hand_landmarks)

    lmList=[]
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHand.HAND_CONNECTIONS)
            for id,lm in enumerate(handLms.landmark):
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                lmList.append([id,cx,cy])


                #if id == 8:
                   # cv2.circle(img, (int(cx), int(cy)), 9, (255, 0, 0), cv2.FILLED)

                #if id == 6:
                    #cv2.circle(img, (int(cx), int(cy)), 9, (0, 255, 0), cv2.FILLED)
    if len(lmList) > 0:
        fingers = []

        # Thumb (special case: comparing tip with knuckle)
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:  # Thumb comparison
            fingers.append(1)  # Thumb is open
        else:
            fingers.append(0)  # Thumb is closed

        # Other four fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:  # Compare y-coordinates
                fingers.append(1)  # Finger is open
            else:
                fingers.append(0)  # Finger is closed

        #print(fingers)
        totalF=fingers.count(1)
        cv2.putText(img, str(totalF), (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Video",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break