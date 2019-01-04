# c4d-scripts
## My collection of Cinema 4D scripts

# A free HDRI-Link for C4D (Redshift only):
<p align = "center">
<img src="https://github.com/lasselauch/c4d-scripts/blob/master/img/rs_hdrlink.png?raw=true" alt="rs_hdrlink.png"/><b>rs_hdrlink.py</b></br>
<br>Download or Clone the Folder <code>rs_hdrlink</code> and add it to your Script-Arsenal for C4D.</p>

![<gif>](./img/RS_HDRLink_Overview_s.gif)</br></br>

The Script will add a new Light Dome with the Python-Tag to your Scene unless you have one selected, then it will only change the path in the Python-Tag.

![<gif>](./img/RS_HDRLink_LocalFavorites.gif)</br></br>
In the <code>res</code> Folder you'll find <code>local_favorites.txt</code> edit it to add your favorite HDR-Directories to your new favorite Dropdown.

---

# Copy & Paste Splines between C4D & Houdini:

![<gif>](./img/copy_paste_splines_c4d-houdini.gif)</br></br>
![<icon>](./img/copy-spline-points-for-houdini-curves-node.png) <b>copy-spline-points-for-houdini-curves-node.py</b></br>
Copy the position of Spline Points to your clipboard and easily paste them into Houdini's Curve Node.</br>

https://twitter.com/lasse_lauch/status/1058057404431110146</br>

![<icon>](./img/paste-spline-from-houdini-geometry-spreadsheet.png) <b>paste-spline-from-houdini-geometry-spreadsheet.py</b></br>
Use "Copy Selection as Text" from Houdini's Geometry Spreadsheet to paste a new Spline into C4D.</br>

---
## redshifttag-displacement-scale.py
Multiply the Displacement-Scale of all Redshift-Tags in your Scene by a given Input-Value.

---
## replace-rendersettings-from-scene.py
Replace Rendersettings from another Scene. <u>Very useful</u> for <b>huge</b> scenes ( >1GB ). It can be a pain to load the whole scene into memory, if you just want to copy the rendersettings. This will speed up the process by a ton, because it's only loading the rendersettings from that file.</br></br>
<b>[ DEFAULT ] APPEND RENDERSETTINGS</b></br>
<b>[ CTRL-CLICK ] OVERWRITE RENDERSETTINGS</b></br>

---
## act-on-same-object-type.py
Scan scene for same Object-Types and _act_ on it...</br></br>
<b>[ DEFAULT ] Select same Object-Types</b></br>
<b>[ CTRL-CLICK ] Turn same Object-Types to OFF</b></br>
<b>[ ALT-CLICK ] Turn same Object-Types to DEFAULT</b></br>

---
## fit-ffd-to-selection.py
Select some Polygons and _run_ the Script:</br>
It adds an FFD-Deformer to your selected Object that fits the current Polygon-Selection.</br></br>
