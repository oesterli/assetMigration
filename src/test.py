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
inCtrlFiles = [r"M:\Appl\DATA\PROD\lg\_restricted\_TP5_TEST-Migration\in\ctrlLog\01_kontr-Daten_2022-06-28_15-12-42.xlsx", r"M:\Appl\DATA\PROD\lg\_restricted\_TP5_TEST-Migration\in\ctrlLog\02_pdf-Dokumentenarchiv_2022-06-28_16-08-33.xlsx", r"M:\Appl\DATA\PROD\lg\_restricted\_TP5_TEST-Migration\in\ctrlLog\03_Dateien-optimiert_2022-06-28_15-23-03.xlsx"]

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
fname = "log" + "_" + now + ".csv"
logFile = os.path.join(outDirLog, fname)
with open(logFile, 'a') as f:
    #print(nowLog, text, sep=';', file=f)
    print("datatime;copyStatus;ctrlfile;inPath;outPath;tofilename;sizeMB", sep=';', file=f)

## Define number of test data (comment this line for productive use)
sampleData = 10

## Define functions
## ==================

## Logger function
def loggerX(logfile, text):
    """

    :param outdir: Directory where the logfile will be saved
    :param text: Output message to be written to logfile
    :return:
    """

    nowLog = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    with open(logfile, 'a') as f:
        print(nowLog, text, sep=';', file=f)

    # print date, time and message to stdout
    print(nowLog + ";" + text)
    print("-------------------")
    return

## Check exisiting files and copy files
## def fileCheckerCopy(inctrlfile, sampledata, outdata, logfile):
def fileCheckerCopy(inctrlfile, sampleFiles, outdata, logfile):
    """

    :param inctrlfile: Contral file to be used
    :param sampledata: Number of lines in control file to be treated
    :param outdata: Path the files to be copied to
    :param logfile: Logfile to write to
    :return:
    """
    ## ######## USER INPUT REQUIRED ########
    ## Read input control file
    df = pd.read_excel(inctrlfile)
    print("Shape (rows, lines) of input control file: ", df.shape)

    ####
    ###    TESTING
    print("SampleFiles: ", sampleFiles)

    dfX = df.loc[df['left'].isin(sampleFiles)]
    print("dfX-shape = ", dfX.shape)
    #print(dfX.dtypes)

    ######
    ## Select only records to be copied ("nichtKopieren" == blank)
    # df2 = df.loc[df['nichtKopieren'].isnull()]
    df2 = dfX.loc[dfX['nichtKopieren'].isnull()]
    print("Shape (rows, lines) of selected records to copy: ", df2.shape)

    ## Generate toPath and write it to dataframe df2
    df2["toPath"] = outdata + '\\' + df2["toFilename"]

    ## Convert selected columns in df2 into lists, in order to loop over them
    # inFilePath = list((df2['inPath'][:sampledata]))
    # toFilePath = list((df2['toPath'][:sampledata]))
    # inFiles = list((df2['toFilename'][:sampledata]))
    # fileSize = list((df2['size_MB'][:sampledata]))
    inFilePath = list((df2['inPath']))
    toFilePath = list((df2['toPath']))
    inFiles = list((df2['toFilename']))
    fileSize = list((df2['size_MB']))

    ## Loop over output data directory and check if files already exist
    i = 0
    for f in inFiles:
        print("======")
        print("control file: ", j)
        print("i =", i)
        print("f = ", f)

        ## Check filenames already existing in destination directory
        existFiles = os.listdir(outdata)
        print("Files exisiting in output dir: ", existFiles)

        ## If file does already is in destination directory, do NOT copy it
        if f in existFiles:
            print("==> NOT COPIED !!! " + f)
            message = "NOT COPIED !!!" + ";" + str(j) + ";" + inFilePath[i] + ";" + "NULL" + ";" + f + ";" + str(fileSize[i])
            loggerX(logfile, message)

        ## If file does NOT already is in destination directory, COPY it
        else:
            ## Copy files
            #shutil.copyfile(inFilePath[i], toFilePath[i])
            shutil.copy2(inFilePath[i], toFilePath[i])
            print("==> COPIED !!! " + f)
            message = "COPIED !!!" + ";" + str(j) + ";" + inFilePath[i] + ";" + toFilePath[i] + ";" + f + ";" + str(fileSize[i])
            loggerX(logfile, message)

        i += 1

    ## Free memory
    # del inFilePath
    # del toFilePath
    # del inFiles
    # del fileSize
    # del existFiles
    # del df
    # del df2

    return


#### Only for TESTING
## define randomly selected data
## Infogeol-Nos, which appear either in Migrationsobjekt 04 "…\Scans-Boss-Repro\_kontr-Daten"; Migrationsobjekt 02 "…\pdf-Dokumentenarchiv" and  Migrationsobjekt 03 "…\pdf-Erst-Rollfilmscans\Dateien-optimiert"
randomSamples =r"M:\Appl\DATA\PROD\lg\_restricted\_TP5_TEST-Migration\admin\randomSamples.csv"

##

sampleFiles = []
with open(randomSamples, 'r') as tf:
    print("Sample files read!")
    for sf in tf:
        sampleFiles.append(tf.readline())

print(sampleFiles)

#sampleFiles = sampleFiles[1].split(";")

## Convert list items to integer
#sampleFiles = [eval(i) for i in sampleFiles[1:]]

# print(sampleFiles)
# print(type(sampleFiles))

## Start
print(" ====== Processing started ====== ")

## Display directories
print("--- DIRECTORIES ---")
print("Input control files", inDirCtrl)
print("Input data files", inDirData)
print("Output logs", outDirLog)
print("Output data files", outData)
print("")

print("--- CONTROL FILES ---")
# call fileCheckerCopy
j=1
for ctrlf in inCtrlFiles:
    print("Control file ", j, " :", ctrlf)
    # fileCheckerCopy(ctrlf, sampleData, outData, logFile)
    fileCheckerCopy(ctrlf, sampleFiles, outData, logFile)
    j+=1

print(" ############### PROCESSING FINISHED ############### ")

del inCtrlFiles



## Statistics
## Number of files in destination directory
## Number of files copied
## Number of files not copied
## total size(MB) of copied files

## Create output file name
#now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
#dfname = os.path.splitext(os.path.basename(outDirLog))[0]
#outdfname = "Log_" + now + ".xlsx"

## Export dataframe to excel-file
#df.to_excel(os.path.join(outDirLog,outdfname), sheet_name=dfname)
