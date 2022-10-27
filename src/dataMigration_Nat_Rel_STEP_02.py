#!/usr/bin/env python3

#########################################################################
## Data migration STEP 02
## Based on STEP 01 do the following:
## > Read ctrl-files for each source directory (output STEP 01)
## > Select only rows which shall be copied ("nichtkopieren == blank")
## > Check the content of the output directory
## > Check of each file IF it already exists in the destination directory
## > For each investigated file write message to log file
#########################################################################

## import libraries
import pandas as pd
import os
import datetime
import shutil

## Declare variables
## ==================

## Define directories
## Input Directory control files
#inDirCtrl = r"M:\Appl\DATA\PROD\lg\_restricted\_TP5_TEST-Migration\in\ctrlLog"
inDirCtrl = r"M:\Appl\DATA\PROD\lg\01_PRODUKTION\DatMgmt\GeolAssets\Daten_Migration"

## List of control files to use
##inCtrlFiles = [r"M:\Appl\DATA\PROD\lg\_restricted\_TP5_TEST-Migration\in\ctrlLog\01_kontr-Daten.xlsx", r"M:\Appl\DATA\PROD\lg\_restricted\_TP5_TEST-Migration\in\ctrlLog\02_pdf-Dokumentenarchiv.xlsx", r"M:\Appl\DATA\PROD\lg\_restricted\_TP5_TEST-Migration\in\ctrlLog\03_Dateien-optimiert.xlsx"]

## For TESTING
#inCtrlFiles = [r"M:\Appl\DATA\PROD\lg\_restricted\_TP5_TEST-Migration\in\ctrlLog\TEST_01_kontr-Daten.xlsx", r"M:\Appl\DATA\PROD\lg\_restricted\_TP5_TEST-Migration\in\ctrlLog\TEST_02_pdf-Dokumentenarchiv.xlsx", r"M:\Appl\DATA\PROD\lg\_restricted\_TP5_TEST-Migration\in\ctrlLog\TEST_03_Dateien-optimiert.xlsx"]

## ================================= For PRODUCTION =================================

## Run 1: ...\lg\...\Scans-Boss-Repro\_kontr-Daten
#inCtrlFiles = [r"M:\Appl\DATA\PROD\lg\01_PRODUKTION\DatMgmt\GeolAssets\Daten_Migration\Filename-Overview__kontr-Daten_2022-06-28_15-12-42_bearbPFI-OK.xlsx"]

## Run 2: ...\GD\...\pdf-Dokumentenarchiv
#inCtrlFiles = [r"M:\Appl\DATA\PROD\lg\01_PRODUKTION\DatMgmt\GeolAssets\Daten_Migration\Filename-Overview_pdf-Dokumentenarchiv_2022-06-28_16-08-33_bearbPFI-OK.xlsx"]

## Run 3: ...\lg\...pdf-Erst-Rollfilmscans\Dateien-optimiert
#inCtrlFiles = [r"M:\Appl\DATA\PROD\lg\01_PRODUKTION\DatMgmt\GeolAssets\Daten_Migration\Filename-Overview_Dateien-optimiert_2022-06-28_15-23-03_bearbPFI-OK.xlsx"]
inCtrlFiles = [r"M:\Appl\DATA\PROD\lg\01_PRODUKTION\DatMgmt\GeolAssets\Daten_Migration\log_nat-rel-files.xlsx_2022-10-26_13-59-14.xlsx"]

## ================================= ############## =================================


## Input ctrl file
#inCtrlFile = r"M:\Appl\DATA\PROD\lg\_restricted\_TP5_TEST-Migration\in\ctrlLog\01_kontr-Daten_2022-06-28_15-12-42.xlsx"

## Input data files
#inDirData = r"M:\Appl\DATA\PROD\lg\_restricted\_TP5_TEST-Migration\in\data"

## For TESTING
## Output logs
#outDirLog = r"M:\Appl\DATA\PROD\lg\_restricted\_TP5_TEST-Migration\out\log"

## Output data files
#outDirData = r"M:\Appl\DATA\PROD\lg\_restricted\_TP5_TEST-Migration\out\data"

## ================================= For PRODUCTION =================================

## Output logs
outDirLog = r"M:\Appl\DATA\GD\landesgeologie\lgAssets\logs"
## Output data files
outDirData = r"M:\Appl\DATA\GD\landesgeologie\lgAssets\assetsNatRel4Cloud"


## ================================= ############## =================================



## define now time
now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

##Define log file name
fname = "log" + "_" + now + ".csv"
logFile = os.path.join(outDirLog, fname)
with open(logFile, 'a') as f:
    #print(nowLog, text, sep=';', file=f)
    #print("datatime;copyStatus;ctrlfile;inPath;outPath;tofilename;sizeMB", sep=';', file=f)
    print("datatime;copyStatus;ctrlfile;ctrlfilename;inPath;outPath;tofilename;sizeMB", sep=';', file=f)

## Define number of test data (comment this line for productive use)
#sampleData = 10

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
def fileCheckerCopy(inctrlfile, outdata, logfile):
    """

    :param inctrlfile: Contral file to be used
    :param outdata: Path the files to be copied to
    :param logfile: Logfile to write to
    :return:
    """
    ## ######## USER INPUT REQUIRED ########
    ## Read input control file
    df = pd.read_excel(inctrlfile)
    print("Shape (rows, lines) of input control file: ", df.shape)

    ## Select only records to be copied ("nichtKopieren" == blank)
    #df2 = df.loc[df['nichtKopieren'].isnull()]
    df2 = df
    print("Shape (rows, lines) of selected records to copy: ", df2.shape)

    ## Generate toPath and write it to dataframe df2
    #df2["toPath"] = outdata + '\\' + df2["toFilename"]

    inFilePath = list((df2['inPath']))
    toFilePath = list((df2['toPath']))
    inFiles = list((df2['toFilename']))
    fileSize = list((df2['size_MB']))

    ## Loop over output data directory and check if files already exist
    i = 0
    for f in inFiles:
        print("=========================================================")
        print("control file: ", j)
        print("i =", i)
        print("f = ", f)

        ## Check filenames already existing in destination directory
        # existFiles = os.listdir(outdata)
        # print("Files exisiting in output dir: ", existFiles)

        # ## If file does already is in destination directory, do NOT copy it
        # if f in existFiles:
        #     print("==> NOT COPIED !!! " + str(f))
        #     message = "NOT COPIED !!!" + ";" + str(j) + ";" + inctrlfile + ";" + inFilePath[i] + ";" + "NULL" + ";" + str(f) + ";" + str(fileSize[i])
        #     #message = "NOT COPIED !!!" + ";" + str(j) + ";" + inFilePath[i] + ";" + "NULL" + ";" + f + ";" + str(fileSize[i])
        #     loggerX(logfile, message)
        #
        # ## If file does NOT already is in destination directory, COPY it
        # else:
        #     ## Copy files
        #     #shutil.copyfile(inFilePath[i], toFilePath[i])
        #     shutil.copy2(inFilePath[i], toFilePath[i])
        #     print("==> COPIED !!! " + str(f))
        #     message = "COPIED !!!" + ";" + str(j) +  ";" + inctrlfile + ";" + inFilePath[i] + ";" + toFilePath[i] + ";" + str(f) + ";" + str(fileSize[i])
        #     #message = "COPIED !!!" + ";" + str(j) + ";" + inFilePath[i] + ";" + toFilePath[i] + ";" + f + ";" + str(fileSize[i])
        #     loggerX(logfile, message)


        ## Copy files
        # shutil.copyfile(inFilePath[i], toFilePath[i])
        shutil.copy2(inFilePath[i], toFilePath[i])
        print("==> COPIED !!! " + str(f))
        message = "COPIED !!!" + ";" + str(j) + ";" + inctrlfile + ";" + inFilePath[i] + ";" + toFilePath[
            i] + ";" + str(f) + ";" + str(fileSize[i])
        # message = "COPIED !!!" + ";" + str(j) + ";" + inFilePath[i] + ";" + toFilePath[i] + ";" + f + ";" + str(fileSize[i])
        loggerX(logfile, message)
        i += 1

    ## Free memory
    del inFilePath
    del toFilePath
    del inFiles
    del fileSize
    #del existFiles
    del df
    del df2

    return

## Start
print(" ====== Processing started ====== ")
print("START time: ", datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))

## Display directories
print("--- DIRECTORIES ---")
print("Input control files", inDirCtrl)
#print("Input data files", inDirData)
print("Output logs", outDirLog)
print("Output data files", outDirData)
print("")

print("--- CONTROL FILES ---")
# call fileCheckerCopy
j=1
for ctrlf in inCtrlFiles:
    print("Control file ", j, " :", ctrlf)
    print("Start run: ", j, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    fileCheckerCopy(ctrlf, outDirData, logFile)
    print("End run: ", j, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    j+=1


print(" ############### PROCESSING FINISHED ############### ")
print("FINISH time: ", datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))

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
