import cv2
import logging
import os
import subprocess
from PIL import Image

# This method checks the functionality of the Raspberry Pi Camera Module
def CheckCameraFunctionality():
    try:
        # Execute the 'vcgencmd get_camera' command to ensure the interface is enabled and a camera is detected
        checkInterface = subprocess.run(['vcgencmd', 'get_camera'], stdout=subprocess.PIPE)
        output = checkInterface.stdout.decode('utf-8')

        # Check if there is one camera module detected
        if(output.__contains__('detected=1')):
            return True
        return False
    except:
        logging.error('No Camera connected')
        return False
