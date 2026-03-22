import os
import sys

## Get the correct path to assets, whether running as a script or an executable.
## pathParts should be formatted as: "Assets," "<subfoldername1>", "<subfoldername2>", ... , "<filename>", omitting the <>'s.
def getAssetPath(*pathParts):
    if getattr(sys, 'frozen', False):  # Running as a PyInstaller bundle
        basePath = sys._MEIPASS  # Temporary folder where PyInstaller extracts files
        path = os.path.join(basePath, *pathParts)
    else:
        path = os.path.join(".", *pathParts)
    return path 