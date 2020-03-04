#!/bin/python3
from const import *
from func import *

filename = "pal4.bmp"

fread = open(filename,"rb")
bytesArray = fread.read()
fread.close()

header = bytesArray[START_HEADER:END_HEADER]
infoHeader = bytesArray[START_INFO_HEADER:END_INFO_HEADER]

dataOffset = readHeader(header)
bitsPerPixel,size,numColors = readInfo(infoHeader)

i = END_INFO_HEADER
if(bitsPerPixel <= 8 or dataOffset > 54):
    end = END_INFO_HEADER + numColors * 4
    readColorTable(bytesArray[i:end])
    i = end

pxUntilEnd = int(len(bytesArray[dataOffset:]))
readPixelData(bytesArray[dataOffset:],bitsPerPixel,30)
