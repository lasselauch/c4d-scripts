import c4d
from c4d import gui

def main():
    bd = doc.GetActiveBaseDraw()
    bd[c4d.BASEDRAW_DATA_RENDERSAFE] =not bd[c4d.BASEDRAW_DATA_RENDERSAFE]
    bd[c4d.BASEDRAW_DATA_TINTBORDER] =not bd[c4d.BASEDRAW_DATA_TINTBORDER]
    bd[c4d.BASEDRAW_DATA_TINTBORDER_OPACITY] = 0.9
    c4d.EventAdd()

if __name__=='__main__':
    main()