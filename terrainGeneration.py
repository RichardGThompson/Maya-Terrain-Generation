import maya.cmds as cmds
import random
import math

# NOTES:
# Z=Height
# X=Width
# Perlin Noise Algorithim based on: https://rtouti.github.io/graphics/perlin-noise-algorithm

'''----- GLOBAL VARAIBLES -----'''
randomNumberRange = [-1.0,1.5]

amplitude = 1.2
ordFreq = 1.5
angFreq = 2 * math.pi * ordFreq
phase = 1

if 'ui' in globals():
    if cmds.window(ui, exists=True):
        cmds.deleteUI(ui, window=True)

ui = cmds.window(title='Terrain Generation', width=400)

cmds.columnLayout(rowSpacing=10)
cmds.text(label='Terrain Generator')

cmds.intSliderGrp('width', label='Width', min=1, max=25)
cmds.intSliderGrp('height', label='Length', min=1, max=25)
cmds.intSliderGrp('subD', label='Subdivision Density', min=1, max=3)

cmds.button(label='Generate Terrain', command='generateTerrain()')

cmds.showWindow(ui)

def vectorFromPoints(pointA, pointB):
    return[pointB[0] - pointA[0], pointB[1] - pointA[1], pointB[2] - pointA[2]]

def getDotProduct(vectorA, vectorB):
    return ((vectorA[0] * vectorB[0]) + (vectorA[1] * vectorB[1]) + (vectorA[2] * vectorB[2]))

def setSinHeight(tValue):
    return(amplitude*math.sin((angFreq*tValue)+phase))

def getVtxId(xValueIn, zValueIn, xCountIn, zCountIn):
    return((zCountIn * zValueIn) + xValueIn)

# Create the range of height values randomly for x and z
def createPermutation():
    p = []
    # Create the x values
    for i in range(256):
        p.append(i)
    random.shuffle(p)
    # Create the z values
    for i in range(256):
        p.append(p[i])
    
    return p

def Noise2D(x,z):
    X = math.floor(x) & 255
    Z = math.floor(z) & 255

    xFloor = x - math.floor(x)
    zFloor = z - math.floor(z)

    tRight = [xFloor-1.0, zFloor-1.0]
    tLeft = [xFloor, zFloor-1.0]
    bRight = [xFloor-1.0, zFloor]
    bLeft = [xFloor, zFloor]

    tRightDot = getDotProduct

def generateTerrain():
    # Get the values from the ui
    pWidth = cmds.intSliderGrp('width', query=True, value=True)
    pHeight = cmds.intSliderGrp('height', query=True, value=True)
    pSubDensity = cmds.intSliderGrp('subD', query=True, value=True)

    # Create a plane based on the user input
    pTerrain = cmds.polyPlane(width=pWidth, height=pHeight, subdivisionsX=pWidth*pSubDensity, subdivisionsY=pHeight*pSubDensity)

    terrainHeights = []
    tempList = []

    vtx = getVtxId(0,0,(pWidth * pSubDensity)+1, (pHeight * pSubDensity)+1)
    print('VTX: {}'.format(vtx))
    cmds.select('{}.vtx[{}]'.format(pTerrain[0], vtx))

    perms = createPermutation()

    # print('createPerm: {} len: {}'.format(perms, len(perms)))

    # Go though each of the z values
    for z in range((pHeight * pSubDensity) + 1):
        for x in range((pWidth * pSubDensity) + 1):
            n = Noise2D(x*0.01, z*0.01)
            # As we are working in 2 dimensions, Noise2D will return values from -1.0f to 1.0f, we can map this to a range that we want later.



            

