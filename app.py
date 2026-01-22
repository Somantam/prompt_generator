# app.py
import streamlit as st
import random
from datetime import datetime
from utils.data_manager import DataManager  # NEW

# Initialize data manager
data_manager = DataManager()

# Initialize session state with file loading
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'favorites' not in st.session_state:
    # Load favorites from file
    st.session_state.favorites = data_manager.load_favorites()
if 'current_prompt' not in st.session_state:
    st.session_state.current_prompt = None

# Chatbot class
class MuseBot:
    def __init__(self):
        self.name = "The Infinite Muse"
        self.characters = [
            "a retired spy who remembers too much",
            "an astronaut who hears colors",
            "a librarian who can read between the lines",
            "a ghost who doesn't know they're dead",
            "a clockmaker whose time runs differently",
            "a chef who cooks memories",
            "a detective who solves metaphysical crimes",
            "a gardener who grows emotions as plants"
        ]
        self.settings = [
            "in a city submerged underwater",
            "on a train that never stops",
            "in a library where books rewrite themselves",
            "at the edge of a black hole",
            "in a house with rooms that don't obey physics",
            "on an island that appears once every seven years",
            "in a theater that only shows forbidden plays",
            "inside a snow globe containing a universe"
        ]
        self.conflicts = [
            "they find a key that fits nothing",
            "time begins moving backwards",
            "they discover they're not who they thought",
            "gravity suddenly fails every hour",
            "they start speaking a language no one knows",
            "their reflection starts acting independently",
            "colors begin to have sounds and smells",
            "they receive letters from their future self"
        ]

    def generate_prompt(self, genre="any"):
        """Generate a writing prompt"""
        character = random.choice(self.characters)
        setting = random.choice(self.settings)
        conflict = random.choice(self.conflicts)
        
        # Add genre flavor
        genre_flavors = {
            "mystery": f"🔍 **Mystery:** {character} {setting}, but {conflict}. The clues don't add up.",
            "fantasy": f"✨ **Fantasy:** {character} {setting}, but {conflict}. Magic has unexpected costs.",
            "scifi": f"🚀 **Sci-Fi:** {character} {setting}, but {conflict}. Technology rebels against its creators.",
            "horror": f"👻 **Horror:** {character} {setting}, but {conflict}. The real monster was inside all along.",
            "noir": f"🌧️ **Noir:** {character} {setting}, but {conflict}. The rain washes away evidence, never guilt."
        }
        
        if genre in genre_flavors:
            prompt = genre_flavors[genre]
        else:
            prompt = f"📖 **Story Idea:** {character} {setting}, but {conflict}."
        
        # Create a prompt object
        prompt_obj = {
            "text": prompt,
            "character": character,
            "setting": setting,
            "conflict": conflict,
            "genre": genre if genre != "any" else "mixed",
            "time": datetime.now().strftime("%H:%M"),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "id": str(datetime.now().timestamp()),  # Unique ID
            "created_at": str(datetime.now())
        }
        
        st.session_state.current_prompt = prompt_obj
        return prompt_obj
    
    def add_twist(self):
        """Add a plot twist"""
        twists = [
            "Suddenly, they realize they've been dead the whole time.",
            "The mentor reveals they were the villain all along, but for understandable reasons.",
            "The magical artifact was never meant to be used; it was a warning.",
            "The spaceship isn't exploring new worlds; it's returning to a lost home.",
            "The detective discovers they're solving their own future crimes.",
            "The love interest is from a parallel universe where different choices were made.",
            "The monster was actually protecting everyone from something much worse.",
            "The treasure map leads not to gold, but to a terrible truth."
        ]
        return random.choice(twists)
    
    def explain_prompt(self):
        """Explain the current prompt"""
        if not st.session_state.current_prompt:
            return "No prompt to explain. Generate one first!"
        
        prompt = st.session_state.current_prompt
        explanations = [
            f"This prompt explores themes of **identity** and **reality** through {prompt['character']} in {prompt['setting']}.",
            f"At its core, this story is about confronting **{prompt['conflict'].split(' ')[-1] if ' ' in prompt['conflict'] else 'the unknown'}**.",
            f"The symbolism here points to **transformation** and **unexpected discoveries**.",
            f"This scenario challenges what we take for granted, asking what happens when **{prompt['conflict'].split(' but ')[-1] if ' but ' in prompt['conflict'] else 'reality bends'}**."
        ]
        return random.choice(explanations)

# Initialize bot
bot = MuseBot()

def save_prompt_to_file(prompt_obj):
    """Save prompt to file and update session state"""
    if prompt_obj:
        # Add save timestamp
        prompt_obj["saved_at"] = str(datetime.now())
        
        # Save to file
        success = data_manager.add_favorite(prompt_obj)
        
        if success:
            # Update session state from file (to ensure sync)
            st.session_state.favorites = data_manager.load_favorites()
            return True
    return False

def process_user_input(user_input):
    """Process user input and generate response"""
    user_input_lower = user_input.lower()
    
    # Add user message to conversation
    st.session_state.conversation.append({
        "role": "user",
        "content": user_input
    })
    
    # Generate response based on input
    if any(word in user_input_lower for word in ["hello", "hi", "hey"]):
        response = f"Hello! I'm {bot.name}, your creative writing assistant. Ready to tell a story?"
    
    elif any(word in user_input_lower for word in ["prompt", "idea", "story", "generate"]):
        # Extract genre
        genre = "any"
        if "mystery" in user_input_lower:
            genre = "mystery"
        elif "fantasy" in user_input_lower:
            genre = "fantasy"
        elif "scifi" in user_input_lower or "science fiction" in user_input_lower:
            genre = "scifi"
        elif "horror" in user_input_lower:
            genre = "horror"
        elif "noir" in user_input_lower:
            genre = "noir"
        
        prompt = bot.generate_prompt(genre)
        response = prompt["text"]
    
    elif any(word in user_input_lower for word in ["twist", "plot twist"]):
        twist = bot.add_twist()
        response = f"💫 **Plot Twist:** {twist}"
    
    elif any(word in user_input_lower for word in ["explain", "meaning", "symbolism"]):
        explanation = bot.explain_prompt()
        response = f"🔍 **Explanation:** {explanation}"
    
    elif any(word in user_input_lower for word in ["save", "favorite"]):
        if st.session_state.current_prompt:
            success = save_prompt_to_file(st.session_state.current_prompt)
            if success:
                response = "✅ Prompt saved to favorites (saved to file)!"
            else:
                response = "⚠️ Could not save prompt (might already be saved)."
        else:
            response = "No prompt to save. Generate one first!"
    
    elif any(word in user_input_lower for word in ["clear", "reset"]):
        st.session_state.conversation = []
        response = "🔄 Conversation cleared. Ready for new ideas!"
    
    elif any(word in user_input_lower for word in ["help", "commands"]):
        response = """
        **📚 Available Commands:**
        
        **Prompt Generation:**
        - "prompt" or "story idea" - Random prompt
        - "fantasy prompt" - Genre-specific
        - "mystery story" - Get a mystery
        
        **Enhancements:**
        - "add a twist" - Plot twist
        - "explain this" - Symbolic meaning
        - "save this" - Save to favorites file
        
        **Conversation:**
        - "hello" - Greet me
        - "clear chat" - Start fresh
        - "help" - This message
        
        **Tip:** Your favorites are saved in data/favorites.json!
        """
    
    else:
        # Creative conversational response
        responses = [
            f"I'm listening... '{user_input}' could be the seed of a wonderful story.",
            f"Interesting thought. '{user_input}' reminds me of stories waiting to be told.",
            f"Let's explore that idea. What story could bloom from '{user_input}'?",
            f"'{user_input}'... there's a fragment of something larger there. Shall we build on it?",
            f"I hear you. '{user_input}' carries echoes of other stories, other possibilities."
        ]
        response = random.choice(responses)
    
    # Add bot response to conversation
    st.session_state.conversation.append({
        "role": "assistant",
        "content": response
    })
    
    # Rerun to update display
    st.rerun()

# Streamlit app
def main():
    st.set_page_config(
        page_title="The Infinite Muse",
        page_icon="📖",
        layout="centered"
    )
    
    # Title
    st.title("📖 The Infinite Muse")
    st.markdown("*Your creative writing assistant with personality*")
    
    # Sidebar
    with st.sidebar:
        st.header("🎭 Creative Controls")
        
        # Genre selection
        genre = st.selectbox(
            "Choose a genre:",
            ["any", "mystery", "fantasy", "scifi", "horror", "noir"]
        )
        
        # Quick action buttons
        st.markdown("### Quick Actions")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✨ Generate", key="sidebar_generate", use_container_width=True):
                prompt = bot.generate_prompt(genre)
                st.session_state.conversation.append({
                    "role": "assistant",
                    "content": prompt["text"],
                    "type": "prompt"
                })
                st.rerun()
        with col2:
            if st.button("🔄 Clear Chat", key="sidebar_clear", use_container_width=True):
                st.session_state.conversation = []
                st.rerun()
        
        st.divider()
        
        # Stats
        st.subheader("📊 Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Prompts", len([m for m in st.session_state.conversation if m.get("type") == "prompt"]))
        with col2:
            st.metric("Favorites", len(st.session_state.favorites))
        
        # Export buttons
        st.markdown("### 💾 Export")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📤 JSON", key="export_json", use_container_width=True):
                export_data = data_manager.export_favorites("json")
                st.download_button(
                    label="Download JSON",
                    data=export_data,
                    file_name="writing_prompts.json",
                    mime="application/json",
                    key="download_json"
                )
        with col2:
            if st.button("📝 Text", key="export_text", use_container_width=True):
                export_data = data_manager.export_favorites("text")
                st.download_button(
                    label="Download Text",
                    data=export_data,
                    file_name="writing_prompts.txt",
                    mime="text/plain",
                    key="download_text"
                )
        
        # Favorites section
        if st.session_state.favorites:
            st.divider()
            st.subheader("💖 Saved Prompts")
            for i, fav in enumerate(st.session_state.favorites):
                # Create unique expander label
                expander_label = f"⭐ {fav.get('genre', 'Prompt')} - {fav.get('time', '')}"
                with st.expander(expander_label):
                    st.write(fav["text"])
                    st.caption(f"Saved: {fav.get('saved_at', 'Unknown')}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Use", key=f"use_fav_{i}"):
                            st.session_state.current_prompt = fav
                            st.session_state.conversation.append({
                                "role": "assistant",
                                "content": fav["text"],
                                "type": "prompt"
                            })
                            st.rerun()
                    with col2:
                        if st.button("Remove", key=f"remove_fav_{i}"):
                            # Remove from file
                            data_manager.remove_favorite(fav.get("id"))
                            # Update session state
                            st.session_state.favorites = data_manager.load_favorites()
                            st.success("Removed from favorites!")
                            st.rerun()
    
    # Main content area - Tabs
    tab1, tab2, tab3 = st.tabs(["💬 Chat", "📝 Current Prompt", "🎯 Quick Start"])
    
    with tab1:
        # Display conversation
        st.subheader("Your Creative Journey")
        
        if not st.session_state.conversation:
            st.info("👋 Welcome! Try generating a prompt or typing a message below.")
        
        # Display messages
        for i, msg in enumerate(st.session_state.conversation):
            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.write(f"**You:** {msg['content']}")
            else:  # assistant
                with st.chat_message("assistant"):
                    st.write(msg["content"])
                    
                    # Add action buttons for prompts
                    if msg.get("type") == "prompt":
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("💾 Save", key=f"save_{i}", use_container_width=True):
                                if st.session_state.current_prompt:
                                    success = save_prompt_to_file(st.session_state.current_prompt)
                                    if success:
                                        st.success("✅ Saved to file!")
                                    else:
                                        st.warning("⚠️ Already saved or error")
                                    st.rerun()
                        with col2:
                            if st.button("✨ Twist", key=f"twist_{i}", use_container_width=True):
                                twist = bot.add_twist()
                                st.session_state.conversation.append({
                                    "role": "assistant",
                                    "content": f"💫 **Plot Twist:** {twist}"
                                })
                                st.rerun()
                        with col3:
                            if st.button("🔍 Explain", key=f"explain_{i}", use_container_width=True):
                                explanation = bot.explain_prompt()
                                st.session_state.conversation.append({
                                    "role": "assistant",
                                    "content": f"🔍 **Explanation:** {explanation}"
                                })
                                st.rerun()
        
        # Chat input at the bottom
        st.divider()
        
        # Use a form for chat input
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input(
                "Type your message...",
                placeholder="Try: 'give me a mystery prompt' or 'explain this'",
                key="chat_input_field"
            )
            
            col1, col2 = st.columns([1, 3])
            with col1:
                submit = st.form_submit_button("Send", type="primary", use_container_width=True)
        
        # Process input when form is submitted
        if submit and user_input:
            process_user_input(user_input)
    
    with tab2:
        # Current prompt details
        st.subheader("📝 Current Prompt Details")
        
        if st.session_state.current_prompt:
            prompt = st.session_state.current_prompt
            
            # Display prompt
            st.write(f"### {prompt['text']}")
            
            st.divider()
            
            # Metadata
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Genre", prompt['genre'].capitalize())
            with col2:
                st.metric("Time", prompt['time'])
            with col3:
                st.metric("Date", prompt['date'])
            
            st.divider()
            
            # Components breakdown
            st.subheader("📖 Story Components")
            st.info(f"**Character:** {prompt['character']}")
            st.info(f"**Setting:** {prompt['setting']}")
            st.info(f"**Conflict:** {prompt['conflict']}")
            
            st.divider()
            
            # Check if already saved
            is_saved = any(fav.get("text") == prompt["text"] for fav in st.session_state.favorites)
            
            if is_saved:
                st.success("✅ This prompt is already saved in your favorites!")
            else:
                # Save button
                if st.button("💾 Save to Favorites", key="save_current", use_container_width=True):
                    success = save_prompt_to_file(prompt)
                    if success:
                        st.success("✅ Saved to favorites file!")
                        st.rerun()
                    else:
                        st.warning("⚠️ Could not save prompt")
            
            st.divider()
            
            # Action buttons
            st.subheader("⚡ Actions")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("✨ Add Twist", key="current_twist", use_container_width=True):
                    twist = bot.add_twist()
                    st.session_state.conversation.append({
                        "role": "assistant",
                        "content": f"💫 **Plot Twist:** {twist}"
                    })
                    st.rerun()
            with col2:
                if st.button("🔄 New Prompt", key="current_new", use_container_width=True):
                    new_prompt = bot.generate_prompt(prompt['genre'])
                    st.session_state.conversation.append({
                        "role": "assistant",
                        "content": new_prompt["text"],
                        "type": "prompt"
                    })
                    st.rerun()
            with col3:
                # Export single prompt
                export_text = f"""Prompt: {prompt['text']}

Character: {prompt['character']}
Setting: {prompt['setting']}
Conflict: {prompt['conflict']}
Genre: {prompt['genre']}
Generated: {prompt['date']} at {prompt['time']}

Happy writing! ✨"""
                st.download_button(
                    label="📤 Export",
                    data=export_text,
                    file_name=f"writing_prompt_{prompt['date']}.txt",
                    mime="text/plain",
                    key="download_current",
                    use_container_width=True
                )
        else:
            st.info("No current prompt. Generate one in the Chat tab!")
    
    with tab3:
        # Quick start guide
        st.subheader("🚀 Get Started Quickly")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🎭 Quick Prompts")
            if st.button("Mystery Prompt", key="quick_mystery", use_container_width=True):
                process_user_input("mystery prompt")
            if st.button("Fantasy Prompt", key="quick_fantasy", use_container_width=True):
                process_user_input("fantasy prompt")
            if st.button("Sci-Fi Prompt", key="quick_scifi", use_container_width=True):
                process_user_input("sci-fi prompt")
        
        with col2:
            st.markdown("### ✨ Enhancements")
            if st.button("Add a Twist", key="quick_twist", use_container_width=True):
                process_user_input("add twist")
            if st.button("Explain Current", key="quick_explain", use_container_width=True):
                process_user_input("explain this")
            if st.button("Save Prompt", key="quick_save", use_container_width=True):
                process_user_input("save this")
        
        with col3:
            st.markdown("### 💬 Conversation")
            if st.button("Say Hello", key="quick_hello", use_container_width=True):
                process_user_input("hello")
            if st.button("Get Help", key="quick_help", use_container_width=True):
                process_user_input("help")
            if st.button("Clear Chat", key="quick_clear", use_container_width=True):
                process_user_input("clear chat")
        
        st.divider()
        
        # File location info
        st.markdown("### 💾 Where Your Data is Saved")
        st.info(f"""
        **Your saved prompts are stored in:** `data/favorites.json`
        
        **Features:**
        - ✅ Prompts persist between app restarts
        - ✅ Can export all prompts as JSON or text
        - ✅ Can remove prompts you don't want
        - ✅ Each prompt has a unique ID and timestamp
        
        **Location on your computer:**
        ```
        {data_manager.favorites_file}
        ```
        """)

if __name__ == "__main__":
    main()