from PySide6.QtWidgets import QInputDialog, QMainWindow, QTabWidget, QPushButton
from PySide6.QtCore import QTimer
from GraphicsEditor import GraphicsEditor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Layoutium")
        self.resize(1000, 700)
        self.menuBar()
        
         # Create a tab widget with closable tabs
        self.tabWidget = QTabWidget()
        self.tabWidget.setTabsClosable(True)  # Enable close buttons on tabs
        #self.tabWidget.tabCloseRequested.connect(self.closeTab)  # Handle tab closing
        
        # Set the QTabWidget as the central widget
        self.setCentralWidget(self.tabWidget)
        
        # Add a button that will appear to the right of the last tab
         #self.buttonUpdateTimer = None  # Used for debouncing updateButtonPosition calls if many are made with high frequency.
        self.addTabButton = QPushButton("+", self)
        self.addTabButton.clicked.connect(self.addNewTab)
        self.addTabButton.setFixedSize(30, 25)  # Set button size
        
        # Update button position whenever tabs change
        self.tabWidget.tabBar().currentChanged.connect(self.updateMenu)
        #self.tabWidget.tabBar().tabMoved.connect(self.updateButtonPosition) # Not sure what this one is good for...
        self.tabWidget.tabCloseRequested.connect(self.removeTab)
        
        # Create first tab
        self.addNewTab()
        
        
    def addNewTab(self, selection=None):
        if not selection:
            listItems = ["Editor"] # TODO: Add "Fragment" when code is ready.
            selection, ok = QInputDialog.getItem(None, "Layoutium Subapps", "Which subapp would you like?", listItems, 0, False)
            if not ok:
                return
            
        # Add a new tab with the given widget.
        if selection and selection == "Editor": 
            widget = GraphicsEditor(self)
            widget.name = "Edith"
        
        title = widget.name
        index =  self.tabWidget.addTab(widget, title) #f"Tab {self.tabWidget.count() + 1}") #(widget, title)
        self.tabWidget.setCurrentIndex(index)
        self.updateButtonPosition()
    
    
    def removeTab(self, index):
        self.tabWidget.removeTab(index)
        self.updateButtonPosition()

    def updateButtonPosition(self):
#         if self.buttonUpdateTimer:
#             return  # A timer is already scheduled
        QTimer.singleShot(0, self._update_button_position)

    def _update_button_position(self):
#         self.buttonUpdateTimer = None  # Reset the timer reference        
        # Move the add tab button to the right of the last tab. 
        tabBar = self.tabWidget.tabBar()
        if self.tabWidget.count() == 0:
            self.addTabButton.move(10, tabBar.geometry().y())  # Default position
            return
        lastTabIndex = self.tabWidget.count() - 1
        lastTabRect = tabBar.tabRect(lastTabIndex)
        xPosition = lastTabRect.right() # Adjust spacing
        #    menuHeight = self.menu.height()
        #yPosition = tabBar.geometry().y() + (tabBar.height() - self.addTabButton.height()) // 2 + menuHeight
        yPosition = 33
        
        self.addTabButton.move(xPosition, yPosition)

    def updateMenu(self):
        widget  = self.tabWidget.currentWidget()
        if widget:
            widget.createMenu(self)
        else:
            self.menuBar().clear()

#     def closeTab(self, index):
#         # Closes the tab at the given index.
#         self.tabWidget.removeTab(index)
