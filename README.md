# Layoutium
A custom graphics and text layout engine built with PySide6.
Supports layered elements, layout templates, rich text formatting and pdf export.

FEATURES  
-Layered graphics system (drag & drop)  
-Custom text rendering with formatting  
-Layout persistence using serialization  
-Modular architecture  
-Built with Python, PySide6 (Qt) and Pillow  

MOTIVATION  
I wanted a flexible and easy to use WYSIWYG editor for tabletop game component design.  
InDesign (expensive) and Scribus are great for rules books, but I needed something else for prototyping and quick iterative development.  

HOW TO RUN  
Run packageThis.py to create executable windows file.  
Or do this:  
pip install -r requirements.txt  
python layoutiumMain.py  

MANUAL  
Disclaimer: Yes, the icons are silly, but this was made for personal use, and they can easily be replaced by others with similar names. Icons do have tool-tips to make the app usable for others...  

~ Textboxes ~  
Add a textbox by hitting the scroll icon. You can embed images by clicking the pixie icon.  
To set a background image for the text box, use the Insert menu.  
Selected text can be formatted by clicking the tome icon.  
Clicking the square to the left of the unicorn, will allow you to select a color. Clicking the unicorn afterwards will apply the chosen color to any selected text in the box. Note that you need to write down the colors you want to use, as the color picker does not "remember" them.
Shortcuts are ctrl +: b(bold), i(italics), u(underline), k(small caps), "up arrow"(superscript), "down arrow"(subscript), p(apply color), d(open color selector).  

~ Bleed ~  
By default, bleed is on and won't allow items to cross it's invisible border. Click the green satyr icon to toggle bleed.  
If an item is refusing to obey bleed, deselect it, by clicking anywhere on the page, and then reselect it.  

~ Layers ~  
Each item is it's own layer and is shown in the layer list on the right.  
Click the layer title in the list to rename it.  
Items are moved up/down in the z-direction by drag-and-dropping the layer title in the list.  

~ Groups ~  
Items can be grouped by ctrl + clicking the actual items (not the titles in the layer list), and then hitting the spider.  
The most resent group (which should be the only group) is destroyed by hitting the sword.  
Note that groups are intended to be temporary while quick, collective adjustments of item positions are done.  
Adding items to an existing group, is possible, you need to click the original group when moving the items or the new item is released.  
Caveats:  
-Groups are nice, but currently they do not obey page borders/bleed/grid and cannot be rotated collectively.  
-Grouped items cannot be edited until they have ben released.  
-While grouped, clicking the group will not highlight group items in the layer list.  
  
~ Rotation ~  
Items can be rotated by just typing in the desired angle (in degrees).  
Caveat: Rotated items do not obey borders/bleed.  

