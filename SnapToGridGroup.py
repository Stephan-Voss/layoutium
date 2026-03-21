from PySide6.QtWidgets import QGraphicsItemGroup, QGraphicsItem
from PySide6.QtCore import QPointF

class SnapToGridGroup(QGraphicsItemGroup):
    def __init__(self):
        super().__init__()
        self.gridSize = 10
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)  # Enables itemChange()

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedChange and self.gridSize > 1:
            try:
                newPos = value
                snappedX = round(newPos.x() / self.gridSize) * self.gridSize
                snappedY = round(newPos.y() / self.gridSize) * self.gridSize
                print(QPointF(snappedX, snappedY))
                return QPointF(snappedX, snappedY)
            except Exception:
                pass
        return super().itemChange(change, value)
