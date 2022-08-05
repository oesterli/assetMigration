## Read Exceltable into Dataframe

## Select only rows with file names to be copied

## For each selected file copy file to destination directory



## import libraries

import pandas as pd
import os
import datetime
import time



## Declare variables
## ==================

## Define directories
## Input control files
inDirCtrl = r"M:\Appl\DATA\PROD\lg\_restricted\_TP5_TEST-Migration\in\ctrlLog"

## Input data files
inDirData = r"M:\Appl\DATA\PROD\lg\_restricted\_TP5_TEST-Migration\in\data"

## Output logs
outDirLog = r"M:\Appl\DATA\PROD\lg\_restricted\_TP5_TEST-Migration\out\log"

## Output data files
outData = r"M:\Appl\DATA\PROD\lg\_restricted\_TP5_TEST-Migration\out\data"

## define now time
now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

## Define functions
## ==================

## Logger
def loggerX(outdir, text):
    """

    :param outdir:
    :param text:
    :return:
    """
    fname = "log" + "_" + now + ".txt"
    logFile = os.path.join(outdir, fname)
    nowLog = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    with open(logFile, 'a') as f:
        print(nowLog, text, sep=';', file=f)

    # print date, time and message to stdout
    print(nowLog, text)
    print("-------------------")
    return


## Check directories

print("--- DIRECTORIES ---")
print("Input control files", inDirCtrl)
print("Input data files", inDirData)
print("Output logs", outDirLog)
print("Output data files", outData)

## Read input control file



### TEST SECTION
testText = "Check!"

loggerX(outDirLog,testText)

#time.sleep(5)

testText2 = "Check 222!"

loggerX(outDirLog,testText2)