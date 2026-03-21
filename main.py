from PySide6.QtWidgets import QApplication
from PySide6.QtCore import qInstallMessageHandler, QtMsgType
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # Ensure current directory is in sys.path to make imports of script files work.
from MainWindow import MainWindow

def customQtMessageHandler(msgType, context, message):
    ignoreList = [ "QVariant::save: unable to save type",
                   "DirectWrite: CreateFontFaceFromHDC() failed"
                 ]
    for ignoreMe in ignoreList:
        if ignoreMe in message:
            return  # Suppress this specific warning
    print(message)  # Print everything else

###
### Start by building the mainwindow which will contain the different tabs/apps.
###
if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    
    qInstallMessageHandler(customQtMessageHandler)  # Install the handler

#     logFile = "debug.log"
#     sys.stdout = open(logFile, "w")  # Redirect print output to a file
#     sys.stderr = sys.stdout  # Also capture errors

    editor = MainWindow()
    editor.show()
    
    sys.exit(app.exec())
