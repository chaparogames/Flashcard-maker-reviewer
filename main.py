from Flashcard_Creation import welcome, load_flashcards, create_flashcard, main_menu
import os

welcome()

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    choice = input(main_menu())
    if choice == "1":
        create_flashcard()
    elif choice == "2":
        flashcards = load_flashcards(filename="flashcards.json")
        if not flashcards:
            print("No flashcards found. Please create some first.")
        else:
            print("You're flashcards:")
            review_later_cards = []
            for card in flashcards:
                print("-"*20)
                print(f"Front: {card['front']}")
                input("Your answer?: ")
                print(f"Back: {card['back']}")
                while True:
                    user_input = input("Did you get it right? (y/n): ").lower()
                    if user_input == 'y':
                        print("Great job! Keep it up!")
                        break
                    elif user_input == 'n':
                        print("Don't worry, keep practicing and you'll get it!")
                        review_later = input("Do you want to review this card later? (y/n): ").lower()
                        if review_later == 'y':
                            review_later_cards.append(card)
                            print("This card will be reviewed later.")
                        else:
                            print("Moving on to the next card.")
                        break
                    else:
                        print("Invalid input, please enter 'y' or 'n'.")
                print("-"*20)
            if review_later_cards:
                print("\nYou marked some cards to review later.")
                review_choice = input("Would you like to review them now? (y/n): ").lower()
                if review_choice == 'y':
                    print("\nReviewing missed cards:")
                    for idx, card in enumerate(review_later_cards):
                        print("-"*20)
                        print(f"Front: {card['front']}")
                        input("Your answer?: ")
                        print(f"Back: {card['back']}")
                        print("-"*20)
                        if idx < len(review_later_cards) - 1:
                            input("Press ENTER to continue to the next card...")
                        else:
                            input("Press ENTER to return to the main menu...")
                
    elif choice == "3":
        flashcards = load_flashcards(filename="flashcards.json")
        if not flashcards:
            print("No flashcards found. Please create some first.")
        else:
            print("-"*20 +
            "\nAll your flashcards:"
            )
            for card in flashcards:
                print(f"Front: {card['front']}| Back: {card['back']}")
        input(("-"*20) + "\nPress ENTER to return to the main menu...")
    elif choice == "4":
        print("Thanks for studying with us! Goodbye!")
        break
