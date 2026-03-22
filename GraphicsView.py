from PySide6.QtWidgets import QGraphicsView
from PySide6.QtGui import  QPainter
from PySide6.QtCore import Qt

###
### The view handles which parts of the scene we actually see.
###
class GraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        # Zoom stuff.
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)  # Zoom towards cursor
        self.zoomFactor = 1.2  # Adjust zoom sensitivity
        self.minZoom = 0.1  # Minimum zoom level
        self.maxZoom = 5.0  # Maximum zoom level
        self.currentZoom = 1.0  # Track zoom level
        
        
    ## Zoom in/out with mouse wheel.
    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if event.modifiers() & Qt.ControlModifier:  # Check if Ctrl is held
            if delta > 0:
                self.zoomIn()
            else:
                self.zoomOut()
        super().wheelEvent(event)
    
    
    ## Zoom in with a scaling factor.
    def zoomIn(self):
        if self.currentZoom < self.maxZoom:
            self.scale(self.zoomFactor, self.zoomFactor)
            self.currentZoom *= self.zoomFactor

    
    ## Zoom out with a scaling factor.
    def zoomOut(self):
        if self.currentZoom > self.minZoom:
            self.scale(1 / self.zoomFactor, 1 / self.zoomFactor)
            self.currentZoom /= self.zoomFactor

    ## Reset zoom to original scale.
    def resetZoom(self):
        self.resetTransform()
        self.currentZoom = 1.0
        
