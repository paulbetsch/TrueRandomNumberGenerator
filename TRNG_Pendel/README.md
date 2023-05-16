# TRNG Pendel

## About
This Folder contains a few Python Scripts which are used to manage the whole TRNG.

## Requirements
- 

## Scripts
- __init.py__: Old script is not used anymore.
- __DataBuffer__: Used to store random generated Bits.
    - The pendelManager will store random Bits as a buffer, for requests with a big amount of randomnumbers.
- __pendelManager.py__: This script handles all tests and the generation of Random Numbers.
    - it uses multiprocessing and the [DataBuffer](DataBuffer.py) to return big amounts of randomnumbers.

