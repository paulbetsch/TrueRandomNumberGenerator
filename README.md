# TRNG (True Random Number Generator)

## About
This repository includes all scripts and files which we use to develop a True Random Number Generator. There is a directory for each tool, we developed to help us. The whole Software solution can be found in the directory called "TRNG-Pendel".

## Requirements for setup
### Basic Setup:
- Tri Pendulum with a black square at the end of the thrid pendulum arm
- Raspberry Pi
- Raspberry Pi Camera Module
### Advanced Setup:
- Same components as for the basic setup and the following in addition:
- 12V electric motor
- 24V electric lifiting magnet
- Relay which can control up to 24V
- Jumper cables
- Power sources for motor, magnet and Raspberry Pi

## Requirements for Installation
- \>= [Python 3.9](https://www.python.org/downloads/release/python-390/)
- Any IDE you prefer, e. g. PyCharm, VS Code, Python IDE
- Git CLI to get the code onto the Raspberry Pi

## Installation
- use command : `git clone https://github.com/paulbetsch/TrueRandomNumberGenerator.git`
- than follow the instructions for [setting up the frontend](./FrontEnd/README.md)
- To setup the API follow these [instructions](./TRNG_API/README.md)
- When both servers are running and you can reach them you are ready to generate!

## Code Style
- Always **comment your code** with a short explanation of what it does.
- Make sure that at least one team member understand your comments.
- Global variables should be written in upper case with underlines instead of spaces e.g TEST_VARIABLE.
- Local variables should be written in camelCase.
- Function names should be written in PascalCase except the main function which is called: `__main__()`.
- If possible divide your code into multiple python files.
- If you have **multiple python files**, make sure you have **one start file**, which should be called `__init__.py`.
- Any other python files should be written in PascalCase excluding the start file.
- You have to **write a README.md file**, which explains everything/script/file contained in the directory.
- The code should always work **without any external Data**.
- All **filepaths must be relative**, so that the code works on every single PC.

## Team
- Carlo Bauer
- Paul Betsch
- Lukas Siegle
- Marina Göppel 
- Carsten Michel
-  Stefan Kleinhenz Leiva
