# Encoding With Search Window And Look Ahead Window
def encoding(text, search, lookAhead):
    tags = []
    index = 0
    while index < len(text):
        tag = longestMatch(text, index, search, lookAhead)
        tags.append(tag)
        if tag[0] == 0 and tag[1] == 0:
            index += 1
        else:
            index = index + tag[1] + 1
    return tags


# Encoding Without Search Window And LookAhead Window
def encodingWithNoRestrictions(text):
    tags = encoding(text, len(text)-1, len(text)-1)
    return tags


# Finding The Longest Match Function
def longestMatch(text, index, search, lookAhead):
    tag = []
    position = 0
    length = 0
    nextSymbol = text[index]

    if search == len(text)-1 or index-search < 0:
        x = 0
    else:
        x = index-search

    # loop from the first char to the index char
    while x < index:
        counter = 0
        pos = index
        i = index
        # check if this char match with the index char
        if text[x] == text[index]:
            pos = x
            counter += 1
            i = index+1
            y = x+1
            # check the longest match from this char
            while y != index and i < len(text)-1 and i < (index + lookAhead - 1):
                if text[y] == text[i]:
                    y += 1
                    i += 1
                    counter += 1
                else:
                    break
        x += 1

        # comparing the longest match
        if counter >= length:
            length = counter
            position = index - pos
            if i >= len(text) and length != 0 and position != 0:
                nextSymbol = "Null"
            else:
                nextSymbol = text[i]

    # make tag
    tag.append(position)
    tag.append(length)
    tag.append(nextSymbol)

    return tag


# Format Tags like this <Position,Length,Next Symbol>
def formatingTagsToPrint (tags):
    tagsFormat = ""
    for x in range(0, len(tags)):
        tagsFormat = tagsFormat + "<" + str(tags[x][0]) + "," + str(tags[x][1]) + "," + "'" + str(tags[x][2]) + "'" + ">"

        if x < len(tags)-1:
            tagsFormat += ","

    return tagsFormat


# Encoding Input
inputText = input("Enter the word you want to encode: ")
print("1) With no restrictions on search window or look ahead window")
print("2) With a specified size of the search window and look ahead buffer window")
print("Enter 1 or 2 : ")
num = int(input())

while num != 1 and num != 2:
    print("Invalid Input. Enter 1 or 2 : ")
    num = int(input())

if num == 1:
    encodedTags = encodingWithNoRestrictions(inputText)
elif num == 2:
    search = int(input("Enter size of search window: "))
    lookAhead = int(input("Enter size of look ahead buffer window: "))
    encodedTags = encoding(inputText, search, lookAhead)

print(formatingTagsToPrint(encodedTags))
