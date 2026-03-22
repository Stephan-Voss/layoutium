from PySide6.QtWidgets import QListWidget, QMenu, QLineEdit
from PySide6.QtCore import Qt, QPoint, QRect, QSize
from PySide6.QtGui import  QAction

###
### A list widget that allows reordering and deletion of layers (boxes).
###
class LayerControl(QListWidget):
    
    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.setDragDropMode(QListWidget.InternalMove)
        self.itemDoubleClicked.connect(self.renameLayer)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setSelectionMode
        self.customContextMenuRequested.connect(self.openContextMenu)
        self.currentItemChanged.connect(self.highlightGraphicsItem)
    
    
    # Opens a right-click context menu for deleting layers.
    def openContextMenu(self, pos: QPoint):
        item = self.itemAt(pos)
        if item:
            menu = QMenu(self)
            deleteAction = QAction("Delete", self)
            deleteAction.triggered.connect(lambda: self.deleteLayer(item))
            menu.addAction(deleteAction)
            menu.exec(self.mapToGlobal(pos))


    ## Deletes the selected layer from the list and scene.
    def deleteLayer(self, item):
        graphicsItem = item.data(Qt.UserRole)
        if graphicsItem:
            self.scene.removeItem(graphicsItem)  # Remove from scene
        self.takeItem(self.row(item))  # Remove from list


    # Update the scene stacking order based on list order.
    def updateLayers(self):
        for i in range(self.count()):
            item = self.item(i)
            graphicsItem = item.data(Qt.UserRole)
            if graphicsItem:
                graphicsItem.setZValue(self.count() - i)

    
    def dropEvent(self, event):
        super().dropEvent(event)
        self.updateLayers()

    
    # Allows renaming a layer via an inline text edit.
    def renameLayer(self, item):
        edit = QLineEdit(item.text())
        self.setItemWidget(item, edit)
        edit.setFocus()
        edit.returnPressed.connect(lambda: self.finishRename(item, edit))


    # Applies the new layer name after editing.
    def finishRename(self, item, edit):
        newName = edit.text().strip()
        if newName:
            item.setText(newName)
            graphicsItem = item.data(Qt.UserRole)
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
            graphicsItem = item.data(Qt.UserRole)  # Retrieve the associated graphics item
            if not event.modifiers() == Qt.ControlModifier:
                self.scene.clearSelection() # Apparently, the scene will remember the selections unless we do this.
                self.scene.setActiveTextItem(graphicsItem)
        # Let the base class handle the event
        super().mousePressEvent(event)
        