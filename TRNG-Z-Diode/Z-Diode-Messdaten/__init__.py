import os
import shutil
import csv
from zipfile import ZipFile

ZIP_FILE_NAME = "scopes.zip"
TMP_DIR_NAME = "tmp"
OUTPUT_FILE_NAME = "data.bin"

# Extract files into a temporary directory
def extractData():
    # Ensure the temporary directory doesnt exists
    if(os.path.isdir(TMP_DIR_NAME)):
        shutil.rmtree(TMP_DIR_NAME)
    # Extract all files of the ZIP FILE into a temporary dircectory
    with ZipFile(ZIP_FILE_NAME, 'r') as zip:
        zip.extractall(TMP_DIR_NAME) 
        print('File is exctracted in temp folder')

# Read all data in files which are stored in a temporary directory
def readData():
    # define vars
    directory = os.fsencode(TMP_DIR_NAME)
    countOfFilesToProcess = 0
    currentFile = 0
    filelist = os.listdir(directory)
    sortedfilelist = sorted(filelist, key=lambda x: getNumber(x))

    # simple counter of the files in the directory
    for file in filelist:
        countOfFilesToProcess += 1
    
    for file in sortedfilelist:
        currentFile += 1
        filename = os.fsdecode(file)
        print('Processing File ' + str(currentFile) + ' out of ' + str(countOfFilesToProcess) + ': ' + filename)
        if filename.endswith(".csv"):
            readFile('tmp/' + filename)
            continue

def getNumber(filename):
    # extract the number from the filename
    return int(filename.decode().split("_")[1].split(".")[0])

def readFile(filename):
    # Read Line by Line of the current file:
    with open(filename, mode='r') as file:
        csvreader = csv.reader(file)
        convertData(csvreader)
    print('Done.')

# check if the voltage in row[1] goes up, than write a 1 into output file if it goes down a 0 is written.
def convertData(data):
    for row in data:
        i = 0
        prev_row = 0
        direction = "up"
        counter = 0
        for row in data:
            if i < 3:
                prev_row = row
                i += 1
                continue

            voltage2 = float(row[1])
            voltage1 = float(prev_row[1])

            if direction == "up":
                if voltage2 >= voltage1:
                    counter += 1
                else:
                    if counter % 2 == 0:
                        writeData(0)
                    else:
                        writeData(1)
                    direction = "down"
                    counter = 0
            else:
                if voltage1 >= voltage2:
                    counter += 1
                else:
                    if counter % 2 == 0:
                        writeData(0)
                    else:
                        writeData(1)
                    direction = "up"
                    counter = 0        

def writeData(bit):
    with open(OUTPUT_FILE_NAME, 'a') as file:
        file.write(str(bit))


# Clean Output File
if(os.path.isdir(OUTPUT_FILE_NAME)):
    os.remove(OUTPUT_FILE_NAME)
# Extract raw data into temporary directory
extractData()
# read and analyse the data in the csv files
readData()
# Clean temporary directory after Analysis
shutil.rmtree(TMP_DIR_NAME)
