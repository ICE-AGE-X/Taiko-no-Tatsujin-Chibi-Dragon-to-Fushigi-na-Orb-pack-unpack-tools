import struct
def readIntN(file,n):
    return struct.unpack('i', file.read(n))[0]

def readInt4(file):
    return readIntN(file,4)

def readInt2(file):
    return readIntN(file,2)

def readInt1(file):
    return readIntN(file,1)

def readStr(file,size):
    name=file.read(size)
    pos=findEndPos(name)
    return str(name[:pos],encoding="utf-8")

def findEndPos(data):
    idx=0
    while data[idx]!=0:
        idx+=1
    return idx