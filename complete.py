import sys
import time
import RPi.GPIO as GPIO
import cv2
from numpy import *
import math

GPIO.setmode(GPIO.BCM)
StepPins = [17,22,23,24]
pwmPin = 18


GPIO.setup(pwmPin, GPIO.OUT)
pwm = GPIO.PWM(pwmPin, 12.5)

 
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)
 
if vc.isOpened(): 
    opened, frame = vc.read()
 
else:
    opened = 0
    print "failed to open webcam"
 

for pin in StepPins:
  print "Setup pins"
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)


def steptake(StepCounter,Seq,StepPins):
  	#print StepCounter,
  	#print Seq[StepCounter]
 
  	for pin in range(0,4):
    		xpin=StepPins[pin]# Get GPIO
    		if Seq[StepCounter][pin]!=0:
      			#print " Enable GPIO %i" %(xpin)
      			GPIO.output(xpin, True)
    		else:
      			GPIO.output(xpin, False)
 	StepCounter += StepDir

  	time.sleep(WaitTime)

def picdist():
	opened, frame = vc.read()

	num = (frame[...,...,2] > 236)

            #print num
	xy_val =  num.nonzero()
 
	y_val = math.floor(median(xy_val[0]))
	x_val = math.floor(median(xy_val[1]))

	if math.isnan(x_val):
    		x_val=320
	if math.isnan(y_val):
        	y_val=240
	print x_val,y_val
	dist = abs(x_val - 320) 
 
	theta =0.0011450*dist + 0.0154
	tan_theta = math.tan(theta)
	cv2.circle(frame, (int(x_val),int(y_val)), 3,(0,255,0),-1)
	if tan_theta > 0: 
		obj_dist =  int(5.33 / tan_theta)
        	print obj_dist



pwm.start(1)

Seq = [[1,0,0,1],
       [1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1]]
        
StepCount = 8
StepDir = 1 

if len(sys.argv)>1:
  WaitTime = int(sys.argv[1])/float(1000)
else:
  WaitTime = 10/float(1000)
 
StepCounter=0

picdist()
for i in range(1024):
	steptake(StepCounter%8,Seq,StepPins)
	StepCounter=StepCounter+1
pwm.ChangeDutyCycle(2)

picdist()
for i in range(1024):
	steptake(StepCounter%8,Seq,StepPins)
	StepCounter=StepCounter+1
picdist()
GPIO.cleanup()


 

