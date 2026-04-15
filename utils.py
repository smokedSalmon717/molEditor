import math


def makePointDiscreteAngle(uniqueAngles, x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    angle = (uniqueAngles * math.atan2(dx, dy))//(2*math.pi)
    angle *= (2*math.pi)/uniqueAngles
    x, y= 50*math.sin(angle), 50*math.cos(angle)
    return (x + x0, y + y0)



def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def getDoubleBondOffsetPoints(angle, pos, offset):
    x, y = pos
    up = (x - math.sin(angle)*offset, y + math.cos(angle)*offset)
    down = (x + math.sin(angle)*offset, y - math.cos(angle)*offset)
    return up, down


def moveGroup(group, dx, dy):
    #take in list of atoms as group, and moves them by dx, dy
    for atom in group:
        atom.pos = vectorSum(atom.pos, (dx, dy))

def vectorSum(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])
    
    
    