def makeProbabilityList(proText):
    pro = []
    begin = 1
    end = 2
    while end <= len(proText)-1:      # [a,0.1,b,0.5]  #a,0.5,b,0.2,c
        if proText[end] == ']' or proText[end] == ',':
            if len(pro) % 2 == 0:
                pro.append(proText[begin:end])
            else:
                pro.append(float(proText[begin:end]))
            end += 1
            begin = end
        end += 1

    return pro


def makeRange(pro):
    range = []
    range.append(pro[0])
    range.append(0)
    range.append(pro[1])
    i = 2

    while i < len(pro)-1:
        range.append(pro[i])
        range.append(range[len(range)-2])
        range.append(range[len(range)-1]+pro[i+1])
        i += 2
    return range


def numberOfBits(pro):
    i = 1
    smallestRange = pro[i]
    i += 2
    while i < len(pro):
        if pro[i] < smallestRange:
            smallestRange = pro[i]
        i += 2
    num = 0
    while (1/pow(2, num)) > smallestRange:
        num += 1

    return num


def binaryToDecimal(binary):
    return int(binary, 2)


def decode(stream, protext):
    text = ""
    pro = makeProbabilityList(proText)
    k = numberOfBits(pro)
    range = makeRange(pro)

    # first symbol
    begin = 0
    shift = 0
    binary = stream[begin:begin+k]
    code = binaryToDecimal(binary)/pow(2, k)

    # check symbol
    i = 0
    while i <= len(range)-3:
        if range[i+1] <= code < range[i+2]:
            lower = range[i+1]
            upper = range[i+2]
            text += range[i]
            break
        i += 3

    while lower > 0.5 or upper < 0.5:
        if lower > 0.5:  # E2
            lower = (lower - 0.5) * 2
            upper = (upper - 0.5) * 2
            shift += 1

        elif upper < 0.5:  #E1
            lower = lower * 2
            upper = upper * 2
            shift += 1

    if shift != 0:
        begin += shift
        binary = stream[begin:begin + k]
        code = binaryToDecimal(binary) / pow(2, k)

    # other
    while begin+k < len(stream):
        shift = 0
        code = (code-lower)/(upper-lower)
        i = 0
        while i <= len(range) - 3:
            if range[i + 1] < code < range[i + 2]:
                newLower = lower + (upper-lower) * range[i + 1]
                newUpper = lower + (upper-lower) * range[i + 2]
                text += range[i]
                break
            i += 3
        while newLower > 0.5 or newUpper < 0.5:
            if newLower > 0.5:
                newLower = (newLower-0.5)*2
                newUpper = (newUpper-0.5)*2
                shift += 1

            elif newUpper < 0.5:
                newLower = newLower*2
                newUpper = newUpper*2
                shift += 1

        lower = newLower
        upper = newUpper
        if shift != 0:
            begin += shift
            binary = stream[begin:begin+k]
            code = binaryToDecimal(binary)/pow(2, k)

    # last symbol
    code = (code - lower) / (upper - lower)
    i = 0
    while i <= len(range) - 3:
        if range[i + 1] < code < range[i + 2]:
            text += range[i]
            break
        i += 3

    return text


# read from file
compressedFile = open("Compressed.txt", "r")
content = compressedFile.read()
proText = ""
stream = ""
i = 0

while content[i] != '\n':
    stream += content[i]
    i += 1
i += 1
while i < len(content):
    proText += content[i]
    i += 1

text = decode(stream, proText)
# write to file
TextFile = open("Text_D.txt", "w")
TextFile.write(text)

compressedFile.close()
TextFile.close()
