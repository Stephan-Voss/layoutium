from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsTextItem, QGraphicsItem, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLineEdit, QLabel, QFontDialog, QTextBrowser, QGraphicsPixmapItem, QToolBar
from PySide6.QtGui import  QPen, QColor, QCursor, QPageSize, QPdfWriter, QPagedPaintDevice, QFont, QPainter, QTextCursor, QTextFormat, QTextImageFormat, QTextCharFormat, QImage, QTextDocument, QPixmap, QAction, QKeySequence, QIcon
from PySide6.QtCore import Qt, QPointF, QByteArray, QUrl, QRectF, QMargins, QSizeF
import json
import os
import sys
#sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # Ensure current directory is in sys.path
from SnapToGridGroup import SnapToGridGroup
from CMYKColorDialog import CMYKColorDialog
from tools import *

###
###
###
class GraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.activeTextItem = None  # Store active item. The CustomGraphicsScene ensures that the GraphicsEditor and the GraphicsTextItems agree on activeTextItem.
        # Scene frame border stuff.
        self.framePen = QPen(QColor(0, 0, 0), 2)  # Black border, 2px thick
        self.framePen.setStyle(Qt.SolidLine)
        self.layerList = None
        self.currentGroup = None
        self.backgroundPixmap = None
        self.cutBleed = False
        self.selectedCMYKColor = QColor.fromCmyk(0, 0, 0, 0)  # Default black
    
    def openColorPicker(self):
        """Opens the CMYK color picker dialog and sets the selected color."""
        dialog = CMYKColorDialog()
        if dialog.exec():
            color = dialog.getSelectedColor()
            self.selectedCMYKColor = color 
            r, g, b, _ = color.getRgb()
            self.parent().colorBox.setStyleSheet(f"background-color: rgb({r},{g},{b}); border: 1px solid gray;")

    # Allow snap-to-grid for groups. NOT WORKING!
    def createItemGroupNOTWORKING(self, selectedItems):
        # Create a new custom group
        group = SnapToGridGroup()
        #group.scene = self
        self.addItem(group)
        # Add existing items to the group
        for item in selectedItems:
            group.gridSize = item.gridSize
            group.addToGroup(item)
        return group
            
    def groupSelectedItems(self):
        """Groups selected items into a QGraphicsItemGroup"""
        selectedItems = self.selectedItems()
        #Break any preexisting group.
        if self.currentGroup:
            self.ungroupItems()
        #Create a new group.        
        if len(selectedItems) > 1:
            group = self.createItemGroup(selectedItems)
            group.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
            self.currentGroup = group  # Store reference to the group

    def ungroupItems(self):
        """Ungroups the items"""
        if self.currentGroup:
            # Get all child items for deselection in a bit.
            items = list(self.currentGroup.childItems())
            # Tear down group.
            self.destroyItemGroup(self.currentGroup)
            self.currentGroup = None
            self.clearSelection()
            # Ensure that items are completely deselected.
            for item in items:
                item.setSelected(False)  # Explicitly deselect
            self.update()
            
    def setActiveTextItem(self, item):
        self.activeTextItem = item
        self.parent().activeTextItem = item
        self.parent().updatePositionInputs()
        self.parent().updateGridInput()
        self.parent().updateBoxLockSize()
        self.parent().updatePaddingInput()
        self.parent().updateRotationInput()

    def getActiveTextItem(self):
        return self.activeTextItem
    
    def drawBackground(self, painter, rect):
        #
        if self.backgroundPixmap:
            painter.drawPixmap(self.sceneRect().topLeft(), QPixmap(self.backgroundPixmap), self.sceneRect())
            self.update()
#         else:
#             return
        #Draw a frame around the scene.
        painter.setPen(self.framePen)
        painter.drawRect(self.sceneRect())  # Draws the border around the scene
        super().drawBackground(painter, rect)
        
    def toggleBleed(self):
        self.cutBleed = not self.cutBleed
        if self.cutBleed:
            
            self.parent().bleedIcon = getAssetPath("Assets", "Bleed Off Icon.png")
            self.bleedTooltip = "Turn Bleed On"
        else:
            self.parent().bleedIcon = getAssetPath("Assets", "Bleed On Icon.png")
            self.parent().bleedTooltip = "Turn Bleed Off"
        # Update the QAction icon and tooltip
        self.parent().toggleBleedAction.setIcon(QIcon(self.parent().bleedIcon))
        self.parent().toggleBleedAction.setToolTip(self.parent().bleedTooltip)
        #self.parent().view.updateViewportMargins()

        
