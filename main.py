# Author: Om Amin
# 
# generates c header files containing function prototypes of all .c files in given folder
 

import os 
import re #import regex
import sys


# get the path to the folders containing the c files and/or header files
# paths given by command line arguments, otherwise default set to directory of main.py file
def getFolderPaths():

    #By default get .c files and export .h files into directory of main.py file
    cFolder = os.getcwd()
    hFolder = os.getcwd()

    # if 1 argument given, then set bot .h and .c folder to it
    if (len(sys.argv) == 2):
        cFolder = sys.argv[1]
        hFolder = sys.argv[1]
    
    # if both .c and .h argument given, set it
    if (len(sys.argv) > 2):
        cFolder = sys.argv[1]
        hFolder = sys.argv[2]
    
    print("path to .c folder set: ", cFolder)
    print("path to .h folder set: ", hFolder)
    
    return (cFolder, hFolder)

# given a list of lines, returns list of lines of function protypes
def parseFile(lines):
    protos = []

    for line in lines:
        #match when line starts with keyword
        match = re.match("(\w+ ).*", line)
        if match != None:
            #filter out the non function protype keywords
            if (not exclude(match[0])):
                protos.append(match[0])

    return protos

#returns true if the line begins with invalid keyword
def exclude(line):
    exclude = {
        "static", 
        "struct"
    }

    #grab first keyword
    keyword = re.search("\w+", line, flags=0)[0]
    
    return (keyword in exclude)

#creates header file and print all function protypes to it
def constructFile(protos, fileName):
    #set path to header file
    fileName = fileName[:-2:] + ".h"

    path = HEADER_FILES + fileName
    file = open(path, "w")

    print(f"generating {fileName} header file")

    #write all the function prototypes
    for p in protos:
        p = prepProto(p)
        file.write(p + "\n")

    file.close()

# removes and trailing '{' and add ';' to end of prototype
def prepProto(proto):
    #if trailing {, remove it
    if (proto[-1] == '{'):
        proto = proto[:-1:]

    #add ; to end 
    if (proto[-1] != ';'):
        proto += ';'
        
    return proto

#get the paths to the .c and .h files
C_FILES, HEADER_FILES = getFolderPaths()

#os.walk to iterate through all subfolder aswell
for root, dirs, files in os.walk(C_FILES):
    for filename in files:
        #for any file with .c extension
        if(filename[len(filename)-2:] == ".c"):
            with open(os.path.join(root, filename)) as fp:
                #grab all the lines and create header files
                lines = fp.readlines()
                protos  = parseFile(lines)
                constructFile(protos, filename)

            
        
    