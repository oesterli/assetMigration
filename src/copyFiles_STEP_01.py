## Import Libraies
import datetime
import pandas as pd
import os
import shutil
import re

## Declare variables

## TEST source directory
sourceDir = r"\\adb.intra.admin.ch\UserHome$\SWISSTOPO-01\U80773132\config\Desktop\_transfer\in"

## PROD source directory
## STEP 1
#sourceDir = r"M:\Appl\DATA\GD\landesgeologie\InfoGeol-Archiv\pdf-Dokumentenarchiv"
## STEP 2
#sourceDir = r"M:\Appl\DATA\PROD\lg\01_PRODUKTION\DatMgmt\Scans-Boss-Repro\_kontr-Daten"
## STEP 3
#sourceDir = r"M:\Appl\DATA\PROD\lg\01_PRODUKTION\DatMgmt\Datenbearbeitung\pdf-Erst-Rollfilmscans\Dateien-optimiert"

## TEST destination directory
destDir = r"\\adb.intra.admin.ch\UserHome$\SWISSTOPO-01\U80773132\config\Desktop\_transfer\out"

## PROD destination directory
#destDir = r"\\adb.intra.admin.ch\UserHome$\SWISSTOPO-01\U80773132\config\Desktop\_transfer\out"

## List of directories to investigate
dirlist = [sourceDir]

## List of files in destnation
destFiles = []

## Define column names of data frame for storing results
columnNames = ["filename", "inPath", "left","right","ext","toFilename","toPath","size_MB","copy"]
destColumnNames = ["destFilename", "destInPath", "destLeft","destRight","destExt"]

## Create dataframe for storing results
df = pd.DataFrame(columns=columnNames)
df_dest = pd.DataFrame(columns=destColumnNames)


#def fNameSplitter():



## Print dirList with all directories to be investigated
print("========= START =========")
#print("----")
print('dirlist', dirlist)

## Loop over files and directories in sourceDir
i=1
for (dirpath, dirnames, filenames) in os.walk(dirlist.pop()):
    print('--- Directory: ', i, ' ----')
    print('dirpath: ', dirpath)
    print('dirname:', dirnames)
    print('filenames: ', filenames)
    print('Number of files: ', len(filenames))

    ## Get files in destination directory
    for (destDirPath, destDirNames, destFilenames) in os.walk(destDir):
        print("----- Destination directory --------")
        print('Dest_dirpath: ', destDirPath)
        print('Dest_filenames: ', destFilenames)
        print('Number of Dest_files: ', len(destFilenames))

        ## Split filename at the first non-digit character
        for f in destFilenames:
            dest_sep = re.search(r"\D", f)

            ## If filename does not start with a digit skip file and continue to the next
            if dest_sep.start() == 0:
                print('NOK!!! Filename does NOT start with a digit!')
                continue
            ## If filename starts with digit go on
            else:
                destLeft = f[:dest_sep.start()]
                destFiles.append(destLeft)
                print('destLeft: ', destLeft)
                print("destFiles: ", destFiles)
                print("Unique destFiles: ",list(set(destFiles)))

    ## Loop over files in respective directory
    j=1
    for filename in filenames:
        print('--- Directory: ', i, '; Item: ', j, ' ----')
       #print('----')
        print("Filename: ", filename)

        ## Search each filename for the positon of the first non digit character
        sep = re.search(r"\D", filename)

        ## If filename does not start with a digit skip file and continue to the next
        if sep.start() == 0:
            print('NOK!!! Filename does NOT start with a digit!')
            continue
        ## If filename starts with digit go on
        else:
            print('OK, go on!')
            ## Split filename at the first non-digit character
            left, right, ext = filename[:sep.start()], filename[sep.start():], os.path.splitext(filename)[1]
            print('left: ', left)
            #print('right: ', right)
            #print('ext: ', ext)

            fileSize = round(os.path.getsize(os.path.join(dirpath,filename))/(1024*1024),2)
            print("filepath: ",os.path.join(dirpath,filename))
            print("fileSize: ", fileSize)

            ## Append filename parts to the output dataframe
            df = df.append({"filename":filename, "inPath":os.path.join(dirpath,filename), "left":left, "right":right, "ext":ext, "toFilename":"", "toPath":"", "size_MB": fileSize, "copy": ""}, ignore_index=True)

            ## If filename is already in destination directory, continue, else copy it
            df.loc[df["left"].isin(destFiles), "copy"] = "Do not copy"
            if left in destFiles:
                print("File is in destination directory")
            else:
                print("File is NOT in destination directory")
                continue
        j+=1
    i+=1

print("===============")

## Sort dataframe
df.sort_values('filename', ascending=True, inplace=True)

## Check for duplicates and assign cumcount to df
df['duplicate'] = df.duplicated(subset=['left'], keep=False)
df['dup_number'] = (df.groupby(['left']).cumcount()+1).apply(str).apply(lambda x: '{0:0>2}'.format(x))

## Select duplicates and concatenate toFilename
df.loc[df['duplicate'] == True, 'toFilename'] = df["left"] + "_" + df['dup_number'] + df['ext']
df.loc[df['duplicate'] == False, 'toFilename'] = df["left"] + df['ext']

## Assign "COPY"-request to files which are not in destination directory
df.loc[df['copy'] != "Do not copy", 'copy'] = "COPY!!!"

## Generate toPath
df["toPath"] = destDir + '\\' + df["toFilename"]

print("===============")
print(df.shape)
print(df.dtypes)
print(df)

## Create output file name
now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
dfname = os.path.splitext(os.path.basename(sourceDir))[0]
#dfname = "Filename_Overview"
outdfname = "Filename-Overview_" + dfname +"_"+ now + ".xlsx"

## Export dataframe to excel-file
df.to_excel(os.path.join(destDir,outdfname), sheet_name=dfname)



