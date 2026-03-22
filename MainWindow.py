from PySide6.QtWidgets import QInputDialog, QMainWindow, QTabWidget, QPushButton
from PySide6.QtCore import QTimer
from GraphicsEditor import GraphicsEditor

### 
### The main window which opens and holds tabbed subapps/widgets.
### Note that menus are part of the indvidual apps, not MainWindow.
###
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Layoutium")
        self.resize(1000, 700)
        self.menuBar()
        
        # Create a tab widget with closable tabs
        self.tabWidget = QTabWidget()
        self.tabWidget.setTabsClosable(True)  # Enable close buttons on tabs
                
        # Set the QTabWidget as the central widget
        self.setCentralWidget(self.tabWidget)
        
        # Add a button that will appear to the right of the last tab
        self.addTabButton = QPushButton("+", self)
        self.addTabButton.clicked.connect(self.addNewTab)
        self.addTabButton.setFixedSize(30, 25)  # Set button size
        
        # Update button position whenever tabs change
        self.tabWidget.tabBar().currentChanged.connect(self.updateMenu)
        self.tabWidget.tabCloseRequested.connect(self.removeTab)
        
        # Create first tab
        self.addNewTab()
        
        
    def addNewTab(self, selection=None):
        if not selection:
            listItems = ["Editor"] # TODO: Add "Fragment" when code is ready.
            selection, ok = QInputDialog.getItem(None, "Layoutium Subapps", "Which subapp would you like?", listItems, 0, False)
            if not ok:
                return
            
        # Add a new tab with the given app/widget.
        if selection and selection == "Editor": 
            widget = GraphicsEditor(self)
            widget.name = "Edith"
        
        title = widget.name
        index = self.tabWidget.addTab(widget, title)
        self.tabWidget.setCurrentIndex(index)
        self.updateButtonPosition()
    
    
    def removeTab(self, index):
        self.tabWidget.removeTab(index)
        self.updateButtonPosition()


    def updateButtonPosition(self):
        QTimer.singleShot(0, self._updateButtonPosition)


    def _updateButtonPosition(self):
        # Move the add tab button to the right of the last tab. 
        tabBar = self.tabWidget.tabBar()
        if self.tabWidget.count() == 0:
            self.addTabButton.move(10, tabBar.geometry().y())  # Default position
            return
        lastTabIndex = self.tabWidget.count() - 1
        lastTabRect = tabBar.tabRect(lastTabIndex)
        xPosition = lastTabRect.right() # Adjust spacing
        yPosition = 33
        self.addTabButton.move(xPosition, yPosition)


    def updateMenu(self):
        widget  = self.tabWidget.currentWidget()
        if widget:
            widget.createMenu(self)
        else:
            self.menuBar().clear()
