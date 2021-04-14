import maya.cmds as cmds
import random
import math

# Perlin Noise Algorithim based on: https://rtouti.github.io/graphics/perlin-noise-algorithm

'''----- GLOBAL VARAIBLES -----'''
yNormalVectorThreshold = 0.985

# Set up all of the UI elements
if 'ui' in globals():
    if cmds.window(ui, exists=True):
        cmds.deleteUI(ui, window=True)

ui = cmds.window(title='Terrain Generation', width=400)

cmds.columnLayout(rowSpacing=10)
cmds.text(label='Terrain Generator')

# Set up all of the sliders that are needed
cmds.intSliderGrp('width', label='Width', min=10, max=25)
cmds.intSliderGrp('height', label='Length', min=10, max=25)
cmds.intSliderGrp('subD', label='Subdivision Density', min=1, max=3)
cmds.floatSliderGrp('minHeight', label='Min Terrain Height', min=-2.0, max=0.0)
cmds.floatSliderGrp('maxHeight', label='Max Terrain Height', min=1.0, max=2.0)
cmds.floatSliderGrp('groundWidth', label='Ground Plane Width', min=2.0, max=8.0)
cmds.floatSliderGrp('foliageDensity', label='Foliage Density', min=0.0, max= 1.0)

# When the user presses this button the program will call on the generateTerrain method
cmds.button(label='Generate Terrain', command='generateTerrain()')

cmds.showWindow(ui)

def moveGrassObject(objectNumber):
    majorPositionVal = random.uniform(1.0, 2.5)
    minorPositionVal = random.uniform(-0.5, 0.5)

    if(objectNumber == 1):
        cmds.move(majorPositionVal, 0, minorPositionVal, r=True)
    elif(objectNumber == 2):
        cmds.move(-majorPositionVal, 0, minorPositionVal)
    elif(objectNumber == 3):
        cmds.move(minorPositionVal,0,majorPositionVal)
    elif(objectNumber == 4):
        cmds.move(minorPositionVal,0,-majorPositionVal)

def generateGrass(numberOfGrassObjects):
    # Create list to hold the objects within the grass to be created
    grassObjects = []
    # Make a grass object for each part
    for i in range(numberOfGrassObjects):
        # Start by creating a new object for the grass to be built with
        grassObjects.append(cmds.polyCube(w=1, h=0.01, d=1))
        # Move the object into a position accordingly
        if (i != 0):moveGrassObject(i)

        # Make the grass do grass things...
        grassSegments = random.randint(3,7)
        currentName = grassObjects[len(grassObjects) - 1][0]
        cmds.select('{}.f[{}]'.format(currentName, 1))  
        # Randomly extrude and position the grass
        for i in range(grassSegments):
            translateList = [random.uniform(-0.5, 0.5),random.uniform(-0.5, 0.5),random.uniform(0.5,1.5)]
            cmds.polyExtrudeFacet(localTranslate=translateList, localScale=(0.7,0.7,0.7))
    

    # Now that we have all of the grass that we need generated we can now group it all and return it
    for grass in grassObjects:
        cmds.select(grass[0], tgl=True)
    
    grassGrp = cmds.polyUnite(ch=False)
    cmds.select(grassGrp[0])

    # My smooth brain made the grass way too big, so let's scale it down afterwards and pretend nothing happened, it will be fine
    scaleValue = random.uniform(0.02,0.1)
    cmds.scale(scaleValue,scaleValue,scaleValue)

    return grassGrp

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
    # Local Varaibles
    terrainHeights = []
    tempList = []
    perlinCount = 0
    
    # Get the values from the ui
    pWidth = cmds.intSliderGrp('width', query=True, value=True)
    pHeight = cmds.intSliderGrp('height', query=True, value=True)
    pSubDensity = cmds.intSliderGrp('subD', query=True, value=True)
    pMinHeight = cmds.floatSliderGrp('minHeight', query=True, value=True)
    pMaxHeight = cmds.floatSliderGrp('maxHeight', query=True, value=True)
    pFoliageDensity = cmds.floatSliderGrp('foliageDensity', q=True, value=True)

    # Create a plane based on the user input
    pTerrain = cmds.polyPlane(width=pWidth, height=pHeight, subdivisionsX=pWidth*pSubDensity, subdivisionsY=pHeight*pSubDensity)

    # Create the permutations needed for the perlin noise algorithim
    perms = createPermutation()

    # Go through each of the verts in the plane and modify them by passing the x/z values into the perlin noise algorithim
    for z in range((pHeight * pSubDensity) + 1):
        for x in range((pWidth * pSubDensity) + 1):
            n = Noise2D(x*0.05, z*0.05, perms)
            # As we are working in 2 dimensions, Noise2D will return values from -1.0f to 1.0f, we can map this to a range that we want later
            n = mapValue(0.0, 1.0, pMinHeight, pMaxHeight, n)
            cmds.select('{}.vtx[{}]'.format(pTerrain[0], perlinCount))
            cmds.move(0,n,0,r=True)
            perlinCount+=1
    
    # Center the pivot point before moving forwards...
    cmds.xform(pTerrain[0], cp=True)

    # Determine how many verts are in x and z
    zRows = (pHeight * pSubDensity) + 1
    xRows = (pWidth * pSubDensity) + 1

    # Determine the x row value for the center of the plane
    xOffset = int(math.ceil(xRows/2.0))
    # Make sure the current selection is clear before moving forwards
    clearSelection()
    
    # Select each of the verts in the Z axis offset by xOffset
    for i in range(zRows):
        vtxId = (xRows * i) + xOffset
        cmds.select('{}.vtx[{}]'.format(pTerrain[0], vtxId), tgl=True)
    
    # Soft select the verts, with a soft selection distance by the user input
    cmds.softSelect(sse=True,ssd=cmds.floatSliderGrp('groundWidth', query=True, value=True), sud=0.5)
    # Flatten the terrain
    cmds.scale(1, 0.00001, 1, r=True)
    # Ensure that soft selection is disabled and clear the current selection
    cmds.softSelect(sse=False)
    clearSelection()

    # Figure out wich of the faces are flat enough for trees to be placed on them.
    # To start let's look at the neighboring faces where the flattening was performed
    
    # NOTE: CLEAN THIS SHIT UP, CODE BAD, UGLY, GROSS
    # zFaces = zRows - 1
    # xFaces = xRows - 1
    centerFaces = [(zRows - 1), (xRows - 1)]

    # The number of faces to check on either side of the center
    neighborsToCheckCount = 3
    xFaceOffsetList = []
    faceIdList = []

    tmpXOffset = (xOffset - 1) - (neighborsToCheckCount - 1)

    # Create a list of x offsets that need to be checked later
    for i in range((neighborsToCheckCount*2) + 1):
        xFaceOffsetList.append(tmpXOffset)
        tmpXOffset += 1
    # Append the IDs of the center faces to be checked
    for offset in xFaceOffsetList:
        for i in range(centerFaces[0]):
            faceIdList.append((centerFaces[1] * i) + offset)

    # A list to store the list of faces that foliage can be placed on
    foliageFaces = []
    
    # Check to see what faces are able to have foilage on them based on their y value of the normal vector
    for faceId in faceIdList:
        faceVerts = []
        vertSequences = []
        normalVectors = []

        for element in getVertices(pTerrain[0], faceId):
            if element:
                faceVerts.append(element)

        # Because we have created a plane with quads we can create 2 vert sequences to check (A,B,C and A,C,D)
        vertSequences.append([faceVerts[0], faceVerts[1], faceVerts[2]])
        vertSequences.append([faceVerts[0], faceVerts[2], faceVerts[3]])
        
        for triangleVertices in vertSequences:
            # Get all the information that we need about the triangle
            triangleNormalVector = getNormalVector(triangleVertices)
            normalVectors.append(triangleNormalVector)

        # Get the averaged normal vector from the face
        faceNormal = averageVectors(normalVectors)

        # If the y normal of the face is greater or equal to the preset threshold then append it to the list of foliage faces
        if faceNormal[1] >= yNormalVectorThreshold:
            foliageFaces.append(faceId)
    # Determine how much foliage should be placed by taking the number of compatable foliage faces and multiplying it by the user-set foliage density value (0.0 to 1.0)
    foliageFacesCount = int(math.ceil(len(foliageFaces) * pFoliageDensity))
    
    # To make sure we don't cause an inf loop, make sure the count is not bigger than the actual avaiable to select
    if foliageFacesCount > len(foliageFaces):
        foliageFacesCount = len(foliageFaces)
    
    # A list that will contain the IDs of the faces to have foliage placed on them
    foliageFacesToAddGrass = []

    # Based on the number of foliage to be created, randomly assign IDs
    for i in range(foliageFacesCount):
        # Okay so this really isn't the best way to go about this, it is wildly inefficient, but it works. Also, insert Silicon Valley reference here: https://youtu.be/KmHZMiohXVM?t=85
        # Set the index value to a random value from 0 to the size of the foliageFaces list
        index = random.randint(0, len(foliageFaces) - 1)
        # Make sure the selected index value isn't already in the list
        if index not in foliageFacesToAddGrass:
            # Append the ID based on the index of the foliageFaces list
            foliageFacesToAddGrass.append(foliageFaces[index])

    # Go through each of the faces that need foliage added to them and add it
    for foliageFaceId in foliageFacesToAddGrass:
        cmds.select('{}.f[{}]'.format(pTerrain[0], foliageFaceId), tgl=True)
        
        # Create a new grass object with a random number of parts
        grassObject = generateGrass(random.randint(2,5))

        # Get the center of the face
        cmds.select('{}.f[{}]'.format(pTerrain[0], foliageFaceId))
        sel = cmds.ls(sl=True)
        faceValues = cmds.xform(sel, q=True, ws=True, t=True)
        
        bottomLeftPoint = [faceValues[0], faceValues[1], faceValues[2]]
        bottomRightPoint = [faceValues[3], faceValues[4], faceValues[5]]
        topLeftPoint = [faceValues[6], faceValues[7], faceValues[8]]
        topRightPoint = [faceValues[9], faceValues[10], faceValues[11]]

        # Average the points of the face to the the center
        centerPoint = [0,0,0]
        centerPoint[0] = (bottomLeftPoint[0] + bottomRightPoint[0] + topLeftPoint [0] + topRightPoint[0]) / 4
        centerPoint[1] = (bottomLeftPoint[1] + bottomRightPoint[1] + topLeftPoint [1] + topRightPoint[1]) / 4
        centerPoint[2] = (bottomLeftPoint[2] + bottomRightPoint[2] + topLeftPoint [2] + topRightPoint[2]) / 4

        # Move the grass to the center of the face
        cmds.select(grassObject[0])
        cmds.move(centerPoint[0], centerPoint[1], centerPoint[2], ws=True)