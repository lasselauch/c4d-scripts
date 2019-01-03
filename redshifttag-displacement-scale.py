#www.lasselauch.com/lab/
#Use at your own risk
"""
Name-US:Multiply Displacement-Scale of all Redshift-Tags
Description-US:
"""
import c4d

def BrowseObjs(obj, liste):

    if not obj: return

    for tag in obj.GetTags():
        if tag.GetType() == 1036222:
            liste.append(tag)

    BrowseObjs(obj.GetNext(), liste)
    BrowseObjs(obj.GetDown(), liste)

def main():
    tag_liste = []
    BrowseObjs(doc.GetFirstObject(), tag_liste)

    if tag_liste == []:
        c4d.gui.MessageDialog("Couldn't find any Redshift-Displacement-Tags.")
        return

    multiplier = c4d.gui.InputDialog("RS_Displacement-Multiplier:", 10)
    if not multiplier:
        return
    if "," in multiplier:
        multiplier = multiplier.replace(',', '.')

    try:
        multiplier = float(multiplier)
    except ValueError:
        c4d.gui.MessageDialog('Please, insert a valid Float.')
        return

    for tag in tag_liste:
        if tag[c4d.REDSHIFT_OBJECT_GEOMETRY_DISPLACEMENTENABLED]:
            old_scale = tag[c4d.REDSHIFT_OBJECT_GEOMETRY_DISPLACEMENTSCALE]
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, tag)
            tag[c4d.REDSHIFT_OBJECT_GEOMETRY_DISPLACEMENTSCALE] *= multiplier

    c4d.EventAdd()

if __name__=='__main__':
    main()
