#www.lasselauch.com/lab/
#Use at your own risk
"""
Name-US:Insert RS_HDRLink
Description-US:Insert RS_HDRLink-Tag for Dome Light.
"""

import c4d
import os

thispath = os.path.dirname(os.path.abspath(__file__))

def getFavorites():
    fav_path = os.path.join(thispath, 'res', 'local_favorites.txt')
    if not os.path.isfile(fav_path):
        print "Couldn't find local HDR-Favorites..."
        return

    fav_list = list()

    with open(fav_path) as f:
        lines = f.readlines()
        for line in lines:
            if not line.startswith('#') and not line.startswith('\n'):
                line = line.split('\n')[0]
                path = os.path.normpath(line)
                if os.path.isdir(path):
                    #print paths
                    fav_list.append(path)

    if fav_list != []:
        return fav_list
    else:
        return None

def PopupMenu(fav_list):

    icon_fav = "&i1019904&"
    icon_folder = "&i1022735&"
    icon_light = "&i1036751&"
    menu = c4d.BaseContainer()
    menu.InsData(0, icon_fav + 'H D R  -  F A V O R I T E S :&d&')

    if fav_list is None:
        menu.InsData(c4d.FIRST_POPUP_ID+1, "Please edit the './res/local_favorites.txt' to add directories.&d&")
        menu.InsData(c4d.FIRST_POPUP_ID+2, icon_light + 'Insert "RS Dome Light" with [RS_HDRLINK]')

    else:
        for i, path in enumerate(fav_list):
            string = '%s' % (icon_folder + path)
            menu.InsData(c4d.FIRST_POPUP_ID + i, string)

    result = c4d.gui.ShowPopupDialog(None, menu, c4d.MOUSEPOS, c4d.MOUSEPOS, c4d.POPUP_RIGHT|c4d.POPUP_EXECUTECOMMANDS)
    return result

def InsertTag(obj, myPath):
    c4d_path = os.path.join(thispath, 'res', 'rs_hdrlink_tag.c4d')
    tdoc = c4d.documents.LoadDocument(c4d_path, c4d.SCENEFILTER_OBJECTS, None)

    if not tdoc:
        c4d.gui.MessageDialog("Check your 'res' Folder, you might be missing a C4D-File.")
        return

    tag = tdoc.GetFirstObject().GetTag(c4d.Tpython, 0)
    if not tag:
        c4d.gui.MessageDialog("Couldn't find Python-Tag in the C4D-File.")
        return

    if myPath is not None:
        tag[c4d.ID_USERDATA,1] = myPath

    if obj and obj.GetType() == 1036751:
        ttag = obj.GetTag(c4d.Tpython, 0)
        if ttag and ttag.GetName()=='[RS_HDRLINK]':
            doc.StartUndo()
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, ttag)
            ttag[c4d.ID_USERDATA,1] = myPath
            doc.EndUndo()
            c4d.EventAdd()
            return

    else:
        doc.StartUndo()
        domelight = RS_DomeLight()
        doc.AddUndo(c4d.UNDOTYPE_NEW, domelight)
        doc.InsertObject(domelight)
        if obj is not None:
            domelight.InsertAfter(obj)
        doc.AddUndo(c4d.UNDOTYPE_NEW, tag)
        domelight.InsertTag(tag)
        doc.EndUndo()
        c4d.EventAdd()
        return

def RS_DomeLight():
    domelight = c4d.BaseObject(1036751)
    domelight[c4d.REDSHIFT_LIGHT_TYPE] = 4
    domelight.SetName('RS Dome Light')
    return domelight

def main():
    redshift_id = 1036221
    plugin = c4d.plugins.FindPlugin(redshift_id, c4d.PLUGINTYPE_ANY)
    if not plugin:
        c4d.gui.MessageDialog('Sorry, works only with Redshift.')
        return

    fav_list = getFavorites()
    result = PopupMenu(fav_list)
    if result == 0:
        return

    if fav_list is None and result == c4d.FIRST_POPUP_ID+2:
        InsertTag(op, "[RS_HDRLINK] Choose a Folder with HDRs")
        return

    myPath = fav_list[result-c4d.FIRST_POPUP_ID]
    obj = doc.GetActiveObject()
    InsertTag(obj, myPath)

if __name__=='__main__':
    main()
