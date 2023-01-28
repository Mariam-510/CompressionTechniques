# Decoding
def decoding(tags):
    text = ""
    for x in range(0,len(tags)):
        position = tags[x][0]
        length = tags[x][1]
        nextSymbol = tags[x][2]
        if position == 0 and length == 0:
            text += nextSymbol
        else:
            text += text[(len(text) - position):(len(text) - position + length)]
            if nextSymbol != "Null":
                text += nextSymbol

    return text


# Enter Tags and Converting them to list
def enteringTags():
    tags = []
    print("Enter tags you to decode with this format <Position,Length,Next Symbol>,<Position,Length,Next Symbol>...:")
    inputTags = input()
    x = 0
    while x < len(inputTags)-1:
        tag = []
        while inputTags[x] != '<':
            x += 1
        x += 1

        # add position
        y = x
        while inputTags[x] != ',':
            x += 1
        tag.append(int(inputTags[y:x]))
        x += 1

        # add length
        y = x
        while inputTags[x] != ',':
            x += 1
        tag.append(int(inputTags[y:x]))
        x += 1

        # add next symbol
        if inputTags[x] == '\'' or inputTags[x] == '’' or inputTags[x] == '"' or inputTags[x] == '”':
            x += 1
            y = x
            while inputTags[x] != '\'' and inputTags[x] != '’' and inputTags[x] != '"' and inputTags[x] != '”':
                x += 1
            tag.append(inputTags[y:x])
            x += 1
        else:
            y = x
            while inputTags[x] != '>':
                x += 1
            tag.append(inputTags[y:x])
        # add tag
        tags.append(tag)

    return tags


# Decoding Input
inputTags = enteringTags()
decodedText = decoding(inputTags)
print(decodedText)
