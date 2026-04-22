#basic philosphy of this mile file is that if the function is not 
#one of the ones built into cmu_graphics, do not include it in the file
#even stuff like drawAtoms is inside a different file is gets called by the
#drawWhiteboard function
from objects.objects import Atom, Molecule
from cmu_graphics import *
from buttons.buttons import Button, drawingButton
import buttons.functions 
import draw
import utils
import keyboard
import json
import objects.objectAdder as objectAdder

        

     
def onAppStart(app):
    app.inside = None
    print('start')
    initAppStates(app)
    initConfigVariables(app)
    makeButtons(app)
    app.atoms = []
    app.bonds = []
    app.rings = []

def makeButtons(app):
    app.buttons = []
    with open("config.json") as f: #svg files I am using I took from
        links = json.load(f)
        start = 100
        size = 60
        #Adding bond-type buttons. Initially I store the URL in config, but realized that was stupid
        app.buttons.append(drawingButton(0, start + size*0, size, size, buttons.functions.singleBond, app, "https://molview.org/img/bond/single.svg"))
        app.buttons.append(drawingButton(0, start + size * 1, size, size, buttons.functions.doubleBond, app, "https://molview.org/img/bond/double.svg"))
        app.buttons.append(drawingButton(0, start + size *2, size, size, buttons.functions.tripleBond, app,  "https://molview.org/img/bond/triple.svg"))
        app.buttons.append(drawingButton(0, start + size*3, size, size, buttons.functions.cyclohexane, app,  "https://molview.org/img/frag/cyclohexane.svg"))
        app.buttons.append(drawingButton(0, start + size*4, size, size, buttons.functions.benzene, app,  "https://molview.org/img/frag/benzene.svg"))





  

def initConfigVariables(app): 
    with open("config.json") as f:
        setting = json.load(f) 
    app.width = setting["width"]
    app.height = setting["height"]
    app.bondGap = setting["bondGap"] #this variable controls how much space there is between atom and bond
    app.defaultBondLength = setting["defaultBondLength"]
    app.uniqueAngles = setting["uniqueAngles"]

def initAppStates(app):
    app.objectHoveringOver = None
    app.tempAtomPos = None  #when dragging to make new atom, stores the new positions to place the new atom. 
                             # when not dragging, will be None, and its truthiness flags for ifDragging
    app.currentObject = objectAdder.addAtom
    app.bondOrder = 1
    app.ringNumber = 6
    app.aromatic = False

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

    if key == 'm':
        mol = Molecule(app.atoms)
        print(mol.structure)
    if key.upper() in Atom.valencyDict:
        app.currElement = key.upper()
    if key == '=':
        app.bondOrder = (app.bondOrder) % 3 + 1  
    if key.isdigit() and 3 <= int(key) <= 8:
        app.ringNumber = int(key)
    if key == 'backspace':
        utils.deleteSelectedAtoms(app)      

def onMouseMove(app, x, y):

    app.inside = utils.insideAButton(app, x, y)
    if not app.tempAtomPos:  #not currently dragging
        app.parentAtom = utils.isWithinAtom(app, x, y)

def onMousePress(app, x, y):




    utils.buttonCheck(app, x, y)
    if not app.inside:
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
        if not utils.insideAButton(app, x, y):
            if not utils.isWithinAtom(app, x, y):
                objectAdder.addObject(app, x, y)
            else:
                otherAtom = utils.isWithinAtom(app, x, y)
                if otherAtom != app.parentAtom:
                    app.parentAtom.addBond(otherAtom, order=app.bondOrder)
            app.parentAtom = None # This is so that the parentAtom is not desynced with position, which can  have weird results


    #------------- reseting vars
    app.tempAtomPos = None 
    

           
def redrawAll(app):
    draw.drawSketchpad(app)
    draw.drawButtons(app)
    drawStatus(app)
   

def drawStatus(app):
    drawLabel(str(app.inside), app.width/2, 20)

def main():
    runApp()


main()

    

        
    

