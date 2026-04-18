import math
import utils
from objects.atom import Atom

class Ring: 
    def __init__(self, seedAtom, n, bondLength, vector, aromatic = False): 
        self.bondOrder = 1
        self.aromatic = aromatic
        self.atoms = [seedAtom]
        self.n = n
        self.pos = seedAtom.pos
        self.angle = - math.tau / n #the angle you rotate by each time. The ring generation is like a turtle
        self.bondLength = bondLength
        self.vector = utils.rotateVector(vector, 0.5*(math.pi + self.angle)) 
        #the angle I rotated by is to align the vector with the polygon
        self.generateRing()

    def generateRing(self):
        for _ in range(self.n - 1):
            if self.aromatic:             #If aromatic, you want alternating double bond single bonds (not literally putting in aromaticity)
                self.bondOrder = (self.bondOrder % 2) + 1 
            self.pos = utils.vectorSum(self.vector, self.pos)
            self.vector = utils.rotateVector(self.vector, self.angle)
            newAtom = Atom('C', parent = self.atoms[-1], position = self.pos)
            newAtom.addBond(self.atoms[-1], order = self.bondOrder )#add bond with previous
            self.atoms.append(newAtom)
        self.atoms[-1].addBond(self.atoms[0]) #fully connect ring

    def __repr__(self):
        res = '<'
        for atom in self.atoms:
            res += repr(atom) + ', '
        return res + '>'
    
    def __hash__(self):
        return hash(str(self))



