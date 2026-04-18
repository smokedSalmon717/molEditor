


#The template button was written by AI (Gemini)
#But the subclasses are written by me.
class BaseButton:
    def __init__(self, x, y, w, h, callback):
        self.rect = (x, y, w, h)
        self.callback = callback # The function to run when clicked

    def checkClick(self, mouse_x, mouse_y):
        x, y, w, h = self.rect
        if x <= mouse_x <= x + w and y <= mouse_y <= y + h:
            self.on_click()
            return True
        return False
        
    def onClick(self):
        # To be overridden by subclasses
        pass


#structure of having the callback as a parameter of 
#the class which is itself a function came from the
#AI (Gemini), but the code itself is pretty much me
class ToggleButton(BaseButton):
    def __init__(self, x, y, w, h, callback, initialState=False):
        super().__init__(x, y, w, h, callback)
        self.isActive = initialState

    def onClick(self):
        self.isActive = not self.isActive
        self.callback(self.isActive) # callback is a function which sets the app variable



