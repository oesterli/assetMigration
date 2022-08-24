#!/usr/bin/env python3

import pandas as pd
import numpy as np
import os
import datetime

## Infogeol numbers so select test fiels from
infoGeolNums = r"M:\Appl\DATA\PROD\lg\_restricted\_TP5_TEST-Migration\admin\infogeol_2021.txt"

## List of control files to use
inCtrlFiles = [r"M:\Appl\DATA\PROD\lg\_restricted\_TP5_TEST-Migration\in\ctrlLog\01_kontr-Daten.xlsx", r"M:\Appl\DATA\PROD\lg\_restricted\_TP5_TEST-Migration\in\ctrlLog\02_pdf-Dokumentenarchiv.xlsx", r"M:\Appl\DATA\PROD\lg\_restricted\_TP5_TEST-Migration\in\ctrlLog\03_Dateien-optimiert.xlsx"]

## Destination Log Directory = in directory for Ctrl files
destDirLog = r"M:\Appl\DATA\PROD\lg\_restricted\_TP5_TEST-Migration\in\ctrlLog"

## Number of random samples
numSamples = 10
igSamples = []

with open(infoGeolNums, "r") as f:
    text = f.readlines()
    text = text[0].split(',')

#print(type(text))
print("Number of InfoGeol-Numbers: ", len(text))

randomFiles = np.random.choice(text[1:], numSamples, replace=False)

print("Randomly selected InfoGeol-Numbers: ", randomFiles)
print("Number of random samples: ", len(randomFiles))


#randomFiles = list(map(int, randomFiles))
#randomFiles = [10302,7145,23964,33265,18427,24557,30618,24488,32560,41497,16005,41018,38422]
randomFiles = [10302,7145]


def randomSampler(infiles, samples, randomfiles):
    i = 1
    print("Number of samples: ", samples)
    print("Sample InfoGeol-Mumbers: ", randomfiles)
    for f in infiles:
        print(i)
        print(f)
        print("basename: ", os.path.splitext(os.path.basename(f))[0])

        ## select randomly
        df = pd.read_excel(f)
        print("Shape (rows, lines) of input control file: ", df.shape)
        df2 = df.loc[df['left'].isin(randomfiles)]
        print("df2.shape: ", df2.shape)
        print(df2[["filename", "left","size_MB"]].head())

        ## Create output file name
        #now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        #dfname = os.path.splitext(os.path.basename(sourceDir))[0]
        dfname = os.path.splitext(os.path.basename(f))[0]

        outdfname = "TEST_" + dfname + ".xlsx"

        print("TEST-Ctrl-file-name: ", outdfname)

        ## Export dataframe to excel-file
        df2.to_excel(os.path.join(destDirLog, outdfname))

        print("--------")

        i += 1
print(" ***** Start ***** ")
randomSampler(inCtrlFiles, numSamples, randomFiles)

print(" === FINISH === ")
