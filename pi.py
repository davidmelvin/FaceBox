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
canvas = tk.Canvas(root, width=790, height=480, bg="#3b5998")
canvas.pack()
camera = picamera.PiCamera()

def stroke_text(x, y, text, size, textcolor, strokecolor, anchoring):
    # make stroke text
    canvas.create_text(x+1, y+1, text=text, font=('Arial', size), fill=strokecolor, anchor=anchoring)
    # make regular text
    canvas.create_text(x, y, text=text, font=('Arial', size), fill=textcolor, anchor=anchoring)

def showInstructions():
  stroke_text(320, 40, "Welcome to FaceBox!",  22, "white", "black", "center")
  canvas.create_text(15, 100, text="Instructions:", font="Arial 18", fill="#8b9dc3", anchor="w")

  canvas.create_text(35, 150, text = "1. Press the red shutter button.\n2. Your picture will be taken after 3 seconds.\n3. After the picture is taken you will be able to view it.\n4. Press the blue confirm button to upload the image to Facebook.\n5. Press the red button to cancel the upload.",  font="Arial 16", fill="#dfe3ee", anchor="nw")

  stroke_text(15, 400, "Press the RED shutter button now to take a picture!", 20, "white", "black", "w")

def checkButton():
  showInstructions()
  canvas.update()
  while True:
    shutter_input = GPIO.input(17)
    if (shutter_input==1):
      canvas.delete("all")
      stroke_text(340, 10, "Taking picture in 5 seconds...", 12, "white", "black", "center")
      canvas.update()
      GPIO.output(22,False) #Turn Shutter Button LED off during upload/confirm phase
      print "Shutter button pressed, taking photo in three seconds"
      
      camera.resolution = (750,450)
      camera.start_preview()
      time.sleep(5)
      camera.stop_preview()
      camera.capture('FaceBox_Pic.jpg')
      canvas.delete("all")
      stroke_text(340, 240, "Loading Picture...", 24, "white", "black", "center")
      canvas.update()
      
      break
  
  
  print "Waiting for upload button press"
  print "displaying photo with Tkinter"
  
  imageFile = "FaceBox_Pic.jpg"
  image1 = ImageTk.PhotoImage(Image.open(imageFile))
  w = image1.width()
  h = image1.height()
   
  canvas.create_image(0,20, anchor="nw", image=image1)

  stroke_text(350, 10, "Press the blue button to post or red button to cancel:", 12, "white", "black", "center")

  canvas.update()
  GPIO.output(23,True)
  
  t1 = datetime.now()
  while True:
    uploadButton = GPIO.input(18)
    cancelButton = GPIO.input(17)
    if (uploadButton==1):
      canvas.delete("all")
      stroke_text(350, 10, "Uploading picture...", 12, "white", "black", "center")
     print "Uploading picture.."
     graph.post(
       path = '1583747018566887/photos',
       source = open("FaceBox_Pic.jpg",'rb')
     )
     print "Picture uploaded!"
     break
     
    t2 = datetime.now()
    delta = t2 - t1
    if (delta.seconds > 10 or cancelButton ==1):
      print "Upload not pressed within 10 seconds.. breaking now."
      break
  
  canvas.delete("all")
  showInstructions()
  GPIO.output(23,False)

  root.after(50,checkButton)

root.after(50, checkButton)
root.mainloop()