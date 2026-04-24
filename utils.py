import math
#from objects.buttons import Button

def checkIfHoveringOverObject(app, x, y):
    objects = app.buttons + app.atoms + app.bonds
    for object in objects:
        if object.isInside(x, y):
            return object
        

def isWithinAtom(app, x, y):
    for atom in app.atoms:
        if atom.isInside(x, y):
            return atom

def makePointDiscreteAngle(uniqueAngles, x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    angle = (uniqueAngles * math.atan2(dx, dy))//(2*math.pi)
    angle *= (2*math.pi)/uniqueAngles
    x, y= 50*math.sin(angle), 50*math.cos(angle)
    return (x + x0, y + y0)

def deleteSelectedAtoms(app):
    for atom in app.selectedAtomList:
        app.atoms.remove(atom)
        for bond in atom.bonds:
            app.bonds.remove(bond)
            for entry in bond.atoms:
                entry.bonds.remove(bond)


    app.selectedAtomList = [] 



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

# AI WRITTEN, GEMINI
def calculate_optimized_hydrogen_angles(existing_angles, h_needed):
    """
    Calculates the best angles to place new hydrogens to maximize repulsion.
    All angles are assumed to be in radians.
    """
    if h_needed == 0:
        return []

    # Case 0: No existing bonds (isolated atom)
    if not existing_angles:
        # Distribute evenly starting from 0 radians
        angle_step = (2 * math.pi) / h_needed
        return [i * angle_step for i in range(h_needed)]

    # Case 1: Exactly 1 existing bond
    if len(existing_angles) == 1:
        base_angle = existing_angles[0]
        # Total bonds will be the 1 existing + the new hydrogens
        total_bonds = h_needed + 1
        if total_bonds > 0:
            angle_step = (2 * math.pi) / total_bonds
        else:
            return []
        # Step away from the base angle symmetrically
        return [(base_angle + (i * angle_step)) % (2 * math.pi) for i in range(1, total_bonds)]

    # Case 2+: Multiple existing bonds
    # Normalize all angles to the range [0, 2pi) and sort them
    sorted_angles = sorted([a % (2 * math.pi) for a in existing_angles])

    max_gap = 0
    best_start_angle = 0
    num_angles = len(sorted_angles)

    # Find the largest angular gap between adjacent bonds
    for i in range(num_angles):
        angle1 = sorted_angles[i]
        angle2 = sorted_angles[(i + 1) % num_angles] # Modulo handles the wrap-around to index 0

        # Calculate the gap, ensuring it wraps around 2*pi correctly
        gap = (angle2 - angle1) % (2 * math.pi)
        
        # Fallback for perfectly overlapping bonds (0 gap becomes 2pi gap)
        if gap <= 0:
            gap += 2 * math.pi

        if gap > max_gap:
            max_gap = gap
            best_start_angle = angle1

    # Subdivide the largest gap evenly
    # Example: If adding 1 H, we want it in the dead center (gap / 2)
    # If adding 2 H's, we want them at 1/3 and 2/3 of the gap (gap / 3)
    if h_needed <= -1:
        h_needed = 0
    angle_step = max_gap / (h_needed + 1)

    new_angles = []
    for i in range(1, h_needed + 1):
        new_angle = (best_start_angle + (i * angle_step)) % (2 * math.pi)
        new_angles.append(new_angle)

    return new_angles

#written by ChatGPT, though I changed the names to match my conventions
#I  do understand the math, just didn't feel like figuring out the signs in our sign convention
def rotateVector(vector, angle):
    x, y = vector
    cosT = math.cos(angle)
    sinT = math.sin(angle)

    xNew = x * cosT + y * sinT
    yNew = -x * sinT + y * cosT

    return (xNew, yNew)

def selectAtomsInsideTheBox(app):
    app.selectedAtomList = []
    x1, y1, x2, y2 = app.box
    for atom in app.atoms:
        if (x1 <= atom.pos[0] <= x2) and (y1 <= atom.pos[1] <= y2):
            app.selectedAtomList.append(atom)



def buttonCheck(app, x, y):
    for button in app.buttons:
        if button.checkClick(x, y):
            for otherButton in app.buttons:
                if ((type(otherButton) == type(button)) and  #Deactivates other button of same kind.
                    (button != otherButton)):

                    otherButton.isActive = False

def insideAButton(app, x, y):
    for button in app.buttons:
        if button.isInside(x, y):
            return True
    return False


def isWithinBond(app, x, y):
    for bond in app.bonds:
        if bond.isInside(x, y):
            return bond
    return None 






def normalizeVector(x, y, length):
    scalar = length / math.hypot(x, y)
    return scalar * x, scalar * y



    
    