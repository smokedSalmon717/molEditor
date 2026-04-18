#This file is for functions which are specific to my application
#utils.py is for generic utils, stuff like vector math
import utils
from objects.atom import Atom



def moveGroup(group, dx, dy):
    #take in list of atoms as group, and moves them by dx, dy
    for atom in group:
        atom.pos = utils.vectorSum(atom.pos, (dx, dy))


  
def addAtom(app, x, y):
    newAtom = Atom(app.currElement, position=(x,y))
    app.atoms.append(newAtom)
    return newAtom

def deleteSelectedAtoms(app):
    for atom in app.selectedAtomList:
        deleteBondReferencesInOtherAtoms(atom)
        app.atoms.remove(atom) 
    app.selectedAtomList = [] 


def deleteBondReferencesInOtherAtoms(self):
    for partner in self.bonds:
        partner.bonds.pop(self)








