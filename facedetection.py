import cv2
import mediapipe as mp

cap=cv2.VideoCapture("people.mp4")

mpFace=mp.solutions.face_detection
face=mpFace.FaceDetection(0.2)
mpDraw=mp.solutions.drawing_utils

while True:
    success,img=cap.read()
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=face.process(imgRGB)
    print(results)

    if results.detections:
        for id, detection in enumerate(results.detections):

            bboxC=detection.location_data.relative_bounding_box
            h, w, _=img.shape
            bbox=int(bboxC.xmin*w),int(bboxC.ymin*h),int(bboxC.width*w),int(bboxC.height*h)
            cv2.rectangle(img,bbox,(255,0,0),2)

    cv2.imshow("image",img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

