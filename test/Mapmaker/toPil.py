# Classifying Segmenter 1
# classifySeg1.py
# Author: Steve Matsumoto
# 16 June 2010
# This file is part of the HMC PixelLaser research project.
# Advisor: Zach Dodds

import cv
import Image

import Classifier as classifier

WIDTH = 640
WRES = 40
HEIGHT = 480
HRES = 40
ACOLOR = (0.0, 0.0, 255.0)
BCOLOR = (255.0, 0.0, 0.0)
PATCHSIZE = 20

def segment(im):
    segpts = []
    classify = classifier.Classifier(['dAbove.txt', 'dBelow.txt'], ['above', 'below'], 'weights.txt', 5)
    for col in range(0, WIDTH-WRES, WRES):
        for row in range(0, HEIGHT-HRES, HRES):
            #print "row:", row
            #print "col:", col
            patch = cv.GetSubRect(im, (col, row, PATCHSIZE, PATCHSIZE))
            Image.fromstring("RGB", cv.GetSize(patch), patch.tostring())
    return im
