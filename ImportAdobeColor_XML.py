#www.lasselauch.com/lab/
#Use at your own risk
#Last-Modified: 03/08/2020
"""
Name-US:Import Adobe Color CC Swatches for R21
Description-US:Copy from "My Themes" as "XML"!\n[DEFAULT] Import Swatches + Reference Cubes|[CTRL] Opens https://color.adobe.com|[SHIFT] Import Swatches only
"""

import c4d
import xml.etree.ElementTree as ET

try:
    import maxon
except:
    pass

def GetModifiers():
    bc = c4d.BaseContainer()
    ctrl, shift, alt = False, False, False
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.BFM_INPUT_CHANNEL, bc):
        if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QSHIFT:
            shift = True
        if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL:
            ctrl = True
        if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT:
            alt = True
    return ctrl, shift, alt

def get_xml_colors():

    clipboard = c4d.GetStringFromClipboard()

    if not clipboard:
        c4d.gui.MessageDialog("Sorry, found nothing in your Clipboard.")
        return

    if not clipboard.startswith('<palette>'):
        c4d.gui.MessageDialog("Sorry, Clipboard has a wrong format.\nPlease, export as XML.")
        return

    root = ET.fromstring(clipboard)

    result = list()
    name = ''
    myDict = dict()

    for child in root:
        name = child.attrib['name']
        r, g, b = child.attrib['r'], child.attrib['g'], child.attrib['b']
        color = c4d.Vector(float(r)/255, float(g)/255, float(b)/255)
        result.append(color)

    myDict[name] = result
    return myDict

def InsertSwatchesR21(doc, group_name, colors):
    swatchData = c4d.modules.colorchooser.ColorSwatchData(doc)
    if swatchData is None:
        return

    group = swatchData.AddGroup(c4d.SWATCH_CATEGORY_DOCUMENT, group_name)

    if group is not None:
        group.AddColors(colors)
        group.SetName(group_name)
        index = swatchData.GetGroupCount(c4d.SWATCH_CATEGORY_DOCUMENT) - 1
        swatchData.SetGroupAtIndex(index, group)

    swatchData.Save(doc)

def InsertObjects(name, colors):
    doc.StartUndo()

    null = c4d.BaseObject(c4d.Onull)
    null.SetName(name)
    doc.InsertObject(null)
    doc.AddUndo(c4d.UNDOTYPE_NEW, null)
    for i, c in enumerate(colors):
        cube = c4d.BaseObject(c4d.Ocube)
        cube[c4d.ID_BASEOBJECT_USECOLOR] = 2
        cube[c4d.PRIM_CUBE_DOFILLET] = True
        cube[c4d.PRIM_CUBE_FRAD] = 5.0
        cube[c4d.ID_BASEOBJECT_COLOR] = c
        cube[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(i*200, 0,0)
        doc.InsertObject(cube)
        cube.InsertUnder(null)
        doc.AddUndo(c4d.UNDOTYPE_NEW, cube)

    c4d.EventAdd()
    doc.EndUndo()

def convert_to_maxon(colors):
    result = list()

    for c in colors:
        # Creates a maxon.ColorA for the current color
        col4 = maxon.ColorA()
        col4.r = c.x
        col4.g = c.y
        col4.b = c.z
        col4.a = 1.0
        result.append(col4)

    return result

def OpenWebsite(url):
    import webbrowser
    webbrowser.open_new_tab(url)

def main():
    ctrl, shift, alt = GetModifiers()
    if ctrl:
        OpenWebsite('https://color.adobe.com/create/color-wheel/')
        return

    myColors = get_xml_colors()
    if not myColors:
        return

    # Strip Color-Index from Name
    name = myColors.keys()[0][:-2]
    colors =  myColors.values()[0]

    #PRE R18 VERSION ( INSERT ONLY OBJECTS )
    if c4d.GetC4DVersion() <= 18011:
        gui.MessageDialog("I'm sorry, Color-Swatches haven't been introduced in your C4D-Version.\nYou need at least C4D R18! I'll just add some Cubes with Colors... Okay!?")
        InsertObjects(name, colors)
        return

    if c4d.GetC4DVersion() >= 20000:
        maxon_colors = convert_to_maxon(colors)
        #SHIFT-CLICK: ONLY ADD SWATCHES
        if shift:
            InsertSwatchesR21(doc, name, maxon_colors)
            return

        #DEFAULT-CLICK: REFERENCE CUBES + SWATCHES
        InsertSwatchesR21(doc, name, maxon_colors)
        InsertObjects(name, colors)

if __name__=='__main__':
    main()
