#! /usr/bin/python3
#
# Coded by --> JCGdev
#
# Convert your CSV file to a valid JSON for NewPipe  
#
#

import os
import sys
import io
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
csvFilename: str = arguments.file
jsonHeaderFilename: list = arguments.jsonHeader

paramEncoding: str = arguments.encoding
if(paramEncoding == None):
    paramEncoding = "utf8"


# ---------------------------------------

def getFilenamesInDir() -> list:
    return os.listdir()

# def getCsvFilename(filenames: str) -> str:
#   return "".join(name for name in filenames if name.endswith(".csv"))

def getFileDescriptor(filename: str, mode: str) -> io.TextIOWrapper:
    global paramEncoding
    return open(filename, mode, encoding=paramEncoding)

def readFileLines(fileDescriptor: io.TextIOWrapper) -> dict:
    lines: dict = fileDescriptor.readlines()
    fileDescriptor.close()
    return lines

def readFileString(fileDescriptor: io.TextIOWrapper) -> str:
    fileContent: str = fileDescriptor.read()
    fileDescriptor.close()
    return fileContent

def writeLinesToFile(fileDescriptor: io.TextIOWrapper, content: list) -> None:
    fileDescriptor.writelines(content)
    fileDescriptor.close()

def writeStringToFile(fileDescriptor: io.TextIOWrapper, content: str) -> None:
    fileDescriptor.write(content)
    fileDescriptor.close()

def removeBlankLines(paramList: list) -> list:
    
    parsedList: list = []

    for section in paramList:
        if not section.isspace():
            parsedList.append(section)

    return parsedList


def cleanFiles() -> None:
    os.remove("parsed_subscriptions.csv")


# ---------- Main functions --------


def parseCsv(csvFileDescriptor: io.TextIOWrapper) -> list:

    csvContent: list = removeBlankLines(readFileLines(csvFileDescriptor))
    csvContent[0] = "service_id,url,name\n" # Overriding not working column names from the 1st line


    for line in csvContent:
        index: int = csvContent.index(line)
        csvContent[index] = line.replace("http", "https") 

    return csvContent


def convertCsvToJson(CsvFileDescriptor: io.TextIOWrapper) -> str:

    global jsonHeaderFilename
    debugPrint("Converting parsed CSV to JSON file...")    

    jsonHeaderContent: dict = json.loads(readFileString(getFileDescriptor(jsonHeaderFilename, "r")))
    csvParser = csv.DictReader(CsvFileDescriptor)
    
    for row in csvParser:
        jsonHeaderContent["subscriptions"].append(row)
        
    return json.dumps(jsonHeaderContent, indent=4)


def debugPrint(message: str) -> None:
    print(f"[*] {message} \n")



def main() -> None:

    global csvFilename
    
    try:
        debugPrint("Parsing CSV file...")
        parsedCsvContent: list = parseCsv(getFileDescriptor(csvFilename, "r"))
        writeLinesToFile(getFileDescriptor("parsed_subscriptions.csv", "w"), parsedCsvContent)

        convertedCsvToJson: str = convertCsvToJson(getFileDescriptor("parsed_subscriptions.csv", "r"))
        writeStringToFile(getFileDescriptor("subscriptions.json", "w"), convertedCsvToJson)
        debugPrint(f"Done! file saved as 'subscriptions.json'")

        cleanFiles()

    except UnicodeDecodeError:
        debugPrint("ERROR (UnicodeDecodeError). Please try to run the script with --encode cp437")
        cleanFiles()
        sys.exit(1)
        

if __name__ == "__main__":
    main()
