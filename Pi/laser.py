#code by Shane Ormonde
import cv2
from numpy import *
import math

loop = 1
dot_dist = 0
 
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)
 
if vc.isOpened(): 
    opened, frame = vc.read()
 
else:
    opened = 0
    print "failed to open webcam"
 
if opened == 1 :
    while loop == 1:
            opened, frame = vc.read()
            key = cv2.waitKey(20)
            if key == 27:
                loop = 0
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
 
            theta =0.000350*dist + 0.007
            tan_theta = math.tan(theta)
            cv2.circle(frame, (int(x_val),int(y_val)), 3,(0,255,0),-1)
            if tan_theta > 0: 
            	obj_dist =  int(5.33 / tan_theta)
            	print obj_dist
            cv2.imshow("preview", frame)
            
elif opened == 0:
        print " webcam error "
