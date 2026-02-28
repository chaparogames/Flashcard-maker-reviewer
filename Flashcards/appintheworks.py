import streamlit as st
import json
import uuid

st.set_page_config(page_title ="Flashcard Reviewer", layout="centered")

def load_flashcards(filename="flashcards.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    
def save_flashcard(cards, filename="flashcards.json"):
    with open(filename, "w") as f:
        json.dump(cards, f)

def ensure_card_ids(cards):
    changed = False
    for card in cards:
        if "id" not in card:
            card["id"] = str(uuid.uuid4())
            changed = True
    if changed:
        save_flashcard(cards)
    return cards

if "page" not in st.session_state:
    st.session_state.page = "home"
    cards = load_flashcards()
    ensure_card_ids(cards)
if "Current_card_index" not in st.session_state:
    st.session_state.current_card_index = 0
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

st.title("Flashcard Reviewer")

# Home Page
if st.session_state.page == "home":
    st.subheader("Welcome to the Flashcard Application!")
    st.write("You can create flashcards to help you study!")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("Create", use_container_width=True):
            st.session_state.page = "create"
            st.rerun()

    with col2:
        if st.button("Study", use_container_width=True):
            st.session_state.page = "study"
            st.rerun()

    with col3:
        if st.button("View All", use_container_width=True):
            st.session_state.page = "view"
            st.rerun()

    with col4:
        if st.button("Edit", use_container_width=True):
            st.session_state.page = "edit"
            st.rerun()

    with col5:
        if st.button("Exit", use_container_width=True):
            st.info("Thanks for studying! Goodbye!")

# Create Flashcards Page
elif st.session_state.page == "create":
    st.subheader("Create a New Flashcard")

    category = st.text_input("Category (e.g., Math, History, Science):")
    front = st.text_input("Front of the card (Question):")
    back = st.text_input("Back of the card (Answer):")
    hints = st.text_input("Hint (optional):")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Save Flashcard", use_container_width=True):
            if category and front and back:
                new_card = {
                    "id": str(uuid.uuid4()),
                    "Category": category,
                    "front": front,
                    "back": back,
                    "hints": hints if hints else None
                }
                cards = load_flashcards()
                cards.append(new_card)
                save_flashcard(cards)
                st.success("Flashcard saved successfully!")
            else:
                st.error("Please fill in all required fields (Category, Front, Back):")
    with col2:
        if st.button("Back to Menu", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

# Study Flashcards Page
elif st.session_state.page == "study":
    cards = load_flashcards()

    if not cards:
        st.error("No flashcards found. Please create some first!")
        if st.button("Back to Menu"):
            st.session_state.page = "home"
            st.rerun()
    else:
        st.subheader("Study Your Flashcards")

        # Study by category or all
        study_type = st.radio("How would you like to study?", ["All Flashcards", "By Category"], key="study_type")

        if study_type == "By Category":
            categories = list(set(card['Category'] for card in cards))
            selected_category = st.selectbox("Select a category to study:", categories, key="selected_cat")
            selected_cards = [card for card in cards if card.get('Category', 'Unknown') == selected_category]
        else:
            selected_cards = cards
            selected_category = "All"
        
        if not selected_cards:
            st.warning("No flashcards found for the selected category. Please create some first!")
        else:
            st.write(f"Total Cards: {len(selected_cards)}")
            # Get current card
            if st.session_state.current_card_index >= len(selected_cards):
                st.session_state.current_card_index = 0

            current_card = selected_cards[st.session_state.current_card_index]

            # Display current card
            st.write(" ")
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Card {st.session_state.current_card_index + 1} of {len(selected_cards)}**")
            with col2:
                st.write(f"**Category:** {current_card['Category']}")

            st.write("---")

            # Front of the card
            st.subheader("Front (Question):")
            st.write(current_card['front'])

            # Show hitns if available
            if current_card.get('hints'):
                with st.expander("Show Hint"):
                    st.write(current_card['hints'])
            
            st.write(" ")
            
            # Show answer button
            if st.button("Show Answer"):
                st.session_state.show_answer = True
            
            if st.session_state.show_answer:
                st.subheader("Back (Answer):")
                st.write(current_card['back'])
                st.write(" ")

                # Row 1: 3 buttons
                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button("Mark as Known (Strong)"):
                        st.success("Great job! Keep it up!")
                        st.session_state.current_card_index += 1
                        st.session_state.show_answer = False
                        st.rerun()
                
                with col2:
                    if st.button("Mark as Unknown (Weak)"):
                        st.session_state.current_card_index += 1
                        st.session_state.show_answer = False
                        st.rerun()
                
                with col3:
                    if st.button("Mark as Unsure (Medium)"):
                        st.session_state.current_card_index += 1
                        st.session_state.show_answer = False
                        st.rerun()

                st.write("---")

                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button("Previous Card"):
                        if st.session_state.current_card_index > 0:
                            st.session_state.current_card_index -= 1
                        st.session_state.show_answer = False
                        st.rerun()

                with col2:
                    if st.button("Next Card"):
                        st.session_state.current_card_index += 1
                        st.session_state.show_answer = False
                        st.rerun()

                with col3:
                    if st.button("Reset Progress"):
                        st.session_state.current_card_index = 0
                        st.session_state.show_answer = False
                        st.rerun()

            st.write("---")

            # Navigation Buttons
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Back to Menu"):
                    st.session_state.page = "home"
                    st.session_state.current_card_index = 0
                    st.session_state.show_answer = False
                    st.rerun()
            
# View/Edit All Flashcards (unified page)
elif st.session_state.page == "view" or st.session_state.page == "edit":
    cards = load_flashcards()

    st.subheader("All Flashcards")

    if not cards:
        st.info("No flashcards yet. Create some to get started!")
    else:
        st.write(f"Total flashcards: {len(cards)}")
        
        # Toggle between grouped and flat view
        group_by_category = st.toggle("Group by category", value=True)
        
        if group_by_category:
            categories = sorted(set(card.get('Category', 'Uncategorized') for card in cards))
            
            for category in categories:
                with st.expander(f"📚 {category}", expanded=True):
                    category_cards = [c for c in cards if c.get('Category', 'Uncategorized') == category]
                    
                    for index, card in enumerate(category_cards, 1):
                        st.write(f"**Card {index}**")
                        st.write(f"**Category:** {card.get('Category', 'Uncategorized')}")
                        st.write(f"**Front:** {card.get('front', '')}")
                        st.write(f"**Back:** {card.get('back', '')}")
                        if card.get('hints'):
                            st.write(f"**Hints:** {card['hints']}")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Edit cards
                            with st.form(key=f"edit_form_{card['id']}"):
                                new_category = st.text_input("Category", value=card.get('Category', ''), key=f"cat_{card['id']}")
                                new_front = st.text_area("Front", value=card.get('front', ''), key=f"front_{card['id']}")
                                new_back = st.text_area("Back", value=card.get('back', ''), key=f"back_{card['id']}")
                                new_hints = st.text_input("Hints (optional)", value=card.get('hints') or '', key=f"hints_{card['id']}")
                                submitted = st.form_submit_button("Save edits")
                            
                            if submitted:
                                all_cards = load_flashcards()
                                for c in all_cards:
                                    if c.get('id') == card['id']:
                                        c['Category'] = new_category
                                        c['front'] = new_front
                                        c['back'] = new_back
                                        c['hints'] = new_hints if new_hints else None
                                        break
                                save_flashcard(all_cards)
                                st.success("Card updated!")
                                st.rerun()
                        
                        with col2:
                            if st.button("Delete", key=f"delete_{card['id']}", type="secondary"):
                                all_cards = load_flashcards()
                                all_cards = [c for c in all_cards if c.get('id') != card['id']]
                                save_flashcard(all_cards)
                                st.warning("Card deleted!")
                                st.rerun()
                        
                        st.write("---")
        else:
            # Flat view (all cards in one list)
            for index, card in enumerate(cards, 1):
                st.write(f"**Card {index}**")
                st.write(f"**Category:** {card.get('Category', 'Uncategorized')}")
                st.write(f"**Front:** {card.get('front', '')}")
                st.write(f"**Back:** {card.get('back', '')}")
                if card.get('hints'):
                    st.write(f"**Hints:** {card['hints']}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Edit cards
                    with st.form(key=f"edit_form_{card['id']}"):
                        new_category = st.text_input("Category", value=card.get('Category', ''), key=f"cat_{card['id']}")
                        new_front = st.text_area("Front", value=card.get('front', ''), key=f"front_{card['id']}")
                        new_back = st.text_area("Back", value=card.get('back', ''), key=f"back_{card['id']}")
                        new_hints = st.text_input("Hints (optional)", value=card.get('hints') or '', key=f"hints_{card['id']}")
                        submitted = st.form_submit_button("Save edits")
                    
                    if submitted:
                        all_cards = load_flashcards()
                        for cards in all_cards:
                            if cards.get('id') == card['id']:
                                cards['Category'] = new_category
                                cards['front'] = new_front
                                cards['back'] = new_back
                                cards['hints'] = new_hints if new_hints else None
                                break
                        save_flashcard(all_cards)
                        st.success("Card updated!")
                        st.rerun()
                
                with col2:
                    if st.button("Delete", key=f"delete_{card['id']}", type="secondary"):
                        all_cards = load_flashcards()
                        all_cards = [c for c in all_cards if c.get('id') != card['id']]
                        save_flashcard(all_cards)
                        st.warning("Card deleted!")
                        st.rerun()
                
                st.write("---")
    
    if st.button("Back to Menu"):
        st.session_state.page = "home"
        st.rerun()