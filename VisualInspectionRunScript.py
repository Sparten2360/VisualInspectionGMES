from math import sqrt
import tensorflow as tf
import cv2 
import time
import easyocr
import statistics as st
reader = easyocr.Reader(['en'],gpu = True) #If you do not have a nvidia gpu or the CUDA toolkit installed, set gpu to False you will get less frames but it should still run.
capList = []
currentCam = -2
for i in range(4):
    capList.append(cv2.VideoCapture(i))
    #This adds all the camera objects to a list if you want to use more cameras increase range currently the code is setup for 5.   
for i in capList:
    #This sets all the camera properties. You may want to change them to see better results. Such as exposure once the ring lights are on. 
    i.set(cv2.CAP_PROP_FRAME_WIDTH,160)
    i.set(cv2.CAP_PROP_FRAME_HEIGHT,160)
    i.set(cv2.CAP_PROP_EXPOSURE, -8) 
totalPreds =0
accuratePreds=0
footage = []
font = cv2.FONT_HERSHEY_SIMPLEX 
targetLoss = 0
'''This method will take in the results of the bounding box detection and crop the image to be only the last four digits. It will then segment the image into 
 and run the OCR on each part. If the OCR returns a digit with a probability of greater than .75, it will add it to the footage list. 
 The method will also display the segmented image and the digit that was detected.'''
def reduceToDigits(results,image,fidelity,portion):
    top_left = tuple(results[0][0][0])
    top_left1 = int(top_left[0])
    top_left2 = int(top_left[1])
    top_left = (top_left1,top_left2)
    bottom_right = tuple(results[0][0][2])
    bottom_right1 = int(bottom_right[0])
    bottom_right2 = int(bottom_right[1])
    bottom_right = (bottom_right1,bottom_right2)
    segmentedImg = image.copy()[top_left2:bottom_right2,top_left1:bottom_right1]
    segmentedImgHeight = segmentedImg.shape[0]
    segmentedImgWidth = segmentedImg.shape[1]
    print(segmentedImg.shape)
    digits = []
    for i in range(fidelity):
        print("height " +str(top_left2)+" "+ str(bottom_right2))
        digits.append(segmentedImg.copy()[0:segmentedImgHeight,i*int(portion*segmentedImgWidth/fidelity+1):segmentedImgWidth])
        for idx,i in enumerate(digits):
            digitsResult = reader.readtext(i,allowlist ='0123456789',threshold=0.5,rotation_info=[180],max_candidates=1)
            if(len(digitsResult)>0):
                print(digitsResult[0][1])
                if(digitsResult[0][2]>.75):
                    if(len(digitsResult[0][1]) == 4):
                        footage.append(int(digitsResult[0][1]))
                        print(str(digitsResult[0][1])+" with a probability of "+ str(digitsResult[0][2])+ " at the " + str(idx) + " part of the image")
                if(i.shape[0]>0 and i.shape[1]>0):
                    cv2.imshow('Digit',i)
            if(segmentedImg.shape[0]>0 and segmentedImg.shape[1]>0):
                cv2.imshow('Segmented',segmentedImg)
            cv2.rectangle(i,top_left,bottom_right,(0,255,0),3)
''' This is the main run loop anything that happens within the loop will be run until the user presses q. 
This cycle runs once each frame so optimization is key to keeping up frame rate. inside this main loop we have a if statement that checks if the camrea has a lock 
meaing the camera has detected text and now we can run the reduce to digits method on this camera. 
This optimization means we are not reducing to digits on every frame which drastically increases preformance. 
However if no camera detects text to save bandwidth on the usb bus I have it loop through each camera only increasing the resolution when we use the text detector.'''
while True:
    if(targetLoss == 0):
        currentCam = -2
    if(currentCam>-1):
        success,img = capList[currentCam].read()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        img = cv2.resize(img, (480, 480),.5,.5,interpolation = cv2.INTER_AREA)
        img  =cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        results = reader.readtext(img,allowlist ='0123456789',threshold=0.5,rotation_info=[180],min_size=200,max_candidates=1,width_ths=.125)
        if(success):
                cv2.imshow('Cam ' + str(currentCam),img)
        if(len(results)>0):
            reduceToDigits(results,img,8,.666666)
        else:
            targetLoss-=1
    else:
        for idx,i in enumerate(capList):
            i.set(cv2.CAP_PROP_FRAME_WIDTH,480)
            i.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
            success,img = i.read()
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
            img = cv2.resize(img, (480, 480),.5,.5,interpolation = cv2.INTER_AREA)
            img  =cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
            if(success):
                cv2.imshow('Cam ' + str(idx),img)
            results = reader.readtext(img,allowlist ='0123456789',threshold=0.5,rotation_info=[180],min_size=200,max_candidates=1,width_ths=.125)
            if(len(results)>0):
                currentCam = idx
                targetLoss = 10
                break
            i.set(cv2.CAP_PROP_FRAME_WIDTH,160)
            i.set(cv2.CAP_PROP_FRAME_HEIGHT,160)
    totalPreds+=1
    if(len(footage)>0):
        print(str(st.mode(footage))+ "FT with a probability of ")
        print(footage)
    if cv2.waitKey(1) == ord('q'):
        break

for i in capList:
    i.release()
cv2.destroyAllWindows()
print("Accuracy is " + str((accuratePreds/totalPreds)*100))

