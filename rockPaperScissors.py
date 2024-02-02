import random

print("Time to play rock, paper scissors!")

loop = True
while loop == True:
    decisions = {1:'rock', 2:'paper', 3:'scissors'}
    compDec = decisions[random.randint(1, 3)]
    rps = input("Rock, paper, or scissors? 1, 2, or 3.")
    humanDec = decisions[int(rps)]
    
    responses = ["Paper covers rock.", "Rock smashes scissors.", "Scissors cuts paper."]
    
    if humanDec == 'rock' and compDec == 'paper':
        print(responses[0], "You lose.")
    elif humanDec == 'rock' and compDec == 'scissors':
        print(responses[1], "You win!")
    elif humanDec == compDec:
        print("It's a tie. No one wins.")
    elif humanDec == 'paper' and compDec == 'scissors':
        print(responses[2], "You lose.")
    elif humanDec == 'paper' and compDec == 'rock':
        print(responses[0], "You win!")
    elif humanDec == 'scissors' and compDec == 'paper':
        print(responses[2], "You win!")
    elif humanDec == 'scissors' and compDec == 'rock':
        print(responses[1], "You lose.")
    
    goAgain = input("Wanna play again? y or n")
    if goAgain == 'y':
        print("Ok.")
        print()
    else:
        print("Ok. See ya later!")
        print()
        loop = False
        
        
        