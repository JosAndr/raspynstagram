import numpy as np
import cv2
face_det=cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt2.xml')
img=cv2.imread('VLA.jpeg')
gris=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_det.detectMultiScale(gris, 1.3, 5)
for(x,y,w,h) in faces:
   img=cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
   roi_gris=gris[y:y+h, x:x+w]
   roi_col=img[y:y+h, x:x+w]
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows


