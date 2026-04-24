import objects.objectAdder as objectAdder



#This is done in this horrible way
#where each button has its own function, and SOO much repetion

#My reasoning is that it streamlines the proccess on the main file.
#All button actions go through the same pipeline, if that makes sense

def showHydrogen(app):
    app.showHydrogens = not app.showHydrogens
    return app.basePath + 'showHydrogens.svg'

def singleBond(app):
    app.bondOrder = 1
    app.currentObject = objectAdder.addBondFunction
    return app.basePath + 'single.svg'



def doubleBond(app):
    app.bondOrder = 2
    app.currentObjetc = objectAdder.addBondFunction
    return app.basePath + 'double.svg'



def tripleBond(app):
    app.bondOrder = 3
    app.currentObject = objectAdder.addBondFunction
    return app.basePath + 'triple.svg'

def benzene(app):
    app.aromatic = True
    app.bondOrder = 1
    app.currentObject = objectAdder.addRing
    app.ringNumber = 6
    return app.basePath + 'benzene.svg'

def cyclohexane(app):
    app.aromatic = False
    app.bondOrder = 1
    app.currentObject = objectAdder.addRing
    app.ringNumber = 6
    return app.basePath + 'cyclohexane.svg'

def cyclopentane(app):
    app.aromatic = False
    app.bondOrder = 1
    app.currentObject = objectAdder.addRing
    app.ringNumber = 5
    return app.basePath + 'cyclopentane.svg'

def carbon(app):
    app.currElement = 'C'
    app.currentObject = objectAdder.addAtom
    return app.basePath + 'C.svg'

def oxygen(app):
    app.currElement = 'O'
    app.currentObject = objectAdder.addAtom
    return app.basePath + 'O.svg'

def hydrogen(app):
    app.currElement = 'H'
    app.currentObject = objectAdder.addAtom
    return app.basePath + 'H.svg'

def nitrogen(app):
    app.currElement = 'N'
    app.currentObject = objectAdder.addAtom
    return app.basePath + 'N.svg'
def chlorine(app):
    app.currElement = 'Cl'
    app.currentObject = objectAdder.addAtom
    return app.basePath + 'Cl.svg'

def cleanStructure(app):
    if app.molecules:
        for molecule in app.molecules:
            molecule.beautify()


    return app.basePath + 'O.svg'

def delete(app):
    app.atoms = []
    app.bonds = []
    app.molecules = []

    return app.basePath + 'H.svg'