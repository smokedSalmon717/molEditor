#This file is for functions which are specific to my application
#utils.py is for generic utils, stuff like vector math
import utils
from objects.objects import Atom, Bond, Ring, Molecule
 








def addObject(app, x, y):
    app.currentObject(app, x, y)


def addBondFunction(app, x, y):
    if app.parentAtom:
        Atom(app, app.currElement, parent=app.parentAtom, position = app.tempAtomPos)
    else:
        atom1 = Atom(app, 'C', position=(x + app.defaultBondLength/2, y))
        atom2 = Atom(app, 'C', parent=atom1, position=(x-app.defaultBondLength/2, y))

def addBond(app, atom1, atom2, order = None):
    if atom1 != atom2:
        if order == None:
            order = app.bondOrder
        Bond(app,atom1, atom2, order)
    if (atom1.element != 'H') and (atom2.element != 'H'):
        atom1.updateHydrogens(app)
        atom2.updateHydrogens(app)




def addAtom(app , x, y):
    if not utils.isWithinAtom(app, x, y):
        Atom(app, app.currElement, parent = app.parentAtom, position=(x,y))







def addRing(app, x, y): #size not used, just have it cuz of how I switched between which objectType I am adding
    n = app.ringNumber
    if not app.parentAtom:
        y += utils.polygonRadius(n, app.defaultBondLength) #in parentless case, make sure you generate ring around center
        vector = (0, -app.defaultBondLength) #with no parent, starting angle is straight up
    else:
        vector = utils.makeVector(app.parentAtom.pos, (x,y)) #generates vector from parents to child
        vector = utils.normalizeVector(*vector, app.defaultBondLength)
    seed = Atom(app, element='C', parent=app.parentAtom if app.parentAtom else None, position=(x, y), hydrogenUpdate= False)
    ring = Ring(app, seed, ringNumber = n, startVector = vector)


    
    
    















