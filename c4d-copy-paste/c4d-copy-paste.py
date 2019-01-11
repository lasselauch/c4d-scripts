#www.lasselauch.com/lab/
#Use at your own risk
#Last-Modified: 01/11/2019
"""
Name-US:Copy/Paste between C4D-Versions
Description-US:CTRL-CLICK: Copy (converted) selected Objects
"""
import c4d
from c4d import gui, utils
import tempfile
import os

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

ctrl, shift, alt = GetModifiers()

def Command_CSTO(op):
    res = utils.SendModelingCommand(command=c4d.MCOMMAND_CURRENTSTATETOOBJECT, list=[op], doc=doc)
    if res is False:
        return None
    return res[0]

def Copy(tmppath, converted):
    sel = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    if not sel:
        gui.MessageDialog('Select some Objects first.')
        return

    c4d.StopAllThreads()
    c4d.StatusSetSpin()

    export = []
    for obj in sel:
        #Convert Current State to Object for all selected Objects
        if converted:
            obj = Command_CSTO(obj)
        export.append(obj)

    if export == []:
        message = 'Sorry, nothing to Export.'
        gui.MessageDialog(message)
        return

    iso_objs=c4d.documents.IsolateObjects(doc, export)
    c4d.documents.SaveDocument(iso_objs, tmppath, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, c4d.FORMAT_C4DEXPORT)

    c4d.StatusClear()

    message = 'Copied Object(s).'
    if converted:
        message = 'Copied converted Object(s).'

    gui.MessageDialog(message)

def Paste(tmppath):
    c4d.StopAllThreads()
    c4d.StatusSetSpin()

    merge = c4d.documents.MergeDocument(doc, tmppath, c4d.SCENEFILTER_OBJECTS | c4d.SCENEFILTER_MATERIALS | c4d.SCENEFILTER_MERGESCENE, None)

    c4d.StatusClear()
    if not merge:
        message = "Couldn't find Objects to paste...\nMake sure to export first."
        gui.MessageDialog(message)
        return

    c4d.EventAdd()

def PopupMenu(tmppath):

    csto_icon = "&i12233&"
    copy_icon = "&i100004821&"
    paste_icon = "&i100004820&"
    delete_icon = "&i100004787&"

    sel = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    first = doc.GetFirstObject()
    menu = c4d.BaseContainer()

    if ctrl:
        if sel:
            menu.InsData(c4d.FIRST_POPUP_ID + 2, csto_icon + 'Copy (converted) selected Objects')
        else:
            menu.InsData(c4d.FIRST_POPUP_ID + 2, csto_icon + 'Copy (converted) selected Objects&d&')
    else:
        if sel:
            menu.InsData(c4d.FIRST_POPUP_ID + 1, copy_icon + 'Copy selected Objects')
        else:
            menu.InsData(c4d.FIRST_POPUP_ID + 1, copy_icon + 'Copy selected Objects&d&')

    if not os.path.exists(tmppath):
        menu.InsData(c4d.FIRST_POPUP_ID + 3, paste_icon + 'Paste Objects&d&')
    else:
        menu.InsData(c4d.FIRST_POPUP_ID + 3, paste_icon + 'Paste Objects')

    if not os.path.exists(tmppath):
        menu.InsData(c4d.FIRST_POPUP_ID + 4, delete_icon + 'Delete Temporary Files&d&')
    else:
        menu.InsData(c4d.FIRST_POPUP_ID + 4, delete_icon + 'Delete Temporary Files')

    result = c4d.gui.ShowPopupDialog(None, menu, c4d.MOUSEPOS, c4d.MOUSEPOS, c4d.POPUP_RIGHT|c4d.POPUP_EXECUTECOMMANDS)

    return result

def main():
    tmp = tempfile.gettempdir()
    tmppath = os.path.join(tmp, 'c4d_copypaste.c4d')

    result = PopupMenu(tmppath)

    #Copy selected Objects
    if result == c4d.FIRST_POPUP_ID + 1:
        Copy(tmppath, False)
        return

    #Copy (converted) selected Objects
    if result == c4d.FIRST_POPUP_ID + 2:
        Copy(tmppath, True)
        return

    #Paste Objects
    if result == c4d.FIRST_POPUP_ID + 3:
        Paste(tmppath)
        return

    #Delete Temporary Files
    if result == c4d.FIRST_POPUP_ID + 4:
        os.remove(tmppath)
        gui.MessageDialog('Deleted Temporary File!')
        return

if __name__=='__main__':
    main()
