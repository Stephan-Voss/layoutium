from PySide6.QtWidgets import QApplication
from PySide6.QtCore import qInstallMessageHandler
import os
import sys
# Ensure current directory is in sys.path to make imports of script files work.
sys.path.append( os.path.dirname(os.path.abspath(__file__)) )
# path = os.path.dirname(os.path.abspath(__file__))
# if path not in sys.path:
#     sys.path.append(path)
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
    
    # DEBUG: Uncomment this when debugging.
    logFile = "debug.log"
    sys.stdout = open(logFile, "w")  # Redirect print output to a file
    sys.stderr = sys.stdout  # Also capture errors

    editor = MainWindow()
    editor.show()
    
    sys.exit(app.exec())
