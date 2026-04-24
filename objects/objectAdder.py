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
    if order == None:
        order = app.bondOrder
    Bond(app,atom1, atom2, order)



def addAtom(app , x, y):
    Atom(app, app.currElement, parent = app.parentAtom, position=(x,y))








    #     newAtom = addBond(app, x, y)
    #     if app.parentAtom.molecule != None:
    #         app.parentAtom.molecule.addAtom(newAtom)
    #     else:
    #         newMolecule = Molecule(app)
    #         newMolecule.addAtom(newAtom)
    #         newMolecule.addAtom(app.parentAtom)
    
    #     #vector = utils.makeVector(app.parentAtom.pos, (x,y))
    #     #vector = utils.normalizeVector(*vector, app.defaultBondLength)
    #     #x, y = utils.vectorSum(vector, app.parentAtom.pos)
    #     #newAtom = objects.Atom(app.currElement, position=(x,y))
    #     #newAtom.addBond(app.parentAtom, app.bondOrder)
    # else:
    #     newMolecule = Molecule(app)
    #     newAtom = Atom(app, app.currElement, position=(x,y))
    #     newAtom.molecule = newMolecule
    #     app.molecules.append(newMolecule)
    # app.atoms.append(newAtom)
    # return newAtom

def addRing(app, x, y): #size not used, just have it cuz of how I switched between which objectType I am adding
    n = app.ringNumber
    if not app.parentAtom:
        y += utils.polygonRadius(n, app.defaultBondLength) #in parentless case, make sure you generate ring around center
        vector = (0, -app.defaultBondLength) #with no parent, starting angle is straight up
    else:
        vector = utils.makeVector(app.parentAtom.pos, (x,y)) #generates vector from parents to child
        vector = utils.normalizeVector(*vector, app.defaultBondLength)
    seed = addAtom(app, x, y)
    ring = Ring(seed, n, app.defaultBondLength, vector, aromatic = app.aromatic)
    addRingToApp(app, ring)

def addRingToApp(app, ring):
    pass
    #WORK ON RINGS LATER
    
    
    















