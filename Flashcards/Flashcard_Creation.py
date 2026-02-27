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

#Defines the category, front, and back of the flashcard with user input
def flashcard_category():
    category = input("What category would you like to create flashcards for? (e.g., Math, History, Science, etc.): ")
    return category

def front_flashcard():
    question = input("What's on the front of the card? (You'll see this side first): ")
    return question

def back_flashcard():
    card_answer = input("What's on the back of the card? (You'll see this side second): ")
    return card_answer

#Should the user want to add hints or edit their flashcard these function will  allow that
def hints_flashcard():
    hints = input("Do you want to add a hint to this card? (y/n): ").lower()
    if hints == 'y':
        hint_text = input("Enter your hint: ")
        return hint_text
    else:
        return None
    
def edit_flashcard(card):
    edit = input("Do you want to edit this card? (y/n): ").lower() #Asks user if they want to edit the current card
    if edit == 'y': #If yes, shows current card details and asks which field to edit
        print(f"""
              {'-'*30}
              Current card details:
              category: {card.get('Category', 'N/A')}
              front: {card.get('front', 'N/A')}
              back: {card.get('back', 'N/A')}
              hints: {card.get('hints', 'N/A')}
             {'-'*30}
              """)
        while True: #Keeps asking which field to edit until user chooses to cancel or go to main menu
            edit_field = input("Which field do you want to edit? (Category, Front, Back, Hints, All, or Cancel): ").lower()
            if edit_field == 'category':
                card['Category'] = input("Enter new category: ").strip()
            elif edit_field == 'front':
              card['front'] = input("Enter new front text: ").strip()
            elif edit_field == 'back':
              card['back'] = input("Enter new back text: ").strip()
            elif edit_field == 'hints':
                add_hint = input("Do you want to add or change the hint? (y/n): ").lower()
                if add_hint == 'y':
                    card['hints'] = input("Enter a new hint: ").strip()
                elif add_hint == 'n':
                    return card.get('hints', None)
                else:
                    print("Invalid input. No changes made to hints.")
            elif edit_field == 'all':
                card['Category'] = input("Enter new category: ").strip()
                card['front'] = input("Enter new front text: ").strip()
                card['back'] = input("Enter new back text: ").strip()
                card['hints'] = input("Enter new hint text (or leave blank): ").strip()
            if edit_field == 'cancel':
                action = input("Edit cancelled. Return to the main menu, continue creating cards, or make another change? (return/continue/edit): ").lower()
                if action == 'return':
                    print("Returning to main menu.")
                    return 'return'
                if action == 'continue':
                    print("Continuing with current card details.")
                    return card
                elif action == 'cancel':
                    return 'cancel'
            else:
                continue

#Saves/Loads flashcards for later use
def save_flashcard(filename = "flashcards.json"):
    with open(filename, "w") as f:
        json.dump(flashcards, f)

def load_flashcards(filename = "flashcards.json"):
    with open(filename, "r") as f:
        return json.load(f)

def create_flashcard():
    print("Entering flashcard creation. Type 'q' at any prompt to stop creating cards.")
    category = flashcard_category()
    if category and category.lower() == 'q':
        print("Exiting flashcard creation.")
        return
    while True:
        front = front_flashcard()
        if front and front.lower() == 'q':
            print("Exiting flashcard creation.")
            break
        back = back_flashcard()
        if back and back.lower() == 'q':
           print("Exiting flashcard creation.")
           break
        hints = hints_flashcard()
        if hints and isinstance(hints, str) and hints.lower() == 'q':
           print("Exiting flashcard creation.")
           break
        edit = edit_flashcard({"Category": category, "front": front, "back": back, "hints": hints})
        if edit and isinstance(edit, str) and edit.lower() in ('return', 'q'):
            print("Exiting flashcard editor.")
            break

        from Flashcard_Creation import flashcards, save_flashcard
        flashcard = {"Category": category, "front": front, "back": back, "hints": hints}
        flashcards.append(flashcard)
        save_flashcard()
        print("Card saved! Add another or type 'q' to quit.")
        print("-"*30)