# muse_bot.py
from chatbot_base import ChatbotBase
import random

class MuseBot(ChatbotBase):
    def __init__(self):
        super().__init__(name="The Infinite Muse")
        print(f"✨ {self.name} awakens...")
        
        # Personality traits
        self.personality = {
            "tone": "mysterious and poetic",
            "speech_style": "metaphorical",
            "obsessions": ["unfinished stories", "what-ifs", "symbolism"]
        }
        
        # Creative database
        self.characters = [
            "a retired spy who remembers too much",
            "an astronaut who hears colors",
            "a librarian who can read between the lines",
            "a ghost who doesn't know they're dead"
        ]
        
        self.settings = [
            "in a city submerged underwater",
            "on a train that never stops",
            "in a library where books rewrite themselves",
            "at the edge of a black hole"
        ]
        
        self.conflicts = [
            "they find a key that fits nothing",
            "time begins moving backwards",
            "they discover they're not who they thought",
            "gravity suddenly fails every hour"
        ]

    def process_input(self, user_input):
        """Process user input with creative logic"""
        user_input_lower = user_input.lower()
        
        if any(word in user_input_lower for word in ['quit', 'exit', 'bye']):
            return {"command": "quit"}
        elif any(word in user_input_lower for word in ['prompt', 'idea', 'story']):
            return {"command": "generate_prompt", "input": user_input}
        elif 'twist' in user_input_lower:
            return {"command": "add_twist"}
        elif 'explain' in user_input_lower:
            return {"command": "explain"}
        elif 'save' in user_input_lower:
            return {"command": "save"}
        elif 'help' in user_input_lower:
            return {"command": "help"}
        else:
            # Creative interpretation
            mood = self._detect_mood(user_input)
            return {"command": "conversation", "input": user_input, "mood": mood}

    def generate_response(self, processed_input):
        """Generate response with personality"""
        command = processed_input.get("command")
        
        if command == "generate_prompt":
            prompt = self._generate_prompt()
            return self._wrap_with_personality(prompt, "📖 **Story Idea:**")
            
        elif command == "add_twist":
            twist = self._add_twist()
            return self._wrap_with_personality(twist, "💫 **Plot Twist:**")
            
        elif command == "explain":
            return "🔍 **Explanation:** Every story holds deeper meanings, waiting to be uncovered."
            
        elif command == "save":
            return "💾 **Saved!** This idea now lives in the library of possibilities."
            
        elif command == "help":
            return "📚 **Help:** Ask for prompts, add twists, or just chat. I'm here to inspire!"
            
        elif command == "quit":
            self.conversation_is_active = False
            return "👋 **Farewell:** May your stories flow like rivers. Return anytime."
            
        else:  # conversation
            user_input = processed_input.get("input", "")
            mood = processed_input.get("mood", "contemplative")
            return self._generate_conversation_response(user_input, mood)

    def _generate_prompt(self):
        """Generate a creative prompt"""
        character = random.choice(self.characters)
        setting = random.choice(self.settings)
        conflict = random.choice(self.conflicts)
        
        return f"{character} {setting}, but {conflict}."

    def _add_twist(self):
        """Add a plot twist"""
        twists = [
            "The mentor was the villain all along, but for reasons you'd understand.",
            "The magical artifact was never meant to be used; it was a warning.",
            "The spaceship isn't exploring new worlds; it's returning home."
        ]
        return random.choice(twists)

    def _detect_mood(self, text):
        """Detect mood from text"""
        text_lower = text.lower()
        if any(word in text_lower for word in ['happy', 'good', 'great']):
            return "happy"
        elif any(word in text_lower for word in ['sad', 'bad', 'tired']):
            return "sad"
        elif any(word in text_lower for word in ['write', 'create', 'story']):
            return "creative"
        return "contemplative"

    def _generate_conversation_response(self, user_input, mood):
        """Generate conversational response based on mood"""
        responses = {
            "happy": [
                f"Your joy is infectious! '{user_input}' could be the start of something wonderful.",
                f"I can feel the creative energy in '{user_input}'. Let's channel it!"
            ],
            "sad": [
                f"I hear the weight in '{user_input}'. Sometimes the best stories come from difficult places.",
                f"'{user_input}' carries depth. Even in shadows, stories wait to be told."
            ],
            "creative": [
                f"'{user_input}'—fertile ground for imagination! What grows from this seed?",
                f"That idea has roots. '{user_input}' could blossom into something extraordinary."
            ],
            "contemplative": [
                f"'{user_input}'... an interesting thought. It reminds me of stories half-remembered.",
                f"There are echoes in '{user_input}'—echoes of possibilities not yet explored."
            ]
        }
        
        return random.choice(responses.get(mood, responses["contemplative"]))

    def _wrap_with_personality(self, text, prefix):
        """Wrap text with personality flair"""
        personalities = [
            f"💭 *The muse whispers:* ",
            f"📜 *From the ancient scrolls:* ",
            f"✨ *A spark of inspiration:* ",
            f"🌌 *In the realm of stories:* "
        ]
        return f"{random.choice(personalities)}{prefix} {text}"