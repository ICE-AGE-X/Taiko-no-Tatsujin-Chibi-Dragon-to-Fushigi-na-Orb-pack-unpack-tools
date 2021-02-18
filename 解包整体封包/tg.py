import libs
import os
import sys

argc = len(sys.argv)
print(sys.argv)
if argc != 4:
    print("usage: python tg.py [packedlist] [packed] [outdir]")
    print("ex: python tg.py c:\\packedlist c:\\packed c:\\outdir")
    exit(0)
listPath = sys.argv[1]
packedPath = sys.argv[2]
outdir = sys.argv[3]

def readFileInfoBlock(rf):
    path = libs.readStr(rf, 0x50)
    count = libs.readInt4(rf)
    offset = libs.readInt4(rf)
    length = libs.readInt4(rf)
    libs.readInt4(rf)
    libs.readInt4(rf)
    return (path, count, offset, length)


fileInfos = []
with open(listPath, "rb") as rf:
    basePath = libs.readStr(rf, 0xd0)
    print(basePath)
    totalCount = libs.readInt4(rf)
    libs.readInt4(rf)
    totalSize = libs.readInt4(rf)
    print(totalSize)
    libs.readInt4(rf)
    libs.readInt4(rf)

    for i in range(totalCount):
        r = readFileInfoBlock(rf)
        print(r)
        fileInfos.append(r)
    rf.close()

with open(packedPath, "rb") as rf:
    for data in fileInfos:
        path = data[0]
        count = data[1]
        offset = data[2]
        length = data[3]
        if(count != 0):
            if(not os.path.exists(outdir+"\\"+path)):
                os.makedirs(outdir+"\\"+path)
                # print("mkdir")
        else:
            with open(outdir+"\\"+path, "wb") as wf:
                rf.seek(offset, 0)
                wf.write(rf.read(length))
                wf.close()
    rf.close()
