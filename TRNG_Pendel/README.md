# TRNG Pendel

## About
This Folder contains a few Python Scripts which are used to manage the whole TRNG.

## Requirements
- setuptools \>= 67.8.0
- scipy \>= 1.8.1
- numpy \>= 1.24.2
- opencv-python \>= 4.5.3.56
- rpi.gpio \>= 0.7.0

## Scripts
- __init.py__: Old script is not used anymore. But necessary for import this folder as a module
- __DataBuffer__: Used to store random generated Bits.
    - The pendelManager will store random Bits as a buffer, for requests with a big amount of randomnumbers.
- __pendelManager.py__: This script handles all tests and the generation of Random Numbers.
    - it uses multiprocessing and the [DataBuffer](DataBuffer.py) to return big amounts of randomnumbers.

