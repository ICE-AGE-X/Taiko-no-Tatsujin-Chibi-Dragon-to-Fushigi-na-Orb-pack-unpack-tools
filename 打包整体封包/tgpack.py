import libs
import sys
import os
argc = len(sys.argv)
if argc != 2:
    print("usage: python tgpack.py [packdir]")
    exit(0)
path = sys.argv[1]

class FileInfo:
    def __init__(self):
        self.subDirs = []
        self.size = 0
        self.realSize = 0
        self.dir = ""
        self.fileNum = 0
        
idx = 0
totalSize = 0

def takeDir(e):
    return e.dir

def getDirFileSize(dir):
    for root, dirs, files in os.walk(dir):
        fInfo = FileInfo()
        fInfo.dir = dir[len(path)+1:len(dir)]
        count = 0
        fileNum = 0
        if(len(dirs) > 0):
            # dirs.sort()
            for d in dirs:
                subfileInfo = getDirFileSize(root+"/"+d)
                count += subfileInfo.size
                fInfo.subDirs.append(subfileInfo)
                fileNum += subfileInfo.fileNum
                fileNum += 1
        if(len(files) > 0):
            # files.sort()
            for f in files:
                subFile = root+"/"+f
                length = os.path.getsize(subFile)
                fixLen = libs.calFixLen(length)+length
                count += fixLen
                subfileInfo = FileInfo()
                subfileInfo.dir = fInfo.dir+"/"+f
                subfileInfo.size = fixLen
                subfileInfo.realSize = length
                fInfo.subDirs.append(subfileInfo)
                fileNum += 1
        fInfo.subDirs.sort(key=takeDir)
        fInfo.size = count
        fInfo.fileNum = fileNum
        return fInfo


seekIdx = 0
wpf=open("packed","wb")

def processFileInfo(wf,fInfo):
    global seekIdx
    global wpf
    if(fInfo.dir != ""):
        if(fInfo.realSize > 0):  # 普通文件
            wf.write(bytes(fInfo.dir, encoding="utf-8"))
            libs.fillByteN(wf, 0x50-len(fInfo.dir))
            libs.fillByteN(wf, 4)
            wf.write(seekIdx.to_bytes(4, "little"))  # 写文件偏移
            wf.write(fInfo.realSize.to_bytes(4, "little"))  # 写文件长度
            wf.write(seekIdx.to_bytes(4, "little"))  # 写文件偏移
            wf.write(fInfo.realSize.to_bytes(4, "little"))  # 写文件长度
            rf= open(path+"/"+fInfo.dir,"rb")
            wpf.write(rf.read(fInfo.realSize))
            libs.fillByteN(wpf,fInfo.size-fInfo.realSize)
            rf.close()
            seekIdx += fInfo.size
        else:  # 文件夹
            wf.write(bytes(fInfo.dir+"/", encoding="utf-8"))
            libs.fillByteN(wf, 0x50-len(fInfo.dir)-1)
            wf.write(fInfo.fileNum.to_bytes(4, "little"))  # 写文件数量
            wf.write(seekIdx.to_bytes(4, "little"))  # 写文件偏移
            wf.write(fInfo.size.to_bytes(4, "little"))  # 写文件长度
            wf.write(seekIdx.to_bytes(4, "little"))  # 写文件偏移
            wf.write(fInfo.size.to_bytes(4, "little"))  # 写文件长度
            for f in fInfo.subDirs:
                processFileInfo(wf, f)
    else:
        for f in fInfo.subDirs:
            processFileInfo(wf, f)


fileInfo = getDirFileSize(path)
with open("packedlist", "wb") as wf:
    wf.write(bytes(
        "c:/Program Files/Jenkins/jobs/taiko3ds_master_build/workspace/taikoThreeDS/master/romfiles", encoding="utf-8"))
    libs.fillByteN(wf, 0x76)
    wf.write(fileInfo.fileNum.to_bytes(4, "little"))
    libs.fillByteN(wf, 4)
    wf.write(fileInfo.size.to_bytes(4, "little"))
    libs.fillByteN(wf, 4)
    wf.write(fileInfo.size.to_bytes(4, "little"))
    processFileInfo(wf, fileInfo)
    wf.close()
wpf.close()

