def makeDic(dicText):
    dic = []
    begin = 1
    end = 2
    while end <= len(dicText):
        if dicText[end] == ',' or dicText[end] == ']':
            dic.append(dicText[begin:end])
            end += 1
            begin = end
        end += 1
    return dic


def decode(dicText,stream):
    text = ""
    dic = makeDic(dicText)
    begin = 0
    end = 1
    while end <= len(stream):
        if stream[begin:end] in dic:
            ind = dic.index(stream[begin:end])
            text += dic[ind-1]
            begin = end
            end += 1
        else:
            end += 1

    return text


# read from file
compressedFile = open("Compressed.txt", "r")
content = compressedFile.read()
dicText = ""
stream = ""
i = 0
while i < len(content):
    if content[i] == ']':
        dicText += content[i]
        i += 1
        break
    else:
        dicText += content[i]
        i += 1

while i < len(content):
    if content[i] == '\n':
        i += 1
        continue
    else:
        stream += content[i]
        i += 1

text = decode(dicText, stream)

# write to file
TextFile = open("Text_D.txt", "w")
TextFile.write(text)

compressedFile.close()
TextFile.close()
