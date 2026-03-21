from PySide6.QtWidgets import QListWidgetItem, QWidgetAction, QToolButton, QHBoxLayout, QVBoxLayout, QWidget, QFileDialog, QLineEdit, QLabel, QFontDialog, QToolBar
from PySide6.QtGui import  QKeyEvent, QPageSize, QPdfWriter, QPagedPaintDevice, QFont, QPainter, QTextCursor, QTextImageFormat, QTextCharFormat, QImage, QAction, QKeySequence, QIcon
from PySide6.QtCore import Qt, QPointF, QUrl, QRectF, QMargins, QSizeF
import json
#sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # Ensure current directory is in sys.path
from GraphicsView import GraphicsView
from GraphicsScene import GraphicsScene
from GraphicsTextItem import GraphicsTextItem
from LayerControl import LayerControl
from tools import getAssetPath

class GraphicsEditor(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.imageResolution = 300
        self.imageColorModel =  QImage.Format_ARGB32
        self.fileName = None
        self.pdfFileName='output.pdf'
        self.pdfVersion = QPagedPaintDevice.PdfVersion_1_6
        self.pdfResolution = 300
        self.pdfUnit = QPageSize.Millimeter
        self.pdfSizeX = 297
        self.pdfSizeY = 210
        self.pdfSize = QSizeF(self.pdfSizeX, self.pdfSizeY)
        self.pdfColorModel = QPdfWriter.ColorModel.CMYK
        self.currentFont = QFont("Arial", 16)
        self.activeTextItem = None
        self.name = ""

        # Set up menu
        self.createMenu(mainWindow)

        # Main layout
        self.mainVerticalLayout = QVBoxLayout()
        self.setLayout(self.mainVerticalLayout)
        
        # Create a toolbar (simulating a Ribbon)
        self.toolbar = QToolBar("Ribbon Toolbar")
        self.mainVerticalLayout.addWidget(self.toolbar)
        self.separator = "  |  "
        
        self.contentsHorizontalLayout = QHBoxLayout()
        self.mainVerticalLayout.addLayout(self.contentsHorizontalLayout)
        
        # Scene & View
        self.scene = GraphicsScene(self)  # Use custom scene
        self.view = GraphicsView(self.scene)
        self.contentsHorizontalLayout.addWidget(self.view)
        
        ###
        ### ACTIONS
        ### Note: Custom selections of the actions below will be added to the toolbar, depending on the subapp.
        
        # Add a "Save Layout" action with an icon
        self.saveLayoutAction = QAction(QIcon(getAssetPath("Assets", "Save Layout Icon.png")), "Save Layout", self)
        self.saveLayoutAction.triggered.connect(self.saveLayout)

        # Add a "Load Layout" action with an icon
        self.loadLayoutAction = QAction(QIcon(getAssetPath("Assets", "Load Layout Icon.png")), "Load Layout", self)
        self.loadLayoutAction.triggered.connect(self.loadLayout)
    
        # Add an "Add Text Box" action with an icon
        self.addTextboxAction = QAction(QIcon(getAssetPath("Assets", "Add Box Icon.png")), "Add Box", self)
        self.addTextboxAction.triggered.connect(self.makeNewGraphicsItem)

        # Add an "Embed Image" action with an icon
        self.embedImageAction = QAction(QIcon(getAssetPath("Assets", "Embed Image Icon.png")), "Embed Image", self)
        self.embedImageAction.triggered.connect(self.embedImage)

        # Add a "Select Font" action with an icon
        self.selectFontAction = QAction(QIcon(getAssetPath("Assets", "Select Font Icon.png")), "Select Font", self)
        self.selectFontAction.triggered.connect(self.selectFont)
        
        # Color Preview Box
        self.colorBox = QToolButton()
        self.colorBox.setFixedSize(20, 20)
        self.colorBox.setStyleSheet("background-color: black; border: 1px solid gray;")
        self.colorBox.clicked.connect(self.scene.openColorPicker)

        # Add an "Apply Color" action with an icon
        self.applyColorAction = QAction(QIcon(getAssetPath("Assets", "Apply Color Icon.png")), "Apply Color", self)
        self.applyColorAction.triggered.connect(self.applyColor)

        self.selectColorAction = QWidgetAction(self)
        self.selectColorAction.setDefaultWidget(self.colorBox)

        # Add a "Rotate Box" action
        self.rotateBoxLabel = QLabel("Rotate:")
        self.rotateBoxInput = QLineEdit("0")
        self.rotateBoxInput.setFixedSize(30, 15)
        self.rotateBoxInput.returnPressed.connect(self.rotateBox)

        # Add a "Delete Item" action with an icon
#         deleteItemAction = QAction(QIcon("Delete Item Icon.png"), "Delete Item", self)
#         deleteItemAction.triggered.connect(self.deleteActiveItem)
        
        # Add a "Resize Scene" action with an icon
#         resizeSceneAction = QAction(QIcon("Resize Scene Icon.png"), "Resize Scene", self)
#         resizeSceneAction.triggered.connect(self.resizeScene)
        self.sceneWidthLabel = QLabel("Paper W:")
        self.widthInput = QLineEdit("800")
        self.widthInput.setFixedSize(40, 15)
        self.widthInput.returnPressed.connect(self.resizeScene)
        self.sceneHeightLabel = QLabel("H:")
        self.heightInput = QLineEdit("600")
        self.heightInput.setFixedSize(40, 15)
        self.heightInput.returnPressed.connect(self.resizeScene)
        
        # Add a "Toggle Bleed" action with an icon
        if self.scene.cutBleed:
            self.bleedIcon = getAssetPath("Assets", "Bleed Off Icon.png")
            self.bleedTooltip = "Turn Bleed On"
        else:
            self.bleedIcon = getAssetPath("Assets", "Bleed On Icon.png")
            self.bleedTooltip = "Turn Bleed Off"
        self.toggleBleedAction = QAction(QIcon(self.bleedIcon), self.bleedTooltip, self)
        self.toggleBleedAction.triggered.connect(self.scene.toggleBleed)

        # Add zoom.
        self.zoomInAction = QAction(QIcon(getAssetPath("Assets", "Zoom In Icon.png")), "Zoom In", self)
        self.zoomInAction.triggered.connect(self.view.zoomIn)
        self.zoomOutAction = QAction(QIcon(getAssetPath("Assets", "Zoom Out Icon.png")), "Zoom Out", self)
        self.zoomOutAction.triggered.connect(self.view.zoomOut)
        self.zoomResetAction = QAction(QIcon(getAssetPath("Assets", "Reset Zoom Icon.png")), "Reset Zoom", self)
        self.zoomResetAction.triggered.connect(self.view.resetZoom)
        
        # Add Grouping/Ungrouping
        self.groupAction = QAction(QIcon(getAssetPath("Assets", "Create Group Icon.png")), "Create Group", self)
        self.groupAction.triggered.connect(self.scene.groupSelectedItems)
        self.ungroupAction = QAction(QIcon(getAssetPath("Assets", "Destroy Group Icon.png")), "Destroy Group", self)
        self.ungroupAction.triggered.connect(self.scene.ungroupItems)

        # Add a "Lock Box" action with an icon
        self.lockBoxAction = QAction(QIcon(getAssetPath("Assets", "Lock Box Icon.png")), "Lock Box", self)
        self.lockBoxAction.triggered.connect(self.toggleBoxLock)
        self.boxWidthLabel = QLabel("Box W:")
        self.boxWidthInput = QLineEdit("200")
        self.boxWidthInput.setFixedSize(40, 15)
        self.boxWidthInput.returnPressed.connect(self.lockBox)
        self.boxHeightLabel = QLabel("H:")
        self.boxHeightInput = QLineEdit("200")
        self.boxHeightInput.setFixedSize(40, 15)
        self.boxHeightInput.returnPressed.connect(self.lockBox)
        self.boxPaddingLabel = QLabel("Pad:")
        self.boxPaddingInput = QLineEdit("5")
        self.boxPaddingInput.setFixedSize(30, 15)
        self.boxPaddingInput.returnPressed.connect(self.setBoxPadding)

        self.gridSizeLabel = QLabel("Grid:")
        self.gridSizeInput = QLineEdit("10")
        self.gridSizeInput.setFixedSize(30, 15)
        self.gridSizeInput.returnPressed.connect(self.setSnapGridSize)

        self.posXLabel = QLabel("Pos X:")
        self.posXInput = QLineEdit("0")
        self.posXInput.setFixedSize(40, 15)
        self.posXInput.returnPressed.connect(self.setNewPosition)
        self.posYLabel = QLabel("Pos Y:")
        self.posYInput = QLineEdit("0")
        self.posYInput.setFixedSize(40, 15)
        self.posYInput.returnPressed.connect(self.setNewPosition)

        self.setupControls()
        

    def setupControls(self):
        # Layer Control List
        # Note: A layer list must always be created, or addLayer() will cry, but it doesn't have to be added to the layout.
        self.layerList = LayerControl(self.scene)
        self.layerList.setFixedWidth(100)
        self.contentsHorizontalLayout.addWidget(self.layerList, 1)
        self.scene.layerList = self.layerList
        
        # Add actions to the toolbar
        self.toolbar.addAction(self.loadLayoutAction)
        self.toolbar.addAction(self.saveLayoutAction)
        self.toolbar.addWidget(QLabel(self.separator))
        self.toolbar.addWidget(self.sceneWidthLabel)
        self.toolbar.addWidget(self.widthInput)
        self.toolbar.addWidget(QLabel(" "))
        self.toolbar.addWidget(self.sceneHeightLabel)
        self.toolbar.addWidget(self.heightInput)
        self.toolbar.addWidget(QLabel(" "))
        self.toolbar.addAction(self.toggleBleedAction)
        self.toolbar.addWidget(QLabel(self.separator))
        self.toolbar.addAction(self.addTextboxAction)
        self.toolbar.addAction(self.embedImageAction)
        self.toolbar.addAction(self.selectFontAction)
        self.toolbar.addWidget(QLabel(self.separator))
        self.toolbar.addAction(self.selectColorAction)
        self.toolbar.addWidget(QLabel(" "))
        self.toolbar.addAction(self.applyColorAction)
        self.toolbar.addWidget(QLabel(self.separator))
        self.toolbar.addWidget(self.boxWidthLabel)
        self.toolbar.addWidget(self.boxWidthInput)
        self.toolbar.addWidget(QLabel(" "))
        self.toolbar.addWidget(self.boxHeightLabel)
        self.toolbar.addWidget(self.boxHeightInput)
        self.toolbar.addWidget(QLabel(" "))
        self.toolbar.addAction(self.lockBoxAction)
        self.toolbar.addWidget(QLabel(" "))
        self.toolbar.addWidget(self.boxPaddingLabel)
        self.toolbar.addWidget(self.boxPaddingInput)
        self.toolbar.addWidget(QLabel(" "))
        self.toolbar.addWidget(self.rotateBoxLabel)
        self.toolbar.addWidget(self.rotateBoxInput)
        self.toolbar.addWidget(QLabel(self.separator))
        self.toolbar.addAction(self.zoomInAction)
        self.toolbar.addAction(self.zoomOutAction)
        self.toolbar.addAction(self.zoomResetAction)
        self.toolbar.addWidget(QLabel(self.separator))
        self.toolbar.addWidget(self.gridSizeLabel)
        self.toolbar.addWidget(self.gridSizeInput)
        self.toolbar.addWidget(QLabel(self.separator))
        self.toolbar.addAction(self.groupAction)
        self.toolbar.addAction(self.ungroupAction)
        self.toolbar.addWidget(QLabel(self.separator))
        self.toolbar.addWidget(self.posXLabel)
        self.toolbar.addWidget(self.posXInput)
        self.toolbar.addWidget(self.posYLabel)
        self.toolbar.addWidget(self.posYInput)
        
        self.resizeScene()

    
    def makeNewGraphicsItem(self):
        # Create a new GraphicsTextItem and add it to the scene.
        graphicsItem = GraphicsTextItem("Click to drag, double-click to edit.", self.currentFont, "New")
        graphicsItem.setPos(QPointF(50, 50))
        self.addLayer(graphicsItem)
        
    def addLayer(self, graphicsItem, hasVisibility=True, addToLayerControl=True): #, name, iconPath):
        """Adds a new item to the scene and layer list."""
        self.scene.addItem(graphicsItem)
        self.scene.setActiveTextItem(graphicsItem)
        self.activeTextItem = graphicsItem
        graphicsItem.setZValue(self.scene.items().__len__()) # Add item to the foreground.

        # Create a layer list entry
        if hasVisibility:
            if graphicsItem.visible:
                eyeconToUse = "Eyecon - Shown.png"
            else:
                eyeconToUse = "Eyecon - Hidden.png"
            visibilityIcon = QIcon(eyeconToUse)
            listItem = QListWidgetItem(visibilityIcon, graphicsItem.name)
            
        else:
            listItem = QListWidgetItem(graphicsItem.name)
        listItem.setData(Qt.UserRole, graphicsItem)
#         listItem.setFlags(listItem.flags() | Qt.ItemIsUserCheckable)  # Make item checkable
#         listItem.setCheckState(Qt.Checked)  # Set default check state
        
        if addToLayerControl:
            self.layerList.addItem(listItem)
            self.layerList.updateLayers()
        
        # Connect the itemChanged signal to toggle visibility
        #self.layerList.itemChanged.connect(lambda item: self.toggleVisibility(item, listItem, graphicsItem)) #Since itemChanged only provides the item that changed, the lambda allows you to capture the current state of the listItem and graphicsItem at the time of the connection.

#     def toggleVisibility(self, item, listItem, graphicsItem):
#         """Toggle visibility of the graphics item and update the icon."""
#         if item == listItem:
#             visible = graphicsItem.visible #toggleVisibility()  # Assuming this method toggles visibility and returns new state
#             listItem.setIcon(QIcon("Eyecon - Shown.png" if visible else "Eyecon - Hidden.png"))
#             listItem.setCheckState(Qt.Checked if visible else Qt.Unchecked)  # Update check state
#             graphicsItem.visible = not graphicsItem.visible # Toggle item state.
            
#     # Handle visibility toggling
#     def toggle():
#         visible = graphicsItem.toggleVisibility()
#         listItem.setIcon(QIcon("Eyecon - Shown.png" if visible else "Eyecon - Hidden.png"))
# 
#         listItem.setCheckState(Qt.Checked)
#         listItem.setFlags(listItem.flags() | Qt.ItemIsUserCheckable)
#         self.layerList.itemChanged.connect(lambda item: toggle() if item == listItem else None)


    def applyColor(self):
        fakeEvent = QKeyEvent(QKeyEvent.KeyPress, Qt.Key_P, Qt.ControlModifier)
        #fakeEvent.setModifiers(Qt.ControlModifier)
        self.activeTextItem.keyPressEvent(fakeEvent)
    
    def createMenu(self, mainWindow):
#         if mainWindow.menuWidget():
#             mainWindow.menuWidget().clear()
        menu = mainWindow.menuBar()
        menu.clear()
        
        ### File Menu
        ### Note: The actions below automatically pass a bolean to the methods called, which can screw up any variables listed in the definition.
        fileMenu = menu.addMenu("File")
        
        loadLayoutAction = QAction("Load Layout", self)
        loadLayoutAction.setShortcut(QKeySequence.Open)
        loadLayoutAction.triggered.connect(self.loadLayout)
        fileMenu.addAction(loadLayoutAction)
        
        saveLayoutAction = QAction("Save Layout", self)
        saveLayoutAction.setShortcut(QKeySequence.Save)
        saveLayoutAction.triggered.connect(lambda: self.saveLayout(self.fileName))
        fileMenu.addAction(saveLayoutAction)

        saveLayoutAsAction = QAction("Save Layout As", self)
        saveLayoutAsAction.triggered.connect(self.saveLayout)
        fileMenu.addAction(saveLayoutAsAction)

        exportPdfAction = QAction("Export PDF", self)
        exportPdfAction.triggered.connect(lambda: self.exportPDF()) # Note: Using a lambda prevents "triggered" from emitting a boolean, which would set "fileList" to False in exportPDF.
        fileMenu.addAction(exportPdfAction)
        
        exportPdfBatchAction = QAction("Export PDF Batch", self)
        exportPdfBatchAction.triggered.connect(self.exportPDFBatch)
        fileMenu.addAction(exportPdfBatchAction)

        exportImageAction = QAction("Export Image", self)
        exportImageAction.triggered.connect(lambda: self.exportImage()) # Note: Using a lambda prevents "triggered" from emitting a boolean, which would set "fileList" to False in exportPDF.
        fileMenu.addAction(exportImageAction)
        
        exportImageBatchAction = QAction("Export Image Batch", self)
        exportImageBatchAction.triggered.connect(self.exportImageBatch)
        fileMenu.addAction(exportImageBatchAction)

        exitAction = QAction("Exit", self)
        exitAction.setShortcut(QKeySequence.Quit)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)
        
        # Insert Menu
        insertMenu = menu.addMenu("Insert")
        
        embedImageAction = QAction("Embed Image", self)
        embedImageAction.triggered.connect(self.embedImage)
        insertMenu.addAction(embedImageAction)
        
        setBoxBackgroundAction = QAction("Set Box Background", self)
        setBoxBackgroundAction.triggered.connect(self.setBoxBackground)
        insertMenu.addAction(setBoxBackgroundAction)
        
        deleteBoxBackgroundAction = QAction("Delete Box Background", self)
        deleteBoxBackgroundAction.triggered.connect(self.deleteBoxBackground)
        insertMenu.addAction(deleteBoxBackgroundAction)
        
        setSceneBackgroundAction = QAction("Set Scene Background", self)
        setSceneBackgroundAction.triggered.connect(self.setSceneBackground)
        insertMenu.addAction(setSceneBackgroundAction)

        deleteSceneBackgroundAction = QAction("Delete Scene Background", self)
        deleteSceneBackgroundAction.triggered.connect(self.deleteSceneBackground)
        insertMenu.addAction(deleteSceneBackgroundAction)

        # Edit Menu
        editMenu = menu.addMenu("Edit")
        
        fontAction = QAction("Select Font", self)
        fontAction.triggered.connect(self.selectFont)
        editMenu.addAction(fontAction)
        
        applyTemplateAction = QAction("Apply Template", self)
        applyTemplateAction.triggered.connect(self.applyTemplate)
        editMenu.addAction(applyTemplateAction)

        batchTemplateAction = QAction("Apply Template Batch", self)
        batchTemplateAction.triggered.connect(self.batchApplyTemplate)
        editMenu.addAction(batchTemplateAction)
        
        
#         deleteItemAction = QAction("Delete Item", self)
#         deleteItemAction.triggered.connect(self.deleteActiveItem)
#         editMenu.addAction(deleteItemAction)
        
        #mainWindow.updateButtonPosition()
        
    def setActiveTextItem(self, item):
        self.activeTextItem = item
        
    def resizeScene(self):
        width = int(self.widthInput.text())
        height = int(self.heightInput.text())
        self.scene.setSceneRect(0, 0, width, height) # Update size dynamically
        self.view.setSceneRect(self.scene.sceneRect())
    
    def embedImage(self):
        self.activeTextItem = self.scene.getActiveTextItem()  # Get active item from scene
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg)")
        if fileName and self.activeTextItem:
            cursor = self.activeTextItem.textCursor()
            image = QImage(fileName)
            if not image.isNull():
                #document = self.activeTextItem.document()
#                 imageFormat = QTextCharFormat()
#                 imageFormat.setObjectType(QTextFormat.UserObject)
#                 imageFormat.setProperty(QTextFormat.ImageName, fileName)
                    # Create a unique URL (using the actual file path)
                    imageFormat = QTextImageFormat()
                    imageFormat.setName(QUrl.fromLocalFile(fileName).toString())
                    # Insert the image with the correct reference
                    cursor.insertImage(imageFormat)
                    self.activeTextItem.setTextCursor(cursor)
#                     cursor.insertImage(image)
#                     self.activeTextItem.setTextCursor(cursor)

    def setNewPosition(self):
        self.activeTextItem = self.scene.getActiveTextItem()  # Get active item from scene
        self.activeTextItem.setPos(int(self.posXInput.text()), int(self.posYInput.text()))
            
    def updatePositionInputs(self):
        """ Update QLineEdit fields with the active item's position. """
        self.activeTextItem = self.scene.getActiveTextItem()
        if self.activeTextItem:
            pos = self.activeTextItem.pos()
            self.posXInput.setText(str(int(pos.x())))
            self.posYInput.setText(str(int(pos.y())))
    
    def rotateBox(self):
        self.activeTextItem = self.scene.getActiveTextItem()
        self.activeTextItem.setRotation(int(self.rotateBoxInput.text()))
        
    def updateRotationInput(self):
        """ Update QLineEdit fields with the active item's rotation. """
        self.activeTextItem = self.scene.getActiveTextItem()
        if self.activeTextItem:
            degrees = self.activeTextItem.rotation()
            self.rotateBoxInput.setText(str(int(degrees)))
            
    def updatePaddingInput(self):
        self.activeTextItem = self.scene.getActiveTextItem()
        if self.activeTextItem:
            self.boxPaddingInput.setText(str(int(self.activeTextItem.padding)))
            
    def updateGridInput(self):
        """ Update QLineEdit field with the active item's grid size. """
        self.activeTextItem = self.scene.getActiveTextItem()
        if self.activeTextItem:
            self.gridSizeInput.setText(str(int(self.activeTextItem.gridSize)))

    def updateBoxLockSize(self):
        self.activeTextItem = self.scene.getActiveTextItem()
        if self.activeTextItem:
            self.boxWidthInput.setText(str(int(self.activeTextItem.lockedWidth)))
            self.boxHeightInput.setText(str(int(self.activeTextItem.lockedHeight)))
        
    def setBoxPadding(self):
        self.activeTextItem = self.scene.getActiveTextItem()
        paddingDummy = int(self.boxPaddingInput.text())
        if paddingDummy <= 0:
                self.activeTextItem.padding = 0
        if paddingDummy > 0:
            self.activeTextItem.padding = paddingDummy
        self.activeTextItem.updatePadding()
            
    def setSnapGridSize(self):
        self.activeTextItem = self.scene.getActiveTextItem()  # Get active item from scene
        gridDummy = int(self.gridSizeInput.text())
        if gridDummy <= 1:
                self.activeTextItem.gridSize = 1
                self.snapToGrid = False
        if gridDummy > 1:
            self.activeTextItem.gridSize =  gridDummy
            self.snapToGrid = True        

    def lockBox(self):
         self.activeTextItem = self.scene.getActiveTextItem()  # Get active item from scene
         self.activeTextItem.lockedWidth = int(self.boxWidthInput.text())
         #print(self.boxWidthInput.text())
         self.activeTextItem.lockedHeight = int(self.boxHeightInput.text())
         self.activeTextItem.update()
         self.scene.update()

    def toggleBoxLock(self):
        self.activeTextItem = self.scene.getActiveTextItem()  # Get active item from scene
        self.activeTextItem.isLocked = not self.activeTextItem.isLocked
        self.activeTextItem.update()
        self.scene.update()
         
    def setBoxBackground(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg)")
        self.activeTextItem = self.scene.getActiveTextItem()  # Get active item from scene
        if fileName and self.activeTextItem:
            self.activeTextItem.setBackgroundImage(fileName)
    
    def deleteBoxBackground(self):
        self.activeTextItem = self.scene.getActiveTextItem()  # Get active item from scene
        if self.activeTextItem:
            self.activeTextItem.setBackgroundImage(None) #backgroundPixmap = None
            
    def setSceneBackground(self, fileName=None):
        # Load and set background image for the scene
        if not fileName:
            fileName, uselessDummy = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg)")
        self.scene.backgroundPixmap = fileName
        self.scene.update()
        #self.scene.drawBackground(QPainter(), self.scene.sceneRect())
        #self.scene.setBackgroundBrush(QBrush(pixmap))

    def deleteSceneBackground(self):
        self.scene.backgroundPixmap = None
    
    def selectFont(self):
        self.activeTextItem = self.scene.getActiveTextItem()  # Get active item from scene
        if not self.activeTextItem:
            return

        ok, font = QFontDialog.getFont(self.currentFont)
        if ok:
            self.currentFont = font

            cursor = self.activeTextItem.textCursor()
            if not cursor.hasSelection():
                cursor.select(QTextCursor.WordUnderCursor)  # Ensure at least a word is selected

            # Store selection range
            selectionStart = cursor.selectionStart()
            selectionEnd = cursor.selectionEnd()

            # Begin modifying the text character by character
            cursor.beginEditBlock()  # Group changes for efficiency

            for i in range(selectionStart, selectionEnd):
                cursor.setPosition(i, QTextCursor.MoveAnchor)
                cursor.setPosition(i + 1, QTextCursor.KeepAnchor)  # Select one character at a time

                # Get current character format
                currentFormat = cursor.charFormat()

                # Create a new QTextCharFormat with only the font changed
                fmt = QTextCharFormat()
                fmt.setFont(font)  # Change only the font
                fmt.setFontWeight(currentFormat.fontWeight())  # Preserve bold
                fmt.setFontItalic(currentFormat.fontItalic())  # Preserve italic
                fmt.setFontUnderline(currentFormat.fontUnderline())  # Preserve underline
                fmt.setFontCapitalization(currentFormat.fontCapitalization())  # Preserve small caps

                # Apply the new format to the single character
                cursor.mergeCharFormat(fmt)

            cursor.endEditBlock()  # End block edit for efficiency
            self.activeTextItem.setTextCursor(cursor)  # Restore cursor position

    def select_fontOLD(self):
        self.activeTextItem = self.scene.getActiveTextItem()  # Get active item from scene
        ok, font = QFontDialog.getFont(self.currentFont)
        if ok:
            self.currentFont = font
            if self.activeTextItem:
                cursor = self.activeTextItem.textCursor()
                currentFormat = cursor.charFormat()  # Get current formatting
                
                fmt = QTextCharFormat()
                fmt.setFont(font)

                fmt.setFontWeight(currentFormat.fontWeight())  # Preserve bold
                fmt.setFontItalic(currentFormat.fontItalic())  # Preserve italic
                fmt.setFontUnderline(currentFormat.fontUnderline())  # Preserve underline
                fmt.setFontCapitalization(currentFormat.fontCapitalization())  # Preserve small caps

                cursor.mergeCharFormat(fmt)
                self.activeTextItem.setTextCursor(cursor)
    
#     def saveLayout(self):
#         self.saveLayoutAs(fileName=self.fileName)
        
    def saveLayout(self, fileName=None):
        if not fileName:
            fileName, dummy = QFileDialog.getSaveFileName(self, "Save Layout", "", "JSON Files (*.json)")
        if fileName:
            layoutData = []
            layoutData.append(self.scene.backgroundPixmap)
            layoutData.append(self.widthInput.text())
            layoutData.append(self.heightInput.text())
            for item in self.scene.items():
                if isinstance(item, GraphicsTextItem):
                    layoutData.append(item.toDict())
            with open(fileName, "w", encoding="utf-8") as file:
                json.dump(layoutData, file, indent=4)

    def loadLayout(self, fileName=None):
        if not fileName:
            fileName, dummy = QFileDialog.getOpenFileName(self, "Load Layout", "", "JSON Files (*.json)")
        if fileName:
            with open(fileName, "r", encoding="utf-8") as file:
                self.fileName = fileName
                layoutData = json.load(file)
                self.scene.clear()
                self.scene.backgroundPixmap = None
                self.layerList.clear()
                layoutDataLength = len(layoutData)
                if layoutData[0]:
                    self.setSceneBackground(layoutData[0])
                self.widthInput.setText( str(int(layoutData[1])) )
                self.heightInput.setText( str(int(layoutData[2])) )
                self.resizeScene()
#                 for itemData in layoutData:
                for i in range(3,layoutDataLength):
                    self.addLayer(GraphicsTextItem.fromDict(layoutData[i]))
#                     textItem = GraphicsTextItem.fromDict(itemData)
#                     self.scene.addItem(textItem)
            self.activeTextItem = None # Removes reference to old, no longer existing object.
            self.scene.setActiveTextItem(self.activeTextItem)


    # Batch process where a list of layouts are loaded onscreen in turn to have a template applied to them.
    def batchApplyTemplate(self):
        fileListName, dummy = QFileDialog.getOpenFileName(self, "Load Targets", "", "List Files (*.list)")
        if fileListName: 
            with open(fileListName, "r", encoding="utf-8") as file:
                fileList = [line.strip() for line in file]
            templateFileName, dummy = QFileDialog.getOpenFileName(self, "Load Template", "", "JSON Files (*.json)")
            for targetFileName in fileList:
                self.applyTemplate(targetFileName=targetFileName, templateFileName=templateFileName)
                self.saveLayout(fileName=targetFileName)
                
    
    def applyTemplate(self, targetFileName=None, templateFileName=None):
        if not templateFileName: # Single file process where the template is loaded and applied to the onscreen page.    
            templateFileName, dummy = QFileDialog.getOpenFileName(self, "Load Template", "", "JSON Files (*.json)")
        if templateFileName:
            with open(templateFileName, "r", encoding="utf-8") as file:
                layoutTemplate = json.load(file)
#                 if not targetFileName:
#                     targetFileName, dummy = QFileDialog.getOpenFileName(self, "Load Layout", "", "JSON Files (*.json)")
                if targetFileName:
                    self.loadLayout(fileName=targetFileName)
                sceneItems = self.scene.items()
                #print(sceneItems)
                noCurrentItems = 0
                if sceneItems:
                    noCurrentItems = len(sceneItems)
                if layoutTemplate[0] and targetFileName and "layoutWeak" in targetFileName: # layoutTemplate[0] is a background image filename or None.
                    self.setSceneBackground(layoutTemplate[0])
                self.widthInput.setText( str(int(layoutTemplate[1])) )
                self.heightInput.setText( str(int(layoutTemplate[2])) )
                self.resizeScene()
                layoutTemplate = layoutTemplate[3:] #"3" because the first three list entries are scene background, height and width.
                noTemplateItems = len(layoutTemplate)
                #print(noTemplateItems)
                #print(noCurrentItems)
                for t in range(noTemplateItems): 
                    if t > noCurrentItems: #There are more items in the template than in the current scene.
                        #print("t: " + str(t))
                        self.makeNewGraphicsItem()
                        sceneItems = self.scene.items()
#                     else:
                        #print(templateItem["font"])
                    templateItem = layoutTemplate[t]
                    templateKeys = templateItem.keys()
                    #i = t-1
                    if "font" in templateKeys:
                        font = QFont()
                        font.fromString(templateItem["font"])
                        sceneItems[t].setFont(font)
#                         sceneItems[t].x = templateItem["x"]
#                         sceneItems[t].y = templateItem["y"]
                    if "x" in templateKeys:
                        x = templateItem["x"]
                    else:
                        x = sceneItems[t].x()
                    if "y" in templateKeys:
                        y = templateItem["y"]
                    else:
                        y = sceneItems[t].y()
                    sceneItems[t].setPos(int(x), int(y))
                    if "name" in templateKeys:
                        sceneItems[t].name = templateItem["name"]
                    if "lockedWidth" in templateKeys:
                        sceneItems[t].lockedWidth = templateItem["lockedWidth"]
                    if "lockedHeight" in templateKeys:
                        sceneItems[t].lockedHeight = templateItem["lockedHeight"]
                    if "isLocked" in templateKeys:
                        sceneItems[t].isLocked = templateItem["isLocked"]
                    if "gridSize" in templateKeys:
                        sceneItems[t].gridSize = templateItem["gridSize"]
                    if "snapToGrid" in templateKeys:
                        sceneItems[t].snapToGrid = templateItem["snapToGrid"]
                    if "padding" in templateKeys:
                        sceneItems[t].padding = templateItem["padding"]
                        sceneItems[t].updatePadding()
                    if "rotation" in templateKeys:
                        sceneItems[t].setRotation(templateItem["rotation"])
                        self.updateRotationInput()
                    if "visible" in templateKeys:
                        sceneItems[t].visible = templateItem["visible"]
                    if targetFileName and "layoutStrict" not in targetFileName:
                        if templateItem["backgroundImagePath"]:
                            sceneItems[t].setBackgroundImage(templateItem["backgroundImagePath"])
                    self.activeTextItem = sceneItems[t]
                    self.scene.setActiveTextItem(self.activeTextItem)
                    self.updatePositionInputs()
                    self.setNewPosition()
                    sceneItems[t].update()
                self.activeTextItem = None # Removes reference to old, no longer existing object.
                self.scene.setActiveTextItem(self.activeTextItem)
                

    def exportPDFBatch(self):
        setupFileName, dummy = QFileDialog.getOpenFileName(self, "Load Setup", "", "List Files (*.setup)")
        if setupFileName: 
            with open(setupFileName, "r", encoding="utf-8") as file:
                fileList = [line.strip() for line in file]
            setupInfo = fileList[0].split(";")
            self.pdfFileName = setupInfo[0].split("=")[1].strip()
            #self.pdfSize = setupInfo[1].split("=")[1].strip()
            #self.pdfVersion = setupInfo[2].split("=")[1].strip()
            self.pdfResolution = int( setupInfo[1].split("=")[1].strip() )
            colorModel = setupInfo[2].split("=")[1].strip()
            if colorModel == "CMYK":
                self.pdfColorModel = QPdfWriter.ColorModel.CMYK
            else:
                self.pdfColorModel = QPdfWriter.ColorModel.RGB
            self.pdfSizeX = int( setupInfo[3].split("=")[1].strip() )
            self.pdfSizeY= int( setupInfo[4].split("=")[1].strip() )
            pdfUnit = setupInfo[5].split("=")[1].strip()
            if pdfUnit == "mm":
                self.pdfUnit = QPageSize.Millimeter
            else:
                self.pdfUnit = QPageSize.Inch
            separator = int( setupInfo[6].split("=")[1].strip() )
            self.exportPDF(fileList=fileList[1:], separator = separator)
            

    ### Prints the QGraphicsScene to a PDF file with vector text and embedded CMYK images.
    def exportPDF(self, fileList=[None], separator = 0):
        #pdfWriter.setPageSize(QPageSize(QPageSize.Letter))
        pdfWriter = QPdfWriter(self.pdfFileName)
        pdfWriter.setPdfVersion(self.pdfVersion)
        pdfWriter.setResolution(self.pdfResolution)
        pdfWriter.setColorModel(self.pdfColorModel)
        self.pdfSize = QSizeF(self.pdfSizeX, self.pdfSizeY)
        pdfWriter.setPageSize( QPageSize(self.pdfSize, self.pdfUnit) )
        pdfWriter.setPageMargins(QMargins(0, 0, 0, 0))#, QtGui.QPageLayout.Millimeter)
        #pdfWriter.setPageMargins(QRectF(0, 0, 0, 0))  # No margins
        painter = QPainter(pdfWriter)
        # Define where to place the scene on the PDF page
        posX = 0  # Adjust left margin (in points)
        posY = 0  # Adjust top margin (in points)
        marginX = None
        marginY = None
        sceneWidth = 0
        sceneHeight = 0
        previousSceneWidth = 0
        previousSceneHeight = 0
        #separator = 5
        #noFiles = len(fileList)
        #for e in range(1,noFiles):
         #   entry = fileList[e]
        
        for entry in fileList:
            if entry:
                entryList = entry.split(";")
                fileName = entryList[0].split("=")[1].strip()
                self.loadLayout(fileName=fileName)
                dummyPosX = int( entryList[1].split("=")[1].strip() )
                dummyPosY = int( entryList[2].split("=")[1].strip() )
                newPage = bool(int( entryList[3].split("=")[1].strip() ))
                if not marginX:
                    marginX = dummyPosX
                if not marginY:
                    marginY = dummyPosY
                if newPage:
                    pdfWriter.newPage()
            sourceRect = self.scene.sceneRect() # self.scene.sceneRect() gets the rectangle of the entire scene.
            if self.scene.cutBleed:
                bleed = 35 #int(3/25,4*300)
                sourceRect = sourceRect.adjusted(bleed, bleed, -bleed, -bleed)
            # Define the target rectangle where the scene will be drawn
            sceneWidth = self.scene.sceneRect().width()
            sceneHeight = self.scene.sceneRect().height()
            
            # Autoposition elements if positions are set to <0.
            if entry:
                if dummyPosX < 0:
                    if self.pdfUnit == QPageSize.Millimeter:
                        pdfSizeX = int(self.pdfSizeX/25.4*self.pdfResolution)
                    else:
                        pdfSizeX = int(self.pdfSizeX*self.pdfResolution)
                    if posX + previousSceneWidth + sceneWidth + marginX > pdfSizeX:
                        posX = marginX
                        if dummyPosY < 0:
                            if self.pdfUnit == QPageSize.Millimeter:
                                pdfSizeY = int(self.pdfSizeY/25.4*self.pdfResolution)
                            else:
                                pdfSizeY = int(self.pdfSizeY*self.pdfResolution)
                            if posY + previousSceneHeight + sceneHeight + marginY > pdfSizeY:
                                posY = marginY
                                pdfWriter.newPage()
                            else:
                                posY += previousSceneHeight + separator
                    else:
                        posX += previousSceneWidth + separator
                else:
                    posX = dummyPosX
                previousSceneWidth = sceneWidth
                if dummyPosY >= 0:
                    posY = dummyPosY
                previousSceneHeight = sceneHeight

            targetRect = QRectF(posX, posY, sceneWidth, sceneHeight)
            #targetRect = QRectF(0, 0, sceneWidth, sceneHeight)
            #painter.save()  # Save current transformation state
            #painter.translate(marginX, marginY)  # Move the scene to the specified position
            self.scene.render(painter, targetRect, sourceRect) # targetRect → Defines where on the PDF page the scene should be drawn. sourceRect → Defines which part of the scene should be drawn.
            #painter.restore()
        painter.end()
        print("Export to PDF complete: " + self.pdfFileName)


    def exportImageBatch(self):
        setupFileName, dummy = QFileDialog.getOpenFileName(self, "Load Setup", "", "List Files (*.setup)")
        if setupFileName: 
            with open(setupFileName, "r", encoding="utf-8") as file:
                fileList = [line.strip() for line in file]
            setupInfo = fileList[0].split(";")
            self.imageResolution = int( setupInfo[0].split("=")[1].strip() )
            colorModel = setupInfo[1].split("=")[1].strip()
            if colorModel == "CMYK":
                self.imageColorModel = QImage.Format_CMYK8888
            else:
                self.imageColorModel = QImage.Format_ARGB32
            self.exportImage(fileList=fileList[1:]) # The first line is setup info and isn't actually a file link, so we remove it.
            

    def exportImage(self, fileList=[None]):
        # Set image color mode.
        if self.imageColorModel == "CMYK":
            imageColorModel = QImage.Format_CMYK8888
            imageFileFormat = ".jpeg"
        else:
            imageColorModel = QImage.Format_ARGB32
            imageFileFormat = ".png"
    
        painter = QPainter()
        for entry in fileList:
            if entry:
                entryList = entry.split(";")
                fileName = entryList[0].split("=")[1].strip()
                self.loadLayout(fileName=fileName)
                #Repurposing filename for output.
                fileName = fileName.split(".")[0] + imageFileFormat
            else:
                fileName = "output" + imageFileFormat
            sourceRect = self.scene.sceneRect()
            if self.scene.cutBleed:
                bleed = 35 #int(3/25,4*300)
                sourceRect = sourceRect.adjusted(bleed, bleed, -bleed, -bleed)
        
            image = QImage(sourceRect.size().toSize(), imageColorModel)
            dpm = int(self.imageResolution/0.0254)
            image.setDotsPerMeterX(dpm)
            image.setDotsPerMeterY(dpm)
            if self.imageColorModel == "CMYK":
                image.fill(Qt.white)  # Fill background with white
            else:
                image.fill(Qt.transparent)
            
            # Prepare rendering
            painter.begin(image)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Render only the specified portion
            self.scene.render(painter, target=QRectF(0, 0, sourceRect.width(), sourceRect.height()), source=sourceRect)
            painter.end()
            
            # Save the image
            image.save(fileName)
        if len(fileList > 1):
            print("Export to images complete.")
        else:
            print("Export to image complete: " + fileName)
