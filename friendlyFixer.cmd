:: Batch script wrapper for a more friendly execute of fixer.py
@echo off

TITLE NewPipe CSV Fixer - JCGdev
set pythonBinary="Python\Windows\amd64\Python-3.9.7\python.exe"

GOTO :main

:main
CALL :debugPrint "Batch Wrappper - JCGdev"

set /P csvFilename=Enter the CSV filename: 
set /P headerFilename=Enter the header filename: 

CALL :fileExistsCheck %csvFilename%
CALL :fileExistsCheck %headerFilename%

"%pythonBinary%" "fixer.py" "-f" %csvFilename% "-j" %headerFilename%
PAUSE


:fileExistsCheck
if EXIST %~1 ( CALL :debugPrint "File %~1 found" ) else ( CALL :debugPrint "File %~1 not found" & EXIT)

:debugPrint
ECHO [*] %~1


