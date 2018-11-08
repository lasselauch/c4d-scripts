#www.lasselauch.com/lab/
#Use at your own risk
#Last-Modified: 08/11/2018
"""
Name-US:Paste Points from Houdini Geometry Spreadsheet
Description-US:#www.lasselauch.com/lab/
"""
import c4d
import re

def PointListFromClipboard():
    clipboard = c4d.GetStringFromClipboard()
    if not c4d.GetClipboardType() == c4d.CLIPBOARDTYPE_STRING:
        return

    re_pattern = "[\t\n\r\*]*"
    points = re.split(re_pattern, clipboard.strip())

    x = points[0::3]
    y = points[1::3]
    z = points[2::3]

    length = len(x)
    # at least one list has a different length
    if any(len(lst) != length for lst in [y, z]):
        print """+++ Bad Formatting: +++\nX: %s Number of Points\nY: %s Number of Points\nZ: %s Number of Points\n""" % (len(x), len(y), len(z))
        return None

    point_list = list()
    for i in xrange(len(x)):
        my_x = x[i]
        my_y = y[i]
        my_z = z[i]
        vector = c4d.Vector(float(my_x), float(my_y), float(my_z))
        point_list.append(vector)

    return point_list

def main():
    point_list = PointListFromClipboard()
    if point_list is None:
        return

    doc.StartUndo()
    spline = c4d.BaseObject(c4d.Ospline)
    spline.SetName("Houdini_Spline")
    #spline[c4d.SPLINEOBJECT_CLOSED] = True
    doc.AddUndo(c4d.UNDOTYPE_NEW, spline)
    doc.InsertObject(spline, checknames=True)

    scale_factor = 100

    c4d.PointObject.ResizeObject(spline, len(point_list))
    for i, v in enumerate(point_list):
        c4d.PointObject.SetPoint(spline, i, v * scale_factor)

    spline.Message(c4d.MSG_UPDATE)

    doc.EndUndo()
    c4d.EventAdd()

if __name__=='__main__':
    main()
