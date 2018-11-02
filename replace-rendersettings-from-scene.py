#www.lasseclausen.com/lab/
#Use at your own risk
"""
Name-US:Replace Current Rendersettings From Scene
Description-US:Replace Rendersettings from another Scene. Very useful for huge scenes!
"""
import c4d

def ReplaceRendersettingsFromScene(scene, append=True):
    c4d.StatusSetSpin()
    message = """Replacing current Render-Settings from: %s""" % (scene)
    c4d.StatusSetText(message)

    tdoc = c4d.documents.LoadDocument(scene, c4d.SCENEFILTER_ONLY_RENDERDATA | c4d.SCENEFILTER_IGNOREMISSINGPLUGINSINNONACTIVERENDERDATA, None)
    if tdoc is None:
        return

    trd = tdoc.GetFirstRenderData()
    active = tdoc.GetActiveRenderData()

    clones = list()
    while trd:
        clones.append(trd.GetClone())
        trd = trd.GetNext()

    rd = doc.GetFirstRenderData()
    current_rd = list()
    while rd:
        current_rd.append(rd)
        rd = rd.GetNext()

    doc.StartUndo()

    if not append:
        for rd in current_rd:
            doc.AddUndo(c4d.UNDOTYPE_DELETE, rd)
            rd.Remove()

    for trd in reversed(clones):
        doc.AddUndo(c4d.UNDOTYPE_NEW, trd)
        doc.InsertRenderDataLast(trd)
        if trd.GetData() == active.GetData():
            doc.SetActiveRenderData(trd)

    doc.EndUndo()
    c4d.EventAdd()

    c4d.StatusSetBar(0)
    c4d.StatusClear()

def main():
    ctrl = False
    bc = c4d.BaseContainer()
    c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.BFM_INPUT_CHANNEL, bc)
    if bc[c4d.BFM_INPUT_QUALIFIER]==2:
        ctrl = True

    #Select a huge scene for fun.
    scene = c4d.storage.LoadDialog(c4d.FILESELECTTYPE_SCENES, "Select your rendersettings file.", c4d.FILESELECT_LOAD)
    if not scene:
        return

    #DEFAULT: APPEND RENDERSETTINGS
    ReplaceRendersettingsFromScene(scene, True)

    #CTRL-CLICK: OVERWRITE RENDERSETTINGS
    if ctrl:
        ReplaceRendersettingsFromScene(scene, False)

if __name__=='__main__':
    main()
