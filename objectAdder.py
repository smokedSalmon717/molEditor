#This file is for functions which are specific to my application
#utils.py is for generic utils, stuff like vector math
import utils
import objects









def addObject(app, x, y):
    app.currentObject(app, x, y)

def addBond(app):
    order = app.bondOrder


def newBondFromParent(app, parent, child):
    pass

def totallyNewBond(app, x, y):
    pass

def addAtom(app , x, y):
    if app.parentAtom:
        vector = utils.makeVector(app.parentAtom.pos, (x,y))
        vector = utils.normalizeVector(*vector, app.defaultBondLength)
        x, y = utils.vectorSum(vector, app.parentAtom.pos)
        newAtom = objects.Atom(app.currElement, position=(x,y))
        newAtom.addBond(app.parentAtom, app.bondOrder)
    else:
        newAtom = objects.Atom(app.currElement, position=(x,y))
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
    ring = objects.Ring(seed, n, app.defaultBondLength, vector, aromatic = app.aromatic)
    addRingToApp(app, ring)

def addRingToApp(app, ring):
    print(ring.atoms)
    for atom in ring.atoms:
        app.atoms.append(atom)
    
    
    















