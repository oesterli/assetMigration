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

## List of control files to use
inCtrlFiles = []

## Input ctrl file
inCtrlFile = r"M:\Appl\DATA\PROD\lg\_restricted\_TP5_TEST-Migration\in\ctrlLog\01_kontr-Daten_2022-06-28_15-12-42.xlsx"

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



### TEST SECTION

## Read input control file
df = pd.read_excel(inCtrlFile, sheet_name='_kontr-Daten')

print(df)

# testText = "Check!"
#
# loggerX(outDirLog,testText)
#
# #time.sleep(5)
#
# testText2 = "Check 222!"
#
# loggerX(outDirLog,testText2)