import cv2
import os
import subprocess


def CheckFunctionality():

    # Create tmp directory for testing picture and video
    os.mkdir('tmp')
    tempdir = subprocess.run(['raspistill', '-o', 'tmp/test.jpg'], stdout=subprocess.PIPE)

    # Determines if the camera is connected and working correctly
    functional = False
    # Amount of all tests
    amountOfTests = 5
    # Determines the amount of tests passed
    passedTest = 0

    # Execute the 'vcgencmd get_camera' command to ensure the interface is enabled and a camera is detected
    checkInterface = subprocess.run(['vcgencmd', 'get_camera'], stdout=subprocess.PIPE)
    output = checkInterface.stdout.decode('utf-8')

    # Check if there is one camera module detected
    if(output.__contains__('detected=1')):
        passedTest += 1

    # Make an example picture and check if its not all black
    testPicture = subprocess.run(['raspistill', '-o', 'tmp/test.jpg'], stdout=subprocess.PIPE)

    # Open the image file and read the pixel values
    with open('tmp/test.jpg', 'rb') as f:
        # Read the header information
        header = f.read(16)
        width = int.from_bytes(header[12:16], byteorder='big')
        height = int.from_bytes(header[8:12], byteorder='big')

        # Read the pixel data
        pixel_data = f.read()

        blackPixelCount = 0
        numPixels = width * height
        # Loop through the pixel data and print the RGB values of each pixel
        for y in range(height):
            for x in range(width):
                index = (y * width + x) * 3
                r = pixel_data[index]
                g = pixel_data[index + 1]
                b = pixel_data[index + 2]
                if(r == 0 and g == 0 and b == 0):
                    blackPixelCount += 1
    
    # Check if the picture is not all black
    if(blackPixelCount != numPixels):
        passedTest += 1

    # Make an example video and check if its not all black
    testVideo = subprocess.run(['raspivid', '-o', 'tmp/test.h264', '-t', '5000'], stdout=subprocess.PIPE)

    # Check if the video file exists and has a non-zero size
    if os.path.isfile('tmp/test.h264') and os.path.getsize('tmp/test.h264') > 0:
        passedTest += 1
    
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
    
    # Execute the 'ls /dev/video*' command to ensure the interface is enabled and a camera is detected
    checkInterface = subprocess.run(['ls', '/dev/video*'], stdout=subprocess.PIPE)
    output = checkInterface.stdout.decode('utf-8')

    # Check if there is at least one device which can record videos
    if(output.__contains__('/dev/video0')):
        passedTest += 1

    # remove test data and set functional true if all tests are passed
    if(passedTest == amountOfTests):
        os.remove('tmp')
        functional = True

    return functional


#print(CheckFunctionality())