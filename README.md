# Layoutium
A custom graphics and text layout engine for printable components.

FEATURES  
Layered graphics system (drag & drop).  
Rich text formatting with CMYK-colors.  
Layout/template persistence using serialization.  
Extendable, modular architecture.  
Built with Python and PySide6 (Qt).  

MOTIVATION  
I wanted a flexible and easy to use WYSIWYG editor for tabletop game component design that could handle CMYK-colors.  
InDesign (expensive) and Scribus are great for rules books, but I needed something else for quick and flexible iterative development.  

HOW TO RUN  
Run packageThis.py to create executable windows file.  
Or do this:  
pip install -r requirements.txt  
python layoutiumMain.py  

MANUAL  
Disclaimer: Yes, the icons are silly, but this was made for personal use, and they can easily be replaced by others with similar names. Icons do have tool-tips to make the app usable for others...  

~ Page Setup ~  
Paper size is adjusted by entering pixel values for "Paper W" and "H".  
You can set a background through the "Insert" menu.  
By default, bleed is on and won't allow items to cross its invisible border. Click the green satyr icon to toggle bleed. If a box is refusing to obey bleed, deselect it (by clicking anywhere on the page) and then reselect it.  
Snap-to-grid can be enabled by entering a pixel value different from 1 for "Grid".  
The page is zoomable through ctrl+scrolling or the egg, dragon and tree icons.  

~ Boxes ~  
Add a text/image box by hitting the scroll icon.  
Boxes by default rezise to fit their contents. Hit the map icon to lock the size of the selected box to the pixel values entered for "Box W" and "H". (Click again to unlock.)  
To position the box, just drag-and-drop or enter pixel values for "Pos X" and "Y".   
You can embed images into text by clicking the pixie icon.  
To set a background image for the box, use the Insert menu.  
Selected text can be formatted by clicking the tome icon.  
Padding (box internal margin) is set by entering a pixel value for "Pad".  
Clicking the square to the left of the unicorn, will allow you to select a color. Clicking the unicorn afterwards will apply the chosen color to any selected text in the box. Note that you need to write down the colors you want to use, as the color picker does not "remember" them.
Boxes can be rotated by just typing in the desired angle (in degrees). Caveat: Rotated boxes do not obey borders/bleed.  
Shortcuts are ctrl +: B(bold), I(italics), U(underline), K(small caps), "Up arrow"(superscript), "Down arrow"(subscript), P(apply color), D(open color selector).  

~ Layers ~  
Each box is its own layer and is shown in the layer list on the right. The currently selected box is highlighted. 
Click the layer title in the list to rename it.  
Boxes are moved up/down in the z-direction by drag-and-dropping the layer title in the list.  

~ Groups ~  
Boxes can be grouped by ctrl + clicking the actual items (not the titles in the layer list), and then hitting the spider icon.  
Destroy the most recent group (which should be the only group) by hitting the sword.  
Note that groups are intended to be temporary, while collective adjustments of box positions are made.  
Adding a box to an existing group, is possible, but you need to click the original group when moving the boxes or the new box is released.  
Caveats:  
-Groups are nice, but currently they do not obey page borders/bleed/grid and cannot be rotated collectively.  
-Grouped boxes cannot be edited until they have ben released.  
-While grouped, clicking the group will not properly highlight boxes in the layer list.  

~ Layout Templates ~  

~ Exporting Files ~  

