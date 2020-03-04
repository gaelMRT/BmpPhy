#!/bin/python3
"""
Author  :   Gaël Mariot
Date    :   20.02.2020
Name    :   func.py
Desc.   :   This file contains all the function for the project
"""
from const import * 

def byteArrayToInt(byteArray,intel = True):
    result = 0
    if(intel):
        byteArray = byteArray[::-1]
    for x in range(len(byteArray)):
        bill = byteArray[len(byteArray)-x-1] * 256**x
        result += bill

    return result
def byteArrayToBits(byteArray, intel = False):
    if(intel):
        byteArray = byteArray[::-1]
    bytes_as_bits = ''.join(format(byte, '08b') for byte in byteArray)
    return bytes_as_bits


def byteArrayToStr(byteArray,intel = False):
    result = ""
    if(intel):
        byteArray = byteArray[::-1]
    for x in byteArray:
        result += ("%02X " % x)
    return result
def byteArrayToWord(byteArray,intel = False):
    if(intel):
        byteArray = byteArray[::-1]
    result = byteArray.decode()
    return result

def readHeader(header):
    print("Header")
    i = 0

    signature = byteArrayToWord(header[:SIGNATURE_SIZE])
    i += SIGNATURE_SIZE
    fileSize = byteArrayToInt(header[i:i+FILE_SIZE_SIZE])
    i += FILE_SIZE_SIZE
    reserved = byteArrayToStr(header[i:i+RESERVED_SIZE])
    i += RESERVED_SIZE
    dataOffset = byteArrayToInt(header[i:i+DATA_OFFSET_SIZE])

    print("Signature : %s"% (signature))
    print("File Size : %d bytes"% (fileSize))
    print("reserved : %s" % (reserved))
    print("DATA OFFSET : %d bytes" % (dataOffset))
    print()
    return dataOffset

def readInfo(infoHeader):
    print("Info Header")
    i = 0
    size = byteArrayToInt(infoHeader[i:i+SIZE])
    i += SIZE
    width = byteArrayToInt(infoHeader[i:i+WIDTH])
    i += WIDTH
    height = byteArrayToInt(infoHeader[i:i+HEIGHT])
    i += HEIGHT
    planes = byteArrayToInt(infoHeader[i:i+PLANES])
    i += PLANES
    bitsPerPixel = byteArrayToInt(infoHeader[i:i+BITS_PER_PIXEL])
    i += BITS_PER_PIXEL
    compression = byteArrayToInt(infoHeader[i:i+COMPRESSION])
    i += COMPRESSION
    imageSizeCompressed = byteArrayToInt(infoHeader[i:i+IMAGE_SIZE])
    i += IMAGE_SIZE
    xPixelsPerM = byteArrayToInt(infoHeader[i:i+X_PIXEL_PER_M])
    i += X_PIXEL_PER_M
    yPixelsPerM = byteArrayToInt(infoHeader[i:i+Y_PIXEL_PER_M])
    i += Y_PIXEL_PER_M
    usedColors = byteArrayToInt(infoHeader[i:i+COLORS_USED])
    i += COLORS_USED
    importantColors = byteArrayToInt(infoHeader[i:i+IMPORTANT_COLORS])
    i += IMPORTANT_COLORS

    print("Size : %d bytes"% (size))    
    print("Width : %d px"% (width))
    print("Height : %d px"% (height))
    print("Planes : %d"% (planes))
    print("Bits Per Pixel : %d"% (bitsPerPixel))
    print("Compression : %d"% (compression))
    print("Image compressed size : %d"% (imageSizeCompressed))
    print("X Pixels Per M : %d"% (xPixelsPerM))
    print("Y Pixels Per M : %d"% (yPixelsPerM))
    print("Colors Used : %d"% (usedColors))
    print("Important Colors : %d"% (importantColors))
    print()
    if(compression == 0):
        return (bitsPerPixel,width*height,usedColors)
    else:
        return (bitsPerPixel,imageSizeCompressed,usedColors)
    
def readColorTable(colorTable):
    print("Color Table")
    i = 0
    while i < len(colorTable) and i+4 <= len(colorTable):
        oneCol = colorTable[i:i+4]
        r = oneCol[0]
        g = oneCol[1]
        b = oneCol[2]
        reserved = oneCol[3]

        print("color %03d - R:%03d G:%03d B:%03d Reserved:%d" %(i/4,r,g,b,reserved))
        i += 4
    print()

def readPixelData(pxDatas,bitsPerPixel,nbDraw = 10):
    print("Pixel Datas")

    if(bitsPerPixel > 8):
        
        bytePerPixel = int(bitsPerPixel/8)
        if(len(pxDatas) / bytePerPixel < nbDraw):
            nbDraw = len(pxDatas) / bytePerPixel
        for i in range(nbDraw):
            thisPxData = byteArrayToStr(pxDatas[i*bytePerPixel:(i+1)*bytePerPixel])
            print("Pixel %d = %s" % (i,thisPxData))

    else: #if file contains a color table
        #verify of nbDraw
        if(len(pxDatas) * bitsPerPixel < nbDraw):
            nbDraw = len(pxDatas) * bitsPerPixel

        #convert to binary
        bitString = byteArrayToBits(pxDatas)
        bitList = list(bitString)
        pixArr = list()
        b = 0
        currentPx = ""
        for bit in bitList:
            currentPx += bit
            b += 1
            if(b >= bitsPerPixel):
                pixArr.append(currentPx)
                currentPx = ""
                b = 0
            pass
        
        #print pixels
        i = 0
        for el in pixArr:
            print("Pixel %d = couleur N°%03d" % (i,int(el,2)))
            i+=1
            if(i >= nbDraw):
                break
            pass
    print()
