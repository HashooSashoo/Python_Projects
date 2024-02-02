def makeNumbers():
    numberlist = ["", "one ", "two ", "three ", "four ", "five ", "six ", "seven ", "eight ", "nine "]
    placementList = ["", "ten ", "twenty ", "thirty ", "forty ", "fifty ", "sixty ", "seventy ", "eighty ", "ninety "]
    anotherPlacementList = ["", "one hundred ", "two hundred ", "three hundred ", "four hundred ", "five hundred ", "six hundred ", "seven hundred ", "eight hundred ", "nine hundred "]
    outlyers = ["ten ", "eleven ", "twelve ", "thirteen ", "fourteen ", "fifteen ", "sixteen ", "seventeen ", "eighteen ", "nineteen "]
    
    index0 = 0
    index1 = 0
    index2 = 1
    indexNega0 = 0
    indexNega1 = 0
    indexNega2 = 1
    
    myTxtFile = open("myNumbers.txt", "a")

    while index0 < 10:
        while index1 < 10:
            while index2 < 10:
                if index1 == 1:
                    print(anotherPlacementList[index0] + outlyers[index2], file=myTxtFile)
                else:
                    print(anotherPlacementList[index0] + placementList[index1] + numberlist[index2], file=myTxtFile)
                index2 = index2 + 1
            index1 = index1 + 1
            index2 = index2 - 10
        index0 = index0 + 1
        index1 = index1 - 10
    index0 = index0 - 10

    while indexNega0 < 10:
        while indexNega1 < 10:
            while indexNega2 < 10:
                while index0 < 10:
                    while index1 < 10:
                        while index2 < 10:
                            if index1 == 1 and indexNega1 == 1:
                                print(anotherPlacementList[indexNega0] + outlyers[indexNega2] + "thousand " + anotherPlacementList[index0] + outlyers[index2], file=myTxtFile)
                            elif index1 == 1:
                                print(anotherPlacementList[indexNega0] + placementList[indexNega1] + numberlist[indexNega2] + "thousand " + anotherPlacementList[index0] + outlyers[index2], file=myTxtFile)
                            elif indexNega1 == 1:
                                print(anotherPlacementList[indexNega0] + outlyers[indexNega2] + "thousand " + anotherPlacementList[index0] + placementList[index1] + numberlist[index2], file=myTxtFile)
                            else:
                                print(anotherPlacementList[indexNega0] + placementList[indexNega1] + numberlist[indexNega2] + "thousand " + anotherPlacementList[index0] + placementList[index1] + numberlist[index2], file=myTxtFile)
                            index2 = index2 + 1
                        index1 = index1 + 1
                        index2 = index2 - 10
                    index0 = index0 + 1
                    index1 = index1 - 10
                indexNega2 = indexNega2 + 1
                index0 = index0 - 10
            indexNega1 = indexNega1 + 1
            indexNega2 = indexNega2 - 10
        indexNega0 = indexNega0 + 1
        indexNega1 = indexNega1 - 10
    print("ONE WHOLE MILLION!!!!", file=myTxtFile)
    myTxtFile.close()

makeNumbers()
        
            