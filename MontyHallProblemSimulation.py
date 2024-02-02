import random
x = 0
y = 0
numberImRight = 0
setOfData = []
loop = True
while loop == True:
    print("This is the Monty Hall Problem. Here's how it works.")
    print()
    print("There are three doors. One door has a car behind it, the others have nothing.\nYou are told to pick a door at random, and you do.\nA door is then taken away that contained nothing.\nYou now have the option to switch to the second door, or stay with your choice.\nThe question is... which decision is more likely to give you the car?")
    print()
    print("Let's find out!")
    print()
    willISwitch = input("Do you want to switch to the second car, or keep your choice? y or n")
    print()
    print("Ok then, let's see how many times you get the car!")
    print()

    while x < 100:
        while y < 10000:
            boolArray = [True, False, False]
            
            boolArray = random.sample(boolArray, 3)

            class Door:
                def __init__(self, doorNum, carBehindDoor):
                    self.doorNum = doorNum
                    self.carBehindDoor = carBehindDoor
                    
                
            firstDoor = Door(1, boolArray[0])
            secondDoor = Door(2, boolArray[1])
            thirdDoor = Door(3, boolArray[2])
            
            doorChoices = [firstDoor, secondDoor, thirdDoor]
            
            myDoorChoice = doorChoices[0]
            
            if myDoorChoice.carBehindDoor:
                doorChoices.remove(secondDoor or thirdDoor)
            elif secondDoor.carBehindDoor:
                doorChoices.remove(thirdDoor)
            else:
                doorChoices.remove(secondDoor)
            
            if willISwitch == "y":
                myDoorChoice = doorChoices[1]
            
            if myDoorChoice.carBehindDoor:
                numberImRight = numberImRight + 1
            
            y = y + 1
        
        setOfData.append(numberImRight)
        numberImRight = 0
        x = x + 1
        y = y - 10000
        
    averageNumberRight = round(sum(setOfData)/10000, 1)

    print("You picked the door with the car ", str(averageNumberRight) + "% of the time.")
    print()
    print("Here is some other information that will be useful.")
    print()
    print("The list of all outputs produced.", setOfData)
    print()
    print()
    goAgain = input("Now, do you want to go again, or are you done? y or n")

    if goAgain == "y":
        print("Ok!")
        print()
    else:
        print("Ok. See ya!")
        loop = False
    
        
