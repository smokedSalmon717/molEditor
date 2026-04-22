import objects.objectAdder as objectAdder

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

















