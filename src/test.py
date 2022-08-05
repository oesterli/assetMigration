## import libraries

import pandas as pd
import os
import datetime
import numpy as np
import time
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
    #fname = "log" + "_" + now + ".txt"
    #logFile = os.path.join(outdir, fname)
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

### TEST SECTION

## Read input control file
df = pd.read_excel(inCtrlFile, sheet_name='_kontr-Daten')
print("df: ", df.shape)

## Select only records to be copied ("nichtKopieren" == blank)
df2 = df.loc[df['nichtKopieren'].isnull()]
print("df2: ", df2.shape)

## Generate toPath
df2["toPath"] = outData + '\\' + df2["toFilename"]

## Change pandas setting to desplay all rows and columns
# with pd.option_context('display.max_rows', None,'display.max_columns', None,'display.precision', 3,):

## Select only specified columns
    # print(df2[['filename', "toFilename", "toPath", 'size_MB']].loc[:3])

## Define number of test data
sampledata = 10

## Convert df colums "inPath" and "outPath" into lists, in order you loop over ist
inFilePath = list((df2['inPath'][:sampledata]))
toFilePath = list((df2['toPath'][:sampledata]))
inFiles = list((df2['toFilename'][:sampledata]))
fileSize = list((df2['size_MB'][:sampledata]))

## Loop over output data directory and check if  files already exist

#print(os.listdir(outData))

# for (destDirPath, destDirNames, destFilenames) in os.walk(outData):
#     print("----- Destination directory --------")
#     print('Dest_dirpath: ', destDirPath)
#     print('Dest_filenames: ', destFilenames)
#     print('Number of Dest_files: ', len(destFilenames))

## Copy files

i=0
for f in inFiles:

    print("======")
    print("i =", i)
    print("f = ", f)
    existfiles = os.listdir(outData)

    print("Files exisiting in output dir: ", existfiles)

    if f in existfiles:
        print("==> NOT COPIED !!! " + f)
        message = "NOT COPIED !!!" + ";" + inFilePath[i] + ";" + "NULL" + ";" + f + ";" + str(fileSize[i])
        loggerX(logFile, message)

    else:
        shutil.copyfile(inFilePath[i], toFilePath[i])
        print("==> COPIED !!! " + f)
        message = "COPIED !!!" + ";" + inFilePath[i] + ";" + toFilePath[i] + ";" + f + ";" + str(fileSize[i])
        loggerX(logFile, message)


    i+=1

## Create output file name
now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
dfname = os.path.splitext(os.path.basename(outDirLog))[0]
outdfname = "Log_" + now + ".xlsx"

## Export dataframe to excel-file
#df2.to_excel(os.path.join(outDirLog,outdfname), sheet_name=dfname)

