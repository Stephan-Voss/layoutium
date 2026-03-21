from PySide6.QtWidgets import QListWidget, QMenu, QLineEdit
from PySide6.QtCore import Qt, QPoint, QRect, QSize
from PySide6.QtGui import  QAction, QIcon

class LayerControl(QListWidget):
    """A list widget that allows reordering and deletion of layers."""
    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.setDragDropMode(QListWidget.InternalMove)
        self.itemDoubleClicked.connect(self.renameLayer)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setSelectionMode
        self.customContextMenuRequested.connect(self.openContextMenu)
        self.currentItemChanged.connect(self.highlightGraphicsItem)
        
    def openContextMenu(self, pos: QPoint):
        """Opens a right-click context menu for deleting layers."""
        item = self.itemAt(pos)
        if item:
            menu = QMenu(self)
            deleteAction = QAction("Delete", self)
            deleteAction.triggered.connect(lambda: self.deleteLayer(item))
            menu.addAction(deleteAction)
            menu.exec(self.mapToGlobal(pos))

    def deleteLayer(self, item):
        """Deletes the selected layer from the list and scene."""
        graphicsItem = item.data(Qt.UserRole)
#         graphicsRef = item.data(Qt.UserRole)  # Returns a weak reference
#         graphicsItem = graphicsRef() if graphicsRef else None  # Dereference
        if graphicsItem:
            self.scene.removeItem(graphicsItem)  # Remove from scene
        self.takeItem(self.row(item))  # Remove from list

    def updateLayers(self):
        """Update the scene stacking order based on list order."""
        for i in range(self.count()):
            item = self.item(i)
            graphicsItem = item.data(Qt.UserRole)
#             graphicsRef = item.data(Qt.UserRole)  # Returns a weak reference
#             graphicsItem = graphicsRef() if graphicsRef else None  # Dereference
            if graphicsItem:
                graphicsItem.setZValue(self.count() - i)
    
    def dropEvent(self, event):
        super().dropEvent(event)
        self.updateLayers()

    def renameLayer(self, item):
        """Allows renaming a layer via an inline text edit."""
        edit = QLineEdit(item.text())
        self.setItemWidget(item, edit)
        edit.setFocus()
        edit.returnPressed.connect(lambda: self.finishRename(item, edit))

    def finishRename(self, item, edit):
        """Applies the new name after editing."""
        newName = edit.text().strip()
        if newName:
            item.setText(newName)
            graphicsItem = item.data(Qt.UserRole)
#             graphicsRef = item.data(Qt.UserRole)  # Returns a weak reference
#             graphicsItem = graphicsRef() if graphicsRef else None  # Dereference
            if graphicsItem:
                graphicsItem.name = newName
        self.setItemWidget(item, None)  # Remove the QLineEdit

    def highlightGraphicsItem(self, current, previous):
        if current:
            graphicsItem = current.data(Qt.UserRole)
            if graphicsItem:
                #graphicsItem.scene().clearSelection()  # Optional: Deselect others
                graphicsItem.setSelected(True)
                #graphicsItem.scene().views()[0].centerOn(graphicsItem)  # Optional: Center view

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        if item:
             # Get the size of the icon
            iconSize = item.icon().actualSize(QSize(20, 20))  # Adjust the size as necessary
            # Get the rect of the item
            itemRect = self.visualItemRect(item)
            # Check if the icon area was clicked
            iconRect = QRect(itemRect.topLeft(), iconSize)
            #iconRect.moveCenter(itemRect.center())  # Center the icon rect within the item rect
            graphicsItem = item.data(Qt.UserRole)  # Retrieve the associated graphics item
            if iconRect.contains(event.pos()):
                # If icon is clicked, toggle visibility
                #graphicsItem = item.data(Qt.UserRole)  # Retrieve the associated graphics item
                if graphicsItem:
                    graphicsItem.visible = not graphicsItem.visible # Toggle item state.
                    visible = graphicsItem.visible
                    graphicsItem.setVisible(visible)  # Actually hide/show the item in the scene
                    item.setIcon(QIcon("Eyecon - Shown.png" if visible else "Eyecon - Hidden.png"))
                    #self.repaint() #self.update()
                    #item.setCheckState(Qt.Checked if visible else Qt.Unchecked)  # Update check state
                return  # Prevent further processing (like editing text)
            elif not event.modifiers() == Qt.ControlModifier:
                self.scene.clearSelection() # Apparently, the scene will remember the selections unless we do this.
                self.scene.setActiveTextItem(graphicsItem)
        # If not on the icon, let the base class handle the event
        super().mousePressEvent(event)
        