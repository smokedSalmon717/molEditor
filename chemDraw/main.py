import math
from objects.atom import Atom
from cmu_graphics import *
import keyboard

        
        
     
def onAppStart(app):
    initAppStates(app)
    app.atoms = []
    app.currElement = 'C'
    app.selectedAtom = None
    app.width = 400
    app.height = 400
    #getBonds(app)
    
def initAppStates(app):
    app.draggingNew = None
    app.moveAtomsMode = False
    app.originalPressPos = None
    app.bondGap = 10 #this variable controls how much space there is between atom and bond
    app.bondOrder = 1

def getBonds(app):
    bonds = set()
    for atom in app.atoms:
        for other in atom.bonds:
            atom1, atom2 = max(atom, other), min(atom, other)
            bondOrder = atom.bonds[other]
            bonds.add((atom1, atom2, bondOrder))
    return bonds
    
def addAtom(app, x, y):
    newAtom = Atom(app.currElement, position=(x,y))
    app.atoms.append(newAtom)
    return newAtom
    


def onKeyPress(app, key):
    if key.upper() in Atom.valencyDict:
        app.currElement = key.upper()
    if key == '=':
        app.bondOrder = (app.bondOrder) % 3 + 1
        

def onMouseMove(app, x, y):
    if not app.draggingNew:
        app.selectedAtom = isWithinAtom(app, x, y)

def onMousePress(app, x, y):
    app.originalPressPos = (x, y)
        
def onKeyHold(app, keys, modifers):  
    #print(keys)
    app.moveAtomsMode = 'shift' in modifers
    
def onKeyRelease(app, key, modifers):
    if  'shift' in modifers:
        app.moveAtomsMode = False
        
    
def onMouseDrag(app, x, y):
    if app.selectedAtom:
        if app.moveAtomsMode:
            app.selectedAtom.pos = (x,y)
        else:
            app.draggingNew = (x, y)
    
def onMouseRelease(app, x, y):
    if app.draggingNew and app.selectedAtom:
        atom1 = isWithinAtom(app, x, y)
        if not atom1:
            atom1 = addAtom(app, *app.draggingNew)
        app.selectedAtom.addBond(atom1, order= app.bondOrder)

    elif not isWithinAtom(app, x, y):
        if app.originalPressPos == (x,y):
            addAtom(app, x, y)
            
    #------------- reseting vars
    app.draggingNew = None
    app.originalPressPos = None
    
    
def isWithinAtom(app, x, y):
    for atom in app.atoms:
        dist = distance(*atom.pos, x, y)
        if dist < 15:
            return atom
   #      
        
        
def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5
        
        
def redrawAll(app):
    drawSelection(app)
    drawAtoms(app)
    drawBonds(app)
    drawTempBond(app)
    drawStatus(app)

def drawSelection(app):
    if app.selectedAtom != None:
        drawCircle(*app.selectedAtom.pos, 15, fill='gray', opacity=25)  

    
def drawAtoms(app):
    for atom in app.atoms:
        element = atom.element
        color = Atom.colorMap[element]
        drawLabel(element,*atom.pos, size=16, fill=color)
        
def drawBonds(app):
    bonds = getBonds(app)
    for atom1, atom2, order in bonds:
        pos1, pos2 = atom1.pos, atom2.pos
        drawBond(app, pos1, pos2, order)

            
def drawBond(app, pos1, pos2, order=1):
        dx, dy = (pos1[1] - pos2[1]),(pos1[0] - pos2[0])
        angle = math.atan2(dx,dy)
        end1 = (pos1[0] - math.cos(angle) * app.bondGap,
                pos1[1] - math.sin(angle) * app.bondGap)
        end2 = (pos2[0] + math.cos(angle) * app.bondGap,
                pos2[1] + math.sin(angle) * app.bondGap)
        if order % 2 == 1:    # if even bond order, draw a middle line
            drawLine(*end1, *end2)
        if order > 1:       # if 2 or 3, draw offset lines
            end1up, end1down = getDoubleBondOffsetPoints(angle, end1, order*2)
            end2up, end2down = getDoubleBondOffsetPoints(angle, end2, order*2)
            drawLine(*end1up, *end2up)
            drawLine(*end1down,*end2down)
        
        
def getDoubleBondOffsetPoints(angle, pos, offset):
    x, y = pos
    up = (x - math.sin(angle)*offset, y + math.cos(angle)*offset)
    down = (x + math.sin(angle)*offset, y - math.cos(angle)*offset)
    return up, down
    
        
def drawTempBond(app):
    if app.draggingNew and app.selectedAtom in app.atoms:
        drawBond(app, app.selectedAtom.pos, app.draggingNew)
    
def drawStatus(app):
    drawLabel(f'Current Atom: {app.currElement}',app.width/2, 20, size = 20)
    drawLabel(f'{app.selectedAtom=}    {app.bondOrder=}  {app.moveAtomsMode=}', app.width/2, 50, size =10)

def main():
    runApp()



main()

    

        
    

