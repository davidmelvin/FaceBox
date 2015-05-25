#from Tkinter import * as tk
import Tkinter as tk
from facepy import GraphAPI #Run pi as root to install
import time
import picamera
import RPi.GPIO as GPIO
from datetime import datetime
from PIL import ImageTk, Image

graph = GraphAPI("CAAK26MZAg81YBAAceN0gEgAcWyZABFqotF8gxJF7JZARAaNozp5HDPFC2iZAZBko1nE12e0mwAasNO55XopImzBbvkqSHnH54E3ZB0k2kdl7g8RfHK7S1tPXZBRhscsNbvb3mpiZCTkB04ZBGaKwGLXj4em1g8c5hg4cBmaDQFZAtjdVPjH4yKaCaCKlYtXa4pJzOoB3QNUuahCuNi9LEeikYp7xGscZCERJ5cZD") 

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN) #SHUTTER BUTTON
GPIO.setup(18,GPIO.IN) #UPLOAD BUTTON
GPIO.setup(22, GPIO.OUT) #RED LED, ALWAYS ON
GPIO.setup(23, GPIO.OUT) #BLUE LED, ON WHEN PICTURE DISPLAYED

GPIO.output(22,True)
GPIO.output(23,False)

root = tk.Tk()
canvas = tk.Canvas(root, width=790, height=480)
canvas.pack()
camera = picamera.PiCamera()

def showInstructions():
  canvas.create_text(300, 10, text="Hi! Welcome to FaceBox. Here are some instructions.", font="Arial 16")
  canvas.create_text(300, 50, text="1. To Start, press the shutter button.", font="Arial 12")
  canvas.create_text(300, 80, text="2. Your picture will be picture will be taken after 10 seconds.", font="Arial 12")
  canvas.create_text(300, 110, text="3. After the picture is taken you will be able to view it.", font="Arial 12")
  canvas.create_text(300, 140, text="4. Press the confirm button to upload the image to Facebook.", font="Arial 12")

  canvas.create_text(300, 270, text="Press the shutter button now to take a picture!", font="Arial 20")

def checkButton():
  showInstructions()
  canvas.update()
  while True:
    shutter_input = GPIO.input(17)
    if (shutter_input==1):
      GPIO.output(22,False) #Turn Shutter Button LED off during upload/confirm phase
      print "Shutter button pressed"
      print "Taking photo in three seconds"

      canvas.delete("all")

      camera.resolution = (750,450)
      camera.start_preview()
      time.sleep(5)
      camera.stop_preview()
      camera.capture('FaceBox_Pic.jpg')
      
      break

  print "Waiting for upload button press"
  print "displaying photo with Tkinter"

  imageFile = "FaceBox_Pic.jpg"
  image1 = ImageTk.PhotoImage(Image.open(imageFile))
  w = image1.width()
  h = image1.height()
   
  canvas.create_image(0,20, anchor="nw", image=image1)

  canvas.create_text(375, 10, text="Press upload to post this picture:", font="Arial 12")

  canvas.update()
  GPIO.output(23,True)
  
  t1 = datetime.now()
  while True:
    input = GPIO.input(18)
    if (input==1):
     print "Uploading picture.."
     graph.post(
       path = '1583747018566887/photos',
       source = open("FaceBox_Pic.jpg",'rb')
     )
     print "Picture uploaded!"
     break
     #tkinter stop displaying 

    t2 = datetime.now()
    delta = t2 - t1
    if (delta.seconds > 15):
      print "Upload not pressed within 10 seconds.. breaking now."
      break
  
  canvas.delete("all")
  showInstructions()
  GPIO.output(23,False)

  root.after(50,checkButton)

root.after(50, checkButton)
root.mainloop()