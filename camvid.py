#import numpy as np
import cv2
cap = cv2.VideoCapture(0)
#ret, frame= cap.read()
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('image', frame)
    cv2.imshow('gray', gray)

    if cv2.waitKey(1) & 0xFF == ord(' '):
        break
cap.release()
cv2.destroyAllWindows()