import math
from objects.atom import Atom
from cmu_graphics import *
import keyboard
import json
        


     
def onAppStart(app):
    initAppStates(app)
    initConfigVariables(app)
    app.atoms = []
    app.angle = None


def initConfigVariables(app): 
    with open("config.json") as f:
        setting = json.load(f) 
    app.width = setting["width"]
    app.height = setting["height"]
    app.bondGap = setting["bondGap"] #this variable controls how much space there is between atom and bond
    app.defaultBondLength = setting["defaultBondLength"]
    app.uniqueAngles = setting["uniqueAngles"]


def initAppStates(app):
    app.tempAtomPos = None  #when dragging to make new atom, stores the new positions to place the new atom. 
                             # when not dragging, will be None, and its truthiness flags for ifDragging
    app.bondOrder = 1 
    app.currElement = 'C'
    app.selectedAtom = None
    app.moveAtomsMode = False  #when True, dragging atoms will move them. When false, dragging on atoms makes new bonds
    app.originalPressPos = None  #this variable is used to prevent the creation of new atoms by dragging, which felt wrong to me
    app.checkingForDoubleClick = None


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
    
def onStep(app):
    app.moveAtomsMode = keyboard.is_pressed('shift') 
    #moveAtomsMode means that dragging atoms will move them and not make new atoms.                                                 
    #It was done using onStep and with foreign module because of cmu_graphics inability
    #to proccess shift presses, and how good using shift for ths functon felt
    if app.stepCounterForDoubleClick != None: 
        doubleClickRoutine(app)

def doubleClickRoutine(app):
    app.stepCounterForDoubleClick -= 1
    if app.stepCounterForDoubleClick >= 0:
        app.stepCounterForDoubleClick = None


    

def onKeyPress(app, key):
    if key.upper() in Atom.valencyDict:
        app.currElement = key.upper()
    if key == '=':
        app.bondOrder = (app.bondOrder) % 3 + 1
        

def onMouseMove(app, x, y):
    if not app.tempAtomPos:  #not currently dragging
        app.selectedAtom = isWithinAtom(app, x, y)

def onMousePress(app, x, y):
    app.originalPressPos = (x, y)
    if app.selectedAtom and not app.tempAtomPos: #this means that we are hovering over atom and not making new bond
        if app.stepCounterForDoubleClick == None:
            app.stepCounterForDoubleClick = 10
            #sets the amount of steps where clicking again will count as double click
        elif type(app.stepCounterForDoubleClick) == int:
            app.highlightedAtom = app.selectedAtom

        



    
        
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
            app.tempAtomPos = makePointDiscreteAngle(app, x, y)

def makePointDiscreteAngle(app, x1, y1):
    x0, y0 = app.selectedAtom.pos
    dx = x1 - x0
    dy = y1 - y0
    angle = (app.uniqueAngles*math.atan2(dx, dy))//(2*math.pi)
    angle *= (2*math.pi)/app.uniqueAngles
    x, y= 50*math.sin(angle), 50*math.cos(angle)
    return (x + x0, y + y0)
    

    
def onMouseRelease(app, x, y):
    if app.tempAtomPos and app.selectedAtom:
        atom1 = isWithinAtom(app, x, y)
        if not atom1:
            atom1 = addAtom(app, *app.tempAtomPos)
        app.selectedAtom.addBond(atom1, order= app.bondOrder)

    elif not isWithinAtom(app, x, y):
        if app.originalPressPos == (x,y):
            addAtom(app, x, y)
            
    #------------- reseting vars
    app.tempAtomPos = None 
    app.originalPressPos = None
    
    
def isWithinAtom(app, x, y):
    for atom in app.atoms:
        if isWithinSpecificAtom(atom, x, y):
            return atom


        
def isWithinSpecificAtom(atom, x, y):
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
    if app.tempAtomPos and app.selectedAtom in app.atoms:
        drawBond(app, app.selectedAtom.pos, app.tempAtomPos, app.bondOrder)
    
def drawStatus(app):
    drawLabel(f'Current Atom: {app.currElement}',app.width/2, 20, size = 20)
    drawLabel(f'{app.selectedAtom=}    {app.bondOrder=}  {app.moveAtomsMode=}', app.width/2, 50, size =10)

def main():
    runApp()



main()

    

        
    

