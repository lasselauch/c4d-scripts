#www.lasselauch.com/lab/
#Use at your own risk
"""
Name-US:Act on same Object-Types
Description-US:[ DEFAULT ] Select same Object-Types<br>[ CTRL-CLICK ] Turn same Object-Types to OFF<br>[ ALT-CLICK ] Turn same Object-Types to DEFAULT
"""
import c4d

def GetModifiers():
    # Check all keys
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

def GetTypeList():
    sel = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)
    if not sel:
        return

    type_list = list()
    for obj in sel:
        type_list.append(obj.GetType())

    return type_list

def BrowseObjs(obj, type_list, liste):

    if not obj: return

    if obj.GetType() in type_list:
        liste.append(obj)

    BrowseObjs(obj.GetNext(), type_list, liste)
    BrowseObjs(obj.GetDown(), type_list, liste)

def main():
    ctrl, shift, alt = GetModifiers()
    type_list = GetTypeList()
    myList = list()
    BrowseObjs(doc.GetFirstObject(), type_list, myList)

    on, off, default = 0, 1, 2

    doc.StartUndo()
    for obj in myList:
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
        obj.SetBit(c4d.BIT_ACTIVE)
        if ctrl:
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
            obj[c4d.ID_BASEOBJECT_GENERATOR_FLAG] = False
            obj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = off
            obj[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = off
        if alt:
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
            obj[c4d.ID_BASEOBJECT_GENERATOR_FLAG] = True
            obj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = default
            obj[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = default

    doc.EndUndo()
    c4d.EventAdd()

if __name__=='__main__':
    main()
