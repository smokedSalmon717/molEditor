
import math
import utils
from pathlib import Path
from collections import deque
import copy

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



    def __init__(self, app, element, parent = None, position=None, hydrogenUpdate = True):
        self.app = app
        self.element = element #atomic symbol
        self.pos = position
        self.getImage()
        self.molecule = None
   
        self.hydrogenCount = Atom.valencyDict[element] #used so if u just add carbon, 4 hydrogen gets added, and 3 for O, and etc
        self.parent = parent
        self.bonds = []  #bonds are a dictionary, keys are the atomID, and values are the order of the bond
        self.addID()  #find the unique id identifier, so you can tell different atoms appart
        self.ID = str(self)
        self.addAIVariables() #Instead of changing my code to work with AI code, Im giving atom new properties that fit with how AI thinks atom work
        self.addBond(parent, 1 if self.element == 'H' else app.bondOrder)
        self.app.atoms.append(self)
        
        self.connectToMolecule()
        if self.element != 'H' and hydrogenUpdate:
            self.updateHydrogens(self.app)
        if self.parent and self.parent.element != 'H' and self.element != 'H' and hydrogenUpdate:
            self.parent.updateHydrogens(self.app)

    def connectToMolecule(self):
            if self.parent:
                if not self.parent.molecule:
                    newMolecule = Molecule(self.app)
                    self.molecule = newMolecule
                    self.parent.molecule = newMolecule
                    newMolecule.addAtom(self.parent)
                    newMolecule.addAtom(self)
                    newMolecule.addBond(self.bonds[-1])
                    self.app.molecules.append(newMolecule)
                else:
                    self.molecule = self.parent.molecule 
                    self.parent.molecule.addAtom(self)
                    self.parent.molecule.addBond(self.bonds[-1])
            else:
                # FIX: If there is no parent, this is a root atom. It needs its own molecule!
                if self.element != 'H': 
                    newMolecule = Molecule(self.app)
                    self.molecule = newMolecule
                    newMolecule.addAtom(self)
                    self.app.molecules.append(newMolecule)




    def getImage(self):
        BASE_DIR = Path(__file__).resolve().parent.parent
        self.imagePath = str(BASE_DIR / "images") + '/' + self.element + '.svg'

    def addAIVariables(self):
        self.x, self.y = self.pos
        self.bondList = []

    def addBond(self, other, order = 1): #bond order defaults to 1
        if isinstance(other, Atom) and other != self:
            bond = Bond(self.app, atom1= self, atom2= other, order = order)
            self.bonds.append(bond)
            other.bonds.append(bond)
            return bond        
        
    def getValencyCount(self):
        valency = Atom.valencyDict[self.element]
        for bond in self.bonds:
            valency -= bond.order
        return valency
    
    def move(self, app, x, y):
        oldPos = self.pos
        vector = (x - oldPos[0], y - oldPos[1])
        self.pos = (x, y)
        for bond in self.bonds:
            for atom in bond.atoms:
                if atom != self:
                    other = atom
            if other.element == 'H':
                other.pos = utils.vectorSum(vector, other.pos)
        
    def updateHydrogens(self, app):
        def popHydrogens():
            bondsToPop = []
            for bond in self.bonds:
                for otherAtom in bond.atoms:
                    if otherAtom != self and otherAtom.element == 'H':
                        
                        if otherAtom in app.atoms:
                            app.atoms.remove(otherAtom)
                        # FIX: Delete ghost atom from the molecule list!
                        if self.molecule and otherAtom in self.molecule.atoms:
                            self.molecule.atoms.remove(otherAtom)
                            
                        if bond in app.bonds:
                            app.bonds.remove(bond)
                        # FIX: Delete ghost bond from the molecule list!
                        if self.molecule and bond in self.molecule.bonds:
                            self.molecule.bonds.remove(bond)
                            
                        bondsToPop.append(bond)
                        break
            
            for hydrogen in bondsToPop:
                self.bonds.remove(hydrogen)
        def addNewHydrogens():
                    valencyWanted = Atom.valencyDict[self.element]
                    currValency = 0
                    for bond in self.bonds:
                        currValency += bond.order
                    
                    hydrogensNeeded = valencyWanted - currValency
                    existingAngles = []
                
                    for bond in self.bonds: 
                        for atom in bond.atoms: 
                            if atom == self:
                                continue 
                            else:
                                other = atom
                        
                        # FIX 1 & 2: Point FROM self TO other, and pass dy first!
                        dx = other.pos[0] - self.pos[0]
                        dy = other.pos[1] - self.pos[1]
                        existingAngles.append(math.atan2(dy, dx))
                    
                    hydrogenAngles = utils.calculate_optimized_hydrogen_angles(existingAngles, hydrogensNeeded)
                    
                    for angle in hydrogenAngles:
                        # FIX 3: Use standard cos/sin to find the exact offset directly
                        # angle is in radians, so math.cos/sin work perfectly
                        hydrogenLength = 20
                        x_offset = hydrogenLength * math.cos(angle)
                        y_offset = hydrogenLength* math.sin(angle)
                        
                        newPos = (self.pos[0] + x_offset, self.pos[1] + y_offset)
                        
                        Atom(app, 'H', parent=self, position=newPos)
        popHydrogens()
        addNewHydrogens()



                    
    def isInside(self, x, y):
        selectionRadius = 5 if self.element == 'H' else 15
        return utils.distance(*self.pos, x, y) < selectionRadius
    
    def checkClick(app, x, y):
        pass
        

    def addID(self):
        Atom.IDMap[self.element] = Atom.IDMap.get(self.element, 0) + 1
        self.idValue = Atom.IDMap[self.element]
        self.id = self.element + str(self.idValue)
        
        
    def __repr__(self):
        return f'{self.element}{self.idValue}'
    
    def __hash__(self):
        return hash(str(self))
        
    
        

        
            
    def __lt__(self, other):
        return hash(self.id()) > hash(other.id())
        #This means that order is consistent but 
        






class Bond:
    def __init__(self, app, atom1, atom2, order):
        self.app = app
        self.atoms = [atom1, atom2]
        self.order = order
        app.bonds.append(self)
    

    def __repr__(self):
        return f'{self.atoms},{self.order}'
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
        for atom in self.atoms:
            atom.updateHydrogens(self.app)
    
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
    def __init__(self, app, seed, ringNumber, startVector):
        app.bondOrder = 1
        self.app = app
        self.aromatic = app.aromatic
        self.atoms = [seed]
        self.n = ringNumber
        self.pos = seed.pos
        self.angle = - math.tau / self.n #the angle you rotate by each time. The ring generation is like a turtle
        self.bondLength = app.defaultBondLength
        self.vector = utils.rotateVector(startVector, 0.5*(math.pi + self.angle)) 
        #the angle I rotated by is to align the vector with the polygon
        self.generateRing()
        app.bondOrder = 1


    def generateRing(self):
        for _ in range(self.n - 1):
            if self.aromatic:             #If aromatic, you want alternating double bond single bonds (not literally putting in aromaticity)
                self.app.bondOrder = (self.app.bondOrder % 2) + 1 
            self.pos = utils.vectorSum(self.vector, self.pos)
            self.vector = utils.rotateVector(self.vector, self.angle)
            newAtom = Atom(self.app, element='C', parent = self.atoms[-1], position = self.pos, hydrogenUpdate=False)
            self.atoms.append(newAtom)

        
        self.atoms[0].addBond(self.atoms[-1], order =1)
        
        #Bond(self.app, self.atoms[0], self.atoms[-1], order = 1)
        







    def __repr__(self):
        res = '<'
        for atom in self.atoms:
            res += repr(atom) + ', '
        return res + '>'
    
    def __hash__(self):
        return hash(str(self))


#-----------------------------
#MOLECULE FUNCTION 90% WRITTEN BY AI
#cleaned up and integrated by me, because it's AI
#I can do a pretty good job of explaining it tho
#I was really looking forward to writing this algorithm and might remake it myself later,
#But just didn't have the time, and thought the functionality of this would be cool.
class Molecule:
    def __init__(self, app):
        self.app = app
        self.atoms = []  # List of Atom objects
        self.bonds = []  # List of Bond objects

    def addAtom(self, atom):
        if atom not in self.atoms:
            self.atoms.append(atom)
    def addBond(self, bond):
        if bond not in self.bonds:
            self.bonds.append(bond)


    def clean_2d_coordinates(self, bond_length=50.0):
        """
        Rebuilds the 2D coordinates of the molecule using a Breadth-First Search.
        Forces a standard 120-degree zig-zag layout for carbon chains.
        """
        if not self.atoms:
            return

        # 1. Reset all coordinates
        self.startPos = copy.copy(self.atoms[0].pos)
        for atom in self.atoms:
            atom.pos = (0.0, 0.0)

        # 2. Setup BFS
        visited = set()
        queue = deque()

        start_atom = self.atoms[0]
        start_atom.pos = (0.0, 0.0)
        visited.add(start_atom)
        
        # Queue stores: (current_atom, parent_atom, incoming_angle, turn_modifier)
        queue.append((start_atom, None, 0.0, 1))

        while queue:
            current_atom, parent_atom, incoming_angle, turn_modifier = queue.popleft()

            neighbors = []
            for bond in current_atom.bonds:
                neighbor = None
                for atom in bond.atoms:
                    if atom != current_atom:
                        neighbor = atom
                
                if neighbor and neighbor not in visited:
                    neighbors.append(neighbor)

            if not neighbors:
                continue

            # FIX 1: Sort neighbors so heavy atoms (C, N, O) are placed first!
            # This ensures they take the primary "zig-zag" slots, pushing H's to the outside.
            neighbors.sort(key=lambda a: 1 if a.element == 'H' else 0)

            if parent_atom is None:
                # Root atom: fan out evenly in a circle
                angle_step = (2 * math.pi) / len(neighbors)
                current_angle = 0.0
                for neighbor in neighbors:
                    new_x = current_atom.pos[0] + (bond_length * math.cos(current_angle))
                    new_y = current_atom.pos[1] + (bond_length * math.sin(current_angle))
                    neighbor.pos = (new_x, new_y)
                    
                    visited.add(neighbor)
                    queue.append((neighbor, current_atom, current_angle, 1))
                    current_angle += angle_step
            else:
                # FIX 2: Hardcode the angles for 2D chemical drawing
                # math.pi / 3 is exactly 60 degrees.
                offsets = [
                    turn_modifier * (math.pi / 3),   # Zig (+60 deg)
                    -turn_modifier * (math.pi / 3),  # Zag (opposite side, -60 deg)
                    0.0                              # Straight ahead (for a 3rd neighbor)
                ]

                for i, neighbor in enumerate(neighbors):
                    # Grab the offset based on what number neighbor this is
                    offset = offsets[i] if i < len(offsets) else 0.0
                    current_angle = incoming_angle + offset

                    new_x = current_atom.pos[0] + (bond_length * math.cos(current_angle))
                    new_y = current_atom.pos[1] + (bond_length * math.sin(current_angle))
                    
                    neighbor.pos = (new_x, new_y)
                    visited.add(neighbor)

                    # FIX 3: Only flip the zig-zag turn modifier for the FIRST neighbor 
                    # (which is the main backbone atom because we sorted the list above)
                    next_turn = -turn_modifier if i == 0 else turn_modifier
                    
                    queue.append((neighbor, current_atom, current_angle, next_turn))

    def relativeCoordsToRealCoords(self):
        for atom in self.atoms:
            pos = atom.pos
            atom.pos = utils.vectorSum(pos, self.startPos)

    def beautify(self):
        self.clean_2d_coordinates()
        self.relativeCoordsToRealCoords()


    #Get smiles function written by AI
    def get_smiles(self):
            """
            Generates a non-canonical SMILES string for the molecule via Depth-First Search.
            Explicit hydrogens are ignored as SMILES calculates them implicitly.
            """
            # 1. Filter out explicit Hydrogens (SMILES assumes standard valency)
            heavy_atoms = [atom for atom in self.atoms if atom.element != 'H']
            
            if not heavy_atoms:
                return ""

            # 2. Find a logical starting point (ideally an atom with only 1 heavy neighbor)
            def get_heavy_degree(atom):
                count = 0
                for bond in atom.bonds:
                    for neighbor in bond.atoms:
                        if neighbor != atom and neighbor.element != 'H':
                            count += 1
                return count

            start_atom = min(heavy_atoms, key=get_heavy_degree)

            # 3. Setup traversal state
            visited = set()
            ring_closures = {} # Tracks (atom1, atom2) -> ring_number
            ring_number = 1

            def dfs(current_atom, incoming_bond=None):
                nonlocal ring_number
                visited.add(current_atom)
                
                smiles_chunk = ""

                # A. Process the incoming bond order
                if incoming_bond:
                    if incoming_bond.order == 2:
                        smiles_chunk += "="
                    elif incoming_bond.order == 3:
                        smiles_chunk += "#"

                # B. Add the current element symbol
                smiles_chunk += current_atom.element

                # C. Find valid neighbors (heavy atoms we didn't just come from)
                neighbors_info = []
                for bond in current_atom.bonds:
                    if bond == incoming_bond: 
                        continue # Don't backtrack
                        
                    for neighbor in bond.atoms:
                        if neighbor != current_atom and neighbor.element != 'H':
                            neighbors_info.append((neighbor, bond))

                # D. Separate into rings (already visited) and branches (unvisited)
                unvisited_branches = []
                
                for neighbor, bond in neighbors_info:
                    if neighbor in visited:
                        # Ring closure detected!
                        # Create a unique, order-independent key for this pair
                        closure_pair = frozenset([current_atom, neighbor])
                        
                        if closure_pair not in ring_closures:
                            # First time seeing this ring bond, assign a number
                            ring_closures[closure_pair] = ring_number
                            smiles_chunk += str(ring_number)
                            ring_number += 1
                            if ring_number > 9: # Simple safeguard for standard parsing
                                ring_number = 1
                        else:
                            # This is the back-half of the ring closure
                            smiles_chunk += str(ring_closures[closure_pair])
                    else:
                        unvisited_branches.append((neighbor, bond))

                # E. Process unvisited branches
                for i, (neighbor, bond) in enumerate(unvisited_branches):
                    is_last = (i == len(unvisited_branches) - 1)
                    
                    # Recursively get the SMILES for the branch
                    branch_smiles = dfs(neighbor, bond)
                    
                    if not is_last:
                        # If it's not the last branch, wrap it in parentheses
                        smiles_chunk += f"({branch_smiles})"
                    else:
                        # The last branch just continues the main chain
                        smiles_chunk += branch_smiles

                return smiles_chunk

            # Run the recursive algorithm
            return dfs(start_atom)

                    


