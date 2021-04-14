import maya.cmds as cmds
import random
import math

debugging = True

def moveObject(objectNumber):
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
    grassObjects = []
    for i in range(numberOfGrassObjects):
        # Start by creating a new object for the grass to be built with
        grassObjects.append(cmds.polyCube(w=1, h=0.01, d=1))
        # Move the object into a position accordingly
        if (i != 0):moveObject(i)

        # Make the grass do grass things...
        grassSegments = random.randint(3,7)
        currentName = grassObjects[len(grassObjects) - 1][0]
        cmds.select('{}.f[{}]'.format(currentName, 1))  
        # Randomly extrude and position the grass
        for i in range(grassSegments):
            translateList = [random.uniform(-0.5, 0.5),random.uniform(-0.5, 0.5),random.uniform(0.5,1.5)]
            cmds.polyExtrudeFacet(localTranslate=translateList, localScale=(0.7,0.7,0.7))
    

if debugging:
    generateGrass(5)
else:
    generateGrass(random.randint(1,5))