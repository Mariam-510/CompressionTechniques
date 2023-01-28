from PIL import Image
import numpy as np


class VecGroup:
    splitVec = []
    children = []
    code = ""

    def __init__(self):
        self.splitVec = []
        self.children = []

    def addVec(self, vec):
        self.splitVec = vec

    def addChild(self, child):
        self.children.append(child)

    def addCode(self, c):
        self.code = c


# average for all block
def average(block, numOfVector, l, w):
    sum = block[0][0]

    for i in range(l):  # l
        for j in range(w):  # w
            sum = np.add(sum.astype(np.uint64), block[i][j])

    sum = np.subtract(sum.astype(np.uint64), block[0][0])
    sum = np.divide(sum.astype(np.uint64), numOfVector)
    return sum


# split vec
def splitting(avg):
    vec1 = np.subtract(avg,1)
    vec2 = np.add(avg,1)
    vec1 = np.ceil(vec1)
    vec2 = np.floor(vec2)

    return vec1, vec2


# find nearest vector
def nearestVector(v, dem1, dem2, vecs):
    nums = []
    x = 0
    while x < len(vecs):
        n = 0
        vec = vecs[x].splitVec
        for i in range(dem2):
            for j in range(dem1):
                n += abs(v[i][j] - vec[i][j])
        nums.append(n)
        x += 1
    minInd = 0
    for y in range(1, len(nums)):
        if nums[y] < nums[minInd]:
            minInd = y

    return minInd


# average for children of vector
def averageChildren(children):
    sum = children[0]
    for n in range(1, len(children)):
        sum = np.add(sum.astype(np.uint64), children[n])

    sum = np.divide(sum.astype(np.uint64), len(children))
    return sum


# check averages children changed or not
def checkChildren(newGroups,vecGroups):
    changed = False
    for n in range(len(newGroups)):
        if len(newGroups[n].children) != len(vecGroups[n].children):
            changed = True
            break
        else:
            for c in range(len(newGroups[n].children)):
                found = False
                for x in range(len(vecGroups[n].children)):
                    if (newGroups[n].children[c] == vecGroups[n].children[x]).all:
                        found = True
                if found == False:
                    changed = True
                    break

    return changed


def encode(numOfBits,block, numOfVector, l, w,dem1,dem2):
    # first 2 vectors
    avg = average(block, numOfVector, l, w)
    vec1, vec2 = splitting(avg)
    group1 = VecGroup()
    group1.addVec(vec1)
    group2 = VecGroup()
    group2.addVec(vec2)
    vecGroups = []
    vecGroups.append(group1)
    vecGroups.append(group2)

    # nearest vector
    for i in range(l):  # l
        for j in range(w):  # w
            nearestVec = nearestVector(block[i][j], dem1, dem2, vecGroups)
            vecGroups[nearestVec].addChild(block[i][j])

    # avgs
    avgs = []
    for x in range(len(vecGroups)):
        avgs.append(averageChildren(vecGroups[x].children))

    # loop for num of levels
    for n in range(1, numOfBits):
        vecGroups = []
        # split new average vectors
        for c in range(len(avgs)):
            vec1, vec2 = splitting(avgs[c])
            group1 = VecGroup()
            group1.splitVec = vec1
            group2 = VecGroup()
            group2.splitVec = vec2
            vecGroups.append(group1)
            vecGroups.append(group2)

        # # nearest vector
        for i in range(l):  # l
            for j in range(w):  # w
                nearestVec = nearestVector(block[i][j], dem1, dem2, vecGroups)
                vecGroups[nearestVec].addChild(block[i][j])

        # new avgs
        avgs = []
        for x in range(len(vecGroups)):
            if len(vecGroups[x].children) != 0:
                avgs.append(averageChildren(vecGroups[x].children))

    # finish split
    # check changed or not
    changed = True
    while(changed == True):
        newGroups = []

        # add new average vectors
        for c in range(len(avgs)):
            group = VecGroup()
            group.splitVec = avgs[c]
            newGroups.append(group)

        # nearest vector
        for i in range(l):  # l
            for j in range(w):  # w
                nearestVec = nearestVector(block[i][j], dem1, dem2, newGroups)
                newGroups[nearestVec].addChild(block[i][j])

        changed = checkChildren(newGroups, vecGroups)
        if changed == True:
            avgs = []
            for x in range(len(newGroups)):
                if len(newGroups[x].children) != 0:
                    avgs.append(averageChildren(newGroups[x].children))
            vecGroups = newGroups

    return newGroups


# main
# imgPath = 'lenna256.png'
imgPath = 'pic.png'
img = Image.open(imgPath).convert("L")
imgArr = np.asarray(img)
length, width = imgArr.shape  # length width

file_in = open("input.txt", "r")
fRead0 = file_in.readline()
fRead0 = fRead0[:len(fRead0)-1]
fRead1 = file_in.readline()
fRead1 = fRead1[:len(fRead1)-1]
fRead2 = file_in.readline()

numOfBits = int(fRead0)  # input
numOfVectorCodebook = pow(2, numOfBits)
dem1 = int(fRead1)   # input width
dem2 = int(fRead2)   # input  length

checkResize = False

while length/dem2 % 1 != 0 or width/dem1 % 1 != 0:
    checkResize = True
    if length/dem2 % 1 != 0:
        length -= 1
    if width/dem1 % 1 != 0:
        width -= 1

if checkResize == True:
    newImage = img.crop((0, 0, width, length))
    # newImage = img.resize((length, width))
    newImage.save('new_image.png')
    imgArr = np.asarray(newImage)
    length, width = imgArr.shape  # length width

numOfVector = int((length*width)/(dem1*dem2))
w = int(width/dem1)
l = int(length/dem2)

# vsplit = size of width ,hplit = length
block = [np.hsplit(x, w) for x in np.vsplit(imgArr, l)]

newG = encode(numOfBits, block, numOfVector, l, w, dem1, dem2)
# give each codebook code
for x in range(len(newG)):
    newG[x].code = bin(x)[numOfBits:].zfill(numOfBits)

# write dems
file_out = open("../output.txt","w")
file_out.write(str(numOfBits)+"\n")
file_out.write(str(length)+"\n"+str(width)+"\n")
file_out.write(str(dem2)+"\n"+str(dem1)+"\n")

strCode = ""
listOfCode = []
for i in range(l):  # l
    for j in range(w):  # w
        nearestVec = nearestVector(block[i][j], dem1, dem2, newG)
        listOfCode.append(newG[nearestVec].code)
        file_out.write(newG[nearestVec].code+"\n")
        strCode += newG[nearestVec].code + " "


# write codebook to file
for x in range(len(newG)):
    file_out.write(newG[x].code + "\n")
    for i in range(dem2):
        for j in range(dem1):
            sV = int(newG[x].splitVec[i][j])
            file_out.write(str(sV) + "\n")

file_out.write("\n")
# print codebook vecs and their children
for x in range(len(newG)):
    print("code book", x)
    print(newG[x].splitVec)
    print("its code")
    print(newG[x].code)
    print("-------------------------------------")

print(strCode)

file_out.close()
file_in.close()
