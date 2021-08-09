#! /usr/bin/python3
#
# Coded by --> JCGdev
#
# Convert your CSV file to a valid JSON for NewPipe  
#
#

import os
import sys
import json
import csv
import argparse

# -------- Setting arguments -----------

argumentParser = argparse.ArgumentParser(description="Convert your Youtube takeout CSV into a JSON that NewPipe is able to read!")
argumentParser.add_argument("-f", "--file", type=str, required=True, help="Path of your subscriptions CSV")
argumentParser.add_argument("-j", "--jsonHeader", type=str, required=True, help="Path to the NewPipe Headers (app_version, app_verion_int...)")

argumentParser.add_argument("-e", "--encoding", type=str, required=False, help="Specify other encoding, by default is utf8")

arguments = argumentParser.parse_args()

# ---------------------------------------


# ------ Defining global variables ------

runtimePath: str = os.getcwd()
csvFile: str = arguments.file
jsonHeaderFile: list = arguments.jsonHeader

if((paramEncoding := arguments.encoding) == None):
    paramEncoding = "utf8"


# ---------------------------------------

def getFilenamesInDir() -> list:
    return os.listdir()

def getCsvFilename(filenames: str) -> str:
    return "".join(name for name in filenames if name.endswith(".csv"))

def getFileDescriptor(filename: str) -> None:
    global paramEncoding
    return open(filename, "r", encoding=paramEncoding)

def readFileLines(filename: str) -> dict:
    global paramEncoding
    with open(filename, "r", encoding=paramEncoding) as file:
        return file.readlines()

def readFile(filename: str) -> str:
    global paramEncoding
    with open(filename, "r", encoding=paramEncoding) as file:
        return file.read()

def writeLinesToFile(filename: str, content: list) -> None:
    global paramEncoding
    with open(filename, "w", encoding=paramEncoding) as file:
        file.writelines(content)

def writeToFile(filename: str, content: str) -> None:
    global paramEncoding
    with open(filename, "w", encoding=paramEncoding) as file:
        file.write(content)

def removeBlankLines(paramList: list) -> list:
    
    parsedList: list = []

    for section in paramList:
        if not section.isspace():
            parsedList.append(section)

    return parsedList


def cleanFiles() -> None:
    os.remove("parsed_subscriptions.csv")


# ---------- Main functions --------


def parseCsv(filename: str) -> list:

    debugPrint("Parsing CSV file...")

    csvContent: list = removeBlankLines(readFileLines(filename))
    csvContent[0] = "service_id,url,name\n" # Overriding not working key names from the 1st line


    for line in csvContent:
        index: int = csvContent.index(line)
        csvContent[index] = line.replace("http", "https") 

    return csvContent


def convertCsvToJson(filename: str) -> str:

    global jsonHeaderFile
    debugPrint("Converting parsed CSV to JSON file...")    

    csvConverted: dict = json.loads(readFile(jsonHeaderFile))
    csvParser = csv.DictReader(getFileDescriptor(filename))
    
    for row in csvParser:
        csvConverted["subscriptions"].append(row)
        
    debugPrint(f"Done! file saved as 'subscriptions.json'")

    return json.dumps(csvConverted, indent=4)



def debugPrint(message: str) -> None:
    print(f"[*] {message} \n")



def main() -> None:

    global csvFile
    
    try:
        parsedCsvContent: list = parseCsv(csvFile)
        writeLinesToFile("parsed_subscriptions.csv", parsedCsvContent)

        convertedCsvToJson: str = convertCsvToJson("parsed_subscriptions.csv")
        writeToFile("subscriptions.json", convertedCsvToJson)

        cleanFiles()

    except UnicodeDecodeError:
        debugPrint("ERROR (UnicodeDecodeError). Please try to run the script with --encode cp437")
        cleanFiles()
        sys.exit(1)
        

if __name__ == "__main__":
    main()
