from PySide6.QtWidgets import (
    QApplication, QGraphicsScene, QGraphicsView, QGraphicsTextItem, 
    QVBoxLayout, QHBoxLayout, QDialog, QPushButton, QLabel, QSlider, QWidget
)
from PySide6.QtGui import QFont, QTextCursor, QTextCharFormat, QColor
from PySide6.QtCore import Qt, Signal

class CMYKColorDialog(QDialog):
    colorSelected = Signal(QColor)  # Signal to send selected color

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select CMYK Color")
        self.setFixedSize(300, 250)

        layout = QVBoxLayout()
        self.sliders = {}
        self.labels = {}

        # Create sliders for C, M, Y, K values
        for color in ["C", "M", "Y", "K"]:
            row = QHBoxLayout()
            label = QLabel(f"{color}: 0")
            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 255)
            slider.valueChanged.connect(lambda val, l=label, c=color: self.updateLabel(l, val, c))
            self.sliders[color] = slider
            self.labels[color] = label

            row.addWidget(QLabel(color))
            row.addWidget(slider)
            row.addWidget(label)
            layout.addLayout(row)

        # Color Preview Box
        self.colorPreview = QWidget()
        self.colorPreview.setFixedSize(100, 50)
        self.colorPreview.setStyleSheet("background-color: black; border: 1px solid gray;")

        previewLayout = QHBoxLayout()
        previewLayout.addWidget(QLabel("Preview:"))
        previewLayout.addWidget(self.colorPreview)
        layout.addLayout(previewLayout)
        
        # OK and Cancel buttons
        btnLayout = QHBoxLayout()
        okBtn = QPushButton("OK")
        cancelBtn = QPushButton("Cancel")
        okBtn.clicked.connect(self.accept)
        cancelBtn.clicked.connect(self.reject)
        btnLayout.addWidget(okBtn)
        btnLayout.addWidget(cancelBtn)

        layout.addLayout(btnLayout)
        self.setLayout(layout)

        # Update preview when sliders change
        for slider in self.sliders.values():
            slider.valueChanged.connect(self.updatePreview)

    def updateLabel(self, label, value, color):
        label.setText(f"{color}: {value}")

    def getSelectedColor(self):
        """Returns the selected CMYK color as a QColor."""
        c, m, y, k = [self.sliders[color].value() for color in ["C", "M", "Y", "K"]]
        return QColor.fromCmyk(c, m, y, k)

    def updatePreview(self):
        """Updates the preview box color."""
        color = self.getSelectedColor()
        r, g, b, _ = color.getRgb()
        self.colorPreview.setStyleSheet(f"background-color: rgb({r},{g},{b}); border: 1px solid gray;")

