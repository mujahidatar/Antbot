import numpy as np
import cv2
import csv
import serial
import cv2.aruco as aruco
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
ids=0
old=0
sim=0
s = serial.Serial("/dev/ttyUSB0",9600) # Select the USB port
s.write(b"S")                          ## Send data to Arduino to follow line

######Detect ArUco Id
def detect_Aruco(image):               
    img=image
    aruco_list = {}
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_7X7_250)
    parameters = aruco.DetectorParameters_create()  
    _, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters = parameters)
    return ids

######Generate CSV file of detected Id's
def csv_cr(ids,sim):
    data = ["sim"+str(sim),str(ids)]
    with open('eYRC#AB#5352.csv','a') as csvFile:
        writer = csv.writer(csvFile,delimiter=',')
        writer.writerow(data)

##### Initialize PiCamera and set resolution and framerate
camera = PiCamera()            
camera.resolution = (640, 480)
camera.framerate = 8
rawCapture = PiRGBArray(camera, size=(640, 480))
 
######Scan ArUco Id's
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    cv2.imshow("Frame", image)
    rawCapture.truncate(0)
    ids=detect_Aruco(image)
    
    if ids!=old:       ####not printing same detected ArUco Id
        if ids:
            print(ids)
            csv_cr(ids,sim)
            sim+=1
            old=ids
            
    if cv2.waitKey(1) & 0xFF == ord(' '):
         break

