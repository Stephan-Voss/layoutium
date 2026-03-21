from PySide6.QtWidgets import QGraphicsItem, QGraphicsTextItem
from PySide6.QtGui import  QCursor, QTextBlockFormat, QPainter, QTextCharFormat, QPixmap
from PySide6.QtCore import Qt, QPointF, QRectF
#sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # Ensure current directory is in sys.path
from GraphicsScene import GraphicsScene

###
###
###
class GraphicsTextItem(QGraphicsTextItem):
    def __init__(self, text, font, name=""):
        super().__init__(text)
        self.setTextInteractionFlags(Qt.TextEditorInteraction) # Enable typing
        self.setFlags(QGraphicsTextItem.ItemIsSelectable | QGraphicsTextItem.ItemIsMovable)  # Allow selection
        #self.setFlag(QGraphicsTextItem.ItemIsMovable)
        self.setCursor(QCursor(Qt.OpenHandCursor))  # Change cursor to hand when hovering
        self._dragging = False  # Track if dragging
        self._drag_start_pos = QPointF()
        self.setFont(font)
        self.backgroundImage = None
        self.backgroundImagePath = None
        self.name = name
        self.visible = True
        self.lockedWidth = 200
        self.lockedHeight = 200
        self.isLocked = False
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.gridSize = 1
        self.snapToGrid = True
        self.padding = 5
#         self.selectedCmykColor = QColor.fromCmyk(0, 0, 0, 0)  # Default black
    
    def updatePadding(self):
        # Get the QTextDocument and set document margins
        doc = self.document()
        doc.setDocumentMargin(self.padding)
        self.setDocument(doc)  # Apply the document back
        #self.update()
        #self.scene().update()
        
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            scene = self.scene()  # Get the scene
            if isinstance(scene, GraphicsScene):  # Ensure it's our scene
                scene.parent().updatePositionInputs()  # Call method in main window
            if self.snapToGrid:
                newPos = value.toPoint()
                snappedX = round(newPos.x() / self.gridSize) * self.gridSize
                snappedY = round(newPos.y() / self.gridSize) * self.gridSize
                return QPointF(snappedX, snappedY)
        return super().itemChange(change, value)

    def boundingRect(self):
        return QRectF(0, 0, self.lockedWidth, self.lockedHeight) if self.isLocked else super().boundingRect()
    
    def mousePressEvent(self, event):
        # Notify the scene that this item was clicked 
        scene = self.scene()  # Get the scene
        if isinstance(scene, GraphicsScene):  # Ensure it's our scene
            scene.setActiveTextItem(self)  # Set this item as active
        # Handle selection correctly
        if event.button() == Qt.LeftButton:
            if event.modifiers() == Qt.ControlModifier:
                # Toggle selection if Ctrl is held
                self.setSelected(not self.isSelected())
                #scene.selectedItems.append(self)
            else:
                # Deselect others and select only this one
                scene.clearSelection()  # Clear all other selections
                self.setSelected(True)
        # Start dragging when the item is clicked (but not double-clicked).
        if event.button() == Qt.LeftButton and not event.modifiers() == Qt.ControlModifier:
            self._dragging = True
            self._drag_start_pos = event.scenePos() - self.pos()  # Store offset
            self.setCursor(QCursor(Qt.ClosedHandCursor))  # Change cursor to grabbing
        super().mousePressEvent(event)
        #self.setSelected(True)  # Mark this item as selected
        # Find corresponding layer list item and select it
        for i in range(self.scene().layerList.count()):
            listItem = self.scene().layerList.item(i)
            if listItem.data(Qt.UserRole) == self:  # Compare stored reference
                self.scene().layerList.setCurrentItem(listItem)
                break

    def mouseMoveEvent(self, event):
        # Move the item as long as the mouse is pressed.
        if self._dragging:
#             newPos = event.scenePos() - self._drag_start_pos
#             self.setPos(newPos)
            scene = self.scene()
            if scene:
                newPos = event.scenePos() - self._drag_start_pos
                if self.rotation() == 0:
                    if self.scene().cutBleed:
                        sceneRect = scene.sceneRect()
                    else:
                        bleed = 70 #int(2*3/25,4*300) # Includes bleed and margin, thus the 2*. Technically should be 71...
                        sceneRect = scene.sceneRect().adjusted(bleed, bleed, -bleed, -bleed)
                    # Constrain X position
                    newX = max( sceneRect.left(), min( newPos.x(), sceneRect.right() - self.boundingRect().width() ) )
                    # Constrain Y position
                    newY = max(sceneRect.top(), min(newPos.y(), sceneRect.bottom() - self.boundingRect().height()))
                else:
                    newX = newPos.x()
                    newY = newPos.y()
                # Set new position
                self.setPos(newX, newY)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        # Stop dragging when the mouse is released.
        self._dragging = False
        self.setCursor(QCursor(Qt.OpenHandCursor))  # Reset cursor
        super().mouseReleaseEvent(event)
        
    def mouseDoubleClickEvent(self, event):
#         cursor = self.textCursor()
#         cursor.movePosition(QTextCursor.End)
#         self.setTextCursor(cursor)
        # Enable text editing when double-clicked.
        self.setTextInteractionFlags(Qt.TextEditorInteraction)  # Enable editing
        self.setFocus()  # Focus on the text box
        parent = self.scene().views()[0].parent()
        if parent:
            parent.activeTextItem = self
        super().mouseDoubleClickEvent(event)

    def toDict(self):
        return {
            "text": self.toHtml(), #toPlainText(),
            "font": self.font().toString(),
            "x": self.x(),
            "y": self.y(),
            "name": self.name,
            "backgroundImagePath": self.backgroundImagePath,
            "visible": self.visible,
            "lockedWidth": self.lockedWidth,
            "lockedHeight": self.lockedHeight,
            "isLocked": self.isLocked,
            "gridSize": self.gridSize,
            "snapToGrid": self.snapToGrid,
            "padding": self.padding,
            "rotation": self.rotation()
            }
     
    @staticmethod
    def fromDict(data):
        font = QFont()
        font.fromString(data["font"])
        #item = GraphicsTextItem(data["text"], font)
        item = GraphicsTextItem("", font)
        #self.textEdit.setHtml(data.get("text", ""))
        #item.setHtml(data.get("text", ""))
        item.setHtml(data["text"])
        item.setPos(QPointF(data["x"], data["y"]))
        item.name = data["name"]
        if data["backgroundImagePath"]:
            item.setBackgroundImage(data["backgroundImagePath"])
        item.visible = data["visible"]
        item.lockedWidth = data["lockedWidth"]
        item.lockedHeight = data["lockedHeight"]
        item.isLocked = data["isLocked"]
        item.gridSize = data["gridSize"]
        item.snapToGrid = data["snapToGrid"]
        item.padding = data["padding"]
        item.updatePadding()
        item.setRotation(data["rotation"])
        return item
    
    def setBackgroundImage(self, filePath):
        self.backgroundImagePath = filePath
        if filePath:
            self.backgroundImage = QPixmap(filePath)
        else:
            self.backgroundImage = None
        self.update()

    def paint(self, painter, option, widget):
        if self.backgroundImage:
            painter.drawPixmap(self.boundingRect().toRect(), self.backgroundImage)
        super().paint(painter, option, widget)
    
    # Allow shortcuts to set text formatting.
    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            cursor = self.textCursor()
            fmt = QTextCharFormat()
            currentFormat = cursor.charFormat()
            blockFmt = QTextBlockFormat()
            useBlockFormat = False
            if event.key() == Qt.Key_B:
                fmt.setFontWeight(QFont.Bold if not cursor.charFormat().fontWeight() == QFont.Bold else QFont.Normal)
            elif event.key() == Qt.Key_I:
                fmt.setFontItalic(not cursor.charFormat().fontItalic())
            elif event.key() == Qt.Key_U:
                fmt.setFontUnderline(not cursor.charFormat().fontUnderline())
            elif event.key() == Qt.Key_K:  # Ctrl+K for Small Caps
                capitalization = (QFont.SmallCaps if currentFormat.fontCapitalization() != QFont.SmallCaps else QFont.MixedCase)
                fmt.setFontCapitalization(capitalization)
            elif event.key() == Qt.Key_Up:  # Ctrl+Up arrow for Superscript
                fmt.setVerticalAlignment(QTextCharFormat.AlignSuperScript)
            elif event.key() == Qt.Key_Down:  # Ctrl+Down arrow for Subsscript
                fmt.setVerticalAlignment(QTextCharFormat.AlignSubScript)
            elif event.key() == Qt.Key_P:  # Ctrl + P to apply selected CMYK color
                    fmt.setForeground(self.scene().selectedCMYKColor)
            elif event.key() == Qt.Key_D:  # Ctrl + D to open color picker
                self.scene().openColorPicker()
                return
            elif event.key() == Qt.Key_Q:
                    self.setResizable(not self.resizable)
            elif event.key() == Qt.Key_L:  # Ctrl + L -> Left Align
                blockFmt.setAlignment(Qt.AlignLeft)
                useBlockFormat = True
            elif event.key() == Qt.Key_E:  # Ctrl + E -> Center Align
                if self.isLocked:
                    self.document().setTextWidth(self.lockedWidth)
                blockFmt.setAlignment(Qt.AlignCenter)
                useBlockFormat = True
            elif event.key() == Qt.Key_R:  # Ctrl + R -> Right Align
                blockFmt.setAlignment(Qt.AlignRight)
                useBlockFormat = True
            elif event.key() == Qt.Key_J:  # Ctrl + J -> Justify
                blockFmt.setAlignment(Qt.AlignJustify)
                useBlockFormat = True
                # Enable word wrap and set text width for justification to work
                self.document().setTextWidth(self.boundingRect().width())
            else:
                super().keyPressEvent(event)
                return
            if useBlockFormat:
                # **Critical Fix:** Ensure text stays within the bounding box
#                 if self.isLocked:
#                     self.document().setTextWidth(self.lockedWidth)
                cursor.mergeBlockFormat(blockFmt)  # Apply format
                self.setTextCursor(cursor)  # Ensure changes take effect
                self.document().adjustSize()  # Force document layout update
                self.update()  # Refresh the QGraphicsTextItem
            else:
                cursor.mergeCharFormat(fmt)
                self.setTextCursor(cursor)
        else:
            super().keyPressEvent(event)
                
    def toggleVisibility(self):
        """Toggle visibility and return the new state."""
        self.setVisible(not self.isVisible())
        self.visible = self.isVisible()
        return self.visible
    