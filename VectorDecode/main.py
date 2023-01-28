from PIL import Image
import numpy as np


class VecGroup:
    vec = []
    code = ""

    def addVec(self, v):
        self.Vec = v

    def addCode(self, c):
        self.code = c


file_out = open("..\output.txt","r")
fRead0 = file_out.readline()
fRead0 = fRead0[:len(fRead0)-1]
fRead1 = file_out.readline()
fRead1 = fRead1[:len(fRead1)-1]
fRead2 = file_out.readline()
fRead2 = fRead2[:len(fRead2)-1]
fRead3 = file_out.readline()
fRead3 = fRead3[:len(fRead3)-1]
fRead4 = file_out.readline()
fRead4 = fRead4[:len(fRead4)-1]

numOfBits = int(fRead0)
numOfCodebook = pow(2, numOfBits)
length = int(fRead1)
width = int(fRead2)
dl = int(fRead3)
dw = int(fRead4)

print(numOfBits, length, width, dl, dw)

listOfCode = []
for i in range(int(length/dl)*int(width/dw)):
    fRead = file_out.readline()
    fRead = fRead[:len(fRead) - 1]
    listOfCode.append(fRead)

print(len(listOfCode))

vecGroup = []
n = 0
while n < numOfCodebook*dl*dw:
    fRead = file_out.readline()
    fRead = fRead[:len(fRead) - 1]
    group = VecGroup()
    group.code = fRead
    n+=1
    l=[]
    for i in range(dl):
        l1=[]
        for j in range(dw):
            fRead = file_out.readline()
            fRead = fRead[:len(fRead) - 1]
            l1.append(int(fRead))
            n+=1
        l.append(l1)
    n += 1
    group.vec = l
    vecGroup.append(group)


file_out.close()

for x in range(len(vecGroup)):
    print("code book", x)
    print(vecGroup[x].vec)
    print("its code")
    print(vecGroup[x].code)


decVec = []
for i in range(len(listOfCode)):
    for x in range(len(vecGroup)):
        if vecGroup[x].code == listOfCode[i]:
            decVec.append(vecGroup[x].vec)
            break


decBlock = np.reshape(decVec, (length, width))

Dec = np.asarray(decVec)
number,dl, dw = Dec.shape
bl, bw = decBlock.shape
print(bl,bw)
n=0
le=0
wi=0
for i in range (int(bl/dl)):#length
     for j in range(int(bw/dw)):#width
         for x in range(dl):#length vector
             for y in range(dw):
                 decBlock[x+le][y+wi]=Dec[n][x][y]
         n=n+1
         wi=wi+dw
     le=le+dl
     wi = 0

print(decBlock)

savePath='something.png'
decodedImg = Image.fromarray(decBlock)
decodedImg = decodedImg.convert("L")
decodedImg.save(savePath) # will save it as gray image