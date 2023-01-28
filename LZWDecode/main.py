# Enter Tags and Converting them to list
def enteringTags():
    tags = []
    print("Enter tags you to decode with this format number,number,...:")
    inputTags = input()
    begin = 1
    end = 1
    while end < len(inputTags):
        while inputTags[end] != '>':
            end += 1
            if end == len(inputTags):
                break
        tags.append(int(inputTags[begin:end]))
        end += 3
        begin = end
    return tags


# ASCII Code from 0 to 255
def makeDictionary():
    list = []
    for ascii_num in range(0, 256):
        list.append(chr(ascii_num))
    return list


# Decode Function
def decode(tags):
    list = makeDictionary()
    text = ""
    for i in range(len(tags)):
        # if tag number is in dictionary
        if tags[i] < len(list):
            # add to text
            text += list[tags[i]]
            # add to dictionary
            if i != 0:
                str = list[tags[i - 1]] + list[tags[i]][0]  # before and the first char from next symbol
                list.append(str)

        # if tag number isn't in dictionary
        else:
            str = list[tags[i-1]] + list[tags[i-1]][0]  # before and the first char from this symbol
            # add to text
            text += str
            # add to dictionary
            list.append(str)

    print(list[256:])
    return text


# Decoding Input
inputTags = enteringTags()
decodedText = decode(inputTags)
print(decodedText)
