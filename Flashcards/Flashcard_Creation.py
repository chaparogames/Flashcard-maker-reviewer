import json
flashcards = []

#Friendly welcome message asking for input on creation/practice/exiting program
def welcome():
    print("="*30)
    print("Welcome to the flashcard application!")
    print("You can make flashcards to help you study!")
    
def main_menu():
    width = 30
    menu = (
        "\n" + "="*width +
        "\n" + "Main Menu".center(width) +
        "\n" + "="*width +
        "\n1. Create flashcards\n2. Study flashcards\n3. View all cards\n4. Exit\n" +
        "-"*width +
        "\nWhere would you like to start? (Enter 1-4): "
    )
    return menu

#Defines the front and back of the flashcard with user input
def front_flashcard():
    question = input("What's on the front of the card? (You'll see this side first): ")
    return question

def back_flashcard():
    card_answer = input("What's on the back of the card? (You'll see this side second): ")
    return card_answer

#Saves/Loads flashcards for later use
def save_flashcard(filename = "flashcards.json"):
    with open(filename, "w") as f:
        json.dump(flashcards, f)

def load_flashcards(filename = "flashcards.json"):
    with open(filename, "r") as f:
        return json.load(f)

def create_flashcard():
    print("Entering flashcard creation. Type 'q' at any prompt to stop creating cards.")
    while True:
       front = input("What's on the front of the card? (You'll see this side first): ")
       if front.lower() == 'q':
           print("Exiting flashcard creation.")
           break
       back = input("What's on the back of the card? (You'll see this side second): ")
       if back.lower() == 'q':
           print("Exiting flashcard creation.")
           break
       print("Your card has been created!")

       from Flashcards.Flashcard_Creation import flashcards, save_flashcard
       flashcard = {"front": front, "back": back}
       flashcards.append(flashcard)
       save_flashcard()
       print("Card saved! Add another or type 'q' to quit.")