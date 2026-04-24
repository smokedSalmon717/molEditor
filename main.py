#basic philosphy of this mile file is that if the function is not 
#one of the ones built into cmu_graphics, do not include it in the file
#even stuff like drawAtoms is inside a different file is gets called by the
#drawWhiteboard function
from objects.objects import Atom, Molecule, Bond
from cmu_graphics import *
from buttons.buttons import drawingButton, actionButton, selectionButton
import buttons.functions 
import draw
import utils
import keyboard
import json
import objects.objectAdder as objectAdder
from pathlib import Path








def onAppStart(app):
    app.moleculeName = None
    app.boxSelect = False
    app.box = None
    app.saveList = []
    app.inspectorEnabled = False
    app.atoms = []
    app.bonds = []
    app.rings = []
    app.molecules = []
    saveState(app)
    initAppStates(app)

    initConfigVariables(app)
    makeButtons(app)
    app.boxSelect = False



def makeButtons(app):
    app.buttons = []
    #AI WRITTEN, kinda understand how it works? -------------
    BASE_DIR = Path(__file__).resolve().parent
    ICON_PATH = BASE_DIR / "images"

    #-----------------------------------
    start = 100
    size = 60
        #Adding bond-type buttons. Initially I store the URL in config, but realized that was stupid
    app.buttons.append(drawingButton(0, start + size*0, size, size, buttons.functions.singleBond, app))
    app.buttons.append(drawingButton(0, start + size * 1, size, size, buttons.functions.doubleBond, app))
    app.buttons.append(drawingButton(0, start + size *2, size, size, buttons.functions.tripleBond, app))
    app.buttons.append(drawingButton(0, start + size*3, size, size, buttons.functions.benzene, app))
    app.buttons.append(drawingButton(0, start + size*4, size, size, buttons.functions.cyclohexane, app))
    app.buttons.append(drawingButton(0, start + size*5, size, size, buttons.functions.cyclopentane, app))

    #Now elements
    size = 50
    app.buttons.append(drawingButton(app.width - size, start + size*0, size, size, buttons.functions.carbon, app))
    app.buttons.append(drawingButton(app.width - size, start + size*1, size, size, buttons.functions.oxygen, app))
    app.buttons.append(drawingButton(app.width - size, start + size*2, size, size, buttons.functions.hydrogen, app))
    app.buttons.append(drawingButton(app.width - size, start + size*3, size, size, buttons.functions.nitrogen, app))
    app.buttons.append(drawingButton(app.width - size, start + size*4, size, size, buttons.functions.chlorine, app))
    app.currElement = 'C'

    #Other functions
    app.buttons.append(actionButton(app.width/2,0, size, size, buttons.functions.cleanStructure, app))
    app.buttons.append(actionButton(app.width/2 + size, 0, size, size, buttons.functions.deleteAll, app))
    app.buttons.append(actionButton(app.width/2 - size, 0, size, size, buttons.functions.smiles, app))
    app.buttons.append(selectionButton(app.width/2 + 2*size,0, size, size, buttons.functions.boxSelect, app))


        


def generateSave(app):
    save = {
        'atoms':[],
        'bonds':[]
                }
    i = 0
    while i < len(app.atoms):
        if app.atoms[i].element == 'H':
            app.atoms.pop(i)
        else:
            i += 1
    i = 0
    while i < len(app.bonds):
        bond = app.bonds[i]
        if (bond.atoms[0].element == 'H') or (bond.atoms[1].element == 'H'):
            app.bonds.pop(i)
        else:
            i += 1

    for atom in app.atoms:
        atomData = {
                    'id':atom.id,
                    'element':atom.element,
                    'pos':atom.pos
                    }
        save['atoms'].append(atomData)

    for bond in app.bonds:
        bondData = {
                    'atom1': bond.atoms[0].id,
                    'atom2': bond.atoms[1].id,
                    'order': bond.order
                    }
        save['bonds'].append(bondData)

    for atom in app.atoms:
        atom.updateHydrogens(app)

    return save

def saveState(app):
    save = generateSave(app)
    app.saveList.append(save)
    if len(app.saveList) > 5:
        app.saveList.pop(0)
    app.status = save

def loadState(app):
        save = app.saveList[-1]

        app.atoms.clear()
        app.bonds.clear()
        app.molecules.clear()
        
        # This is our magic translation book: { Old_ID : New_Atom_Object }
        atomIDMap = {}
        for atomData in save['atoms']:
            # Note: you might need to adjust your Atom __init__ to accept raw data 
            # without triggering your auto-molecule or auto-hydrogen functions here
            newAtom = Atom(app, element=atomData['element'], position=atomData['pos'], hydrogenUpdate = False)
            newAtom.id = atomData['id'] # Force the ID to match the save file
            atomIDMap[newAtom.id] =newAtom
        for bondData in save['bonds']:

            atom1, atom2 = atomIDMap[bondData['atom1']], atomIDMap[bondData['atom2']]
            order = bondData['order']
            newBond = Bond(app, atom1, atom2, order)
            atom1.bonds.append(newBond)
            atom2.bonds.append(newBond)


        if app.saveList:
            app.saveList.pop()
        for atom in app.atoms:
            if atom.element != 'H':
                atom.updateHydrogens(app)



  

def initConfigVariables(app): 
    app.basePath = str(Path(__file__).resolve().parent) + '/images/'
    with open("config.json") as f:
        setting = json.load(f) 
    app.width = setting["width"]
    app.height = setting["height"]
    app.bondGap = setting["bondGap"] #this variable controls how much space there is between atom and bond
    app.defaultBondLength = setting["defaultBondLength"]
    app.uniqueAngles = setting["uniqueAngles"]
    app.atomSize = setting["atomSize"]

def initAppStates(app):
    app.objectHoveringOver = None
    app.tempAtomPos = None  #when dragging to make new atom, stores the new positions to place the new atom. 
                             # when not dragging, will be None, and its truthiness flags for ifDragging
    app.currentObject = objectAdder.addAtom
    app.bondOrder = 1
    app.ringNumber = 6
    app.aromatic = False

    app.selectedAtomList = []
    app.selectedBond = None
    app.stepCounterForDoubleClick = None
    app.currElement = 'C'
    app.parentAtom = None
    app.moveAtomsMode = False  #when True, dragging atoms will move them. When false, dragging on atoms makes new bonds



def onKeyPress(app, key, modifiers):
    if (key == 'z') and ('control' in modifiers) and (len(app.saveList) > 0):
        loadState(app)
    if key == 'backspace':
        utils.deleteSelectedAtoms(app)
    
def onStep(app):
    



    
    app.temp = len(app.molecules)
    app.moveAtomsMode = keyboard.is_pressed('shift') 
    #moveAtomsMode means that dragging atoms will move them and not make new atoms.                                                 
    #It was done using onStep and with foreign module because of cmu_graphics inability
    #to proccess shift presses, and how good using shift for ths functon felt
    if app.stepCounterForDoubleClick != None:
        app.stepCounterForDoubleClick -= 1
        if app.stepCounterForDoubleClick <= 0:
            app.stepCounterForDoubleClick = None

    

def onMouseMove(app, x, y):
    app.inside = utils.insideAButton(app, x, y)
    if not app.tempAtomPos:  #not currently dragging
        app.parentAtom = utils.isWithinAtom(app, x, y)
        if not app.parentAtom:
            app.selectedBond = utils.isWithinBond(app, x, y)
        


def onMousePress(app, x, y):
    utils.buttonCheck(app, x, y)
    if app.box == None and app.boxSelect:
        app.box = [x,y,x,y]
    
    elif not app.moveAtomsMode:
        if app.selectedBond != None:
            app.selectedBond.checkClick(x, y)
        elif not (app.inside):
            if not app.parentAtom:
                objectAdder.addObject(app, x, y)

            else:
                if app.stepCounterForDoubleClick != None:
                    app.selectedAtomList.append(app.parentAtom) 
                    #abuse of notation, not literally parent atom, just atom being hovered over
                else:
                    app.stepCounterForDoubleClick = 10
                    #Time for double clicks to work. Rn its 0.5 seconds
        


            
def onMouseDrag(app, x, y):
    if app.boxSelect:

        if app.box == None:
            app.box = [x, y, x, y]
        else:
            app.box = [app.box[0], app.box[1], x, y]

    elif app.parentAtom:
        if app.moveAtomsMode:
            if app.parentAtom in app.selectedAtomList:
                x0, y0 = app.parentAtom.pos
                dx, dy = x - x0, y - y0                                                             
                utils.moveGroup(app.selectedAtomList, dx, dy)
            else:
                app.parentAtom.move(app, x, y)

        else:
            app.tempAtomPos = utils.makePointDiscreteAngle(app.uniqueAngles ,*app.parentAtom.pos, x, y)
   
def onMouseRelease(app, x, y):
    saveState(app)
    if app.boxSelect:
        utils.selectAtomsInsideTheBox(app)
        app.box = None
    elif app.parentAtom and not utils.insideAButton(app, x, y) and app.tempAtomPos:
        if utils.isWithinAtom(app, x, y):
            atom1, atom2 = app.parentAtom, utils.isWithinAtom(app, x, y)
            objectAdder.addBond(app, atom1, atom2, order = app.bondOrder)
        else:
            objectAdder.addObject(app, x, y)
    app.parentAtom = None
    app.tempAtomPos = None




           
def redrawAll(app):
    draw.drawSketchpad(app)
    draw.drawButtons(app)
    #if app.moleculeName:
    drawLabel(f'{app.moleculeName}', 100, 100)


def main():
    runApp()


main()

    

        
    

