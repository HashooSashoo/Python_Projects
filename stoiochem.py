import math

#This is a Python program that can give you stoiochemical information

'''
Example Problem:
How many grams of Potassium Phosphate can be produced with water by the reaction of 15.00g of tetraphosphorus decoxide and 15.00g of potassium hydroxide?
Which is the limiting reaction and which is in excess?
How much of the excess reaction is consumed in the reaction?

Variables:
    Substance One - Given
    Substance Two - Given
    Substance Produced - Given
    Moles of Substance One - In Equation
    Moles of Substance Two - In Equation
    Moles of Substance Produced - In Equation
'''
option = int(input("What would you like to do? \n1. Simple Gram of 1 sub to Gram of another\n2. Complicated Excess and Limiting Shit"))
if option == 2:
    nameSub1 = input("What is the name of substance 1?")
    massSub1 = float(input("What is mass of substance 1?"))
    amuSub1 = float(input("AMU of substance 1?"))
    molSub1 = int(input("Moles of substance 1?"))
    nameSub2 = input("What is the name of substance 2?")
    massSub2 = float(input("What is mass of substance 2?"))
    amuSub2 = float(input("AMU of substance 2?"))
    molSub2 = int(input("Moles of substance 2?"))
    nameSubProd = input("What is the name of the produced substance?")
    amuSubProd = float(input("What is the AMU of the substance produced?"))
    molSubProd = int(input("And the moles?"))
    print()
    print("******************************************************************************")
    print()
    massSubProd1 = (massSub1*(1/amuSub1)*(molSubProd/molSub1)*amuSubProd)
    massSubProd2 = (massSub2*(1/amuSub2)*(molSubProd/molSub2)*amuSubProd)

    if massSubProd1 > massSubProd2:
        print(nameSub1, "is in excess, producing a mass of", str(round(massSubProd1, 2)) + ".")
        print(nameSub2, "is the limiting reactant, producing a mass of", str(round(massSubProd2, 2)) + ".")
        print()
        print("The most amount of", nameSubProd, "that could be produced is", massSubProd2 + ".")
        print()
        sub1UsedInReac = (massSub2*(1/amuSub2)*(molSub1/molSub2)*amuSub1)
        amountOfSubLeft1 = (massSub1-sub1UsedInReac)
        print("The theoretical amount of", nameSub1, "used in the reaction is", str(round(sub1UsedInReac, 2)), "grams.")
        print("The amount of", nameSub1, "left unused is", str(round(amountOfSubLeft1, 2)) + ".")
        
    else:
        print(nameSub2, "is in excess, producing a mass of", str(round(massSubProd2, 2)) + ".")
        print(nameSub1, "is the limiting reactant, producing a mass of", str(round(massSubProd1, 2)) + ".")
        print()
        sub2UsedInReac = (massSub1*(1/amuSub1)*(molSub2/molSub1)*amuSub2)
        amountOfSubLeft2 = (massSub2-sub2UsedInReac)
        print("The theoretical amount of", nameSub2, "used in the reaction is", str(round(sub2UsedInReac, 2)), "grams.")
        print("The amount of", nameSub2, "left is", str(round(amountOfSubLeft2, 2)) + ".")
    
elif option == 1:
    nameSub1 = input("What is the name of substance 1?")
    massSub1 = float(input("What is mass of substance 1?"))
    amuSub1 = float(input("AMU of substance 1?"))
    molSub1 = int(input("Moles of substance 1?"))
    nameSub2 = input("What is the name of substance 2?")
    massSub2 = float(input("What is mass of substance 2?"))
    amuSub2 = float(input("AMU of substance 2?"))
    molSub2 = int(input("Moles of substance 2?"))
    
    sub2UsedInReac = (massSub1*(1/amuSub1)*(molSub2/molSub1)*amuSub2)
    
    print("****************************************************")
    print()
    print("You gave", massSub1, "grams in the calculation...")
    print()
    print("You ended up getting", sub2UsedInReac, "grams of the second substance.")





















