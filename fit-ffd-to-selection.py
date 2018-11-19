#www.lasselauch.com/lab/
#Use at your own risk
#Known Limitations: Doesn't respect Normal-Orientation
import c4d

def Command_Split(op):
    res = c4d.utils.SendModelingCommand(command=c4d.MCOMMAND_SPLIT, list=[op], doc=doc)
    if res is False:
        return None
    return res[0]

def main():
    if op is None:
        return

    #Run Split Command
    s = Command_Split(op)

    #Insert FFD-Deformer under Split-Object and Fit
    ffd = c4d.BaseObject(c4d.Offd)
    doc.AddUndo(c4d.UNDOTYPE_NEW, ffd)
    doc.InsertObject(ffd)
    ffd.InsertUnder(s)
    c4d.CallButton(ffd, c4d.FFDOBJECT_FITTOPARENT)

    #Clone that FFD-Deformer under our Original Object
    clone = ffd.GetClone()
    doc.AddUndo(c4d.UNDOTYPE_NEW, clone)
    clone.InsertUnder(op)

    #Remove Split-Object
    doc.AddUndo(c4d.UNDOTYPE_DELETE, s)
    s.Remove()

    c4d.EventAdd()

if __name__=='__main__':
    main()
