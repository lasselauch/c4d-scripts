#www.lasselauch.com/lab/
#Use at your own risk
#Last-Modified: 25/10/2018
"""
Name-US:Copy Spline-Points for Houdini Curves-Node
Description-US:#www.lasselauch.com/lab/
"""
import c4d
from c4d import gui

def Command_CurrentStateToObject(op):
    res = c4d.utils.SendModelingCommand(command=c4d.MCOMMAND_CURRENTSTATETOOBJECT, list=[op], doc=doc)
    if res is False:
        return None
    return res[0]

def main():
    if not op:
        return

    try:
        #Convert "Current State to Object"
        obj = Command_CurrentStateToObject(op)
        if obj is None:
            return

        #Get All Points of converted Spline and multiply by Scaling-Factor
        points = obj.GetAllPoints()
        scalefactor = float(0.01)
        points = [p*scalefactor for p in points]

        #Initiate Clipboard-String
        code = ""

        for p in points:
            code += """%s, %s, %s """  % (p.x, p.y, p.z)

        #Copy First Point at End of String to Close the Spline
        if obj.IsClosed():
            code +=  """%s, %s, %s"""  % (points[0].x, points[0].y, points[0].z)

        #Copy Code to Clipboard
        c4d.CopyStringToClipboard(code)
        print "Spline-Info copied to Clipboard..!"

    except:
        message = "...N O T  a  S p l i n e  ! ! !"
        gui.MessageDialog(message)
        return

if __name__=='__main__':
    main()