import objectAdder

class Button:
    
    def __init__(self, x, y, w, h, callback, app, imageKey):
        self.app = app
        self.rect = (x, y, w, h)
        self.callback = callback # The function to run when clicked
        self.imageKey = imageKey
        self.isActive = False

    def checkClick(self, mouseX, mouseY):
        x, y, w, h = self.rect
        if self.isInside(mouseX, mouseY):
            self.onClick()
            return True
        return False
    
    def isInside(self, mouseX, mouseY):
        x, y, w, h = self.rect
        return (x <= mouseX <= x + w) and (y <= mouseY <= y + h)
    
    def isOn(self):
        return self.isActive
        #No real good reason for this, I just noticed that in hw examples
        #these sorts of properties that are checked externally and not internally tend to be methods 
        #instead of variables. Also makes it more clear what is going on
    

        
    def onClick(self):
        pass

class drawingButton(Button):
    def checkIfActive(self):
        self.isActive = self.variable == self.output

    def onClick(self):
        self.callback(self.app)
        self.isActive = not self.isActive

class selectionButton(Button):
    pass



#No reason for these functions to be here structurely, but it makes things code easier for me
def singleBond(app):
    app.bondOrder = 1
    app.currentObject = objectAdder.addAtom

def doubleBond(app):
    app.bondOrder = 2
    app.currentObjetc = objectAdder.addAtom


def tripleBond(app):
    app.bondOrder = 3
    app.currentObject = objectAdder.addAtom

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


    


class drawingButton(Button):
    def checkIfActive(self):
        self.isActive = self.variable == self.output

    def onClick(self):
        self.callback(self.app)
        self.isActive = not self.isActive

class selectionButton(Button):
    pass

















