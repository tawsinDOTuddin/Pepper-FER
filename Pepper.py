# This test demonstrates how to use the ALPhotoCapture module.
# Note that you might not have this module depending on your distribution
import os
import sys
import time

import paramiko as paramiko
from naoqi import ALProxy

import qi

#where should I write the files for my application "myapp"?

#dataPath = qi.path.userWritableDataPath("myapp", "mydatafile")
#datapath => /home/nao/.local/share/myapp/mydatafile
#confPath = qi.path.userWritableConfPath("myapp", "myconffile")
# confPath => /home/nao/.config/myapp/myconffile

# Replace this with your robot's IP address
IP = "192.168.137.145"
PORT = 9559

# Create a proxy to ALPhotoCapture
try:
  photoCaptureProxy = ALProxy("ALPhotoCapture", IP, PORT)
  faceProxy = ALProxy("ALFaceDetection", IP, PORT)

  period = 500
  faceProxy.subscribe("Test_Face", period, 0.0)
  # Create a proxy to ALMemory
  memoryProxy = ALProxy("ALMemory", IP, PORT)

  tts = ALProxy("ALTextToSpeech", IP, PORT)
  tts.setParameter("speed", 200)
  tts.resetSpeed()
  tts.say("Look at me. Let me take your picture")

  photoCaptureProxy.setResolution(2)
  photoCaptureProxy.setPictureFormat("jpg")
  photoCaptureProxy.takePictures(15, '/home/nao/recordings/cameras/', "image")
except Exception, e:
  print "Error when creating ALPhotoCapture proxy:"
  print str(e)
  exit(1)

# Take 3 pictures in VGA and store them in /home/nao/recordings/cameras/



# This call returns ['/home/nao/recordings/cameras/image_0.jpg', '/home/nao/recordings/cameras/image_1.jpg', '/home/nao/recordings/cameras/image_2.jpg']
image_path =  'D:\\face\\'
local_path = '/home/nao/recordings/cameras/'
t = paramiko.Transport(IP, PORT)
t.connect(username="nao", password="edutech123")
sftp = paramiko.SFTPClient.from_transport(t)
files = sftp.listdir(local_path)
for f in files:
  print ('')
  print ('##############################################')
#print ('Beginning to download file from %s %s' %
#       ("130.232.164.94", datetime.datetime.now()))
  print ('Downloading file:', os.path.join(image_path, f))
  sftp.get(os.path.join(local_path, f),os.path.join(image_path, f))
#print ('Download file success %s' % datetime.datetime.now())
#print ('')
  print ('##############################################')
t.close()

tts = ALProxy("ALTextToSpeech", IP, PORT)
tts.setParameter("speed", 200)
tts.resetSpeed()
tts.say("Thanks. Pictures are taken!")

#pscp.exe nao@192.168.137.181:/home/nao/recordings/cameras/image_0.jpg d:\face\
