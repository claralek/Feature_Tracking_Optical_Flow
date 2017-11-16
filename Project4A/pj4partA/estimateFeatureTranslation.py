'''
  File name: estimateFeatureTranslation.py
  Author:
  Date created:
'''

import cv2
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import inv
from scipy import interpolate
from detectFace import detectFace
from getFeatures import getFeatures

'''
  File clarification:
    Estimate the translation for single features 
    - Input startX: the x coordinate for single feature wrt the first frame
    - Input startY: the y coordinate for single feature wrt the first frame
    - Input Ix: the gradient along the x direction
    - Input Iy: the gradient along the y direction
    - Input img1: the first image frame
    - Input img2: the second image frame
    - Output newX: the x coordinate for the feature wrt the second frame
    - Output newY: the y coordinate for the feature wrt the second frame
'''

def estimateFeatureTranslation(startX, startY, Ix, Iy, img0, img1):
  gray0 = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
  gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
  It =gray1 -gray0

  # Ax =b => x =inv(A)b
  It_w =It[startX-5:startX+5, startY-5:startY+5]
  Ix_w =Ix[startX-5:startX+5, startY-5:startY+5]
  Iy_w =Iy[startX-5:startX+5, startY-5:startY+5]
  IxIx = np.sum(np.dot(Ix_w, Ix_w))
  IyIy = np.sum(np.dot(Iy_w, Iy_w))
  IxIy = np.sum(np.dot(Ix_w, Iy_w))
  IxIt = np.sum(np.dot(Ix_w, It_w))
  IyIt = np.sum(np.dot(Iy_w, It_w))
  A =np.array([[IxIx, IxIy], [IxIy, IyIy]])
  b =np.array([[IxIt], [IyIt]])*(-1)
  [u, v] =np.dot(inv(A), b)

  newX =startX +u
  newY =startY +v

  plt.figure(0)
  plt.subplot(121)
  plt.imshow(img0)
  plt.plot(startY, startX, 'ro')
  plt.axis('off')
  plt.subplot(122)
  plt.imshow(img1)
  plt.plot(newY, newX, 'ro')
  plt.axis('off')
  plt.show()

  return newX, newY
