import objects.objectAdder as objectAdder
import time
class Button:
    
    def __init__(self, x, y, w, h, callback, app):
        self.app = app
        self.rect = (x, y, w, h)
        self.callback = callback # The function to run when clicked
        self.imageKey = callback(app)
        self.isActive = False
        self.isPressed = False


    def checkClick(self, mouseX, mouseY):
        if self.isInside(mouseX, mouseY):
            self.onClick()
            return True
        return False
    
    def onClick(self):
        pass

    def isInside(self, mouseX, mouseY):
        x, y, w, h = self.rect
        return (x <= mouseX <= x + w) and (y <= mouseY <= y + h)
    def isOn(self):
        return self.isActive
    
    def updateButton(self):
        pass
    


class drawingButton(Button):


    def checkIfActive(self):
        self.isActive = self.variable == self.output

    def onClick(self):
        self.callback(self.app)
        self.isActive = not self.isActive



class actionButton(Button):
    def __init__(self, x, y, w, h, callback, app):
        super().__init__(x, y ,w, h, callback, app)
        self.lastClickTime = None

    def onClick(self):
        if not self.isPressed:
            self.callback(self.app)
            self.lastClickTime = time.time()
            self.isPressed = True
        

    def updateButton(self):
        if self.isPressed:
            timeElapsed = time.time() - self.lastClickTime
            if timeElapsed > 0.2:
                self.isPressed = False

    
class selectionButton(Button):

    def checkIfActive(self):
        self.isActive = self.variable == self.output

    def onClick(self):
        self.callback(self.app)
        self.isActive = not self.isActive



















