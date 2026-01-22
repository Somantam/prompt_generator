# muse_bot.py
from chatbot_base import ChatbotBase
import random
from datetime import datetime

class MuseBot(ChatbotBase):
    def __init__(self):
        super().__init__(name="The Infinite Muse")
        
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

    # Required by parent class
    def process_input(self, user_input):
        return user_input

    # Required by parent class
    def generate_response(self, processed_input):
        return "I am the Muse."

    # --- YOUR CUSTOM METHODS ---
    
    def generate_prompt(self, genre="any"):
        """Generate a writing prompt dictionary"""
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
            prompt_text = genre_flavors[genre]
        else:
            prompt_text = f"📖 **Story Idea:** {character} {setting}, but {conflict}."
        
        return {
            "text": prompt_text,
            "character": character,
            "setting": setting,
            "conflict": conflict,
            "genre": genre if genre != "any" else "mixed",
            "time": datetime.now().strftime("%H:%M"),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "id": str(datetime.now().timestamp()),
            "created_at": str(datetime.now())
        }
    
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
    
    def explain_prompt(self, current_prompt=None):
        """Explain the current prompt"""
        if not current_prompt:
            return "No prompt to explain. Generate one first!"
        
        explanations = [
            f"This prompt explores themes of **identity** and **reality** through {current_prompt['character']} in {current_prompt['setting']}.",
            f"At its core, this story is about confronting **{current_prompt['conflict'].split(' ')[-1] if ' ' in current_prompt['conflict'] else 'the unknown'}**.",
            f"The symbolism here points to **transformation** and **unexpected discoveries**.",
            f"This scenario challenges what we take for granted."
        ]
        return random.choice(explanations)
