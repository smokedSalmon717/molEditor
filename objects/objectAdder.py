#This file is for functions which are specific to my application
#utils.py is for generic utils, stuff like vector math
import utils
from objects.objects import Atom, Bond, Ring
 








def addObject(app, x, y):
    app.currentObject(app, x, y)

def addBond(app, x, y):
    order = app.bondOrder
    if not app.parentAtom:
        length = app.defaultBondLength /2
        atom1, atom2 = addAtom(app, x - length, y), addAtom(app, x + length, y)
        app.parentAtom = atom1
    else:
        atom2 = Atom(app.currElement, position=(x,y))
        app.atoms.append(atom2)
        atom1 = app.parentAtom
    atom1.addBond(atom2)
    app.bonds.append(Bond(atom1, atom2, order))
    return atom2

        
        


def newBondFromParent(app, parent, child):
    pass

def totallyNewBond(app, x, y):
    pass

def addAtom(app , x, y):
    if app.parentAtom:
        return addBond(app, x, y)
        #vector = utils.makeVector(app.parentAtom.pos, (x,y))
        #vector = utils.normalizeVector(*vector, app.defaultBondLength)
        #x, y = utils.vectorSum(vector, app.parentAtom.pos)
        #newAtom = objects.Atom(app.currElement, position=(x,y))
        #newAtom.addBond(app.parentAtom, app.bondOrder)
    else:
        newAtom = Atom(app.currElement, position=(x,y))
    app.atoms.append(newAtom)
    return newAtom

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
    print(ring.atoms)
    for i in range(len(ring.atoms)):
        app.atoms.append(ring.atoms[i])
        atom1, atom2 = ring.atoms[i], ring.atoms[(i + 1) % len(ring.atoms)]
        app.bonds.append(Bond(atom1, atom2, order = atom1.bonds[atom2]))
    
    
    















