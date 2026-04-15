
from objects.atom import Atom
from cmu_graphics import *
import draw
import utils
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
    app.selectedAtomList = []
    app.stepCounterForDoubleClick = None
    app.currElement = 'C'
    app.parentAtom = None
    app.moveAtomsMode = False  #when True, dragging atoms will move them. When false, dragging on atoms makes new bonds
  
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
        app.stepCounterForDoubleClick -= 1
        if app.stepCounterForDoubleClick <= 0:
            app.stepCounterForDoubleClick = None

def onKeyPress(app, key):
    if key.upper() in Atom.valencyDict:
        app.currElement = key.upper()
    if key == '=':
        app.bondOrder = (app.bondOrder) % 3 + 1        

def onMouseMove(app, x, y):
    if not app.tempAtomPos:  #not currently dragging
        app.parentAtom = isWithinAtom(app, x, y)

def onMousePress(app, x, y):
    atomPressed = isWithinAtom(app, x, y)
    if not atomPressed:
            if app.selectedAtomList == []: #dont add atom if your doing box selection
                addAtom(app, x, y)
            else:
                app.selectedAtomList = []
    else:
        if app.stepCounterForDoubleClick != None:
            app.selectedAtomList.append(atomPressed)
        else:
            app.stepCounterForDoubleClick = 10



            
def onMouseDrag(app, x, y):
    if app.parentAtom:
        if app.moveAtomsMode:
            if app.parentAtom in app.selectedAtomList:
                x0, y0 = app.parentAtom.pos
                dx, dy = x - x0, y - y0
                utils.moveGroup(app.selectedAtomList, dx, dy)
            else:
                app.parentAtom.pos = (x,y)
        else:
            app.tempAtomPos = utils.makePointDiscreteAngle(app.uniqueAngles ,*app.parentAtom.pos, x, y)
   
def onMouseRelease(app, x, y):
    if app.tempAtomPos and app.parentAtom:
        atom1 = isWithinAtom(app, x, y)
        if not atom1:
            atom1 = addAtom(app, *app.tempAtomPos)
        app.parentAtom.addBond(atom1, order= app.bondOrder)

    #------------- reseting vars
    app.tempAtomPos = None 
    
def isWithinAtom(app, x, y):
    for atom in app.atoms:
        if isWithinSpecificAtom(atom, x, y):
            return atom
       
def isWithinSpecificAtom(atom, x, y):
    dist = utils.distance(*atom.pos, x, y)
    if dist < 15:
        return atom
           
def redrawAll(app):
    draw.drawSketchpad(app)
    drawStatus(app)

    
def drawStatus(app):
    drawLabel(f'Current Atom: {app.currElement}',app.width/2, 20, size = 20)
    drawLabel(f'{app.selectedAtomList=} {app.stepCounterForDoubleClick=} {app.moveAtomsMode=}', app.width/2, 50, size =10)

def main():
    runApp()



main()

    

        
    

