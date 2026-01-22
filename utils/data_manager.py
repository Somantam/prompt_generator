# utils/data_manager.py
import json
import os
from datetime import datetime

class DataManager:
    """Handles saving and loading data to/from files"""
    
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.favorites_file = os.path.join(data_dir, "favorites.json")
        
        # Create data directory if it doesn't exist
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # Create favorites file if it doesn't exist
        if not os.path.exists(self.favorites_file):
            self._initialize_favorites_file()
    
    def _initialize_favorites_file(self):
        """Create an empty favorites file"""
        with open(self.favorites_file, 'w') as f:
            json.dump({"favorites": [], "last_updated": str(datetime.now())}, f, indent=2)
    
    def save_favorites(self, favorites_list):
        """Save favorites list to JSON file"""
        try:
            data = {
                "favorites": favorites_list,
                "last_updated": str(datetime.now()),
                "count": len(favorites_list)
            }
            
            with open(self.favorites_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Saved {len(favorites_list)} favorites to {self.favorites_file}")
            return True
        except Exception as e:
            print(f"❌ Error saving favorites: {e}")
            return False
    
    def load_favorites(self):
        """Load favorites from JSON file"""
        try:
            if os.path.exists(self.favorites_file):
                with open(self.favorites_file, 'r') as f:
                    data = json.load(f)
                
                favorites = data.get("favorites", [])
                print(f"📂 Loaded {len(favorites)} favorites from file")
                return favorites
            else:
                print("📂 No favorites file found, starting fresh")
                return []
        except Exception as e:
            print(f"❌ Error loading favorites: {e}")
            return []
    
    def add_favorite(self, prompt_obj):
        """Add a single prompt to favorites and save to file"""
        try:
            # Load existing favorites
            favorites = self.load_favorites()
            
            # Add ID and timestamp if not present
            if "id" not in prompt_obj:
                prompt_obj["id"] = str(datetime.now().timestamp())
            if "saved_at" not in prompt_obj:
                prompt_obj["saved_at"] = str(datetime.now())
            
            # Add to favorites (avoid duplicates based on text)
            existing_texts = [fav.get("text", "") for fav in favorites]
            if prompt_obj.get("text", "") not in existing_texts:
                favorites.append(prompt_obj)
                
                # Save updated list
                self.save_favorites(favorites)
                print(f"✅ Added prompt to favorites: {prompt_obj.get('text', '')[:50]}...")
                return True
            else:
                print("⚠️ Prompt already in favorites")
                return False
                
        except Exception as e:
            print(f"❌ Error adding favorite: {e}")
            return False
    
    def remove_favorite(self, prompt_id):
        """Remove a favorite by ID"""
        try:
            favorites = self.load_favorites()
            filtered_favorites = [fav for fav in favorites if fav.get("id") != prompt_id]
            
            if len(filtered_favorites) < len(favorites):
                self.save_favorites(filtered_favorites)
                print(f"✅ Removed favorite with ID: {prompt_id}")
                return True
            else:
                print(f"⚠️ Favorite with ID {prompt_id} not found")
                return False
                
        except Exception as e:
            print(f"❌ Error removing favorite: {e}")
            return False
    
    def export_favorites(self, format="json"):
        """Export favorites in specified format"""
        try:
            favorites = self.load_favorites()
            
            if format == "json":
                return json.dumps({"favorites": favorites}, indent=2)
            elif format == "text":
                text = "🌟 MY SAVED WRITING PROMPTS 🌟\n\n"
                for i, fav in enumerate(favorites, 1):
                    text += f"{i}. {fav.get('text', '')}\n"
                    text += f"   Character: {fav.get('character', '')}\n"
                    text += f"   Setting: {fav.get('setting', '')}\n"
                    text += f"   Conflict: {fav.get('conflict', '')}\n"
                    text += f"   Saved: {fav.get('saved_at', '')}\n\n"
                return text
            else:
                return f"Unsupported format: {format}"
                
        except Exception as e:
            return f"Error exporting: {e}"