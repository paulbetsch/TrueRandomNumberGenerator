import os
import time
import picamera

with picamera.PiCamera() as camera:
	camera.resolution = (1920, 1080)
	camera.framerate = 30
	camera.shutter_speed = 10000
	time.sleep(2)
	for i in range(100):
		print("Picture: " + i )
		camera.capture("PiPictures/Image" + str(i) + ".jpg")
		
# Close the camera
camera.close()
