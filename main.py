#basic philosphy of this mile file is that if the function is not 
#one of the ones built into cmu_graphics, do not include it in the file
#even stuff like drawAtoms is inside a different file is gets called by the
#drawWhiteboard function


import objects.atom
from cmu_graphics import *
import objects.buttons
import draw
import utils
import keyboard
import json
import objectAdder
        
     
def onAppStart(app):
    print('started')
    initAppStates(app)
    initConfigVariables(app)
    makeButtons(app)
    app.atoms = []
    app.rings = []

def makeButtons(app):
    app.buttons = []
    #app.buttons.append(objects.buttons.Button(0, 0, 50, 50, '6-ring'))
  

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
    app.currentObject = objectAdder.addRing
    app.bondOrder = 1
    app.ringNumber = 6

    app.selectedAtomList = []
    app.stepCounterForDoubleClick = None
    app.currElement = 'C'
    app.parentAtom = None
    app.moveAtomsMode = False  #when True, dragging atoms will move them. When false, dragging on atoms makes new bonds

    
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
    if key.upper() in objects.atom.Atom.valencyDict:
        app.currElement = key.upper()
    if key == '=':
        app.bondOrder = (app.bondOrder) % 3 + 1  
    if key.isdigit() and 3 <= int(key) <= 8:
        app.ringNumber = int(key)
    if key == 'backspace':
        utils.deleteSelectedAtoms(app)      

def onMouseMove(app, x, y):
    if not app.tempAtomPos:  #not currently dragging
        app.parentAtom = isWithinAtom(app, x, y)

def onMousePress(app, x, y):
    if not app.parentAtom:
        if app.selectedAtomList == []: #dont add atom if your doing box selection
            objectAdder.addObject(app, x, y)
        else:
            app.selectedAtomList = []
    else:
        if app.stepCounterForDoubleClick != None:
            app.selectedAtomList.append(app.parentAtom) 
            #abuse of notation, not literally parent atom, just atom being hovered over
        else:
            app.stepCounterForDoubleClick = 10
            #Time for double clicks to work. Rn its 0.5 seconds



            
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
        if not isWithinAtom(app, x, y):
            objectAdder.addObject(app, x, y)
            app.parentAtom = None # This is so that the parentAtom is not desynced with position, which can  have weird results


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
    draw.drawButtons(app)
    #drawStatus(app)
   

def drawStatus(app):
    pass

def main():
    runApp()


main()

    

        
    

