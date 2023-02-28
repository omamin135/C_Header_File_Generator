import os
import re

C_FILES = "c_files/"
HEADER_FILES = "header_files/"


def parseFile(lines):
    protos = []

    for line in lines:
        match = re.match("(\w+ ).*", line)
        if match != None:
            if (not exclude(match[0])):
                protos.append(match[0])

    return protos

def exclude(line):
    exclude = {
        "static", 
        "struct"
    }

    keyword = re.search("\w+", line, flags=0)[0]
    
    return (keyword in exclude)

def constructFile(protos, fileName):
    path = HEADER_FILES + fileName + ".h"
    file = open(path, "w")

    for p in protos:
        
        p = prepProto(p)
        file.write(p + "\n")

    file.close()

def prepProto(proto):
    #if trailing {, remove it
    if (proto[-1] == '{'):
        proto = proto[:-1:]

    #add ; to end 
    if (proto[-1] != ';'):
        proto += ';'
        
    
    return proto

    


for root, dirs, files in os.walk(C_FILES):
    for filename in files:
        with open(os.path.join(root, filename)) as fp:
            lines = fp.readlines()
            protos  = parseFile(lines)
            constructFile(protos, filename)

            
        
    