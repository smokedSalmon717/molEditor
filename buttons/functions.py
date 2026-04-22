import objects.objectAdder as objectAdder


#This is done in this horrible way
#where each button has its own function, and SOO much repetion

#My reasoning is that it streamlines the proccess on the main file.
#All button actions go through the same pipeline, if that makes sense

def singleBond(app):
    app.bondOrder = 1
    app.currentObject = objectAdder.addBond



def doubleBond(app):
    app.bondOrder = 2
    app.currentObjetc = objectAdder.addBond


def tripleBond(app):
    app.bondOrder = 3
    app.currentObject = objectAdder.addBond

def benzene(app):
    app.aromatic = True
    app.bondOrder = 1
    app.currentObject = objectAdder.addRing
    app.ringNumber = 6

def cyclohexane(app):
    app.aromatic = False
    app.bondOrder = 1
    app.currentObject = objectAdder.addRing
    app.ringNumber = 6

def cyclopentane(app):
    app.aromatic = False
    app.bondOrder = 1
    app.currentObject = objectAdder.addRing
    app.ringNumber = 5

def carbon(app):
    app.element = 'C'
    app.currentObject = objectAdder.addAtom

def oxygen(app):
    app.element = 'O'
    app.currentObject = objectAdder.addAtom

def hydrogen(app):
    app.element = 'H'
    app.currentObject = objectAdder.addAtom

def nitrogen(app):
    app.element = 'N'
    app.currentObject = objectAdder.addAtom

