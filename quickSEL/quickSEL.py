"""
Copyright: Lasse Lauch
Written for Cinema 4D R20.059

Name-US:quickSEL
Description-US:A quick Selection-Menu for last selected Objects/Tags.\nAdd to Hotkey (i.e. Shift+TAB)
Idea by Lars Jandel
Last Modified Date: 09/08/2019
"""

import c4d
import os

PLUGIN_ID = 1053141

def set_pluginData(sel, docData, two_selected=False):
    myBC = c4d.BaseContainer()
    for i, obj in enumerate(sel):
        if two_selected:
            myBC.SetLink(1000+i, obj)
        else:
            myBC.SetLink(i, obj)

    docData.SetData(PLUGIN_ID, myBC)

def popupMenu(docData):
    if docData is not None:
        pluginData = docData.GetData(PLUGIN_ID)
        if not pluginData:
            return None

    menu = c4d.BaseContainer()
    for i, (k, obj) in enumerate(pluginData):
        icon = '&i%s&' % (obj.GetType())
        name =  obj.GetName()
        menu.InsData(c4d.FIRST_POPUP_ID+i, icon+name)

    result = c4d.gui.ShowPopupDialog(None, menu, c4d.MOUSEPOS, c4d.MOUSEPOS, c4d.POPUP_CENTERVERT|c4d.POPUP_CENTERHORIZ|c4d.POPUP_EXECUTECOMMANDS)
    return result - c4d.FIRST_POPUP_ID

def ToggleSetBit(a, b):
    a_sel, b_sel = False, False

    if a.GetBit(c4d.BIT_ACTIVE): a_sel = True
    if b.GetBit(c4d.BIT_ACTIVE): b_sel = True

    if a_sel:
        doc.AddUndo(c4d.UNDOTYPE_BITS, a)
        doc.SetSelection(b, c4d.SELECTION_NEW)
    if b_sel:
        doc.AddUndo(c4d.UNDOTYPE_BITS, b)
        doc.SetSelection(a, c4d.SELECTION_NEW)

    if a_sel and b_sel:
        doc.AddUndo(c4d.UNDOTYPE_BITS, a)
        a.DelBit(c4d.BIT_ACTIVE)
        doc.AddUndo(c4d.UNDOTYPE_BITS, b)
        b.DelBit(c4d.BIT_ACTIVE)
        b.SetBit(c4d.BIT_ACTIVE)

    if not a_sel and not b_sel:
        doc.AddUndo(c4d.UNDOTYPE_BITS, b)
        b.SetBit(c4d.BIT_ACTIVE)

def main():
    doc.StartUndo()
    docData = doc.GetDataInstance()

    if docData is not None:
        pluginData = docData.GetData(PLUGIN_ID)

    sel = doc.GetSelection()

    if sel:
        if len(sel) == 1:
            pass

        if len(sel) > 2:
            if pluginData:
                pluginData.RemoveIndex(1000)
                pluginData.RemoveIndex(1001)
            set_pluginData(sel, docData)

        if len(sel) == 2:
            set_pluginData(sel, docData, two_selected=True)

        if pluginData:
            a = pluginData.GetLink(1000, doc)
            b = pluginData.GetLink(1001, doc)

            if a and b:
                if len(sel)<=2:
                    ToggleSetBit(a, b)
                    c4d.EventAdd()
                    doc.EndUndo()
                    return

    if len(sel) != 2:
        selection = popupMenu(docData)
        if selection >= 0:
                hero = pluginData.GetLink(selection, doc)
                if hero:
                    doc.SetSelection(hero, c4d.SELECTION_NEW)
                    c4d.EventAdd()
                    doc.EndUndo()

        if len(sel) == 0:
            if len(pluginData) == 2:
                a = pluginData.GetLink(1000+selection, doc)
                if a:
                    doc.SetSelection(a, c4d.SELECTION_NEW)
                    c4d.EventAdd()
                    doc.EndUndo()
if __name__=='__main__':
    main()