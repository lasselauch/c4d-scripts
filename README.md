# c4d-scripts
## My collection of Cinema 4D scripts

# [RS-HDRI-Link](https://github.com/lasselauch/c4d-scripts/tree/master/rs_hdrlink/)
##### A free HDRI-Link for C4D (Redshift only)

# [Copy-Paste-Splines-C4D-Houdini](https://github.com/lasselauch/c4d-scripts/tree/master/copy-paste-splines-c4d-houdini)
##### Copy Splines to your clipboard and paste them into Houdini's Curve Node.

# [Quick-Folder](https://github.com/lasselauch/c4d-scripts/tree/master/quick-folder)
##### Shortcut to open your Document-, Render-Folder and open your Rendering in any Viewer.

# [C4D Copy/Paste](https://github.com/lasselauch/c4d-scripts/tree/master/c4d-copy-paste)
##### Quickly copy Objects between different C4D-Versions.
---
# Simple Task-Scripts:

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
It adds an FFD-Deformer to your selected Object that fits the current Polygon-Selection.
