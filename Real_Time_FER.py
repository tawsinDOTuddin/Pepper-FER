import numpy as np
import cv2
from keras.preprocessing import image
import time
import sys
sys.stdout = open('output.txt','w')

#-----------------------------
#opencv initialization

face_cascade = cv2.CascadeClassifier('C:\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml')
'''faceDet = cv2.CascadeClassifier("C:\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml")
faceDet_two = cv2.CascadeClassifier("C:\opencv\sources\data\haarcascades\haarcascade_frontalface_alt2.xml")
faceDet_three = cv2.CascadeClassifier("C:\opencv\sources\data\haarcascades\haarcascade_frontalface_alt.xml")
faceDet_four = cv2.CascadeClassifier("C:\opencv\sources\data\haarcascades\haarcascade_frontalface_alt_tree.xml")
'''#-----------------------------
#face expression recognizer initialization
from keras.models import model_from_json
model = model_from_json(open("emoji_10_Emotion.json", "r").read())
model.load_weights('emoji_10_Emotion.h5') #load weights
#-----------------------------
device = torch.device("cuda")
model.to(device)
emotions = ('Angry', 'Disgust', 'Fear', 'Happy','Mockery', 'Neutral', 'Sad', 'Surprise','Think','Wink')

# #process videos
#cap = cv2.VideoCapture(0) #process real time web-cam
cap = cv2.VideoCapture('Pepper_Video_from_Image_Frames.mp4')

frame = 0

sec = 0
frameRate = 0.5 #//it will capture image in each 0.5 second
count=1
   
while(True):
    cap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    ret, img = cap.read()
    count = count + 1
    sec = sec + frameRate
    sec = round(sec, 2) 
    
    
    
    #img = cv2.resize(img, (640, 360))
    #img = img[0:308,:]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    #face_one = faceDet.detectMultiScale(gray, scaleFactor=1.4, minNeighbors=5)
    #face_two = faceDet_two.detectMultiScale(gray, scaleFactor=1.4, minNeighbors=5)
    #face_three = faceDet_three.detectMultiScale(gray, scaleFactor=1.4, minNeighbors=5)
    #face_four = faceDet_four.detectMultiScale(gray, scaleFactor=1.4, minNeighbors=5)
    #Go over detected faces, stop at first detected face, return empty if no face.
    '''if len(face_one) == 1:
        faces = face_one
    elif len(face_two) == 1:
        faces = face_two
    elif len(face_three) == 1:
        faces = face_three
    elif len(face_four) == 1:
        faces = face_four
    else:
        faces = ""
'''
    for (x,y,w,h) in faces:
		 #trick: ignore small faces
         cv2.rectangle(img,(x,y),(x+w,y+h),(109, 224, 33),2) #highlight detected face
			
         detected_face = img[int(y):int(y+h), int(x):int(x+w)] #crop detected face
         detected_face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY) #transform to gray scale
         detected_face = cv2.resize(detected_face, (48, 48)) #resize to 48x48
			
         img_pixels = image.img_to_array(detected_face)
         img_pixels = np.expand_dims(img_pixels, axis = 0)
			
         img_pixels /= 255 #pixels are in scale of [0, 255]. normalize all pixels in scale of [0, 1]
			
		
			
			#background of expression list
         overlay = img.copy()
         opacity = 0.4
         cv2.rectangle(img,(x+w+10,y-25),(x+w+150,y+200),(255,0,0),cv2.FILLED)
         cv2.addWeighted(overlay, opacity, img, 1 - opacity, 0, img)
			
			#connect face and expressions
         cv2.line(img,(int((x+x+w)/2),y+15),(x+w,y-20),(255,255,255),1)
         cv2.line(img,(x+w,y-20),(x+w+10,y-20),(255,255,255),1)
			
         emotion = ""
         print('{')
         for i in range(len(predictions[0])):
             #emotion = "%s %s%s" % (emotions[i], round(predictions[0][i]*100, 2), '%')
             emotion = str(round(predictions[0][i], 2))
             print(emotion)
				
					
             color = (255,255,255)
				
             cv2.putText(img, emotion, (int(x+w+15), int(y-12+i*20)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
				
			#-------------------------
         print('}')
	
    frame = frame + 1
    print(frame)
	
	#---------------------------------
	
	
	
    if cv2.waitKey(1) & 0xFF == ord('q'): #press q to quit
        break


cap.release()
cv2.destroyAllWindows()# -*- coding: utf-8 -*-

