from PySide6.QtWidgets import QAbstractItemView, QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsTextItem, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLineEdit, QLabel, QFontDialog, QTextBrowser, QGraphicsPixmapItem, QToolBar
from PySide6.QtGui import  QPen, QColor, QCursor, QPageSize, QPdfWriter, QPagedPaintDevice, QFont, QPainter, QTextCursor, QTextFormat, QTextImageFormat, QTextCharFormat, QImage, QTextDocument, QPixmap, QAction, QKeySequence, QIcon
from PySide6.QtCore import Qt, QPointF, QByteArray, QUrl, QRectF, QMargins, QSizeF
import json
import sys

###
###
###
class GraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        #self.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)  # Zoom towards cursor
        # Zoom stuff.
        self.zoomFactor = 1.2  # Adjust zoom sensitivity
        self.minZoom = 0.1  # Minimum zoom level
        self.maxZoom = 5.0  # Maximum zoom level
        self.currentZoom = 1.0  # Track zoom level
        #self.cutBleed = False

#     def toggleBleed(self):
#         self.cutBleed = not self.cutBleed
#         self.updateViewportMargins()    

#     def updateViewportMargins(self):
#         bleed = 35 if self.scene().cutBleed else 0
#         self.setSceneRect( self.scene().sceneRect().adjusted(bleed, bleed, -bleed, -bleed) )
#         self.viewport().update()
        
    def wheelEvent(self, event):
        #Zoom in/out with mouse wheel.
        delta = event.angleDelta().y()
        if event.modifiers() & Qt.ControlModifier:  # Check if Ctrl is held
            if delta > 0:
                self.zoomIn()
            else:
                self.zoomOut()
        super().wheelEvent(event)
        
    def zoomIn(self):
        #Zoom in with a scaling factor.
        if self.currentZoom < self.maxZoom:
            self.scale(self.zoomFactor, self.zoomFactor)
            self.currentZoom *= self.zoomFactor

    def zoomOut(self):
        #Zoom out with a scaling factor.
        if self.currentZoom > self.minZoom:
            self.scale(1 / self.zoomFactor, 1 / self.zoomFactor)
            self.currentZoom /= self.zoomFactor

    def resetZoom(self):
        #Reset zoom to original scale.
        self.resetTransform()
        self.currentZoom = 1.0
        
