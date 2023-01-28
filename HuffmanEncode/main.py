def count(text):
    numOfSymbols = []
    for i in text:
        if i in numOfSymbols:
            ind = numOfSymbols.index(i)
            numOfSymbols[ind+1] += 1
        else:
            numOfSymbols.append(i)
            numOfSymbols.append(1)

    return numOfSymbols


def probability(numOfSymbols, length):
    proOfSymbols = []
    i = 0
    while i < len(numOfSymbols):
        proOfSymbols.append(numOfSymbols[i])
        proOfSymbols.append(numOfSymbols[i+1]/length)
        i += 2

    return proOfSymbols


def sort(list):
    i = 1
    while i < len(list)-1:
        max = i
        j = i+2
        while j < len(list):
            if list[j] >= list[max]:
                max = j
            j += 2
        list[max], list[i] = list[i], list[max]
        list[max-1], list[i-1] = list[i-1], list[max-1]
        i += 2
    return list


def makeBranches(probs):
    lists = []
    probs = sort(probs)
    lists.append(probs)
    length = len(probs)
    # loop until it be 2 elements only
    while length != 4:
        list = lists[len(lists)-1].copy()
        last = len(list)-1
        beforeLast = last-2
        # add 2 elements
        list[beforeLast] += list[last]
        list[beforeLast-1] += '+' + list[last-1]
        # delete last elements
        del list[len(list)-1]
        del list[len(list)-1]
        # sort new list
        list = sort(list)
        length = len(list)
        lists.append(list)
    return lists


def encode(lists):
    dec = []
    i = len(lists)-1

    # last branch
    lists[i][1] = '0'
    lists[i][3] = '1'

    i -= 1
    # loop for branches
    while i >= 0:
        # length of branch
        length = len(lists[i])-2
        # last 2 elements in this branch
        str = lists[i][length-2]+'+'+lists[i][length]
        # find binary num of last 2 elements
        ind = lists[i+1].index(str)
        # add previse binary num to 2 elements with addition 0 or 1 o them
        lists[i][length-1] = lists[i+1][ind+1]+'0'
        lists[i][length+1] = lists[i+1][ind+1]+'1'

        # add previse binary num of elements that already assigned
        x = 0
        while x < len(lists[i+1]):
            if lists[i+1][x] in lists[i]:
                ind = lists[i].index(lists[i+1][x])
                lists[i][ind+1] = lists[i+1][x+1]
            x += 2

        i -= 1

    dec = lists[0].copy()
    return dec


def makeStream(dic,text):
    stream = ""
    for i in text:
        ind = dic.index(i)
        stream += dic[ind+1]

    return stream


# read from file
textFile = open("Text_E.txt", "r")
text = textFile.read()

num = count(text)
pro = probability(num, len(text))
list = makeBranches(pro)
dic = encode(list)
stream = makeStream(dic,text)
str = "["
for i in dic:
    if i == dic[len(dic)-1]:
        str += i
    else:
        str += i + ','
str += "]"

# write to file
compressedFile = open("Compressed.txt", "w")
compressedFile.write(str + '\n')
compressedFile.write(stream)

textFile.close()
compressedFile.close()


