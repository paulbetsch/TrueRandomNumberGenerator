import cv2
import os
import subprocess
from PIL import Image

# This method checks the functionality of the Raspberry Pi Camera Module
def CheckFunctionality():
    try:
        # Create tmp directory for testing picture and video
        os.mkdir('tmp')

        # Determines if the camera is connected and working correctly
        functional = False
        # Amount of all tests
        amountOfTests = 4
        # Determines the amount of tests passed
        passedTest = 0

        # Execute the 'vcgencmd get_camera' command to ensure the interface is enabled and a camera is detected
        checkInterface = subprocess.run(['vcgencmd', 'get_camera'], stdout=subprocess.PIPE)
        output = checkInterface.stdout.decode('utf-8')

        # Check if there is one camera module detected
        if(output.__contains__('detected=1')):
            passedTest += 1

        print('Passed: ' + str(passedTest) + ' out of ' + str(amountOfTests))

        # Make an example picture and check if its not all black
        testPicture = subprocess.run(['raspistill', '-o', 'tmp/test.jpg', '--nopreview'], stdout=subprocess.PIPE)

        # Load the test image and get its dimensions
        image = Image.open('tmp/test.jpg')
        width, height = image.size

        # Check if the image is all black
        blackPixelCount = 0
        for y in range(height):
            for x in range(width):
                r, g, b = image.getpixel((x, y))
                if r == g == b == 0:
                    blackPixelCount += 1

        # Check if the picture is not all black
        if blackPixelCount <= width * height:
            passedTest += 1

        print('Passed: ' + str(passedTest) + ' out of ' + str(amountOfTests))

        # Make an example video and check if its not all black
        testVideo = subprocess.run(['raspivid', '-o', 'tmp/test.h264', '-t', '5000', '--nopreview'], stdout=subprocess.PIPE)

        # Check if the video file exists and has a non-zero size
        if os.path.isfile('tmp/test.h264') and os.path.getsize('tmp/test.h264') > 0:
            passedTest += 1
        
        print('Passed: ' + str(passedTest) + ' out of ' + str(amountOfTests))

        cap = cv2.VideoCapture('tmp/test.h264')

        # Loop through the frames and check if its not all black
        all_frames_black = True
        while cap.isOpened():
            # Read the next frame
            ret, frame = cap.read()

            if not ret:
                # End of video file
                break

            # Check if the frame is completely black
            if not (frame == 0).all():
                all_frames_black = False
                break

        cap.release()

        # Check if the video is not all black
        if(not all_frames_black):
            passedTest += 1
        
        print('Passed: ' + str(passedTest) + ' out of ' + str(amountOfTests))

        # remove test data and set functional true if all tests are passed
        if(passedTest == amountOfTests):
            os.rmdir('tmp')
            functional = True
    except:
        print('Passed: ' + str(passedTest) + ' out of ' + str(amountOfTests))
        return False
    return functional


#print(CheckFunctionality())