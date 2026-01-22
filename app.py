# app.py
import streamlit as st
import random
from datetime import datetime
from utils.data_manager import DataManager 
from muse_bot import MuseBot  # Importing the separated class

# Initialize data manager
data_manager = DataManager()

# Initialize session state
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'favorites' not in st.session_state:
    st.session_state.favorites = data_manager.load_favorites()
if 'current_prompt' not in st.session_state:
    st.session_state.current_prompt = None

# Initialize bot
bot = MuseBot()

def save_prompt_to_file(prompt_obj):
    """Save prompt to file and update session state"""
    if prompt_obj:
        prompt_obj["saved_at"] = str(datetime.now())
        success = data_manager.add_favorite(prompt_obj)
        if success:
            st.session_state.favorites = data_manager.load_favorites()
            return True
    return False

def process_user_input(user_input):
    """Process user input and generate response"""
    user_input_lower = user_input.lower()
    
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
        for g in ["mystery", "fantasy", "scifi", "horror", "noir"]:
            if g in user_input_lower:
                genre = g
                break
        
        prompt = bot.generate_prompt(genre)
        st.session_state.current_prompt = prompt
        response = prompt["text"]
        # Add a flag to show this is a prompt
        st.session_state.conversation.append({
            "role": "assistant",
            "content": response,
            "type": "prompt"
        })
        st.rerun()
        return

    elif any(word in user_input_lower for word in ["twist", "plot twist"]):
        twist = bot.add_twist()
        response = f"💫 **Plot Twist:** {twist}"
    
    elif any(word in user_input_lower for word in ["explain", "meaning", "symbolism"]):
        explanation = bot.explain_prompt(st.session_state.current_prompt)
        response = f"🔍 **Explanation:** {explanation}"
    
    elif any(word in user_input_lower for word in ["save", "favorite"]):
        if st.session_state.current_prompt:
            success = save_prompt_to_file(st.session_state.current_prompt)
            response = "✅ Prompt saved to favorites!" if success else "⚠️ Could not save."
        else:
            response = "No prompt to save. Generate one first!"
    
    elif any(word in user_input_lower for word in ["clear", "reset"]):
        st.session_state.conversation = []
        response = "🔄 Conversation cleared."
    
    elif any(word in user_input_lower for word in ["help", "commands"]):
        response = "**Commands:** prompt, twist, explain, save, clear, help."
    
    else:
        # Creative fallback
        response = f"Interesting thought. '{user_input}' reminds me of stories waiting to be told."
    
    st.session_state.conversation.append({
        "role": "assistant",
        "content": response
    })
    st.rerun()

# Streamlit app
def main():
    st.set_page_config(page_title="The Infinite Muse", page_icon="📖", layout="centered")
    st.title("📖 The Infinite Muse")
    st.markdown("*Your creative writing assistant with personality*")
    
    # --- SIDEBAR ---
    with st.sidebar:
        st.header("🎭 Creative Controls")
        
        # Genre selection
        genre = st.selectbox("Choose a genre:", ["any", "mystery", "fantasy", "scifi", "horror", "noir"])
        
        # Quick action buttons
        st.markdown("### Quick Actions")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✨ Generate", use_container_width=True):
                process_user_input(f"{genre} prompt")
        with col2:
            if st.button("🔄 Clear Chat", use_container_width=True):
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
        if st.button("📤 Export JSON", use_container_width=True):
            st.download_button("Download JSON", data_manager.export_favorites("json"), "prompts.json")
        
        # Favorites List in Sidebar
        if st.session_state.favorites:
            st.divider()
            st.subheader("💖 Saved Prompts")
            for i, fav in enumerate(st.session_state.favorites):
                with st.expander(f"⭐ {fav.get('genre', 'Prompt')} - {fav.get('time', '')}"):
                    st.write(fav["text"])
                    if st.button("Use", key=f"use_{i}"):
                        st.session_state.current_prompt = fav
                        st.session_state.conversation.append({"role": "assistant", "content": fav["text"], "type": "prompt"})
                        st.rerun()

    # --- MAIN TABS ---
    tab1, tab2, tab3 = st.tabs(["💬 Chat", "📝 Current Prompt", "🎯 Quick Start"])
    
    with tab1:
        st.subheader("Your Creative Journey")
        if not st.session_state.conversation:
            st.info("👋 Welcome! Try generating a prompt or typing a message below.")
        
        for i, msg in enumerate(st.session_state.conversation):
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                # Add action buttons only for prompts
                if msg.get("type") == "prompt":
                    c1, c2, c3 = st.columns(3)
                    if c1.button("💾 Save", key=f"save_{i}"):
                        if st.session_state.current_prompt: save_prompt_to_file(st.session_state.current_prompt)
                    if c2.button("✨ Twist", key=f"twist_{i}"):
                        process_user_input("twist")
                    if c3.button("🔍 Explain", key=f"explain_{i}"):
                        process_user_input("explain")

        # Chat input
        st.divider()
        if user_input := st.chat_input("Type your message..."):
            process_user_input(user_input)
    
    with tab2:
        st.subheader("📝 Current Prompt Details")
        if st.session_state.current_prompt:
            p = st.session_state.current_prompt
            st.write(f"### {p['text']}")
            st.divider()
            col1, col2, col3 = st.columns(3)
            col1.metric("Genre", p['genre'].capitalize())
            col2.metric("Time", p['time'])
            col3.metric("Date", p['date'])
            st.info(f"**Character:** {p['character']}\n\n**Setting:** {p['setting']}\n\n**Conflict:** {p['conflict']}")
            
            if st.button("💾 Save to Favorites", key="save_current_tab"):
                if save_prompt_to_file(p): st.success("Saved!")
        else:
            st.info("No current prompt. Generate one in the Chat tab!")
    
    with tab3:
        st.subheader("🚀 Get Started Quickly")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Mystery Prompt"): process_user_input("mystery prompt")
            if st.button("Fantasy Prompt"): process_user_input("fantasy prompt")
        with c2:
            if st.button("Add Twist"): process_user_input("add twist")
            if st.button("Explain This"): process_user_input("explain")
        with c3:
            if st.button("Say Hello"): process_user_input("hello")
            if st.button("Clear Chat"): process_user_input("clear chat")
        
        st.divider()
        st.markdown(f"**Data Location:** `{data_manager.favorites_file}`")

if __name__ == "__main__":
    main()
