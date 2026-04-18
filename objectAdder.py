#This file is for functions which are specific to my application
#utils.py is for generic utils, stuff like vector math
import utils
from objects.atom import Atom









def addObject(app, x, y):
    app.currentObject(app, x, y, app.objectOrder)



def addAtom(app, x, y, bondOrder = 1):
    newAtom = Atom(app.currElement, position=(x,y))
    app.atoms.append(newAtom)
    if app.parentAtom:
        newAtom.addBond(app.parentAtom, bondOrder)

def addBenzene(app, x, y, size): #size not used, just have it cuz of how I switched between which objectType I am adding
    pass

def addRing(app, x, y, size=6):
    if app.parentAtom: #this case is when adding the ring to an existing structure
        pass
    else:
        pass














