"""
Copyright: Lasse Lauch
Written for Cinema 4D R20.059

Name-US:quickSel_v0.01
Description-US:A quick Selection-Menu for last selected Objects. Add to Hotkey (i.e. CTRL+TAB)
Idea by Lars Jandel
Last Modified Date: 07/08/2019
"""

PLUGIN_ID = 1053141

import c4d

def GetNextElement(op):
    if not op:
        return

    if op.GetDown():
        return op.GetDown()

    while (not op.GetNext()) and op.GetUp():
        op = op.GetUp()

    return op.GetNext()

def set_pluginData(sel, docData):
    myBC = c4d.BaseContainer()

    bc1 = c4d.BaseContainer()
    bc2 = c4d.BaseContainer()
    for i, obj in enumerate(reversed(sel)):
        icon = '&i%s&' % (obj.GetType())
        name = icon + obj.GetName()
        unique_id = obj.GetGUID()
        bc1.SetString(i, name)
        bc2.SetData(i, unique_id)

    myBC.SetData(0, bc1)
    myBC.SetData(1, bc2)

    docData.SetData(PLUGIN_ID, myBC)

def get_pluginData(docData):
    if docData is not None:
        pluginData = docData.GetData(PLUGIN_ID)

    names = list()
    unique_ids = list()

    # Loop through both Containers 0 / 1
    for i, bc in pluginData:
        # print i, bc
        #Loop through individual Containers (name and unique_id)
        for k, v in bc:
            if isinstance(v, basestring):
                names.append(v)
            if isinstance(v, long):
                unique_ids.append(v)

    return names, unique_ids

def popupMenu(liste):
    if not liste:
        return None

    menu = c4d.BaseContainer()
    for i, name in enumerate(liste):
        menu.InsData(c4d.FIRST_POPUP_ID+i, name)

    result = c4d.gui.ShowPopupDialog(None, menu, c4d.MOUSEPOS, c4d.MOUSEPOS, c4d.POPUP_CENTERVERT|c4d.POPUP_CENTERHORIZ|c4d.POPUP_EXECUTECOMMANDS)
    return result - c4d.FIRST_POPUP_ID

def FindObject(unique_id):
    obj = doc.GetFirstObject()
    while(obj is not None):
        if obj.GetGUID() == unique_id:
            return obj
            break
        obj = GetNextElement(obj)

def ToggleSetBit(a, b):
    a_sel, b_sel = False, False

    if a.GetBit(c4d.BIT_ACTIVE): a_sel = True
    if b.GetBit(c4d.BIT_ACTIVE): b_sel = True

    if a_sel:
        a.DelBit(c4d.BIT_ACTIVE)
        b.SetBit(c4d.BIT_ACTIVE)
    if b_sel:
        b.DelBit(c4d.BIT_ACTIVE)
        a.SetBit(c4d.BIT_ACTIVE)
    if a_sel and b_sel:
        a.DelBit(c4d.BIT_ACTIVE)
        b.DelBit(c4d.BIT_ACTIVE)
        a.SetBit(c4d.BIT_ACTIVE)
    if not a_sel and not b_sel:
        a.SetBit(c4d.BIT_ACTIVE)

def main():
    docData = doc.GetDataInstance()
    sel = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN | c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)

    if sel:
        if len(sel) > 1:
            set_pluginData(sel, docData)

    names, unique_ids = get_pluginData(docData)

    if len(names) == 2:
        a = FindObject(unique_ids[0])
        b = FindObject(unique_ids[1])
        ToggleSetBit(a, b)
        c4d.EventAdd()
        return

    selection = popupMenu(names)
    if selection >= 0:
        obj = FindObject(unique_ids[selection])
        doc.SetSelection(obj, c4d.SELECTION_NEW)
        c4d.EventAdd()

if __name__=='__main__':
    main()
