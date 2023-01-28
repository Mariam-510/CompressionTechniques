import math

# ASCII Code from 0 to 255
def makeDictionary():
    list = []
    for ascii_num in range(0, 256):
        list.append(chr(ascii_num))
    return list


# Encode Function
def encode(text):
    list = makeDictionary()
    tags = []
    begin = 0
    end = begin + 1
    # find the longest match
    while begin < len(text):
        while text[begin:end] in list and end <= len(text):
            ind = list.index(text[begin:end])
            end += 1
        # add index of the longest match in list to tags
        tags.append(ind)
        # add the longest match chars + next symbol to dictionary
        if end <= len(text):
            list.append(text[begin:end])
        # loop again from next symbol
        begin = end-1
    return tags


# Converting Tags to String to print
def printEncodedNum(tags):
    numbers = ""
    for i in range(len(tags)):
        if i != 0:
            numbers += ','
        numbers += "<"+str(tags[i])+">"
    return numbers


def calculateOiginalSize (text):
    print("Original Size =", len(text), "Symbols *", 8, "Bits =", len(text)*8)


def findMaxIndexValue(tags):
    max = tags[0]
    for i in range(1, len(tags)):
        if tags[i] > max:
            max = tags[i]
    return max


def calculateNumOfBit(num):
    bits = math.ceil(math.log(num, 2))
    return bits


def calculateCompressedSize (tags):
    max = findMaxIndexValue(tags)
    bits = calculateNumOfBit(max)
    print("Max Index Value =", max)
    print("Compressed Size =", len(tags), "Tags *", bits, "Bits =", bits*len(tags))


# Encoding Input
inputText = input("Enter the word you want to encode: ")
encodedTags = encode(inputText)
print()
print(printEncodedNum(encodedTags))
print()
# Original Size
calculateOiginalSize(inputText)
# Compressed Size
calculateCompressedSize(encodedTags)
