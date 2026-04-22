
import math
import utils

class Atom:
    IDMap = dict() #counts number of atoms for each element for
                       #id assignment, but no reassignment with deletion
                       #so not for counting number of elements
    valencyDict = {
    'H':1,
    'C':4,
    'N':3,
    'O':2}     #this will be used in the cleanup functon/parcing.
    colorMap = {
        'H':'black',
        'C':'black',
        'O':'red',
        'N':'blue'
    } #this is used for coloring of each element


    def __init__(self, element='C', parent=None, position=None, id=0):
        self.element = element #atomic symbol
        self.pos = position
        self.hydrogenCount = Atom.valencyDict[element] #used so if u just add carbon, 4 hydrogen gets added, and 3 for O, and etc
        self.bonds = dict()  #bonds are a dictionary, keys are the atomID, and values are the order of the bond
        self.parent = parent  #future use for SMILE parsing
        self.addID()  #find the unique id identifier, so you can tell different atoms appart

        
    def addID(self):
        Atom.IDMap[self.element] = Atom.IDMap.get(self.element, 0) + 1
        self.idValue = Atom.IDMap[self.element]
        
        
    def __repr__(self):
        return f'{self.element}{self.idValue}'
        
    
    def id(self):
        return str(self)
        
        
    def addBond(self, other, order = 1): #bond order defaults to 1
        if isinstance(other, Atom) and other != self:
            self.bonds[other] = order
            other.bonds[self] = order
            #self.updateHydrogens()
           # other.updateHydrogens()
            
        
            
    def __lt__(self, other):
        return hash(self.id()) > hash(other.id())
        #This means that order is consistent but 
        
class Bond:
    def __int__(self, atom1, atom2, order):
        self.atoms = [atom1, atom2]
        self.order = order
        self.endpoints = (*atom1.pos, *atom2.pos)

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

