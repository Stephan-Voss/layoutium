import os
import PyInstaller.__main__

# Define the main script entry point
mainScript = "mainLayoutium.py"  

# Define the folder containing assets to include
assetsFolder = "Assets"

# Recursively find all files in the assets folder
def collectDataFiles(sourceFolder):
    dataFiles = []
    for root, _, files in os.walk(sourceFolder):
        for file in files:
            fullPath = os.path.join( os.path.abspath(root), file ) # fullPath is the absolute file path to where it should be copied from (but would also work if it was just os.path.abspath(root)).
            relativePath = os.path.relpath( os.path.abspath(root) ) # relativePath is the relative path to the folder where the file should be placed in the packaged app.
            separator = ":" #";" if os.name == "nt" else ":"
            paths = f"{fullPath}{separator}{relativePath}" 
            dataFiles.append(paths)
    return dataFiles

# Collect all assets
dataFiles = collectDataFiles(assetsFolder)

# Run PyInstaller with all required options.
PyInstaller.__main__.run([
    "--onefile",          # Single executable. To keep it in a folder instead of one .exe, remove --onefile.
    "--windowed",         # Hide console (for GUI apps). For Linux, replace --windowed with --noconsole.
    "--noconfirm",        # Overwrite previous builds
    "--strip",
    "--clean",
    #"--exclude-module", "PySide6.QtMultimedia",
    #"--exclude-module", "PySide6.QtWebEngineWidgets",
    #"--upx-dir", "upx.exe", # Compress bundled libraries
    "--name", "Layoutium",    # Output name
    "--icon", "icon.ico", # For Windows
    #"--icon", "icon.icns", " For MacOS
    #"--debug", "all", # To debug issues, try --log-level=DEBUG.
] + [f"--add-data={item}" for item in dataFiles] + [
    mainScript  # The main script
])

print("Build complete!")
