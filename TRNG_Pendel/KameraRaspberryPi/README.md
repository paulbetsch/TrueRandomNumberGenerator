# TRNG Live Image Capturing

## About
This repository includes code snippets, which we currently use on capturing live images from a RaspberryPi camera.

## Requirements
- These Scripts can only be run on the Raspberry Pi due to specific libraries

## Scripts
- __ObjectTracker__: The PendelManger class controls the interaction between the ObjectTracker and itself through shared variables. While a specific shared variable is set to true, the ObjectTracker continuously tracks black contours captured by a connected camera. If an error occurs during tracking, an error event is triggered and set as another shared variable, which can be accessed by the PendelManger. The PendelManger has the ability to set the first shared variable to false, effectively stopping the ObjectTracker. Additionally, the ObjectTracker generates random bits with the tracked Contours and writes them into a shared list with the PendelManger.
