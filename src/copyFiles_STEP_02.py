#!/usr/bin/env python3

## import libraries
import pandas as pd
import os
import datetime
import shutil

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

##Define log file name
fname = "log" + "_" + now + ".txt"
logFile = os.path.join(outDirLog, fname)
with open(logFile, 'a') as f:
    #print(nowLog, text, sep=';', file=f)
    print("datatime;copyStatus;inPath;outPath;tofilename;sizeMB", sep=';', file=f)


## Define functions
## ==================

## Logger
def loggerX(logFile, text):
    """

    :param outdir:
    :param text:
    :return:
    """

    nowLog = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    with open(logFile, 'a') as f:
        print(nowLog, text, sep=';', file=f)

    # print date, time and message to stdout
    print(nowLog + ";" + text)
    print("-------------------")
    return


## Check directories

print("--- DIRECTORIES ---")
print("Input control files", inDirCtrl)
print("Input data files", inDirData)
print("Output logs", outDirLog)
print("Output data files", outData)


## ######## USER INPUT REQUIRED ########
## Read input control file
df = pd.read_excel(inCtrlFile, sheet_name='_kontr-Daten')
print("Shape (rows, lines) of input control file: ", df.shape)

## Select only records to be copied ("nichtKopieren" == blank)
df2 = df.loc[df['nichtKopieren'].isnull()]
print("Shape (rows, lines) of selected records to copy: ", df2.shape)

## Generate toPath and write it to dataframe df2
df2["toPath"] = outData + '\\' + df2["toFilename"]

## ######## USER INPUT REQUIRED ########
## Define number of test data (comment this line for productive use)
sampledata = 10

## Convert selected columns in df2 into lists, in order to loop over them
inFilePath = list((df2['inPath'][:sampledata]))
toFilePath = list((df2['toPath'][:sampledata]))
inFiles = list((df2['toFilename'][:sampledata]))
fileSize = list((df2['size_MB'][:sampledata]))

## Loop over output data directory and check if  files already exist
i=0
for f in inFiles:
    print("======")
    print("i =", i)
    print("f = ", f)

    ## Check filenames already existing in destination directory
    existFiles = os.listdir(outData)
    print("Files exisiting in output dir: ", existFiles)

    ## If file does already is in destination directory, do NOT copy it
    if f in existFiles:
        print("==> NOT COPIED !!! " + f)
        message = "NOT COPIED !!!" + ";" + inFilePath[i] + ";" + "NULL" + ";" + f + ";" + str(fileSize[i])
        loggerX(logFile, message)

    ## If file does NOT already is in destination directory, COPY it
    else:
        ## Copy files
        shutil.copyfile(inFilePath[i], toFilePath[i])
        print("==> COPIED !!! " + f)
        message = "COPIED !!!" + ";" + inFilePath[i] + ";" + toFilePath[i] + ";" + f + ";" + str(fileSize[i])
        loggerX(logFile, message)

    i+=1

## Create output file name
now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
dfname = os.path.splitext(os.path.basename(outDirLog))[0]
outdfname = "Log_" + now + ".xlsx"


