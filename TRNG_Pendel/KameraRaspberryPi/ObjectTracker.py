import cv2
import math
import struct
import time

# Set up video capture from default camera
cap = cv2.VideoCapture(0)

# Define lower and upper bounds of black color in HSV color space
lower_black = (0, 0, 0)
upper_black = (255,255,80)
x_middle = 1169
y_middle = 514
# Set minimum area for contour detection
min_contour_area = 75

distanz = []
winkel = []
timestamp = []
def coords():
	n = 0
	for x in distanz:
		with open('distanz.csv', 'a') as f:
				f.write(str(timestamp[n]) + ", " + str(x) + "\n")
		n += 1
	
	n = 0
	for i in winkel:
		with open('winkel.csv', 'a') as f:
				f.write(str(timestamp[n]) + ", " + str(i) + "\n")
		n += 1 

def bin():
	for x in winkel:
		binary_str = ''.join(format(c, '08b') for c in struct.pack('!f', x))
		if len(binary_str) > 8:
			lsb = binary_str[-1]
			print(str(lsb))

			with open('bin.txt', 'a') as f:
				f.write(lsb)

while True:
    # Read frame from camera
    ret, frame = cap.read()
    
    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create a mask for black pixels
    mask = cv2.inRange(hsv, lower_black, upper_black)
    
    # Find contours in the mask
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw a circle around each big black object and track its position
    for contour in contours:
        # Compute the area of the contour
        area = cv2.contourArea(contour)
        
        # Only consider contours that meet the minimum area threshold
        if area >= min_contour_area:
            # Compute the center and radius of the contour
            (x, y), radius = cv2.minEnclosingCircle(contour)
            timestamp.append(time.time())
            center = (float(x), float(y))
            radius = int(radius)
              # Draw a circle around the contour
            cv2.circle(frame, (int(x), int(y)), radius, (0, 255, 0), 2)
            
            # Print the position of the center
            print("Black object position: ({}, {})".format(center[0], center[1]))
            dx = x_middle - float(x)
            dy = y_middle - float(y)
            abstand = math.sqrt(dx**2 + dy**2)
            distanz.append(abstand)
            x = math.acos(dx/abstand)
            winkel.append(x)
           
     
    
    # Display the frame
    cv2.imshow("Frame", frame)
    
    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

bin()
coords()
cap.release()
cv2.destroyAllWindows()
