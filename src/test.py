#!/usr/bin/env python3

import numpy as np
import csv
import os
import datetime

## Infogeol-Nos, which appear either in Migrationsobjekt 04 "…\Scans-Boss-Repro\_kontr-Daten"; Migrationsobjekt 02 "…\pdf-Dokumentenarchiv" and  Migrationsobjekt 03 "…\pdf-Erst-Rollfilmscans\Dateien-optimiert"
infogeolTriples =r"M:\Appl\DATA\PROD\lg\_restricted\_TP5_TEST-Migration\admin\infogeol_triples.txt"

## Read file with INfoGeol-Nos to select from
f=open(infogeolTriples)
for row in csv.reader(f):
    print("File read!")
    print("File convertes to list!")

## Specify number of sample to take randomly
numSamples = 10

## Take randm samples
randomFiles = np.random.choice(row[1:], numSamples, replace=False)

## Print random samples to stdout
print(numSamples, "randomly selected files: ", randomFiles)

## define now time
now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

##Define output file name
fname = "randomSamples" + "_" + now + ".csv"
outDir = r"M:\Appl\DATA\PROD\lg\_restricted\_TP5_TEST-Migration\admin"
randomSamples = os.path.join(outDir, fname)
with open(randomSamples, 'a') as f:
    print("Random samples = ", numSamples, sep=';', file=f)
    for item in randomFiles:
        ## write each item on a new line
        f.write("%s\n" % item)
    print('Done')

