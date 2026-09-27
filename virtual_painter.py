import cv2
import numpy as np
import mediapipe as mp
import os
import time
import hand_tracking_module as htm
folderPath="virtualpainter"
myList=os.listdir(folderPath)
print(myList)
overlayList=[]
for imPath in myList:
    image=cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))
header=overlayList[0]
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,1250)
t=(255,0,255)
xp,yp=0,0
imgCanvas=np.zeros((480,640,3),np.uint8)
while True:
    #import image
    
    ret,frame=cap.read()
    detector=htm.handDetector()
    if ret:
        img=cv2.flip(frame,1)
        img=detector.findHands(img)
        #find hand landmarks
        lmList=detector.findPos(img,draw=False)
        if len(lmList)!=0:
            
            #print(lmList)
            x1,y1=lmList[8][1:]
            x2,y2=lmList[12][1:]
            #check which fingers are up
            fingers=detector.fingersup()
            #print(fingers)
            #If selection mode-Two fingers are up
            
            if fingers[1] and fingers[2]:
                xp,yp=0,0
                cv2.rectangle(img,(x1,y1-25),(x2,y2+25),t,cv2.FILLED)
                #print("Selection Mode")
                if y1<60:
                    if 0<x1<60:
                        header=overlayList[0]
                        t=(89,222,255)
                        #cv2.rectangle(img,(x1,y1-25),(x2,y2+25),,cv2.FILLED)
                    elif 65<x1<126:
                        header=overlayList[1]
                        t=(49,49,255)
                    elif 131<x1<192:
                        header=overlayList[2]
                        t=(173,0,24)
                    elif 194<x1<255:
                        header=overlayList[3]
                        t=(199,191,0)
                    elif 257<x1<317:
                        header=overlayList[4]
                        t=(204,54,104)
                    elif 320<x1<380:
                        header=overlayList[5]
                        t=(177,52,255)
                    elif 381<x1<441:
                        header=overlayList[6]
                        t=(0,0,0)
                    elif 443<x1<503:
                        header=overlayList[7]
                        t=(255,255,255)
                    elif 510<x1<640:
                        header=overlayList[8]
                        t=(0,0,0)
                        
                    
                    
                cv2.rectangle(img,(x1,y1-25),(x2,y2+25),t,cv2.FILLED)
            #5. if drawing mod -index finger is up
            
            if fingers[1] and fingers[2]==False:
                
                cv2.circle(img,(x1,y1),15,t,cv2.FILLED)
                if xp==0 and yp==0:
                    xp,yp=x1,y1
                if t==(0,0,0):
                    cv2.line(img,(xp,yp),(x1,y1),t,17)
                    cv2.line(imgCanvas,(xp,yp),(x1,y1),t,17)
                else:
                    cv2.line(img,(xp,yp),(x1,y1),t,9)
                    cv2.line(imgCanvas,(xp,yp),(x1,y1),t,9)
                    
                xp,yp=x1,y1
                #print("Drawing mode")
        imgGray=cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
        _,imgInv=cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
        imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
        img=cv2.bitwise_and(img,imgInv)
        img=cv2.bitwise_or(img,imgCanvas)
                
        img[0:60,0:640]=header
        #a,b,c=img.shape
        #d,e,f=imgCanvas.shape
        #print(a,d,b,e)
        #img=cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
        cv2.imshow('imge',img)
        #cv2.imshow('canvas',imgCanvas)
        if cv2.waitKey(1) &0xFF==ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
