import os
import shutil

from PIL import Image, ImageEnhance
import glob
import numpy as np
import random

def rotateImage(folderName, fileName, degree):

    img = Image.open(f'{folderName}/images/{fileName}.jpg')
    match degree:
        case 'R90':
            flip_img = img.transpose(Image.ROTATE_90)
        case 'R180':
            flip_img = img.transpose(Image.ROTATE_180)
        case 'R270':
            flip_img = img.transpose(Image.ROTATE_270)
        case _:
            raise ValueError('Wrong Rotation Please use R90/R180/R270')
    flip_img.save(f'{folderName}/images/{fileName}{degree}.jpg')
    with open(f'{folderName}/labels/{fileName}.txt', 'r') as labelCoordinates:
        newCoordinates = open(f'{folderName}/labels/{fileName}{degree}.txt', 'a')
        for line in labelCoordinates:
            splitLine = line.rstrip("\n").split(" ")
            if len(splitLine) > 0:
                match degree:
                    case 'R90':
                        x = float(splitLine[1])
                        y = float(splitLine[2])
                        splitLine[1] = str(y)
                        splitLine[2] = str(1-x)
                        newCoordinates.write(' '.join(splitLine))
                        newCoordinates.write('\n')
                    case 'R180':
                        x = float(splitLine[1])
                        y = float(splitLine[2])
                        splitLine[1] = str(1-x)
                        splitLine[2] = str(1-y)
                        newCoordinates.write(' '.join(splitLine))
                        newCoordinates.write('\n')
                    case 'R270':
                        x = float(splitLine[1])
                        y = float(splitLine[2])
                        splitLine[1] = str(1-y)
                        splitLine[2] = str(x)
                        newCoordinates.write(' '.join(splitLine))
                        newCoordinates.write('\n')

def flipImage(folderName, fileName, orientation):
    img = Image.open(f'{folderName}/images/{fileName}.jpg')
    match orientation:
        case 'LeftRight':
            flip_img = img.transpose(Image.FLIP_LEFT_RIGHT)
        case 'TopBottom':
            flip_img = img.transpose(Image.FLIP_TOP_BOTTOM)
        case _:
            raise ValueError('Wrong Rotation Please use LeftRight/TopBottom')
    flip_img.save(f'{folderName}/images/{fileName}{orientation}.jpg')
    with open(f'{folderName}/labels/{fileName}.txt', 'r') as labelCoordinates:
        newCoordinates = open(f'{folderName}/labels/{fileName}{orientation}.txt', 'a')
        for line in labelCoordinates:
            splitLine = line.rstrip("\n").split(" ")
            if len(splitLine) > 0:
                match orientation:
                    case 'LeftRight':
                        splitLine[1] = str(1 - float(splitLine[1]))
                        newCoordinates.write(' '.join(splitLine))
                        newCoordinates.write('\n')
                    case 'TopBottom':
                        splitLine[2] = str(1 - float(splitLine[2]))
                        newCoordinates.write(' '.join(splitLine))
                        newCoordinates.write('\n')

def changeAllBrightness(folderName, allFiles):
    for file in allFiles:
        for percent in np.arange(0,2.5,.25):
            if percent != 0:
                changeImageAttribute(folderName,file,percent, 'brightness')

def changeAllConstrast(folderName, allFiles):
    for file in allFiles:
        for percent in np.arange(0,3.5,.25):
            if percent != 0:
                changeImageAttribute(folderName,file,percent, 'contrast')

def changeAllSharpness(folderName, allFiles):
    for file in allFiles:
        x = np.arange(-3,3.5,.25)
        for percent in x:
            if percent != 0:
                changeImageAttribute(folderName,file,percent, 'sharpness')

def changeImageAttribute(folderName, imagePath, percent, mode):
    global enhancer
    img = Image.open(imagePath)
    match mode:
        case 'brightness':
            enhancer = ImageEnhance.Brightness(img)
        case 'contrast':
            enhancer = ImageEnhance.Contrast(img)
        case 'sharpness':
            enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(percent)
    imageName = os.path.basename(imagePath)[:-4]
    img.save(f'{folderName}/images/{imageName}{mode}{percent}.jpg')
    with open(f'{folderName}/labels/{imageName}.txt') as original:
        with open(f'{folderName}/labels/{imageName}{mode}{percent}.txt', 'w') as copy:
            for line in original:
                if len(line) > 0:
                    copy.write(line)
def manipulateAll(folderName, fileName):
    rotateImage(folderName, fileName, 'R90')
    rotateImage(folderName, fileName, 'R180')
    rotateImage(folderName, fileName, 'R270')
    flipImage(folderName, fileName, 'LeftRight')
    flipImage(folderName, fileName, 'TopBottom')
    #allFiles = glob.glob(f'{folderName}/images/{fileName}*.jpg')
    #changeAllSharpness(folderName,allFiles)
    #changeAllConstrast(folderName,allFiles)
    #changeAllBrightness(folderName,allFiles)

def shuffleFilesIntoDataSet(folderName):
    allFiles = glob.glob(f'{folderName}/images/*.jpg')
    amountTrain = int(len(allFiles)*0.6)
    amountVal = int((len(allFiles)-amountTrain)/2)
    amountTest = amountVal
    for i in range(0, amountTrain):
        choosenFile = random.choice(allFiles)
        shutil.copy(choosenFile,'todo/dataset/train/images')
        shutil.copy(f'todo/labels/{os.path.basename(choosenFile)[:-4]}.txt','todo/dataset/train/labels')
        allFiles.remove(choosenFile)
    for i in range(0, amountVal):
        choosenFile = random.choice(allFiles)
        shutil.copy(choosenFile, 'todo/dataset/valid/images')
        shutil.copy(f'todo/labels/{os.path.basename(choosenFile)[:-4]}.txt', 'todo/dataset/valid/labels')
        allFiles.remove(choosenFile)
    for i in range(0, amountTest):
        choosenFile = random.choice(allFiles)
        shutil.copy(choosenFile, 'todo/dataset/test/images')
        shutil.copy(f'todo/labels/{os.path.basename(choosenFile)[:-4]}.txt', 'todo/dataset/test/labels')
        allFiles.remove(choosenFile)


if __name__ == '__main__':
    print (len([name for name in os.listdir('todo/images') if os.path.isfile(os.path.join('todo/images', name))]))
    for files in glob.glob('todo/images/*.jpg'):
        fileName = os.path.basename(files)[:-4]
        manipulateAll('todo', fileName)
    print (len([name for name in os.listdir('todo/images') if os.path.isfile(os.path.join('todo/images', name))]))
    shuffleFilesIntoDataSet('todo')

