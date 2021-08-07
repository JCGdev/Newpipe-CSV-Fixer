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


runtimePath: str = os.getcwd()
jsonHeader: dict = {"app_version":"0.21.7","app_version_int":973,"subscriptions":[]}



def getFilenamesInDir() -> list:
    return os.listdir()

def getCsvFilename(filenames: str) -> str:
    return "".join(name for name in filenames if name.endswith(".csv"))

def getFileDescriptor(filename: str) -> None:
    return open(filename, "r", encoding="utf8")

def readFileLines(filename: str) -> dict:
    with open(filename, "r", encoding="utf8") as file:
        return file.readlines()

def readFile(filename: str) -> str:
    with open(filename, "r", encoding="utf8") as file:
        return file.read()

def writeLinesToFile(filename: str, content: list) -> None:
    with open(filename, "w", encoding="utf8") as file:
        file.writelines(content)

def writeToFile(filename: str, content: str) -> None:
    with open(filename, "w", encoding="utf8") as file:
        file.write(content)


def cleanFiles() -> None:
    os.remove("parsed_subscriptions.csv")


# ---------- Main functions --------


def prepareCsv(filename: str) -> list:

    debugPrint("Parsing CSV file...")

    csvContent: list = readFileLines(filename)
    csvContent[0] = "service_id,url,name\n" # Overriding not working key names from the 1st line

    parsedCsvContent: list = []

    for line in csvContent:
        parsedCsvContent.append(line.replace("http", "https")) 

    return parsedCsvContent


def convertCsvToJson(filename: str) -> str:

    debugPrint("Converting parsed CSV to JSON file...")    

    global jsonHeader

    csvConverted: list = jsonHeader 
    csvParser = csv.DictReader(getFileDescriptor(filename))
    
    for row in csvParser:
        csvConverted["subscriptions"].append(row)
        
    debugPrint(f"Done! file saved as 'subscriptions.json'")

    return json.dumps(csvConverted, indent=4)



def debugPrint(message: str) -> None:
    print(f"[*] {message} \n")



def main() -> None:

    filenames: list = getFilenamesInDir()
    csvFilename: str = getCsvFilename(filenames)

    debugPrint(f"Detected CSV File --> {csvFilename}")

    parsedCsvContent: list = prepareCsv(csvFilename)
    writeLinesToFile("parsed_subscriptions.csv", parsedCsvContent)

    convertedCsvToJson: str = convertCsvToJson("parsed_subscriptions.csv")
    writeToFile("subscriptions.json", convertedCsvToJson)

    
    cleanFiles()


if __name__ == "__main__":
    main()
