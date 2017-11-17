'''
  File name: estimateFeatureTranslation.py
  Author:
  Date created:
'''

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

from basic_packages import *
from helper import *

def estimateFeatureTranslation(startX, startY, Ix, Iy, img1, img2):
    #                   IxIx IxIy   u          Itx   
    # Apply the formula                 =  -
    #                   IyIx IyIy   v          Ity
    # For each x and y, create a patch of window 10*10)


    m, n = img1.shape

    # calculate temperate gradient
    It = img2 - img1;

    # Padding with mirror length = 5
    Ix_pad = np.pad(Ix,5,'symmetric')
    Iy_pad = np.pad(Iy,5,'symmetric')
    It_pad = np.pad(It,5,'symmetric')

    patch_Ix = Ix_pad[startX:startX+10,startY:startY+10]
    patch_Iy = Iy_pad[startX:startX+10,startY:startY+10]
    patch_It = It_pad[startX:startX+10,startY:startY+10]

    IxIx = np.sum(np.dot(patch_Ix,patch_Ix))
    IxIy = np.sum(np.dot(patch_Ix,patch_Iy))
    IyIy = np.sum(np.dot(patch_Iy,patch_Iy))
    ItIx = np.sum(np.dot(patch_Ix,patch_It))
    ItIy = np.sum(np.dot(patch_Iy,patch_It))

    # matrix
    H_inv = np.linalg.inv(np.asarray(([IxIx,IxIy],[IxIy,IyIy])))
    b  = np.asarray([ItIx,ItIy])

    # compute u v 
    A   = -np.dot(H_inv,b)
    u,v = A[0],A[1]
    
    # Interpolation
    meshX,meshY = np.meshgrid(np.arange(0,m),np.arange(0,n))
    meshX = meshX.flatten()
    meshY = meshY.flatten()
    newPoint = np.concatenate((meshX+u,meshY+v))
    pdb.set_trace()
    newPosition = interpolate.interp2d(meshX,meshY,newPoint)
    newX_matrix,newY_matrix = newPosition[0:m*n],newPosition[m*n,newPosition.size]
    newX = newX_matrix.reshape(m,n)[startX][startY]
    newY = newY_matrix.reshape(m,n)[startX][startY]
 
    
    return newX, newY