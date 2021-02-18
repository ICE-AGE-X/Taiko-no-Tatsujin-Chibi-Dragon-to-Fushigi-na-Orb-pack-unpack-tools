from PIL import Image
import sys

argc = len(sys.argv)
if argc != 5:
    print("usage: python lmtpng2normalpng.py i|e g|n [inpng] [outpng]")
    print("ex   : python lmtpng2normalpng.py e g lmt.png gray.png")
    print("       python lmtpng2normalpng.py i g gray.png lmt.png")
    print("       python lmtpng2normalpng.py e n lmt.png normal.png")
    print("       python lmtpng2normalpng.py i n normal.png lmt.png")
    exit(0)

doType = sys.argv[1]
isReColorFormat = sys.argv[2] == "n"
inPath = sys.argv[3]
outPath = sys.argv[4]

img = Image.open(inPath)
width, height = img.size

order = (42, 43, 46, 47, 58, 59, 62, 63,
         40, 41, 44, 45, 56, 57, 60, 61,
         34, 35, 38, 39, 50, 51, 54, 55,
         32, 33, 36, 37, 48, 49, 52, 53,
         10, 11, 14, 15, 26, 27, 30, 31,
         8, 9, 12, 13, 24, 25, 28, 29,
         2, 3, 6, 7, 18, 19, 22, 23,
         0, 1, 4, 5, 16, 17, 20, 21)

order2 = (0, 1, 4, 5, 16, 17, 20, 21,
          2, 3, 6, 7, 18, 19, 22, 23,
          8, 9, 12, 13, 24, 25, 28, 29,
          10, 11, 14, 15, 26, 27, 30, 31,
          32, 33, 36, 37, 48, 49, 52, 53,
          34, 35, 38, 39, 50, 51, 54, 55,
          40, 41, 44, 45, 56, 57, 60, 61,
          42, 43, 46, 47, 58, 59, 62, 63)


def orderData(img, colors, cIdx, ix, iy, ox, oy):
    img.putpixel((ix, iy), colors[cIdx+order2[ox+oy*8]])


def lmtPng2NormalPng(img):
    colors = []
    for h in range(height):
        for w in range(width):
            c = img.getpixel((w, h))
            if(isReColorFormat):
                colors.append((c[3], c[2], c[1], c[0]))
            else:
                colors.append(c)
            # colors.append((c[2], c[0], c[1], c[3]))
            # a wf.write(c[0].to_bytes(1, "little"))
            # r wf.write(c[1].to_bytes(1, "little"))
            # g wf.write(c[2].to_bytes(1, "little"))
            # b wf.write(c[3].to_bytes(1, "little"))
    x = 0
    y = 0
    for cIdx in range(0, width*height, 8*8):
        for oy in range(8):
            for ox in range(8):
                orderData(img, colors, cIdx, x+ox, y+oy, ox, oy)
        x += 8
        if(x >= width):
            x = 0
            y += 8
        if(y >= height):
            break


def normalPng2LmtPng(img):
    orgData = list(img.getdata())
    dstData = orgData[:]

    dstIdx = 0
    for y in range(0, height, 8):
        for x in range(0, width, 8):
            block8Data = []
            for oy in range(8):
                for ox in range(8):
                    c = img.getpixel((x+ox, y+oy))
                    if(isReColorFormat):
                        block8Data.append((c[3], c[2], c[1], c[0]))
                    else:
                        block8Data.append(c)
            for i in range(64):
                dstData[dstIdx+order2[i]] = block8Data[i]
            dstIdx += 64
    for y in range(height):
        for x in range(width):
            img.putpixel((x, y), dstData[x+y*width])

if(doType == "e"):
    lmtPng2NormalPng(img)
elif(doType == "i"):
    normalPng2LmtPng(img)
else:
    print("error type")
img.save(outPath, "PNG")
