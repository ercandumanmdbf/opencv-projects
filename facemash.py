import cv2
import mediapipe as mp
import time

cap=cv2.VideoCapture("face.mp4")

mpFaceMesh=mp.solutions.face_mesh
faceMesh=mpFaceMesh.FaceMesh(max_num_faces=1)
mpDraw=mp.solutions.drawing_utils
drawSpec=mpDraw.DrawingSpec(thickness=1, circle_radius=1)

while True:
    success,img=cap.read()

    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=faceMesh.process(imgRGB)
    print(results.multi_face_landmarks)

    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACEMESH_TESSELATION, drawSpec, drawSpec)

        for id,lms in enumerate(faceLms.landmark):
            h,w,c=img.shape
            print(id,lms)
            cx,cy=int(lms.x*w),int(lms.y*h)
            cv2.circle(img,(cx,cy),1,(255,0,0),cv2.FILLED)

    cv2.imshow("image", img)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break