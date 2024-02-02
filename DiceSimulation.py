import random

firstDiceNum = 0
secondDiceNum = 0
thirdDiceNum = 0

twoTheSame = 0
threeTheSame = 0

valuesOfTwoSames = []
valuesOfThreeSames = []

valuesOfTwoAverages = []
valuesOfThreeAverages = []

x = 0
y = 0
z = 0
while x < 10000:
    while y < 10000:
        while z < 100000:
            firstDiceNum = random.randint(1, 6)
            secondDiceNum = random.randint(1, 6)
            thirdDiceNum = random.randint(1, 6)
            
            if firstDiceNum == secondDiceNum or firstDiceNum == thirdDiceNum or secondDiceNum == thirdDiceNum:
                twoTheSame = twoTheSame + 1
            
            if firstDiceNum == secondDiceNum == thirdDiceNum:
                threeTheSame = threeTheSame + 1
                
            z = z + 1
            
        valuesOfTwoSames.append(twoTheSame)
        twoTheSame = 0
        
        valuesOfThreeSames.append(threeTheSame)
        threeTheSame = 0
        
        y = y + 1

    twoSamesAverage = round(sum(valuesOfTwoSames)/1000, 1)
    valuesOfTwoAverages.append(twoSamesAverage)
    twoSamesAverage = 0
    threeSamesAverage = round(sum(valuesOfThreeSames)/1000, 1)
    valuesOfThreeAverages.append(threeSamesAverage)
    threeSamesAverages = 0
    
    x = x + 1
    
finalTwoAverage = round(sum(valuesOfTwoAverages)/10000, 1)
finalThreeAverage = round(sum(valuesOfThreeAverages)/10000, 1)
    
print("There was two that were the same", str(finalTwoAverage) + "% of the time on average and three that were the same", str(finalThreeAverage) + "% of the time on average.")

