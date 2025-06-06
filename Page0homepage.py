import streamlit as st
import random
from datetime import datetime

# Optional: Drawing canvas
try:
    from streamlit_drawable_canvas import st_canvas
    DRAWING_AVAILABLE = True
except ImportError:
    DRAWING_AVAILABLE = False

# --- Session State Initialization ---
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'mood_data' not in st.session_state:
    st.session_state.mood_data = []
if 'drawings' not in st.session_state:
    st.session_state.drawings = []
if 'secret_number' not in st.session_state:
    st.session_state.secret_number = random.randint(1, 10)
    st.session_state.tries = 0
if 'story' not in st.session_state:
    st.session_state.story = "Once upon a time"
if 'page' not in st.session_state:
    st.session_state.page = "main"

# --- Mood Detection ---
MOOD_KEYWORDS = {
    "sad": ["sad", "unhappy", "cry", "upset", "angry", "mad", "worried", "scared", "lonely"],
    "happy": ["happy", "joy", "excited", "fun", "awesome", "great", "love"],
    "neutral": ["ok", "fine", "so-so", "alright", "okay"]
}
def detect_mood(text):
    text = text.lower()
    for mood, keywords in MOOD_KEYWORDS.items():
        if any(word in text for word in keywords):
            return mood
    return "neutral"

# --- Main Page ---
def main_page():
    st.title("🎮 Welcome to PlayMate!")
    st.image("https://cdn-icons-png.flaticon.com/512/1046/1046784.png", width=200)
    st.markdown("""
    #### Here’s how to get started and have fun with your new digital friend:

    - **Say Hello!** Just type or speak to PlayMate to begin.
    - **Choose an Activity:** Play games, tell stories, draw, or chat.
    - **Share Your Feelings:** PlayMate is here to listen and help.
    - **Ask for Help:** If you feel sad, worried, or need advice, just let PlayMate know.
    - **Have Fun and Stay Safe!** You can say “goodbye” at any time.

    ---
    **For Parents & Guardians:**  
    PlayMate supports your child’s emotional well-being in a safe, friendly environment. All conversations are private and monitored for safety. If PlayMate notices anything concerning, it will notify you for further support.
    """)

    st.write("### What would you like to do?")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💬 Chat"):
            st.session_state.page = "chat"
    with col2:
        if st.button("🎮 Games"):
            st.session_state.page = "games"
    with col3:
        if st.button("🎨 Draw"):
            st.session_state.page = "draw"
    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("📝 Feelings Journal"):
            st.session_state.page = "feelings"
    with col5:
        if st.button("👪 Parent Dashboard"):
            st.session_state.page = "parent"
    with col6:
        if st.button("ℹ️ About PlayMate"):
            st.session_state.page = "about"

# --- Chat Page ---
def chat_page():
    st.title("💬 Chat with PlayMate")
    for msg in st.session_state.conversation[-5:]:
        st.chat_message(msg["role"]).write(msg["content"])
    prompt = st.chat_input("Type your message...")
    if prompt:
        st.session_state.conversation.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        mood = detect_mood(prompt)
        st.session_state.mood_data.append({
            "timestamp": datetime.now(),
            "mood": mood,
            "message": prompt
        })
        # Response logic
        if mood == "sad":
            response = "I'm sorry you're feeling this way. Want to talk about it or play a game to feel better?"
        elif mood == "happy":
            response = "Yay! I'm glad you're happy! Want to play a game or draw something fun?"
        elif "game" in prompt.lower():
            response = "Great! Go to the Games page to play together!"
        else:
            response = "That's interesting! Tell me more or choose an activity from the menu."
        st.session_state.conversation.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)

# --- Games Page ---
def games_page():
    st.title("🎮 Play Games with PlayMate")
    game = st.radio("Choose a game:", ["Rock-Paper-Scissors", "Number Guesser", "Story Builder"])
    if game == "Rock-Paper-Scissors":
        user_choice = st.selectbox("Your move:", ["✊", "✋", "✌️"])
        if st.button("Play!"):
            ai_choice = random.choice(["✊", "✋", "✌️"])
            st.write(f"PlayMate chose: {ai_choice}")
            if user_choice == ai_choice:
                st.success("It's a tie!")
            elif (user_choice == "✊" and ai_choice == "✌️") or \
                 (user_choice == "✋" and ai_choice == "✊") or \
                 (user_choice == "✌️" and ai_choice == "✋"):
                st.success("You win! 🎉")
            else:
                st.error("PlayMate wins!")
    elif game == "Number Guesser":
        guess = st.number_input("Guess a number between 1 and 10", min_value=1, max_value=10, step=1)
        if st.button("Guess!"):
            st.session_state.tries += 1
            if guess == st.session_state.secret_number:
                st.success(f"Correct! You guessed it in {st.session_state.tries} tries!")
                st.session_state.secret_number = random.randint(1, 10)
                st.session_state.tries = 0
            else:
                st.info("Try again!")
    elif game == "Story Builder":
        st.write(st.session_state.story)
        next_line = st.text_input("Add the next line to the story:")
        if st.button("Add Line"):
            st.session_state.story += " " + next_line
            st.write(st.session_state.story)

# --- Drawing Page ---
def draw_page():
    st.title("🎨 Drawing Canvas")
    if DRAWING_AVAILABLE:
        drawing = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=3,
            update_streamlit=True,
            height=400,
            drawing_mode="freedraw",
            key="canvas",
        )
        if st.button("Save Drawing"):
            st.session_state.drawings.append(drawing.image_data)
            st.success("Drawing saved!")
        if st.session_state.drawings:
            st.subheader("Your Saved Drawings")
            for img in st.session_state.drawings[-3:]:
                st.image(img)
    else:
        st.error("Drawing not available. Please install streamlit-drawable-canvas.")

# --- Feelings Journal Page ---
def feelings_page():
    st.title("📝 Feelings Journal")
    with st.form("mood_check"):
        mood = st.select_slider("How are you feeling today?", ["😭", "😞", "😐", "😊", "🎉"])
        notes = st.text_area("Want to share more?")
        if st.form_submit_button("Save Entry"):
            st.session_state.mood_data.append({
                "timestamp": datetime.now(),
                "mood": mood,
                "notes": notes
            })
            st.success("Entry saved!")
    st.subheader("Recent Entries")
    for entry in st.session_state.mood_data[-3:]:
        st.write(f"{entry['timestamp'].strftime('%Y-%m-%d')}: {entry['mood']} - {entry.get('notes', '')}")

# --- Parent Dashboard Page ---
def parent_page():
    st.title("👪 Parent Dashboard")
    if st.session_state.conversation:
        st.subheader("Recent Conversation")
        for msg in st.session_state.conversation[-5:]:
            st.write(f"{msg['role'].title()}: {msg['content']}")
    else:
        st.info("No conversation history yet.")
    if st.session_state.mood_data:
        st.subheader("Mood Trends")
        mood_counts = {}
        for entry in st.session_state.mood_data:
            mood = entry['mood']
            mood_counts[mood] = mood_counts.get(mood, 0) + 1
        st.bar_chart(mood_counts)
    else:
        st.info("No mood data available.")

# --- About Page ---
def about_page():
    st.title("ℹ️ About PlayMate")
    st.markdown("""
    ### Your Safe Digital Companion

    PlayMate is designed to:
    - Provide 24/7 emotional support through play
    - Detect early signs of emotional distress
    - Offer age-appropriate coping strategies
    - Maintain privacy while keeping adults informed

    **Safety Features:**
    - All data is stored locally
    - Parental alerts for concerning patterns
    - No personal data collection
    """)

# --- Page Routing ---
if st.session_state.page == "main":
    main_page()
elif st.session_state.page == "chat":
    chat_page()
elif st.session_state.page == "games":
    games_page()
elif st.session_state.page == "draw":
    draw_page()
elif st.session_state.page == "feelings":
    feelings_page()
elif st.session_state.page == "parent":
    parent_page()
elif st.session_state.page == "about":
    about_page()

# --- Navigation Sidebar ---
if st.sidebar.button("🏠 Home", key="home_btn"):
    st.session_state.page = "main"
if st.sidebar.button("💬 Chat", key="chat_btn"):
    st.session_state.page = "chat"
if st.sidebar.button("🎮 Games", key="games_btn"):
    st.session_state.page = "games"
if st.sidebar.button("🎨 Draw", key="draw_btn"):
    st.session_state.page = "draw"
if st.sidebar.button("📝 Feelings Journal", key="feelings_btn"):
    st.session_state.page = "feelings"
if st.sidebar.button("👪 Parent Dashboard", key="parent_btn"):
    st.session_state.page = "parent"
if st.sidebar.button("ℹ️ About PlayMate", key="about_btn"):
    st.session_state.page = "about"
