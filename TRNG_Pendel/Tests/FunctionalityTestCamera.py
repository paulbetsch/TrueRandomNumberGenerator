import cv2
import logging
import os
import subprocess
from PIL import Image

# This method checks the functionality of the Raspberry Pi Camera Module
def CheckCameraFunctionality():
    try:
        # Create tmp directory for testing picture and video
        os.mkdir('tmp')

        # Determines if the camera is connected and working correctly
        functional = False
        # Amount of all tests
        amountOfTests = 1
        # Determines the amount of tests passed
        passedTest = 0

        # Execute the 'vcgencmd get_camera' command to ensure the interface is enabled and a camera is detected
        checkInterface = subprocess.run(['vcgencmd', 'get_camera'], stdout=subprocess.PIPE)
        output = checkInterface.stdout.decode('utf-8')

        # Check if there is one camera module detected
        if(output.__contains__('detected=1')):
            passedTest += 1

        #print('Passed: ' + str(passedTest) + ' out of ' + str(amountOfTests))

#         cap = cv2.VideoCapture('tmp/test.h264')
#         
#         cap.release()
# 
#         # Check if the video is not all black
#         if(os.path.isfile('tmp/test.264')):
#             passedTest += 1
#         
#         print('Passed: ' + str(passedTest) + ' out of ' + str(amountOfTests))

        # remove test data and set functional true if all tests are passed
        if(passedTest == amountOfTests):
            os.rmdir('tmp')
            functional = True
    except:
        logging.debug('Passed: ' + str(passedTest) + ' out of ' + str(amountOfTests))
        return False
    return functional


#print(CheckFunctionality())