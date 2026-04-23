
import math
import utils
from pathlib import Path
class Atom:

    IDMap = dict() #counts number of atoms for each element for
                       #id assignment, but no reassignment with deletion
                       #so not for counting number of elements
    valencyDict = {
    'H':1,
    'C':4,
    'N':3,
    'O':2,
    'Cl':1,
    'F':1,
    'S':2}     #this will be used in the cleanup functon/parcing.

    BASE_DIR = Path(__file__).resolve().parent.parent
    ICON_PATH = BASE_DIR / "images"



    def __init__(self, element, parent=None, position=None, id=0):
        self.element = element #atomic symbol
        self.pos = position
        self.getImage()
        self.hydrogenCount = Atom.valencyDict[element] #used so if u just add carbon, 4 hydrogen gets added, and 3 for O, and etc
        self.bonds = dict()  #bonds are a dictionary, keys are the atomID, and values are the order of the bond
        self.parent = parent  #future use for SMILE parsing
        self.addID()  #find the unique id identifier, so you can tell different atoms appart
        #if self.element != 'H':
          #  self.addImplicitHydrogens()

    def getImage(self):
        BASE_DIR = Path(__file__).resolve().parent.parent
        self.imagePath = str(BASE_DIR / "images") + '/' + self.element + '.svg'



    def isInside(self, x, y):
        return utils.distance(*self.pos, x, y) < 15
    
    def checkClick(app, x, y):
        pass

    def addImplicitHydrogens(self):
        valency = int(Atom.valencyDict[self.element])
        for bondOrder in self.bonds.values():
            valency -= bondOrder
        self.implicitHydrogens = []
        for i in range(valency):
            hydrogen = ImplicitHydrogen(self)
            self.addBond(hydrogen)

        


        

        

    def addID(self):
        Atom.IDMap[self.element] = Atom.IDMap.get(self.element, 0) + 1
        self.idValue = Atom.IDMap[self.element]
        
        
    def __repr__(self):
        return f'{self.element}{self.idValue}'
    
    def __hash__(self):
        return hash(str(self))
        
    
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
        



class ImplicitHydrogen(Atom):
    def __init__(self, parent):
        super().__init__('H', parent, 0)
        self.parent = parent
        self.theta = 2
        self.pos = utils.vectorSum(utils.rotateVector((30,0),self.theta), self.parent.pos)



class Bond:
    def __init__(self, atom1, atom2, order):
        self.atoms = [atom1, atom2]
        self.order = order


    @property
    def endpoints(self):
        x1, y1 = self.atoms[0].pos
        x2, y2 = self.atoms[1].pos
        return x1, y1, x2, y2


    def checkClick(self, x, y):
        if self.isInside(x, y):
            self.onClick()

    def isInside(self, x, y):
        return self.point_near_segment(x, y)
    
    def onClick(self):
        self.order = (self.order % 3) + 1
    
    #AI WRITTEN, Chat GPT ------------
    def point_near_segment(self,mouseX, mouseY):
        tolerance = 5
        x1, y1, x2, y2 = self.endpoints
        dx = x2 - x1
        dy = y2 - y1

        if dx == 0 and dy == 0:
            # segment is just a point
            return math.hypot(mouseX - x1, mouseY - y1) <= tolerance

        # projection factor
        t = ((mouseX - x1) * dx + (mouseY - y1) * dy) / (dx * dx + dy * dy)
        t = max(0, min(1, t))

        # closest point
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy

        # distance check
        distance = math.hypot(mouseX - closest_x, mouseY - closest_y)
        return distance <= tolerance

    #-----------------------------
    



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
        self.atoms[-1].addBond(self.atoms[0], order= 1)


    def __repr__(self):
        res = '<'
        for atom in self.atoms:
            res += repr(atom) + ', '
        return res + '>'
    
    def __hash__(self):
        return hash(str(self))

class Molecule: #Bad, not needed
    def __init__(self, atoms):
        self.atoms = atoms
        self.addedBonds = []
        self.structure = {atoms[0] : self.generateStructureDict([None, atoms[0]])}


    def generateStructureDict(self, parentAtomChain):
        currAtom = parentAtomChain[-1]
        prevAtom = parentAtomChain[-2]
        res = dict()
        for atom in currAtom.bonds.keys():
            if not (atom in parentAtomChain): 
                next = self.generateStructureDict(parentAtomChain + [atom])
                res[atom] = next
        
        return res
    
    def addImplicitHydrogen(self, app, tree):
        for parent in tree:
            if parent.element == 'H':
                continue
            initialValence = Atom.valencyDict[parent.element]


                


                

                
        

    


