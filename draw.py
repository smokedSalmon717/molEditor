from cmu_graphics import *
from objects import Atom
import math
import utils

def drawSelection(app):
    if app.parentAtom != None:
        drawCircle(*app.parentAtom.pos, 15, fill='gray', opacity=25)  
    for atom in app.selectedAtomList:
        drawCircle(*atom.pos, 20, fill='cyan',opacity = 20)
        
def drawAtoms(app):
    for atom in app.atoms:
        element = atom.element
        color = Atom.colorMap[element]
        drawLabel(atom.id(),*atom.pos, size=16, fill=color)
        
def drawBonds(app):
    bonds = getBonds(app)
    for atom1, atom2, order in bonds:
        pos1, pos2 = atom1.pos, atom2.pos
        drawBond(app, pos1, pos2, order)

def getBonds(app):
    bonds = set()
    for atom in app.atoms:
        for other in atom.bonds:
            atom1, atom2 = max(atom, other), min(atom, other)
            bondOrder = atom.bonds[other]
            bonds.add((atom1, atom2, bondOrder))
    return bonds
            
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
    for button in app.buttons:
        #color = rgb(150, 150, 150) if button.isActive else rgb(100, 100, 100)
        drawRect(*button.rect, fill=None, border='black') #drawing border
        if button.isOn():
            drawRect(*button.rect, fill='red', opacity=50)

        x, y, w, h  = button.rect

        drawImage(button.imageKey, x + w/2, y + w/2, width=30, height=30, align='center')