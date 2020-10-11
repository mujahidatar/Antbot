'''#############################################################
#                                                              #
#  Color Identificatin, ArUco Scanning and Bit manipulation    #
#                                                              #
#                                                              #
################################################################'''                                                              

'''
#############################################################################################################################################################################################################
#                                                                                                                                                                                                           #
#  Team ID:             eYRC-5352                                                                                                                                                                           #                                               
#  Author list:         Mujahid Atar, Gade Atul, Patil Sujata                                                                                                                            #
#  File name:           task-4-main.py                                                                                                                                                                      #
#  Theme name:          Ant Bot                                                                                                                                                                             #
#  Functions:           Supply(), AH0_Supply(), AH1_Supply(), AH2_Supply(), AH3_Supply(), Aruco_scan(), detect_Aruco, bit_manipulation, Store_Data(), Supply_detection, Color_detection, Supply_scan()      #
#  Global variables:    old, sim, Ah, AServ1, AServ2, ATR, Bh, BServ1, BServ2, BTR, Ch, CServ1, CServ2, CTR, Dh, DServ1, DServ2, DTR, m                                                                     #
#############################################################################################################################################################################################################
'''

#classes and subclasses to import
import numpy as np
import cv2
import serial
import cv2.aruco as aruco
from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
from time import sleep
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD)
s = serial.Serial("/dev/ttyUSB0",9600)                                                                                        # Select the USB port

'''
#############################################################################################
# Initialization of variables used in program
# All comments are on right side
#############################################################################################'''
n=0                                                                                                                           #
m=0                                                                                                                           #
C=[]                                                                                                                          #
R =0                                                                                                                          #
read=0                                                                                                                        #
ids=0                                                                                                                         #
old=0                                                                                                                         #
sim=0                                                                                                                         #
key=0                                                                                                                         #
Ah=1                                                                                                                          #
Bh=1                                                                                                                          #
Ch=1                                                                                                                          #
Dh=1                                                                                                                          #
AServ1=0                                                                                                                      #
AServ2=0                                                                                                                      #
BServ1=0                                                                                                                      #
BServ2=0                                                                                                                      #
CServ1=0                                                                                                                      #
CServ2=0                                                                                                                      #
DServ1=0                                                                                                                      #
DServ2=0                                                                                                                      #
ATR=0                                                                                                                         #
BTR=0                                                                                                                         #
CTR=0                                                                                                                         #
DTR=0                                                                                                                         #
Trash_Check=0                                                                                                                 # Function to check trash

### Declare LED pins 
RED1 = 11
GREEN1 = 13
BLUE1 = 15

### Set LED pins as OUTPUT pins
GPIO.setup(RED1,GPIO.OUT)
GPIO.output(RED1,1)                                                                                                           # Turn off RED LED             
GPIO.setup(GREEN1,GPIO.OUT)
GPIO.output(GREEN1,1)                                                                                                         # Turn off GREEN LED 
GPIO.setup(BLUE1,GPIO.OUT)
GPIO.output(BLUE1,1)                                                                                                          # Turn off BLUE LED 



'''###########################################################################################################################
# Function name: Supply()                                                                                                    
# Input:         Ah, Bh, Ch, Dh                                                                                             
# Output:        sqeuence in which QAH and remaining RAH are to be served                                                    
# Logic:         cheking with Ah, Bh, Ch, and Dh gives the QAH and sequence to provide service                               
# Example call:  Supply(Ah)                                                                                                  
##############################################################################################################################'''

def Supply():
    ## if input is Ah it means AH0 = QAH and further service to RAH will be provided as follow
    if Ah:                                                                                                                    
        AH0_Supply()                                                                                                          
        AH1_Supply()
        AH2_Supply()
        AH3_Supply()

    ## if input is Bh it means AH1 = QAH and further service to RAH will be provided as follow
    elif Bh:
        AH1_Supply()
        AH0_Supply()
        AH2_Supply()
        AH3_Supply()
        
    ## if input is Ch it means AH2 = QAH and further service to RAH will be provided as follow
    elif Ch:
        AH2_Supply()
        AH0_Supply()
        AH1_Supply()
        AH3_Supply()

    ## if input is Dh it means AH3 = QAH and further service to RAH will be provided as follow
    elif Dh:
        AH3_Supply()
        AH0_Supply()
        AH1_Supply()
        AH2_Supply()

'''########################################################################################################################
# Function name: AH0_Supply()                                                                                             
# Input:         Ah, AServ1, Aserv2, ATR                                                                                  
# Output:        Supply requirement of  AH0                                                                               
# Logic:         If input is AH, it print the output for AH0 i.e. service 1, service 2, and Trash removal for AHO         
# Example call:  AH0_Supply()                                                                                             
###########################################################################################################################'''

def AH0_Supply():
    #print("\n")
    #print("Supply to AH0")
    #print("\n"+str(AServ1)+"   "+str(AServ2)+"   "+str(ATR))
    m=0
    read=0
    val=0
    while(m<=3):
        #print(m)
        while read==0:
            s.flush()
            read=s.readline()
            val = str(read).strip("b'").strip("\\r\\n")
            #print(val)
        if(val=="P"):
            s.write(b"A")
            m=m+1
            s.flush()
        if(val=="Q"):
            s.write('b'+AServ2)
            m=m+1
            s.flush()
        if(val=="R"):
            s.write('b'+AServ1)
            m=m+1
            s.flush()
        if(val=="S"):
            s.write('b'+ATR)
            m=m+1
            s.flush()
        read=0
        val=0
        if (ATR=="T"):
            while read==0:
                s.flush()
                read=s.readline()
                val = str(read).strip("b'").strip("\\r\\n")
                #print(val)
                if val=="C":
                    supply_detection()
                    if Trash_Check=="Yes":
                        s.write(b"Y")
                        s.flush()
                    else:
                        s.write(b"N")
                        s.flush()
                        read=0
                        val=0
                        while read==0:
                            s.flush()
                            read=s.readline()
                            val = str(read).strip("b'").strip("\\r\\n")
                            #print(val)
                        if val=="Y":
                            GPIO.output(RED1,0)                                             # Turn on RED and GREEN LED simultaneously
                            GPIO.output(GREEN1,0)
                            sleep(2)
                            GPIO.output(RED1,1)                                             # Turn off RED and GREEN LED simultaneously
                            GPIO.output(GREEN1,1)
                elif val=="Y":
                    GPIO.output(RED1,0)                                             # Turn on RED and GREEN LED simultaneously
                    GPIO.output(GREEN1,0)
                    sleep(2)
                    GPIO.output(RED1,1)                                             # Turn off RED and GREEN LED simultaneously
                    GPIO.output(GREEN1,1)

'''########################################################################################################################
# Function name: AH1_Supply()
# Input:         Bh, BServ1, Bserv2, BTR
# Output:        Supply requirement of  AH1
# Logic:         If input is AH, it print the output for AH0 i.e. service 1, service 2, and Trash removal for AH1 
# Example call:  AH1_Supply()
###########################################################################################################################'''

def AH1_Supply():
    #print("\n")
    #print("Supply to AH1")
    #print("\n"+str(BServ1)+"   "+str(BServ2)+"   "+str(BTR))
    m=0
    read=0
    val=0
    while(m<=3):
        #print(m)
        while read==0:
            s.flush()
            read=s.readline()
            val = str(read).strip("b'").strip("\\r\\n")
            #print(val)
        if(val=="P"):
            s.write(b"B")
            m=m+1
            s.flush()
        if(val=="Q"):
            s.write('b'+BServ2)
            m=m+1
            s.flush()
        if(val=="R"):
            s.write('b'+BServ1)
            m=m+1
            s.flush()
        if(val=="S"):
            s.write('b'+BTR)
            m=m+1
            s.flush()
        read=0
        val=0
        if (BTR=="T"):
            while read==0:
                s.flush()
                read=s.readline()
                val = str(read).strip("b'").strip("\\r\\n")
                #print(val)
                if val=="C":
                    supply_detection()
                    if Trash_Check=="Yes":
                        s.write(b"Y")
                        s.flush()
                    else:
                        s.write(b"N")
                        s.flush()
                        read=0
                        val=0
                        while read==0:
                            s.flush()
                            read=s.readline()
                            val = str(read).strip("b'").strip("\\r\\n")
                            #print(val)
                        if val=="Y":
                            GPIO.output(RED1,0)                                             # Turn on RED and GREEN LED simultaneously
                            GPIO.output(GREEN1,0)
                            sleep(2)
                            GPIO.output(RED1,1)                                             # Turn off RED and GREEN LED simultaneously
                            GPIO.output(GREEN1,1)
                elif val=="Y":
                    GPIO.output(RED1,0)                                             # Turn on RED and GREEN LED simultaneously
                    GPIO.output(GREEN1,0)
                    sleep(2)
                    GPIO.output(RED1,1)                                             # Turn off RED and GREEN LED simultaneously
                    GPIO.output(GREEN1,1)
    
'''########################################################################################################################
# Function name: AH2_Supply()
# Input:         Ch, CServ1, Cserv2, CTR
# Output:        Supply requirement of  AH2
# Logic:         If input is AH, it print the output for AH0 i.e. service 1, service 2, and Trash removal for AH2
# Example call:  AH2_Supply()
###########################################################################################################################'''

def AH2_Supply():
    #print("\n")
    #print("Supply to AH2")
    #print("\n"+str(CServ1)+"   "+str(CServ2)+"   "+str(CTR))
    m=0
    read=0
    val=0
    while(m<=3):
        #print(m)
        while read==0:
            s.flush()
            read=s.readline()
            val = str(read).strip("b'").strip("\\r\\n")
            #print(val)
        if(val=="P"):
            s.write(b"C")
            m=m+1
            s.flush()
        if(val=="Q"):
            s.write('b'+CServ2)
            m=m+1
            s.flush()
        if(val=="R"):
            s.write('b'+CServ1)
            m=m+1
            s.flush()
        if(val=="S"):
            s.write('b'+CTR)
            m=m+1
            s.flush()
        read=0
        val=0
        if (CTR=="T"):
            while read==0:
                s.flush()
                read=s.readline()
                val = str(read).strip("b'").strip("\\r\\n")
                #print(val)
                if val=="C":
                    supply_detection()
                    if Trash_Check=="Yes":
                        s.write(b"Y")
                        s.flush()
                    else:
                        s.write(b"N")
                        s.flush()
                        read=0
                        val=0
                        while read==0:
                            s.flush()
                            read=s.readline()
                            val = str(read).strip("b'").strip("\\r\\n")
                            #print(val)
                        if val=="Y":
                            GPIO.output(RED1,0)                                             # Turn on RED and GREEN LED simultaneously
                            GPIO.output(GREEN1,0)
                            sleep(2)
                            GPIO.output(RED1,1)                                             # Turn off RED and GREEN LED simultaneously
                            GPIO.output(GREEN1,1)
                elif val=="Y":
                    GPIO.output(RED1,0)                                             # Turn on RED and GREEN LED simultaneously
                    GPIO.output(GREEN1,0)
                    sleep(2)
                    GPIO.output(RED1,1)                                             # Turn off RED and GREEN LED simultaneously
                    GPIO.output(GREEN1,1)

'''########################################################################################################################
# Function name: AH3_Supply()
# Input:         Dh, DServ1, Dserv2, DTR
# Output:        Supply requirement of  AH3
# Logic:         If input is AH, it print the output for AH0 i.e. service 1, service 2, and Trash removal for AH3
# Example call:  AH3_Supply()
###########################################################################################################################'''

def AH3_Supply():
    #print("\n")
    #print("Supply to AH3")
    #print("\n"+str(DServ1)+"   "+str(DServ2)+"   "+str(DTR))
    m=0
    read=0
    val=0
    while(m<=3):
        #print(m)
        while read==0:
            s.flush()
            read=s.readline()
            val = str(read).strip("b'").strip("\\r\\n")
            #print(val)
        if(val=="P"):
            s.write(b"D")
            m=m+1
            s.flush()
        if(val=="Q"):
            s.write('b'+DServ2)
            m=m+1
            s.flush()
        if(val=="R"):
            s.write('b'+DServ1)
            m=m+1
            s.flush()
        if(val=="S"):
            s.write('b'+DTR)
            m=m+1
            s.flush()
        read=0
        val=0
    
        if (DTR=="T"):
            while read==0:
                s.flush()
                read=s.readline()
                val = str(read).strip("b'").strip("\\r\\n")
                #print(val)
                if val=="C":
                    supply_detection()
                    if Trash_Check=="Yes":
                        s.write(b"Y")
                        s.flush()
                    else:
                        s.write(b"N")
                        s.flush()
                        read=0
                        val=0
                        while read==0:
                            s.flush()
                            read=s.readline()
                            val = str(read).strip("b'").strip("\\r\\n")
                            #print(val)
                        if val=="Y":
                            GPIO.output(RED1,0)                                             # Turn on RED and GREEN LED simultaneously
                            GPIO.output(GREEN1,0)
                            sleep(2)
                            GPIO.output(RED1,1)                                             # Turn off RED and GREEN LED simultaneously
                            GPIO.output(GREEN1,1)
                elif val=="Y":
                    GPIO.output(RED1,0)                                             # Turn on RED and GREEN LED simultaneously
                    GPIO.output(GREEN1,0)
                    sleep(2)
                    GPIO.output(RED1,1)                                             # Turn off RED and GREEN LED simultaneously
                    GPIO.output(GREEN1,1)
                

'''#######################################################################################################################
# Function name: Aruco_scan()
# Input:         Image from picamera
# Output:        Detected ID of ArUco
# Logic:         ID of ArUco is scanned with the help of Picam
# Example call:  Aruco_scan()
##########################################################################################################################'''

def Aruco_scan():
    global old
    global sim
    '''######                     Detect ArUco Id                     ####################################################
    ######################################################################################################################
    # Function name: detect_Aruco()
    # Input:         image
    # Output:        detected ID
    # Logic:         scan ArUco and detect ID with help of ArUco library
    # Example call:  detect_Aruco(img)
    ######################################################################################################################'''
    
    def detect_Aruco(image):               
        img=image
        aruco_list = {}
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_7X7_250)
        parameters = aruco.DetectorParameters_create()  
        _, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters = parameters)
        return ids
    '''###################################################################################################################
    # Function name: bit_manipulation()
    # Input:         key, sim   
    # Output:        AH,Serv2,Serv1,TR,QAH
    # Logic:         Multiplying with 10000000 i.e 128(decimal) gives that is any AH is QAH in this way bit manipulation is done
    # Example call:  bit_manipulation(25, 1)
    ######################################################################################################################'''
    
    def bit_manipulation(key,sim):
       #print(sim)
        Chk_QAH= key & 128
        AH_No=key & 96
        Chk_S2= key & 24
        Chk_S1= key & 6
        Chk_Tr= key & 1
        #print(Chk_QAH)

    
        if Chk_QAH==128:
            QAH=("QAH")
        else:
            QAH=0
        if AH_No==0:
            AH=("AH0")
        elif AH_No==32:
            AH=("AH1")
        elif AH_No==64:
            AH=("AH2")
        else:
            AH=("AH3")

            
        if Chk_S1==0:
            Serv1=("N")
        elif Chk_S1==2:
            Serv1=("H")
        elif Chk_S1==4:
            Serv1=("L")
        else:
            Serv1=("W")
        if Chk_S2==0:
            Serv2=("N")
        elif Chk_S2==8:
            Serv2=("H")
        elif Chk_S2==16:
            Serv2=("L")
        else:
            Serv2=("W")
        if Chk_Tr==1:
            TR=("T")
        else:
            TR=("t")   
        return AH,Serv2,Serv1,TR,QAH
        
    '''###########################################################################################################################
    # Function name: Store_Data()
    # Input:         AH,Serv2,Serv1,TR,QAH
    # Output:        Ah,AServ1,AServ2,ATR or Bh,BServ1,BServ2,BTR or Ch,CServ1,CServ2,CTR or Dh,DServ1,DServ2,DTR
    # Logic:         Compare given data with data from Aruco code and decide QAH, RAH and their service requirement 
    # Example call:  Store_Data(AH,Serv2,Serv1,TR,QAH)
    ##############################################################################################################################'''
    
    def Store_Data(AH,Serv2,Serv1,TR,QAH):
        if AH=="AH0":                                                                                                              
            global Ah                                                                                                              # Variable to store is AH0 is QAH or not                                                                                                               
            global AServ1                                                                                                          # Varible to store service 1 of AH0
            global AServ2                                                                                                          # Varible to store service 2 of AH0 
            global ATR                                                                                                             # Varible to store trash removal of AH0 
            if QAH:
                Ah=QAH                                                                                                             #  AH0 is  QAH
            else:
                Ah=0
            AServ1=Serv1
            AServ2=Serv2
            ATR=TR
            return Ah,AServ1,AServ2,ATR
        elif AH=="AH1":
            global Bh                                                                                                              # Variable to store is AH1 is QAH or not
            global BServ1                                                                                                          # Varible to store service 1 of AH1
            global BServ2                                                                                                          # Varible to store service 2 of AH1
            global BTR                                                                                                             # Varible to store trash removal of AH1
            if QAH:
                Bh=QAH                                                                                                             #  AH1 is QAH
            else:
                Bh=0
            BServ1=Serv1
            BServ2=Serv2
            BTR=TR
            return Bh,BServ1,BServ2,BTR
        elif AH=="AH2":
            global Ch                                                                                                              # Variable to store is AH2 is QAH or not
            global CServ1                                                                                                          # Varible to store service 1 of AH2
            global CServ2                                                                                                          # Varible to store service 2 of AH2
            global CTR                                                                                                             # Varible to store trash removal of AH2
            if QAH:
                Ch=QAH                                                                                                             #  AH2 is QAH
            else:
                Ch=0
            CServ1=Serv1
            CServ2=Serv2
            CTR=TR
            return Ch,CServ1,CServ2,CTR
        elif AH=="AH3":
            global Dh                                                                                                               # Variable to store is AH3 is QAH or not
            global DServ1                                                                                                           # Varible to store service 1 of AH3
            global DServ2                                                                                                           # Varible to store service 2 of AH3
            global DTR                                                                                                              # Varible to store trash removal of AH3
            if QAH:
                Dh=QAH                                                                                                              #  AH3 is QAH
            else:
                Dh=0
            DServ1=Serv1
            DServ2=Serv2
            DTR=TR
            return Dh,DServ1,DServ2,DTR

   

    ##### Initialize PiCamera and set resolution and framerate
    camera = PiCamera()            
    camera.resolution = (640, 480)
    camera.framerate = 8
    rawCapture = PiRGBArray(camera, size=(640, 480))
 
   
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):                                         # Function to take continuous frames from picam
        image = frame.array                                                                                                        # Array to store continuous frames
        cv2.imshow("Frame", image)                                                                                                 # Window to show frames 
        rawCapture.truncate(0)                                                                                                     
        ids=detect_Aruco(image)                                                                                                    # Function called to detect ids of ArUco
        if ids!=old:                                                                                                               ####not printing same detected ArUco Id
            if ids:
                for k in range (len(ids)):
                    temp_1 = ids[k]
                    key = temp_1[0]
                    print ("ID Detected:"+str(key))                                                                                # print ID detected along its decimal value
                    old = ids
                    AH, Serv2, Serv1,TR, QAH = bit_manipulation(key,sim)                                                           # Function call to bit manipulation of ID detected
                    sim +=1                                                                                                        # Variable to count no sim detected
                    Store_Data(AH, Serv2,Serv1,TR,QAH)                                                                             # Store data after bit manipulation
        if cv2.waitKey(1) & 0xFF == ord(' '):
             break                   
        if sim ==4:                                                                                                                # If sim no excced 4 then close camera
            camera.close()
            break
'''###############################################################################################################################
# Function name: supply_detection()
# Input:         frame from picamera
# Output:        Detected supply
# Logic:         Supply detection is done with the help of color identification
# Example call:  supply_detection()
##################################################################################################################################'''
          
def supply_detection():
    '''#########         Function to detect the color of block or supply     #####################################################
    ##############################################################################################################################
    # Function name: color_detection()
    # Input:         Frames from picamera
    # Output:        Detected supply    
    # Logic:         Supply detection is done with the help of color identification
    # Example call:  color_detection()
    ##############################################################################################################################'''
    def color_detection(frame):
        global Trash_Check
        img = frame.array                                                                                                           # Array to store continuous frame
        hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)                                                                                     # Convert BGR to HSV for color detection
        mask0=cv2.inRange(hsv,np.array([170,150,50]),np.array([180,255,255]))                                                       # HSV range for Red color
        mask1=cv2.inRange(hsv,np.array([95,100,50]),np.array([140,255,255]))                                                        # HSV range for Blue color
        mask2=cv2.inRange(hsv,np.array([60,150,30]),np.array([80,255,255]))                                                         # HSV range for Green color
        mask3=cv2.inRange(hsv,np.array([20,150,70]),np.array([35,255,255]))                                                         # HSV range for Yellow color
        
        if (mask0.any()!=0):                                                                                                        # Check for Red Color
            res2   = cv2.bitwise_and(img, img, mask= mask0)                                                                         # Mask everything except Red Block
            #print ('Red block')
            GPIO.output(RED1,0)                                                                                                     # Turn on RED LED
            sleep(1)                                                                                                                # delay for 1 sec
            GPIO.output(RED1,1)                                                                                                     # Turn off RED LED
            C.extend(str('H'))
            

        elif (mask1.any()!=0):                                                                                                      # Check for Blue Color
            res1   = cv2.bitwise_and(img, img, mask= mask1)                                                                         # Mask everything except Blue Block
            #print ('Blue block')
            GPIO.output(BLUE1,0)                                                                                                    # Turn on BLUE LED
            sleep(1)                                                                                                                # delay for 1 sec
            GPIO.output(BLUE1,1)                                                                                                    # Turn off BLUE LED
            C.extend(str('W'))
    
            
            
        elif (mask2.any()!=0):                                                                                                      # Check for Green Color     
            res   = cv2.bitwise_and(img, img, mask= mask2)                                                                          # Mask everything except Green Block
            #print ('Green block')
            GPIO.output(GREEN1,0)                                                                                                   # Turn on GREEN LED
            sleep(1)                                                                                                                # delay for 1 sec
            GPIO.output(GREEN1,1)                                                                                                   # Turn off GREEN LED
            C.extend(str('L'))
            
            
        elif(mask3.any()!=0):                                                                                                       # Check for Yellow Color
            res3   = cv2.bitwise_and(img, img, mask= mask3)                                                                         # Mask everything except Yellow Block
            #print('Yellow block')
            GPIO.output(RED1,0)                                                                                                     # Turn on RED and GREEN LED simultaneously
            GPIO.output(GREEN1,0)
            sleep(2)
            GPIO.output(RED1,1)                                                                                                     # Turn off RED and GREEN LED simultaneously
            GPIO.output(GREEN1,1)
            Trash_Check="Yes"
    
            
        
        #else:
            #print ('None color found')
    

        
    #### Instructions for camera initilization and  to take continuous from picamera ######
    camera = PiCamera()
    camera.resolution = (640, 480)  
    camera.framerate = 32
    rawCapture = PiRGBArray (camera, size=(640, 480))
    sleep(2)
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port= True):
            image = frame.array
            rawCapture.truncate(0)
            if cv2.waitKey(1) & 0xFF == ord(' '):
             break
            n=+1
            color_detection(frame)                                                                                   # Function call to color detection for detection of supply block
            if n==1:
                camera.close()                                                                                                   # function to close the camera
            return 



'''############################################################################################################################
# Function name: Supply_scan()
# Input:         
# Output:
# Logic:
# Example call:
###############################################################################################################################'''

def Supply_scan():
    global m
    read=0
    val=0
    while(m<=5):
        print(m)
        while read==0:
            s.flush()
            read=s.readline()
            val = str(read).strip("b'").strip("\\r\\n")
            #print(val)
        if(val=="C"):
            supply_detection()
            s.write(b"O")
            m=m+1
            s.flush()   
        read=0
        val=0
    return C
def Send_supply(C):
    read=0
    val=0
    while read==0:
        s.flush()
        read=s.readline()
        val = str(read).strip("b'").strip("\\r\\n")
    if(val=="S"):
        m=0
        while (m<=5):
            s.flush()
            s.write('b'+C[m])
            sleep(1)
            m=m+1
if __name__ == "__main__":
    s.write(b"S")
    C=Supply_scan()
    Send_suply(C)
    #print(C)  
    Aruco_scan()
    Supply()
