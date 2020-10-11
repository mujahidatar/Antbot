import numpy as np
import cv2
import cv2.aruco as aruco
import aruco_lib
import csv

def aruco_detect(path_to_image):
    
    img = cv2.imread(path_to_image)                                                         
    id_aruco_trace = 0
    det_aruco_list = {}
    img2 = img[0:425,0:425,:]                                                               
    det_aruco_list = aruco_lib.detect_Aruco(img2,no)
    if det_aruco_list:
            img3 = aruco_lib.mark_Aruco(img2,det_aruco_list)
            id_aruco_trace, key = aruco_lib.calculate_Robot_State(img3,det_aruco_list)
            #print(key)
            return img,key


        
def color_detect(img):
    
    img=img
    c=str(input('enter color of first object'))
    s=str(input('enter shape of first object'))
    img,cx,cy=color_check(img,c,s)
    c=str(input('enter color of second object'))
    s=str(input('enter shape of second object'))
    img,cx1 ,cy1=color_check(img,c,s)
    
    return img,cx,cy,cx1,cy1
   


def color_check(img,c,s):
    contscrn=0
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    if c=='red':
        lower=np.array([0,100,20])
        upper=np.array([15,255,255])
        mask=cv2.inRange(hsv,lower,upper)
        image,contours,hierarchy=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cv2.imshow('mask',mask)
        contscrn=shape_detect(mask,s)
    elif c=='blue':
        lower=np.array([100,100,20])
        upper=np.array([140,255,255])
        mask=cv2.inRange(hsv,lower,upper)
        image,contours,hierarchy=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        contscrn=shape_detect(mask,s)
    elif c=='green':
        lower=np.array([40,100,20])
        upper=np.array([70,255,255])
        mask=cv2.inRange(hsv,lower,upper)
        image,contours,hierarchy=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        contscrn=shape_detect(mask,s)
    elif c=='yellow':
        lower=np.array([25,100,20])
        upper=np.array([35,255,255])
        mask=cv2.inRange(hsv,lower,upper)
        image,contours,hierarchy=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        contscrn=shape_detect(mask,s)
    elif c=='orange':
        lower=np.array([10,100,20])
        upper=np.array([20,255,255])
        mask=cv2.inRange(hsv,lower,upper)
        image,contours,hierarchy=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        contscrn=shape_detect(mask,s)
    else:
        print ('none color found')
       
    if c=='red':
        cnt = contscrn
        cv2.drawContours(img, [cnt], -1, (0,255,0), 25)
        M = cv2.moments(cnt)
        cx = int (M['m10']/M['m00'])
        cy = int (M['m01']/M['m00'])
        cv2.putText(img,"("+str(cx)+","+str(cy)+")", (cx,cy), font,0.6,(0),2)
        return img,cx,cy

    elif c=='blue':
        cnt = contscrn
        cv2.drawContours(img,[cnt], -1, (0,0,255), 25)
        M = cv2.moments(cnt)
        cx = int (M['m10']/M['m00'])
        cy = int (M['m01']/M['m00'])
        cv2.putText(img,"("+str(cx)+","+str(cy)+")", (cx,cy), font,0.6,(0),2)
        return img,cx,cy
        
    elif c=='green':
        cnt = contscrn
        cv2.drawContours(img, [cnt], -1, (255,0,0), 25)
        M = cv2.moments(cnt)
        cx = int (M['m10']/M['m00'])
        cy = int (M['m01']/M['m00'])
        cv2.putText(img,"("+str(cx)+","+str(cy)+")", (cx,cy), font,0.6,(0),2)
        return img,cx,cy

    elif c=='yellow':
        cnt = contscrn
        cv2.drawContours(img, [cnt], -1, (0,255,0), 25)
        M = cv2.moments(cnt)
        cx = int (M['m10']/M['m00'])
        cy = int (M['m01']/M['m00'])
        cv2.putText(img,"("+str(cx)+","+str(cy)+")", (cx,cy), font,0.6,(0),2)
        return img,cx,cy

    elif c=='orange':
        cnt = contscrn
        cv2.drawContours(img, [cnt], -1, (0,255,0), 25)
        M = cv2.moments(cnt)
        cx = int (M['m10']/M['m00'])
        cy = int (M['m01']/M['m00'])
        cv2.putText(img,"("+str(cx)+","+str(cy)+")", (cx,cy), font,0.6,(0),2)
        return img,cx,cy
    else:
        print('none shape')
        cx=0
        cy=0
        img=img
        return img,cx,cy


def shape_detect(mask,s):
    if s=='triangle':
        s=3
    elif s=='square':
        s=4
    elif s=='circle':
        s=20
    else:
        s=0
    cntscrn=0
    approx=0
    cv2.imshow('mask',mask)

    _, threshold = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)
    _, contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
     
    font = cv2.FONT_HERSHEY_COMPLEX
     
    for cnt in contours:
        if s==3 or s==4:
            approx = cv2.approxPolyDP(cnt, 0.1*cv2.arcLength(cnt, True), True)
            #print(len(approx))
            if s==3:
                if len(approx)==3 :
                    cntscrn=approx
                    return cntscrn
            elif s==4:   
                if len(approx)==4:
                    cntscrn=approx
                    print(len(approx))
                    return cntscrn
                else:
                     print('none shape')
        elif s==20:
            approx = cv2.approxPolyDP(cnt, 0.01*0.01*cv2.arcLength(cnt, True), True)
            if len(approx) >50:
                print(len(approx))
                cntscrn=approx
                return cntscrn
        else:
            print('none shape')




def csv_print(image,ID,cx,cy,cx1,cy1,no):
   # w = (r"C:\Users\Suraj Chormale\Desktop\Set11\Task 1\Task1.2\2. Code\5352_Task1.2.csv",'wb')
    csvData = ['Image Name', 'ArUco ID' , '(x y)Object-1' , '(x y)Object-2']
    data =[image,ID   ,'('+str(cx)+' '+str(cy)+')','('+str(cx1)+' '+str(cy1)+')']
    with open('5352_Task1.2.csv','a') as csvFile:
        writer = csv.writer(csvFile, delimiter=',')
        if no==1:
            writer.writerow(csvData)
            writer.writerow(data)
        else:
            writer.writerow(data)
            

if __name__ == "__main__":
    key=0
    ID=0
    cx=0
    cy=0
    cx1=0
    cy1=0
    no=int(input('enter no of image'))
    path_to_image=r"C:\Users\Suraj Chormale\Desktop\Set11\Task 1\Task1.2\3. Images\Image"+str(no)+".jpg"
    image="Image"+str(no)+".jpg"
    font=cv2.FONT_HERSHEY_COMPLEX
    img,key = aruco_detect(path_to_image)
    ID = key
    img,cx,cy,cx1,cy1 = color_detect(img)
    csv_print(image,ID,cx,cy,cx1,cy1,no)
    cv2.imshow("ColorImage",img)
    cv2.imwrite('Det_Image'+str(no)+'.jpg',img)
