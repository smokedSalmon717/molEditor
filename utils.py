import math


def makePointDiscreteAngle(uniqueAngles, x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    angle = (uniqueAngles * math.atan2(dx, dy))//(2*math.pi)
    angle *= (2*math.pi)/uniqueAngles
    x, y= 50*math.sin(angle), 50*math.cos(angle)
    return (x + x0, y + y0)

def deleteSelectedAtoms(app):
    for atom in app.selectedAtomList:
        deleteBondReferencesInOtherAtoms(atom)
        app.atoms.remove(atom) 
    app.selectedAtomList = [] 


def deleteBondReferencesInOtherAtoms(self):
    for partner in self.bonds:
        partner.bonds.pop(self)

def moveGroup(group, dx, dy):
    #take in list of atoms as group, and moves them by dx, dy
    for atom in group:
        atom.pos = vectorSum(atom.pos, (dx, dy))

#This function is written by AI, documentation made partially by hand
def point_to_segment_distance(px, py, x1, y1, x2, y2): 
    # Vector AB
    dx = x2 - x1
    dy = y2 - y1

    # Handle degenerate case (A == B)
    if dx == 0 and dy == 0:
        return math.hypot(px - x1, py - y1)

    # Projection factor
    t = ((px - x1) * dx + (py - y1) * dy) / (dx*dx + dy*dy)
    #This is the dot product of the bond represented as a vector
    #and the 

    # Clamp to segment
    t = max(0, min(1, t))

    # Closest point
    cx = x1 + t * dx
    cy = y1 + t * dy

    # Distance
    return math.hypot(px - cx, py - cy)

def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def getDoubleBondOffsetPoints(angle, pos, offset):
    x, y = pos
    up = (x - math.sin(angle)*offset, y + math.cos(angle)*offset)
    down = (x + math.sin(angle)*offset, y - math.cos(angle)*offset)
    return up, down



def vectorSum(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])
    

def polygonRadius(n, s):
    return s / (2 * math.sin(math.pi / n))


def makeVector(p1, p0):
    x0, y0 = p0
    x1, y1 = p1
    return (x0 - x1, y0 - y1)


#written by ChatGPT, though I changed the names to match my conventions
#I  do understand the math, just didn't feel like figuring out the signs in our sign convention
def rotateVector(vector, angle):
    x, y = vector
    cosT = math.cos(angle)
    sinT = math.sin(angle)

    xNew = x * cosT + y * sinT
    yNew = -x * sinT + y * cosT

    return (xNew, yNew)




def buttonCheck(app, x, y):
    for button in app.buttons:
        if button.checkClick():
            updateButtonStates(app, button)





def normalizeVector(x, y, length):
    scalar = length / math.hypot(x, y)
    return scalar * x, scalar * y



    
    