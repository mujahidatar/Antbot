import numpy as np
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
from time import sleep
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD)
n=0
R =0

### Declare LED pins 
RED1 = 11
RED2 = 12
GREEN1 = 13
GREEN2 = 16
BLUE1 = 15
BLUE2 = 18

### Set LED pins as OUTPUT pins
GPIO.setup(RED1,GPIO.OUT)

GPIO.setup(RED2,GPIO.OUT)

GPIO.setup(GREEN1,GPIO.OUT)

GPIO.setup(GREEN2,GPIO.OUT)

GPIO.setup(BLUE1,GPIO.OUT)

GPIO.setup(BLUE2,GPIO.OUT)

GPIO.output(RED1,1)
GPIO.output(RED2,1) 
GPIO.output(BLUE1,1)                                            # Turn off BLUE LED
GPIO.output(BLUE2,1)
GPIO.output(GREEN1,1)                                           # Turn on GREEN LED
GPIO.output(GREEN2,1)



shrub_area = []
### Function to detect the color of block or supply

def color_detection(frame):
    R =0
    img = frame.array
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

   
    lower_red1 = np.array([170,150,50])                                                                        # HSV range for Red colour 
    upper_red1 = np.array([180,255,255])

    #lower_red2 = np.array([170,50,50])
    #upper_red2 = np.array([180,255,255])

    lower_blue = np.array([95,100,50])                                                                         # HSV range for Blue colour
    upper_blue = np.array([140,255,255])

    lower_yellow = np.array([20,150,70])                                                                       # HSV range for Yellow colour
    upper_yellow = np.array([35,255,255])

    lower_green = np.array([60,150,30])                                                                        # HSV range for Green colour
    upper_green = np.array([80,255,255])

    

    
    
    maskr0=cv2.inRange(hsv,lower_red1,upper_red1)
    #maskr1=cv2.inRange(hsv,lower_red2,upper_red2)
    mask1=cv2.inRange(hsv,lower_blue,upper_blue)
    mask2=cv2.inRange(hsv,lower_green,upper_green)
    mask3=cv2.inRange(hsv,lower_yellow,upper_yellow)
    #image,contours,hierarchy=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    mask0= maskr0 # +maskr1
    a = mask0
    b = mask1
    c = mask2
    d = mask3

    if (c.any()!=0):        
        res   = cv2.bitwise_and(img, img, mask= mask2)
        cv2.imshow ('Res', res)
        print ('Green block')
        #shrub_area.insert(2, 'GREEN Block')
        GPIO.output(RED1,1)
        GPIO.output(RED2,1) 
        GPIO.output(BLUE1,1)                                            # Turn off BLUE LED
        GPIO.output(BLUE2,1)
        GPIO.output(GREEN1,0)                                           # Turn on GREEN LED
        GPIO.output(GREEN2,0)
        sleep(1)
        GPIO.output(GREEN1,1)                                           # Turn off GREEN LED 
        GPIO.output(GREEN2,1)
        
    elif(d.any()!=0):
        res3   = cv2.bitwise_and(img, img, mask= mask3)
        cv2.imshow ('Res', res3)
        print('Yellow block')
        #shrub_area.insert(3, 'YELLOW Block')
        GPIO.output(RED1,0)                                             # Turn on RED and GREEN LED simultaneously
        GPIO.output(GREEN1,0)
        GPIO.output(RED2,0)
        GPIO.output(GREEN2,0)
        sleep(2)
        GPIO.output(RED1,1)                                             # Turn off RED and GREEN LED simultaneously
        GPIO.output(GREEN1,1)
        GPIO.output(RED2,1)
        GPIO.output(GREEN2,1)
        
    elif (a.any()!=0):
        res2   = cv2.bitwise_and(img, img, mask= mask0) 
        cv2.imshow ('Res', res2)
        print ('Red block')
        #shrub_area.insert(0, 'RED Block')
        GPIO.output(RED1,0)                                             # Turn on RED LED
        GPIO.output(RED2,0)
        sleep(1)
        GPIO.output(RED1,1)                                             # Turn off RED LED
        GPIO.output(RED2,1)

    elif (b.any()!=0):
        res1   = cv2.bitwise_and(img, img, mask= mask1)
        cv2.imshow ('Res', res1)
        print ('Blue block')
        #shrub_area.insert(1, 'BLUE Block')
        GPIO.output(BLUE1,0)                                            # Turn on BLUE LED
        GPIO.output(BLUE2,0)
        sleep(1)
        GPIO.output(BLUE1,1)                                            # Turn off BLUE LED
        GPIO.output(BLUE2,1)
            
   
            
    
        
    else:
        print ('None color found')
    #print (shrub_area)
    
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray (camera, size=(640, 480))
sleep(2)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port= True):
        image = frame.array
        cv2.imshow("Frame", image)
        rawCapture.truncate(0)
        if cv2.waitKey(1) & 0xFF == ord(' '):
         break
        n=+1
        det_color = color_detection(frame)
        if n==0:
         break
            
