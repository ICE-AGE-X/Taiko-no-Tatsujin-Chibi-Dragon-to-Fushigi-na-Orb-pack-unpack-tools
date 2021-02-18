import libs
import sys

argc = len(sys.argv)
if argc < 4:
    print("usage: python lmt_import.py old_lmt new_lmt pics_paths")
    print("ex   : python lmt_import.py o.lmt n.lmt a.png b.png c.png")
    exit(0)

oldLmt = sys.argv[1]
newLmt = sys.argv[2]
pics = sys.argv[3:argc]

with open(oldLmt, "rb") as rf:
    count = libs.readInt4(rf)
    zero = libs.readInt4(rf)
    with open(newLmt, "wb") as wf:
        wf.write(count.to_bytes(4, "little"))
        wf.write(zero.to_bytes(4, "little"))
        wf.write(rf.read(0x14*count))
        rf.close()
        for path in pics:
            with open(path,"rb") as rpb:
                rpb.seek(0,2)
                length=rpb.tell()
                rpb.seek(0,0)
                wf.write(length.to_bytes(4,"little"))
                wf.write(rpb.read(length))
                rpb.close()
        wf.close()
