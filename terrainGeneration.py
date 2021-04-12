import maya.cmds as cmds
import random
import math

# NOTES:
# Z=Height
# X=Width
# Perlin Noise Algorithim based on: https://rtouti.github.io/graphics/perlin-noise-algorithm

'''----- GLOBAL VARAIBLES -----'''
yNormalVectorThreshold = 0.985

if 'ui' in globals():
    if cmds.window(ui, exists=True):
        cmds.deleteUI(ui, window=True)

ui = cmds.window(title='Terrain Generation', width=400)

cmds.columnLayout(rowSpacing=10)
cmds.text(label='Terrain Generator')

cmds.intSliderGrp('width', label='Width', min=1, max=25)
cmds.intSliderGrp('height', label='Length', min=1, max=25)
cmds.intSliderGrp('subD', label='Subdivision Density', min=1, max=3)
cmds.floatSliderGrp('minHeight', label='Min Terrain Height', min=-2.0, max=0.0)
cmds.floatSliderGrp('maxHeight', label='Max Terrain Height', min=1.0, max=2.0)
cmds.floatSliderGrp('groundWidth', label='Ground Plane Width', min=2.0, max=8.0)

cmds.button(label='Generate Terrain', command='generateTerrain()')

cmds.showWindow(ui)

def getVertices(object, faceID):
    vertexIDs = cmds.polyInfo('{}.f[{}]'.format(object, faceID), faceToVertex=True)
    vertexIDs = str(vertexIDs).split()
    vertexA = cmds.xform('{}.vtx[{}]'.format(object, vertexIDs[2]), query=True, translation=True, worldSpace=True)
    vertexB = cmds.xform('{}.vtx[{}]'.format(object, vertexIDs[3]), query=True, translation=True, worldSpace=True)
    vertexC = cmds.xform('{}.vtx[{}]'.format(object, vertexIDs[4]), query=True, translation=True, worldSpace=True)
    vertexD = []
    if(len(vertexIDs) == 7):
        vertexD = cmds.xform('{}.vtx[{}]'.format(object, vertexIDs[5]), query=True, translation=True, worldSpace=True)

    return [vertexA, vertexB, vertexC, vertexD]

def vectorFromPoints(pointA, pointB):
    return[pointB[0] - pointA[0], pointB[1] - pointA[1], pointB[2] - pointA[2]]

def getVectorMagnitude(vector):
    return((vector[0] ** 2) + (vector[1] ** 2) + (vector[2] ** 2)) ** 0.5

def getCrossProduct(vectorA, vectorB):
    crossProduct = [0.0,0.0,0.0]
    crossProduct[0] = (vectorA[1] * vectorB[2]) - (vectorA[2] * vectorB[1])
    crossProduct[1] = (vectorA[2] * vectorB[0]) - (vectorA[0] * vectorB[2])
    crossProduct[2] = (vectorA[0] * vectorB[1]) - (vectorA[1] * vectorB[0])
    return crossProduct

def getNormalVector(triangleVerticies):
    vectorA = vectorFromPoints(triangleVerticies[0], triangleVerticies[1])
    vectorB = vectorFromPoints(triangleVerticies[0], triangleVerticies[2])
    crossProduct = getCrossProduct(vectorA, vectorB)
    magnitude = getVectorMagnitude(crossProduct)
    return [crossProduct[0] / magnitude, crossProduct[1] / magnitude, crossProduct[2] / magnitude]

def vectorFromPoints(pointA, pointB):
    return[pointB[0] - pointA[0], pointB[1] - pointA[1], pointB[2] - pointA[2]]

def getDotProduct(vectorA, vectorB):
    return ((vectorA[0] * vectorB[0]) + (vectorA[1] * vectorB[1]))

def setSinHeight(tValue):
    return(amplitude*math.sin((angFreq*tValue)+phase))

def getVtxId(xValueIn, zValueIn, xCountIn, zCountIn):
    return((zCountIn * zValueIn) + xValueIn)


def averageVectors(vectorsIn):
    # Create a vector to store the averaged values
    averagedVector = [0,0,0]
    # Tracking the current axis values are being added to
    axisCount = 0
    # Go through each of the vectors contained in vectorsIn
    for vector in vectorsIn:
        # Reset the axisCount before moving to the first/next vector
        axisCount = 0
        # Get the value from each axis in the vector and add them to the vector to be averaged
        for val in vector:
            averagedVector[axisCount] += val
            # Increment the axisCounter
            axisCount += 1
    
    # Average each of the axies of the vector
    for i in range(len(averagedVector)):
        averagedVector[i] = averagedVector[i] / len(vectorsIn)
    
    return averagedVector

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

def lerpValues(t, a1, a2):
    return (a1 + t*(a2-a1))

def fade(t):
    return((6*t - 15)*t + 10)*t*t*t

def getConstantVector(v):
    h = int(v) & 3
    if(h == 0):
        return [1.0,1.0]
    elif(h == 1):
        return [-1.0, 1.0]
    elif(h == 2):
        return [-1.0,-1.0]
    else:
        return [1.0,-1.0]

# A function to map a number from one range, to another range. Code adapted from: https://stackoverflow.com/questions/12931115/algorithm-to-map-an-interval-to-a-smaller-interval/12931306
def mapValue(originLow, originHigh, newLow, newHigh, valueIn):
    return (valueIn - originLow)*(newHigh-newLow)/(originHigh-originLow) + newHigh 

def Noise2D(x,z,permIn):
    X = int(math.floor(x)) & 255
    Z = int(math.floor(z)) & 255

    xFloor = x - math.floor(x)
    zFloor = z - math.floor(z)

    tRight = [xFloor-1.0, zFloor-1.0]
    tLeft = [xFloor, zFloor-1.0]
    bRight = [xFloor-1.0, zFloor]
    bLeft = [xFloor, zFloor]

    valTRight = permIn[permIn[X+1]+Z+1]
    valTLeft = permIn[permIn[X]+Z+1]
    valBRight = permIn[permIn[X+1]+Z]
    valBLeft = permIn[permIn[X]+Z]

    dotTRight = getDotProduct(tRight, getConstantVector(valTRight))
    dotTLeft = getDotProduct(tLeft, getConstantVector(valTLeft))
    dotBRight = getDotProduct(bRight, getConstantVector(valBRight))
    dotBLeft = getDotProduct(bLeft, getConstantVector(valBLeft))

    u = fade(xFloor)
    v = fade(zFloor)

    return lerpValues(u, lerpValues(v, dotBLeft, dotTLeft), lerpValues(v, dotBRight, dotTRight))

# This is purley because I don't want to write out the command everytime, pure laziness...
def clearSelection():
    cmds.select(clear=True)

def generateTerrain():
    # Get the values from the ui
    pWidth = cmds.intSliderGrp('width', query=True, value=True)
    pHeight = cmds.intSliderGrp('height', query=True, value=True)
    pSubDensity = cmds.intSliderGrp('subD', query=True, value=True)
    pMinHeight = cmds.floatSliderGrp('minHeight', query=True, value=True)
    pMaxHeight = cmds.floatSliderGrp('maxHeight', query=True, value=True)

    # Create a plane based on the user input
    pTerrain = cmds.polyPlane(width=pWidth, height=pHeight, subdivisionsX=pWidth*pSubDensity, subdivisionsY=pHeight*pSubDensity)

    terrainHeights = []
    tempList = []

    vtx = getVtxId(0,0,(pWidth * pSubDensity)+1, (pHeight * pSubDensity)+1)
    cmds.select('{}.vtx[{}]'.format(pTerrain[0], vtx))

    perms = createPermutation()

    # print('createPerm: {} len: {}'.format(perms, len(perms)))
    count = 0

    # Go though each of the z values
    for z in range((pHeight * pSubDensity) + 1):
        for x in range((pWidth * pSubDensity) + 1):
            #print('x: {}'.format(x))
            n = Noise2D(x*0.05, z*0.05, perms)
            #print('n val: {}'.format(n))
            # As we are working in 2 dimensions, Noise2D will return values from -1.0f to 1.0f, we can map this to a range that we want later.
            n = mapValue(0.0, 1.0, pMinHeight, pMaxHeight, n)
            cmds.select('{}.vtx[{}]'.format(pTerrain[0], count))
            cmds.move(0,n,0,r=True)
            count+=1
    
    # Center the pivot point before moving forwards...
    cmds.xform(pTerrain[0], cp=True)
    
    # TESTING OF CREATING A GROUND PLANE ALONG THE Z AXIS!

    # See if we are able to select a whole row of verts...
    # First we need to figure out how many verts are in x and z
    zRows = (pHeight * pSubDensity) + 1
    xRows = (pWidth * pSubDensity) + 1

    #Now that we know how many verts are in each dimension we can now select a whole-ass row of them (maybe)
    xOffset = int(math.ceil(xRows/2.0))
    print('xOffset: {}'.format(xOffset))
    # Make sure the current selection is clear before moving forwards
    clearSelection()
    # Iterate through each of the verts in the z

    for i in range(zRows):
        vtxId = (xRows * i) + xOffset
        cmds.select('{}.vtx[{}]'.format(pTerrain[0], vtxId), tgl=True)
    
    cmds.softSelect(sse=True,ssd=cmds.floatSliderGrp('groundWidth', query=True, value=True), sud=0.5)

    cmds.scale(1, 0.00001, 1, r=True)

    cmds.softSelect(sse=False)

    clearSelection()

    # Figure out wich of the faces are flat enough for trees to be placed on them.
    # To start let's look at the neighboring faces where the flattening was performed
    
    # NOTE: CLEAN THIS SHIT UP, CODE BAD, UGLY, GROSS
    zFaces = zRows - 1
    xFaces = xRows - 1

    xFaceOffset = xOffset - 1

    # Check n on each side
    neighborsToCheckCount = 3
    xFaceOffsetList = []
    faceIdList = []

    tmpXOffset = xFaceOffset - (neighborsToCheckCount - 1)

    for i in range((neighborsToCheckCount*2) + 1):
        xFaceOffsetList.append(tmpXOffset)
        tmpXOffset += 1

    for offset in xFaceOffsetList:
        for i in range(zFaces):
            faceIdList.append((xFaces * i) + offset)

    foliageFaces = []
    
    # Check to see what faces are able to have foilage on them based on their y value of the normal vector.
    for faceId in faceIdList:
        faceVerts = []
        vertSequences = []
        normalVectors = []

        for element in getVertices(pTerrain[0], faceId):
            if element:
                faceVerts.append(element)

        if len(faceVerts) == 4:
            vertSequences.append([faceVerts[0], faceVerts[1], faceVerts[2]])
            vertSequences.append([faceVerts[0], faceVerts[2], faceVerts[3]])
        elif len(faceVerts) == 3:
            vertSequences.append([faceVerts[0], faceVerts[1], faceVerts[2]])
        
        for triangleVertices in vertSequences:
            # Get all the information that we need about the triangle
            triangleNormalVector = getNormalVector(triangleVertices)
            normalVectors.append(triangleNormalVector)

        # Get the averaged normal vector from the face
        faceNormal = averageVectors(normalVectors)
        

        if faceNormal[1] >= yNormalVectorThreshold:
            foliageFaces.append(faceId)
    
    # Print out what faces are compatable
    print('Compatable faces: {}'.format(foliageFaces))

    for face in foliageFaces:
        cmds.select('{}.f[{}]'.format(pTerrain[0], face), tgl=True)

    

    


            

