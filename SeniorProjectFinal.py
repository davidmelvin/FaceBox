from Tkinter import *
from facepy import GraphAPI #Run pi as root to install
import time
import picamera
import RPi.GPIO as GPIO
from datetime import datetime
from PIL import ImageTk, Image

graph = GraphAPI("CAAK26MZAg81YBAOZAnYQozDy9j4kqCIsY9ecgrAEUSN9ElUeuB0ZAZBWNo7n9Kjk346eXsYOjMFBLKIZBmUTYAOSMPkcxZAijYd2owIv8U2gm1ZBRHU1mFR0gnSGVT6SYSwTZBzZAY2GgxyWDP11lSevVnAp1OZCismRTo4cvQb0s9zzKTmbNULYPIHteJChZAuZCtGDX1WjZA51ZCjKI0DSSUEgoZBZBxn0TYPTNl8ZD") 

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN) #SHUTTER BUTTON
GPIO.setup(18,GPIO.IN) #UPLOAD BUTTON
GPIO.setup(22, GPIO.OUT) #RED LED, ALWAYS ON
GPIO.setup(23, GPIO.OUT) #BLUE LED, ON WHEN PICTURE DISPLAYED

GPIO.output(22,True)
GPIO.output(23,False)

root = Tk()
canvas = Canvas(root, width=790, height=480)
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
      print "Shutter button pressed"
      print "Taking photo in three seconds"
      camera.resolution = (750,450)
      camera.start_preview()
      time.sleep(5)
      camera.stop_preview()
      camera.capture('FaceBox_Pic.gif')
      break

  print "Waiting for upload button press"
  print "displaying photo with Tkinter"

  canvas.delete("all")
  canvas.create_text(375, 10, text="Press upload to post this picture:", font="Arial 12")

#  img = Image.open("FaceBox_Pic.jpg")
# photoImg = ImageTk.PhotoImage(img)
  
  #displayPic = Label(root, image=img)
  #displayPic.image = photo # keep a reference!
  #displayPic.pack()
  
  #photo = PhotoImage(file = "girl")
  #canvas.create_image(390, 240, image = photo)
  canvas.update()
  GPIO.output(23,True)
  #if the last reading was low and this one high, print

  #for x in range (0,1000):
    #Tkinter display

  t1 = datetime.now()
  while True:
    input = GPIO.input(18)
    if (input==1):
     print "Uploading picture.."
     graph.post(
       path = '1583747018566887/photos',
       source = open("Rubber",'rb')
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
