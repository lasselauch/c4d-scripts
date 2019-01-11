#www.lasselauch.com/lab/
#Use at your own risk
"""
Name-US:Quick-Folder
Description-US:Shortcut to open your Project, Render-Folder and Open in Viewer.
"""
import c4d
import os
from c4d import gui, storage
from c4d.modules import tokensystem as tokensys

DEBUG = False
VIEWER = r"C:\Program Files\djv-1.1.0-Windows-64\bin\djv_view.exe"

def FilePath(docpath):
    rd = doc.GetActiveRenderData()

    if rd is None: return
    filepath = rd[c4d.RDATA_PATH]

    if filepath == "":
        if DEBUG:
            print "D'oh, your #FILEPATH is empty."
        return False

    if filepath.startswith("./"):
        if DEBUG:
            print "Congrats, you're using a relative path!"
        filepath = os.path.join(docpath, filepath[2:])

    rS = c4d.BaseContainer()
    rpData = {'_doc': doc, '_rData': rd, '_rBc': rS, '_frame': 0}
    filepath = tokensys.FilenameConvertTokens(filepath, rpData)

    return os.path.dirname(filepath.split("$take")[0])

def ActiveDoc():
    doc = c4d.documents.GetActiveDocument()
    if doc is None: return False
    path = doc.GetDocumentPath()
    if path=="":
        return False
    else:
        return path

def OpenInVIEWER(filepath):

    try:
        os.chdir(filepath)
        files = filter(os.path.isfile, os.listdir(filepath))
        files = [os.path.join(filepath, f) for f in files] # add path to each file
    except:
        message = "Couldn't find Image in:\n\n'%s'" % (filepath)
        c4d.gui.MessageDialog(message)
        return

    print 'Opening: "%s" in your VIEWER.' % (os.path.basename(files[0]))

    img_path = os.path.join(filepath, files[0])
    c4d.storage.GeExecuteProgram(VIEWER, img_path)

def main():
    #Icons
    icon_home ="&i465003521&"
    icon_image = "&i465003528&"
    icon_play = "&i12412&"

    docpath = ActiveDoc()
    filepath = FilePath(docpath)

    #Menu
    menu=c4d.BaseContainer()
    ID=c4d.FIRST_POPUP_ID

    #Document | Open Folder:
    if docpath is False:
        menu.InsData(ID+1, icon_home + 'Open: Document-Folder&d&')
    else:
        menu.InsData(ID+1, icon_home + 'Open: Document-Folder')
        if DEBUG:
            print "Document-Folder: " + docpath

    #Render-Settings | File:
    if filepath is False:
        menu.InsData(ID+2, icon_image + 'Open: Image-Folder&d&')
        menu.InsData(ID+3, icon_play + 'Open: Viewer&d&')
    else:
        menu.InsData(ID+2, icon_image + 'Open: Image-Folder')
        menu.InsData(ID+3, icon_play + 'Open: Viewer')
        if DEBUG:
            print "Saved File-Folder: " + filepath

    result = gui.ShowPopupDialog(cd=None, bc=menu, x=c4d.MOUSEPOS, y=c4d.MOUSEPOS, flags = c4d.POPUP_BELOW)

    if result == ID+1:
        storage.ShowInFinder(docpath)
    elif result == ID+2:
        storage.ShowInFinder(filepath)
    elif result == ID+3:
        OpenInVIEWER(filepath)
    else: return

if __name__=='__main__':
    main()