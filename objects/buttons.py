

import objectAdder
#The template button was written by AI (Gemini)
#But the subclasses are written by me.
class Button:
    def __init__(self, x, y, w, h, text, callback, app):
        self.app = app
        self.rect = (x, y, w, h)
        self.callback = callback # The function to run when clicked
        self.text = text
        self.isActive = False

    def checkClick(self, mouse_x, mouse_y):
        x, y, w, h = self.rect
        if x <= mouse_x <= x + w and y <= mouse_y <= y + h:
            self.onClick()
            return True
        return False
        
    def onClick(self):
        pass


    


class drawingButton(Button):
    def checkIfActive(self):
        self.isActive = self.variable == self.output

    def onClick(self):
        self.callback(self.app)
        self.isActive = True

class selectionButton(Button):
    pass




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








