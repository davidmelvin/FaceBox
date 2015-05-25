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

def stroke_text(x, y, text, size, textcolor, strokecolor):
    # make stroke text
    canvas.create_text(x, y, text=text, font=('Arial', size, 'bold'), fill=strokecolor)
    # make regular text
    canvas.create_text(x, y, text=text, font=('Arial', size), fill=textcolor)


def showInstructions():
  stroke_text(350, 30, "Welcome to FaceBox!",  20, "white", "black")
  canvas.create_text(15, 70, text="Instructions:", font="Arial 18", fill="#8b9dc3", anchor="w")

  canvas.create_text(35, 110, text = "1. Press the red shutter button.\n. Your picture will be picture will be taken after 3 seconds.'\n3. After the picture is taken you will be able to view it.\n4. Press the confirm button to upload the image to Facebook.\n5. Press nothing for 10 seconds to cancel the upload.",  font="Arial 16", fill="#dfe3ee", anchor="w")
  #canvas.create_text(35, 110, text="1. Press the red shutter button.", fill="#dfe3ee", font="Arial 16", anchor="w")
  #canvas.create_text(35, 150, text="2. Your picture will be picture will be taken after 10 seconds.", font="Arial 16", fil="#dfe3ee", anchor="w")
  #canvas.create_text(35, 190, text="3. After the picture is taken you will be able to view it.", font="Arial 16", fill="#dfe3ee", anchor="w")
  #canvas.create_text(35, 230, text="4. Press the confirm button to upload the image to Facebook.", font="Arial 16", fill="#dfe3ee", anchor="w")

  stroke_text(350, 350, "Press the RED shutter button now to take a picture!", 20, "white", "black")

def checkButton():
  showInstructions()
  canvas.update()
  while True:
    shutter_input = GPIO.input(17)
    if (shutter_input==1):
      canvas.delete("all")
      GPIO.output(22,False) #Turn Shutter Button LED off during upload/confirm phase
      print "Shutter button pressed, taking photo in three seconds"
      
      canvas.create_text(375, 10, text="Here is a preview of your picture:", font="Arial 12")
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

  canvas.create_text(375, 10, text="Press the blue button to post this picture:", font="Arial 12", fill = "white")

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
     
    t2 = datetime.now()
    delta = t2 - t1
    if (delta.seconds > 10):
      print "Upload not pressed within 10 seconds.. breaking now."
      break
  
  canvas.delete("all")
  showInstructions()
  GPIO.output(23,False)

  root.after(50,checkButton)

root.after(50, checkButton)
root.mainloop()