import os
import platform
import PyInstaller.__main__

# =========================
# CONFIG
# =========================
mainScript = "mainLayoutium.py"
assetsFolder = "Assets"
appName = "Layoutium"

# =========================
# HELPERS
# =========================
def collectDataFiles(sourceFolder):
    dataFiles = []
    separator = ";" if os.name == "nt" else ":"

    for root, _, files in os.walk(sourceFolder):
        for file in files:
            # fullPath is the absolute file path to where it should be copied from.
            fullPath = os.path.join(root, file)
            # relativePath is the relative path to the folder where the file should be placed in the packaged app.
            relativePath = os.path.join(assetsFolder, os.path.relpath(root, sourceFolder)) #os.path.relpath(root, sourceFolder)
            dataFiles.append(f"{fullPath}{separator}{relativePath}")

    return dataFiles


def buildForCurrentPlatform():
    currentOS = platform.system()
    print(f"Detected OS: {currentOS}")

    dataFiles = collectDataFiles(assetsFolder)

    # =========================
    # BASE OPTIONS
    # =========================
    options = [
        "--onefile", # Single executable. To keep it in a folder instead of one .exe, remove --onefile.
        "--noconfirm", # Overwrite previous builds
        "--clean",
        "--name", appName,
        "--distpath", "../build/dist",
        "--workpath", "../build/build",
        #"--windowed",         # Hide console (for GUI apps). For Linux, replace --windowed with --noconsole? Not sure why this can be omitted...
        #"--exclude-module", "PySide6.QtMultimedia",
        #"--exclude-module", "PySide6.QtWebEngineWidgets",
        #"--upx-dir", "upx.exe", # Compress bundled libraries
        #"--debug", "all", # To debug issues, try --log-level=DEBUG.
    ]

    # =========================
    # PLATFORM-SPECIFIC OPTIONS
    # =========================
    if currentOS == "Windows":
        print("Building for Windows...")
        options += [
            "--windowed",
            "--icon=icon.ico",
        ]

    elif currentOS == "Linux":
        print("Building for Linux...")
        options += [
            "--windowed",
            "--strip",
            "--icon=icon.png",
        ]

    elif currentOS == "Darwin":
        print("Building for macOS...")
        options += [
            "--windowed",
            "--icon=icon.icns",
        ]

    else:
        raise RuntimeError(f"Unsupported OS: {currentOS}")

    # =========================
    # ADD DATA FILES
    # =========================
    options += [f"--add-data={item}" for item in dataFiles]

    # Entry script
    options.append(mainScript)

    # =========================
    # RUN BUILD
    # =========================
    print("Running PyInstaller with options:")
    for opt in options:
        print(" ", opt)

    PyInstaller.__main__.run(options)

    print("Build complete!")


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    buildForCurrentPlatform()
    