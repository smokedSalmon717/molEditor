from cmu_graphics import *
from objects.objects import Atom
import math
import utils

def drawSelection(app):
    if app.parentAtom != None:
        drawCircle(*app.parentAtom.pos, 15, fill='gray', opacity=25)  
    for atom in app.selectedAtomList:
        drawCircle(*atom.pos, 20, fill='cyan',opacity = 20)
    if app.selectedBond != None:
        x1, y1, x2, y2 = app.selectedBond.endpoints
        cx, cy = (x1 + x2)/2, (y1 + y2)/2
        angle = 90 - math.degrees(math.atan2(x1-x2,y1-y2))
        width = distance(x1, y1, x2, y2)
        drawOval(cx, cy, width, 20, rotateAngle=angle, fill='yellow', opacity=25)
        
def drawAtoms(app):
    for atom in app.atoms:
        width, height= getImageSize(atom.imagePath)
        scale = app.atomSize / max(height, width)
        height, width = height*scale, width*scale
        drawImage(atom.imagePath, *atom.pos, height= height, width =width, align='center')

def drawBonds(app):
    for bond in app.bonds:
        x1, y1, x2, y2 = bond.endpoints
        drawBond(app, (x1, y1), (x2, y2), bond.order)


            
def drawBond(app, pos1, pos2, order=1):
        dx, dy = (pos1[1] - pos2[1]),(pos1[0] - pos2[0])
        angle = math.atan2(dx,dy)
        end1 = (pos1[0] - math.cos(angle) * app.bondGap,
                pos1[1] - math.sin(angle) * app.bondGap)
        end2 = (pos2[0] + math.cos(angle) * app.bondGap,
                pos2[1] + math.sin(angle) * app.bondGap)
        if order % 2 == 1:    # if even bond order, draw a middle line
            drawLine(*end1, *end2)
        if order > 1:       # if 2 or 3, draw offset lines
            end1up, end1down = utils.getDoubleBondOffsetPoints(angle, end1, order*2)
            end2up, end2down = utils.getDoubleBondOffsetPoints(angle, end2, order*2)
            drawLine(*end1up, *end2up)
            drawLine(*end1down,*end2down)
                  
def drawTempBond(app):
    if app.tempAtomPos and app.parentAtom in app.atoms:
        drawBond(app, app.parentAtom.pos, app.tempAtomPos, app.bondOrder)

def drawSketchpad(app):
    drawSelection(app)
    drawAtoms(app)
    drawBonds(app)
    drawTempBond(app)




def drawButtons(app):
    def drawButtonBody(button):
        x, y, w, h  = button.rect
        color = rgb(220,220,215)
        if button.isPressed:
            color = rgb(150,150,135)
        drawRect(x, y, w, h, fill=color, border=rgb(10,10,30)) #drawing border
    def drawButtonIcon(button):
        height, width = getImageSize(button.imageKey)
        aspectRatio = height/width 
        x, y, w, h  = button.rect
        drawImage(button.imageKey, x + w/2, y + h/2, width=30*aspectRatio, height=30, align='center')
    def drawButtonHighlight(button):
        if button.isOn():
            drawRect(*button.rect, fill='red', opacity=25)

    for button in app.buttons:
        button.updateButton()
        drawButtonBody(button)
        drawButtonIcon(button)
        drawButtonHighlight(button)






