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
        
