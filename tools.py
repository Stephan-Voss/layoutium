import os
import sys

# pathParts should be formatted as: "Assets," "<subfoldername1>", "<subfoldername2>", ... , "<filename>", omitting the <>'s.
def getAssetPath(*pathParts):
    """Get the correct path to assets, whether running as a script or an executable."""
    if getattr(sys, 'frozen', False):  # Running as a PyInstaller bundle
        basePath = sys._MEIPASS  # Temporary folder where PyInstaller extracts files
        path = os.path.join(basePath, *pathParts)
    else:
        #basePath = os.path.abspath(".")  # Normal script execution
        path = os.path.join(".", *pathParts)
    #print(path)
    return path 